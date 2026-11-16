# Protocolo congelado — corpus limpio de XSS, Ronda 5 (2026-10-25)

Este documento se escribe y congela ANTES de medir nada (regla inviolable 1/8 de la tarea). No
contiene ningún resultado de bloqueo. Todo lo de abajo son decisiones de diseño y su justificación,
tomadas sobre los hallazgos de T1-T7.

## Contexto (T1 — inventario de lo existente)

- `attack-sim/build_corpus.py`: orquesta la construcción del corpus por categoría (sqli, path_traversal,
  cmdi, xss), llama al filtro de exclusión por categoría y escribe `large_corpus_requests.json` +
  `exclusion_report.json`. El XSS actual ahí es n=1 (el payload real confirmado por ZAP), de ahí esta
  tarea.
- `attack-sim/generators/path_traversal_gen.py`: generador propio determinista (semilla fija,
  `random.Random(seed)`, sin `random.random()`/`random.choice()` sueltos), combina archivo objetivo x
  profundidad x codificador, deduplica preservando orden de iteración (no por orden de `set`).
  Patrón que este trabajo replica para XSS.
- `attack-sim/run_large_corpus.py` / `run_large_corpus_fixed.py`: ejecutor HTTP contra el stack
  corriendo. Carga `large_corpus_requests.json`, hace login como alice/admin, manda cada request,
  clasifica `blocked = status==403`, intenta adivinar la capa (`layer_guess`) por la presencia de
  `X-Powered-By`. El defecto corregido (T2): para categorías pre-codificadas (`path_traversal`,
  `cmdi`), `urllib.parse.urlencode()` volvía a escapar el `%` de un payload ya codificado por el
  generador, añadiendo una capa de codificación no intencional. La corrección: si el payload ya trae
  bytes `%XX` y pertenece a una categoría pre-codificada, se inserta literal en la query string o el
  body en vez de pasar por `urlencode()`.
- `attack-sim/exclusion_filter.py`: construye un índice de hashes SHA-256 por clase
  (`training/data_clean/*.jsonl`, campos `path`/`query`/`body`, variantes cruda y URL-decodificada), más
  un índice de "forma de plantilla" solo para cmdi (canario de 6 mayúsculas -> `CANARY`, dígitos -> `N`,
  igual que `training/parsers/parse_seclists_cmdi.py`). Compara por categoría (el llamador decide
  contra qué bucket de clase comparar); `build_corpus.py` solo compara xss contra el bucket "xss".
- `training/leakage_check.py` (repo `logSguarDian`, solo lectura): audita corpus de evaluación contra
  `training/splits/{train,val,test}.parquet`. Dos mecanismos: coincidencia exacta (el payload es
  substring literal de algún campo `path`/`query`/`body` de la misma clase en la partición) y
  coincidencia por plantilla normalizada. La normalización NO es uniforme entre clases:
  `template_shape()` (canario+dígitos, solo cmdi) vs `generic_template()` (decodificar URL una vez,
  minúsculas, dígitos -> `N`, para sqli/xss/path_traversal — exactamente la "igualdad normalizada" que
  pide T6/T7 de esta tarea). Las particiones solo tienen las 73 features calculadas, no el texto crudo;
  el texto se recupera uniendo por `_row_hash` contra `training/data_clean/unified.jsonl`.

## T3 — transportes aceptados (verificado empíricamente, Config 1, 2026-10-25)

`POST /profile` (bio) y `POST /posts` (content/title) aceptan y persisten correctamente los tres
Content-Type probados: `application/x-www-form-urlencoded`, `multipart/form-data`, `application/json`.
Verificado con marcadores únicos por combinación, reconfirmando el guardado con una lectura inmediata
después de cada envío (ver `docs/evidence/t3-content-type-probe-20261025.txt`).

Nota de diseño: `POST /posts` exige `title` Y `content` no vacíos a nivel de ruta (`src/routes/posts.js:53`,
`if (!title || !content) return 400`) para persistir el post. El corpus de esta tarea envía solo el
campo objetivo de la dimensión `campo` (content o title) poblado con el payload, sin rellenar el otro
campo. Esto no afecta la medición de T9: la decisión de bloqueo de logSguarDian ocurre en el
middleware, antes de que la ruta valide `title`/`content`, así que un payload "campo=content" se
bloquea o no se bloquea exactamente igual que si `title` también viniera poblado. Si T11 (P1) llega a
ejecutarse, los candidatos con campo=content/title que no completen el formulario no van a persistir
visualmente en `/posts` y quedan fuera de la muestra de explotabilidad en navegador — se declara aquí,
no se descubre después.

## T4 — dimensiones del generador propio (`generate_xss.py`)

No derivado de SecLists, PayloadsAllTheThings ni ningún cheat sheet público. Cuatro dimensiones
combinables generan `payload_raw`; una quinta (transporte+campo) se aplica al muestrear, no cambia el
texto del payload:

- **contexto** (8): html_body, attr_double, attr_single, attr_unquoted, js_string, url_href_src, svg,
  html_comment.
- **vector** (9): script, event_onerror, event_onload_body, event_onfocus_autofocus, event_ontoggle,
  event_onmouseover, javascript_uri, svg_onload, iframe_srcdoc. No todo vector es válido en todo
  contexto (p. ej. `javascript_uri` solo aplica a `url_href_src`); el mapeo contexto->vectores válidos
  está en `CONTEXT_VECTORS` dentro del generador, explícito y revisable.
- **función ejecutada** (7): alert, confirm, prompt, fetch_externo, document_cookie, fromcharcode,
  eval_atob. `fetch_externo`/`document_cookie` apuntan a `https://xss-poc.invalid/c` (TLD reservado
  por RFC 2606 para no resolver nunca a un host real).
- **codificación y evasión** (10): raw, url_single, url_double, html_entities_dec, html_entities_hex,
  unicode_escape, mixed_case, whitespace_tab_newline, slash_for_space, inline_comment.
- **transporte y campo**: 3 transportes (urlencoded, multipart, json) x 3 destinos
  (`/posts`#content, `/posts`#title, `/profile`#bio).

Determinismo: una sola instancia `random.Random(seed)`, combinaciones recorridas en orden fijo
explícito (no por orden de `dict`/`set`), deduplicado preservando el primer orden visto. Semilla
`20261025`, documentada en el propio archivo. 400 candidatos generados (`xss_candidates_20261025.jsonl`);
verificado determinismo (dos corridas, mismo SHA-256 del JSON serializado).

`forma_enviada` = cómo se ve `payload_raw` en el cable para su transporte. Para `urlencoded`, un
payload cuya `codificacion` ya es `url_single`/`url_double` se trata como pre-codificado (mismo
criterio que `PRE_ENCODED_CATEGORIES` del ejecutor, extendido aquí al campo `codificacion` del propio
generador en vez de inferirlo por categoría) y no se vuelve a escapar. `multipart`/`json` nunca
re-escapan `%`, así que ahí `forma_enviada` = `payload_raw` siempre.

## T5 — muestreo 400 -> 200 (`sample_xss.py`)

Reglas fijadas antes de ver resultados:
- Ningún valor de una dimensión supera el 30 % del corpus final (60 de 200) — **excepto** `transporte`
  y `campo`, que solo tienen 3 valores posibles cada una: el mínimo matemático para el valor más
  frecuente de una dimensión de 3 valores que debe sumar 200 es 200/3 = 66.67 (33.3 %), por encima del
  30 %. Es una imposibilidad aritmética, verificada y reportada antes de tocar el muestreador
  (confirmada en la sesión: con el 30 % estricto el proceso de aceptación se atasca en 180/200).
  **Decisión del usuario (2026-10-25):** mantener el 30 % estricto en las cuatro dimensiones con margen
  real (contexto, vector, función, codificación — 7 a 10 valores cada una) y usar el reparto más
  equilibrado posible (tope 34 %, 68/200) en transporte y campo, declarado como desviación.
- Mínimo 20 payloads por transporte aceptado: cumplido con margen (64-68 cada uno).
- Al menos 30 % sin la función alert (sin la subcadena literal "alert", calculada sobre `payload_raw`
  ya con su codificación aplicada — p. ej. `fromcharcode`/`eval_atob` NO contienen la subcadena
  "alert" en el texto final, es la evasión real que esas funciones buscan demostrar): cumplido con
  amplio margen, 91.5 % del corpus final no contiene "alert".

Procedimiento: candidatos barajados con la misma semilla, aceptados en ese orden fijo salvo que
exceder el tope de alguna dimensión; sin curaduría manual caso por caso. Resultado: 200/200,
`xss_sampling_report_20261025.json` con el detalle y el veredicto de cada regla.

## T6 — filtro de exclusión (`exclusion_filter_xss.py`)

A diferencia de `build_corpus.py` (que solo compara cada candidato contra el bucket de su propia
clase), este filtro compara cada candidato XSS contra las **cinco** clases de
`training/data_clean/*.jsonl` (sqli, xss, path_traversal, cmdi, benign), por si alguna coincide
aunque esté etiquetada distinto. Dos mecanismos:
1. Hash exacto SHA-256 de tres formas — cruda (`payload_raw`), codificada (`forma_enviada`),
   decodificada (`urllib.parse.unquote(payload_raw)`) — contra el índice ya existente de
   `exclusion_filter.TrainingIndex` (reutilizado sin modificar, solo extendido para iterar las 5
   clases en vez de una).
2. Igualdad normalizada: `generic_template()` de `training/leakage_check.py` (decodificar URL una vez,
   minúsculas, dígitos -> `N`) importado en solo lectura desde el repo hermano — mismo criterio que
   usará T7, para que ambos pasos midan lo mismo.

Resultado: 200/200 conservados, 0 descartes (`exclusion_report_xss_20261025.json`). Determinismo
verificado: dos corridas, mismo SHA-256 del JSONL de salida
(`ef67ffd34d09a59c4cf8212722f78d5a2e8894f8d6a38d6e63a2f4598b6fae0d`).

## T7 — auditoría con `leakage_check.py` (`leakage_check_xss.py`)

Reutiliza (no reimplementa) `load_splits()`, `load_unified_by_hash()`, `build_class_text_pool()`,
`generic_template()` del `leakage_check.py` real, contra `train`/`val`/`test`. Dos chequeos:
substring exacto y substring normalizado, ambos sobre el pool de texto etiquetado `xss` de cada
partición.

**Resultado (declarado aquí, no oculto, tal como pide la regla "si queda alguna coincidencia por
igualdad normalizada, es un fallo del filtro: repórtalo"):** 3 de 200 payloads (`xss_118`, `xss_254`,
`xss_342`) tienen coincidencia por igualdad normalizada contra train Y test (0 contra val, 0
coincidencias exactas en ninguna partición). Los tres son variantes de patrones de XSS extremadamente
genéricos y comunes en cualquier corpus de la categoría (`javascript:alert(1)`/`javascript:confirm(1)`
codificados como entidades HTML decimales, y el breakout canónico `";alert(1);//`) — no derivados de
una fuente pública específica, pero sí lo bastante genéricos como para coincidir, tras normalizar, con
algo ya presente en el entrenamiento. Es un fallo real del filtro de T6 (que solo compara igualdad
exacta de la forma normalizada completa, no contención de subcadena como sí hace
`leakage_check.py`), no corregido en esta tarea por la regla 2 (no ajustar el filtro después de ver
resultados). El corpus final se mantiene en 200 (regla 3: no se quitan payloads), con esta coincidencia
declarada explícitamente en el entregable final como limitación/amenaza a la validez.

## Plan de T9 (medición)

- Configuración 1 (control, `LOGSGUARDIAN_DISABLED=true`): debe bloquear 0/200. Un bloqueo ahí
  invalida la medición de Configuración 2 y se reporta, no se descarta en silencio.
- Configuración 2: `logsguardian@0.1.1` instalado desde el registro npm (`npm install logsguardian@0.1.1`,
  sin `file:`, sin tarball, sin `modelDir` override). Verificación dentro del contenedor antes de medir:
  `shasum` del tarball instalado contra `dist.shasum` del registro; SHA-256 de `rf.onnx`/`if.onnx`
  contra el par C documentado (`25b407e6...`, `5be28ee8...`).
- Ejecutor: `send_xss_corpus.py` (este documento, T9 sender) para los tres transportes, que reutiliza
  `run_large_corpus_fixed.py` como dependencia de referencia de la convención de pre-codificación.
- 3 corridas por configuración, reiniciando contenedores y base de datos entre corridas. Corrida 1 =
  cifra principal; corridas 2-3 = estabilidad. Se lista cualquier payload cuyo veredicto cambie entre
  corridas.
- Por payload: id, estrato completo (contexto, vector, función, codificación, transporte, campo),
  HTTP status, bloqueado sí/no, motivo si no se bloqueó, probabilidad RF (leída de
  `detection_events` en SQLite, unión best-effort por ventana de tiempo — la app no devuelve un id de
  request, así que la unión es por orden de llegada dentro de la ventana de la corrida, documentado
  como limitación), latencia.
- El payload original confirmado por ZAP (`</div><scrIpt>alert(1);</scRipt><div>`, en `bio`) se mide
  aparte, no como parte de las 200 muestras del corpus nuevo.

## Plan de T10 (análisis)

- k/n global y por estrato (cada dimensión por separado: contexto, vector, función, codificación,
  transporte, campo, con/sin alert), con intervalo de Wilson al 95 %:
  ```
  p_hat = k/n
  z = 1.959963984540054 (aprox. 1.96)
  centro = (p_hat + z^2/(2n)) / (1 + z^2/n)
  margen = z * sqrt(p_hat*(1-p_hat)/n + z^2/(4n^2)) / (1 + z^2/n)
  IC95% = [centro - margen, centro + margen]
  ```
- Lista de fallos (payloads no bloqueados en Config 2, corrida 1) con causa clasificada: (a) veredicto
  del modelo (RF por debajo del umbral 0.35, probabilidad leída del log), (b) defecto del middleware,
  (c) defecto del ejecutor (ver T2, ya descartado para este corpus), (d) fallo de infraestructura
  (timeout, 5xx, error de red). Para (a), se reporta la distancia de la probabilidad al umbral 0.35.
