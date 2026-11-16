# Delta de tesis — corpus limpio de XSS, Ronda 5 (2026-10-25)

Insumo para que otra persona corrija y agregue el texto de la tesis. No contiene redacción de
capítulos completos — solo cifras, procedencia y propuestas mínimas por sección.

## 1. Resumen

Se construyó un corpus propio de 200 payloads XSS (generador determinista, no derivado de listas
públicas), filtrado contra las cinco clases de entrenamiento y auditado contra train/val/test con
la misma metodología de `leakage_check.py`. Contra `logsguardian@0.1.1` (registro npm, modelo
verificado byte a byte), el bloqueo fue 200/200 (100 %, IC95% Wilson [98.1 %, 100 %]) en las tres
corridas, sin una sola variación entre repeticiones ni entre los 6 estratos medidos. El control sin
protección bloqueó 0/200 en las tres corridas, confirmando que el corpus y el arnés miden lo que
dicen medir. Quedan dos limitaciones declaradas: 3 de los 200 payloads coinciden por igualdad
normalizada con texto de entrenamiento (hallazgo de T7, un fallo real del filtro de T6, no
corregido por regla del protocolo) y la medición no es ciega porque el corpus se construyó después
de conocer el resultado de la Ronda 5 anterior.

## 2. Tabla de procedencia

| Artefacto | Ruta | SHA-256 | SHA base / rama | Versión paquete | Hashes de modelos | Fecha | Comando de reproducción |
|---|---|---|---|---|---|---|---|
| Protocolo congelado | `docs/protocol-xss.md` | `ae52abc3227feb00650e98e0e1e81185fc76a56d8bd6b93ba1ca5cb3cc53134f` | `exp/ronda5-20261025` @ `07e80ead6a64db5db086216322624bc5bfa4edb0` | — | — | 2026-10-25 | — |
| Generador XSS | `attack-sim/generate_xss.py` | `20119bf29df62b514895e4a6978607eb15d6dbf56415b435a0c3b7bde27e93b2` | idem | — | — | 2026-10-25 | `python3 attack-sim/generate_xss.py` |
| Muestreador | `attack-sim/sample_xss.py` | `c1fedaf67582d93b357142a07537a78b44a0cf56d9a926c3d8287a79e09e102d` | idem | — | — | 2026-10-25 | `python3 attack-sim/sample_xss.py` |
| Filtro de exclusión (T6) | `attack-sim/exclusion_filter_xss.py` | `da4e7732290e3f1fd28eb5de57932784d9105a8e9bd88bd6ddf88c87d46767cc` | idem | — | — | 2026-10-25 | `python3 attack-sim/exclusion_filter_xss.py` |
| Auditoría de fuga (T7) | `attack-sim/leakage_check_xss.py` | `8649e9193b5b6f6718c7d4cfdade05e7214791f467ca136e22767b03ab623a0e` | idem | — | — | 2026-10-25 | `python3 attack-sim/leakage_check_xss.py` |
| Ejecutor multi-transporte (T9) | `attack-sim/send_xss_corpus.py` | `18c645527d1c6944734edb899ce10279928285abef1a627691c06223dcaa75ee` | idem | — | — | 2026-10-25 | `python3 attack-sim/send_xss_corpus.py <config> <corpus> <run>` |
| Ejecutor base corregido (T2) | `attack-sim/run_large_corpus_fixed.py` | `422393460dfea808efe411d358166d37b662bbcaad77843ede0247c684c61af1` | extraído de commit `00ea3a3` ("test: verify logsguardian@0.1.1 closes the path_traversal gap to 100%"), ya ancestro de HEAD | — | — | commit original: 2026-10-10/11; extraído: 2026-10-25 | `git show 00ea3a3:attack-sim/run_large_corpus.py` |
| Candidatos (400) | `attack-sim/xss_candidates_20261025.jsonl` | `98d6e846899feedb0e736f3cb842d13c8d506751fb60911318bf840137883614` | idem | — | — | 2026-10-25 | — |
| Corpus final (200, post T6) | `attack-sim/xss_corpus_filtered_20261025.jsonl` | `ef67ffd34d09a59c4cf8212722f78d5a2e8894f8d6a38d6e63a2f4598b6fae0d` | idem | — | — | 2026-10-25 | — |
| Reporte de exclusión (T6) | `attack-sim/exclusion_report_xss_20261025.json` | `4537ea3f6f9598b8b11264ca36880d55c9df5820ebaea85ea950ef84bddb43c3` | idem | — | — | 2026-10-25 | — |
| Reporte de fuga (T7) | `attack-sim/leakage_report_xss_20261025.json` | `0c7f700961ddfbb9a8f8425d54ecbff0af61e3a372bf15e95b52e3fe96d96fb9` | idem | — | — | 2026-10-25 | — |
| Dependencia de solo lectura | `logSguarDian/training/leakage_check.py` | `0e52e1ac4d4b94909fd4ad1ac3b30d4012d1235ee9bea37fbc093cd590e8e5a9` | repo `logSguarDian` @ `develop` @ `64a11aa7a6bdea7b85dd97a0134aa87b8b6c7cd5` | — | — | preexistente | — |
| Paquete medido | `node_modules/logsguardian` (dentro del contenedor) | tarball `shasum` `e108ec4509727cd8b0a6234c74b04e7ac6658e11` (= `dist.shasum` del registro npm para 0.1.1, verificado) | — | `0.1.1`, instalado desde `registry.npmjs.org`, sin `file:`, sin tarball local, sin `modelDir` override | `rf.onnx` = `25b407e649283606a231665a5a8c8ea1c2c7ad4fd0374a8945b3f119651b0870`; `if.onnx` = `5be28ee8437643b2f13708eee1ac3175348a350ea6fb8f8daeb09bd5717f797e` (coinciden con el par C documentado) | 2026-10-25 | `docker exec <contenedor> sh -c "npm pack logsguardian@0.1.1 && shasum ..."` |

**Estado de git de esta tarea (sin commits, regla 6):** ver `docs/evidence/git-state-xss-20261025.txt`.
Rama `exp/ronda5-20261025`, creada desde `main` (HEAD `07e80ead6a64db5db086216322624bc5bfa4edb0`, sin
cambios propios: el SHA es idéntico antes y después de toda la tarea en ambos repos). 26 archivos
nuevos, todos sin seguimiento (`??`), ningún archivo trackeado modificado (`git diff --stat` vacío).

## 3. Resultados

### 3.1 Bloqueo global (Configuración 2, `logsguardian@0.1.1`, corrida 1 = cifra principal)

| | k | n | % | IC95% Wilson |
|---|---|---|---|---|
| Config 1 (control, sin protección) | 0 | 200 | 0.0 % | [0.0 %, 1.9 %] |
| Config 2 (logsguardian 0.1.1) | 200 | 200 | 100.0 % | [98.1 %, 100.0 %] |

Fórmula: `p=k/n; centro=(p+z²/2n)/(1+z²/n); margen=z·√(p(1-p)/n+z²/4n²)/(1+z²/n)`, `z=1.959963984540054`.

### 3.2 Desglose por estrato (Config 2, corrida 1) — 100.0 % en los 7 estratos, sin excepción

| Dimensión | Valores (todos 100.0 %, IC95% más bajo por tamaño de muestra) |
|---|---|
| contexto | js_string (n=7, IC95 bajo 64.6 %) · svg (n=13, 77.2 %) · url_href_src (n=9, 70.1 %) · html_comment (n=16, 80.6 %) · attr_unquoted (n=23, 85.7 %) · attr_double (n=41, 91.4 %) · attr_single (n=44, 92.0 %) · html_body (n=47, 92.4 %) |
| vector | iframe_srcdoc (n=6, 61.0 %) · javascript_uri (n=9, 70.1 %) · event_onfocus_autofocus (n=15, 79.6 %) · event_onload_body (n=15, 79.6 %) · event_ontoggle (n=25, 86.7 %) · script (n=21, 84.5 %) · event_onerror (n=37, 90.6 %) · event_onmouseover (n=36, 90.4 %) · svg_onload (n=36, 90.4 %) |
| función | prompt (n=22, 85.1 %) · document_cookie (n=18, 82.4 %) · alert (n=28, 87.9 %) · confirm (n=31, 89.0 %) · fromcharcode (n=29, 88.3 %) · eval_atob (n=32, 89.3 %) · fetch_externo (n=40, 91.2 %) |
| codificación | raw (n=14, 78.5 %) · mixed_case (n=15, 79.6 %) · slash_for_space (n=16, 80.6 %) · whitespace_tab_newline (n=20, 83.9 %) · html_entities_hex (n=21, 84.5 %) · html_entities_dec/inline_comment (n=23, 85.7 %) · unicode_escape (n=18, 82.4 %) · url_single/url_double (n=25, 86.7 %) |
| transporte | urlencoded (n=64, 94.3 %) · json/multipart (n=68, 94.7 %) |
| campo | bio (n=64, 94.3 %) · content/title (n=68, 94.7 %) |
| con/sin "alert" literal | con alert (n=17, 81.6 %) · sin alert (n=183, 97.9 %) |

(Columna "IC95 bajo" = extremo inferior del intervalo de Wilson al 95 %, dado que la proporción
puntual es 1.0 en todos los casos y lo único que varía con *n* es el ancho del intervalo.)

### 3.3 Lista de fallos (Config 2, corrida 1)

Ninguno. 0 de 200 payloads sin bloquear. Por lo tanto no hay distancia al umbral 0.35 que reportar
(regla del protocolo T10: "para los fallos del modelo, indica qué tan cerca..." — no aplica, no hubo
fallos de ningún tipo: ni de modelo, ni de middleware, ni de ejecutor, ni de infraestructura).

### 3.4 Estabilidad entre corridas

3 corridas por configuración, contenedor y base de datos reiniciados entre cada una. Cero cambios de
veredicto por payload entre corridas, en ambas configuraciones: Config 1 = 0/200 las tres veces;
Config 2 = 200/200 las tres veces, mismos 200 IDs bloqueados cada vez.

### 3.5 Clasificación de clase (Config 2, corrida 1, desde `detection_events`)

De los 200 bloqueos, 193 se registraron con `predicted_class=xss` y 7 con `predicted_class=sqli`
(verdict `block` en ambos casos — el bloqueo no depende de que la clase predicha sea la correcta,
solo de que el Random Forest supere el umbral en alguna clase de ataque). Es el mismo patrón de
confusión entre clases ya documentado para cmdi/sqli en `docs/config2-results-v1.md` y
`k-resultados.tex:376-378` (DVNA), ahora también observado para xss/sqli. No se midió la
probabilidad RF por payload de forma sistemática en esta corrida (ver sección 7); con 0 fallos de
bloqueo, esa cifra no cambia el resultado de cobertura, solo habría enriquecido el detalle de la
clasificación.

### 3.6 Payload original confirmado por ZAP (medido aparte, no es parte de las 200 muestras)

`</div><scrIpt>alert(1);</scRipt><div>` en `bio`: Config 1 → `200`, persiste sin escapar (vulnerable,
confirmado de nuevo); Config 2 → `403` (bloqueado). Consistente con el resultado ya reportado en
`docs/config3b-results.md` ("XSS: ZAP Active Scan result").

## 4. Cambios por sección de la tesis

| Ubicación | Valor/texto actual | Qué cambia | Propuesta mínima |
|---|---|---|---|
| Cuadro 28 | Dice que XSS usa "payloads clásicos, ZAP no automatizado" | Incoherente con el resto (XSS ahora usa generador propio automatizado, igual que path_traversal/cmdi) | "XSS: generador propio determinista (`generate_xss.py`), 200 payloads tras filtro de exclusión y auditoría de fuga, igual metodología que path_traversal/cmdi." |
| Procedimiento 4.3 / Sección 7.5 | Describe la generación de XSS como el payload único de ZAP | Ahora hay un generador propio de 200 payloads además del caso ZAP (que se conserva como hallazgo de vulnerabilidad real, no como corpus de medición) | Agregar un párrafo describiendo las 4 dimensiones combinables (contexto, vector, función, codificación) y la quinta de muestreo (transporte/campo), con referencia a `docs/protocol-xss.md`. |
| Cuadro 36 (fila XSS: ZAP, 1 alerta, 0 descartados, 1 final) | n=1 | Sigue siendo cierto para el hallazgo de vulnerabilidad real; se agrega una fila nueva para el corpus de cobertura (400 candidatos → 200 finales, 0 descartados por T6, 3 con coincidencia normalizada no resuelta en T7) | Agregar fila: "Corpus de cobertura XSS: 400 candidatos, 200 finales (T5), 0 descartados por hash/plantilla (T6), 3/200 con coincidencia normalizada contra train/test no resuelta (T7)." |
| Cuadro 37 (XSS 1/1 en tres columnas, n=1) | n=1 | Se agrega la cifra de cobertura n=200 junto a la de vulnerabilidad n=1, sin reemplazarla (son preguntas distintas: "¿es explotable?" vs "¿se bloquea un corpus representativo?") | "XSS (vulnerabilidad real, ZAP): 1/1. XSS (cobertura, corpus propio n=200): 200/200, IC95% Wilson [98.1%, 100%]." |
| Cuadro 38 (XSS 0/1, 1/1, 1/1, 1/1 por configuración) | n=1 en las 4 configuraciones | Se mantiene para el payload ZAP (medido aparte en esta tarea también, mismo resultado: Config1=200/no bloqueado, Config2=403/bloqueado); se agrega el dato de cobertura solo para Config 1 y 2 (3a/3b no se midieron en esta tarea, ver sección 8) | Mantener la fila existente tal cual (sigue siendo cierta); agregar nota: "cobertura adicional sobre corpus n=200 medida solo para Config 1 (0/200) y Config 2 (200/200) en esta ronda." |
| Sección 8.4.2 (538 alertas de ZAP, n=1) | n=1 | Sin cambio en los hechos de ZAP; se puede añadir una frase de contraste con el nuevo n=200 | "El hallazgo de ZAP (n=1) se complementa con un corpus de cobertura construido independientemente (n=200, ver Sección X), que no reemplaza la necesidad de un hallazgo de explotabilidad real, pero sí responde la pregunta de cobertura que el n=1 no podía responder por sí solo." |
| Sección 7.12 ("Cobertura de XSS con n=1") / Sección 7.11 (amenazas a la validez) | Restricción de n=1 | Deja de ser la limitación central de cobertura de XSS (aunque la limitación de n=1 para *explotabilidad confirmada* se mantiene, son cosas distintas) | Reescribir la restricción como: "La cobertura de bloqueo de XSS se midió sobre un corpus propio de 200 payloads (IC95% [98.1%,100%]); la confirmación de explotabilidad real sigue descansando en un único caso (ZAP), que no se amplió en esta ronda." |
| Discusión/conclusiones que citan n=1 o "no permite afirmar el criterio del 80%" para XSS | n=1 no alcanza el 80% con confianza | Con n=200 y 100% (IC95% bajo 98.1%), el criterio del 80% para XSS queda ampliamente superado con evidencia estadística, no solo con el caso puntual de ZAP | "El criterio de cobertura ≥80% por categoría se cumple para XSS con evidencia estadística (200/200, IC95% [98.1%,100%]), además del caso de explotabilidad real confirmado por ZAP (n=1)." |
| Cuadros 40 y 41 (indicadores y cumplimiento de OE3) | XSS marcado con reserva por n=1 | La reserva por tamaño de muestra para el criterio de cobertura deja de aplicar a XSS; la reserva de "un único caso de explotabilidad confirmada" se mantiene como nota aparte, no como incumplimiento de cobertura | Mover XSS de "cumplido con reserva" a "cumplido" en la fila de cobertura; mantener nota aparte sobre explotabilidad n=1. |
| Resumen y abstract | Probablemente mencionan el criterio de cobertura por categoría de forma agregada | Si citan explícitamente la limitación de XSS n=1 para cobertura, ya no es exacto | Revisar si el resumen/abstract nombra XSS específicamente; si no lo hace, sin cambio. |

## 5. Afirmaciones que dejan de ser ciertas / que siguen siendo ciertas

**Dejan de ser ciertas (tal como estaban escritas):**
- "La cobertura de XSS no se puede afirmar con el criterio del 80% por tener n=1" — ya no, hay n=200
  con 100% y un IC95% cuyo extremo inferior (98.1%) está muy por encima del 80%.
- Cualquier frase que iguale "cobertura de XSS" con "el caso de ZAP" como si fueran la misma medición.

**Siguen siendo ciertas, sin cambio:**
- El hallazgo de vulnerabilidad real de XSS almacenado en `bio` (ZAP, n=1) sigue siendo el único caso
  de explotabilidad *confirmada* contra la app de referencia — eso no se amplió en esta tarea.
- `content`/`title` en `/posts` siguen sin vulnerabilidad confirmada (ZAP los probó limpios en su
  momento; esta tarea no volvió a correr ZAP contra ellos, solo midió bloqueo del corpus propio).
- Todo lo ya reportado sobre sqli, path_traversal y cmdi en Rondas anteriores: sin cambio, esta tarea
  no los tocó.

## 6. Hechos verificados frente a hipótesis

**Hechos verificados (medidos en esta sesión, con evidencia en archivo):**
- 200/200 bloqueados en Config 2, 3 corridas idénticas, 0 flips.
- 0/200 bloqueados en Config 1 (control), 3 corridas.
- Paquete instalado: 0.1.1 real del registro npm, shasum de tarball y de ambos modelos verificados
  byte a byte.
- 0 descartes por el filtro T6; 3 coincidencias normalizadas encontradas por la auditoría T7 (más
  estricta que T6) que el filtro no atrapó.
- El payload ZAP original: Config1=no bloqueado/explotable, Config2=bloqueado. Reconfirmado, no es
  nuevo.

**Hipótesis / interpretación (no medidas directamente, para que quien redacte lo marque como tal si
las usa):**
- Que los 3 payloads con coincidencia normalizada (`xss_118`, `xss_254`, `xss_342`) coinciden por ser
  patrones JS genéricos extremadamente comunes (`javascript:alert(1)`, `";alert(1);//`) y no porque el
  generador haya derivado de una fuente pública — es una explicación razonable dado el texto de los
  payloads, pero no se verificó de dónde exactamente viene el texto de entrenamiento que coincide
  (no se inspeccionó manualmente el archivo fuente de esa coincidencia más allá del nombre de archivo
  que reporta `exclusion_report_xss_20261025.json`/`leakage_report_xss_20261025.json`).
- Que la confusión xss→sqli en 7/200 eventos tiene la misma causa raíz que la confusión cmdi→sqli ya
  documentada (features compartidas) — es plausible por analogía, no se investigó el mecanismo
  específico para xss en esta tarea.

## 7. Desviaciones del plan, limitaciones y amenazas a la validez nuevas

- **Base de la rama compartida:** `origin/feat/waf-modsecurity-crs` (indicada en las instrucciones)
  no contiene `docker-compose.direct.yml`; `main` no contiene la variante de Config 3a. Se creó
  `exp/ronda5-20261025` desde `main` por decisión explícita del usuario, dejando Config 3a pendiente
  para quien la necesite. Reportado antes de crear la rama, no decidido en silencio.
- **Tope del 30% por dimensión, inviable para transporte/campo:** con exactamente 3 valores posibles
  cada una, el mínimo matemático para el valor más frecuente de un total de 200 es 33.3%, no 30%. Se
  usó un tope relajado del 34% solo para esas dos dimensiones, decidido explícitamente con el usuario
  antes de aplicarlo, no descubierto después.
- **Sesgo del autor del generador:** las 4 dimensiones (contexto, vector, función, codificación) y
  los mapeos contexto→vectores válidos fueron diseñados por quien ejecutó esta tarea, no derivados de
  una taxonomía externa ya publicada. Es una limitación inherente a "generador propio, no de lista
  pública": la cobertura de patrones depende de qué combinaciones se consideraron válidas al
  construir `CONTEXT_VECTORS` en `generate_xss.py`.
- **Filtro exacto frente a normalizado:** T6 (este corpus) solo descarta por igualdad *exacta* de la
  forma normalizada completa; T7 (`leakage_check.py`) busca *contención de subcadena* normalizada
  contra el pool concatenado de cada partición — un chequeo más estricto. La auditoría T7 encontró 3
  coincidencias que T6 no había atrapado, exactamente por esa diferencia de método. No se corrigió el
  filtro después de ver este resultado (regla 2); queda documentado como un fallo real y declarado.
- **Corpus construido después de conocer el resultado de la Ronda 5 anterior:** quien diseñó
  `generate_xss.py` conocía de antemano que la Ronda 5 original medía XSS con n=1 y que las otras
  categorías ya tenían generadores propios — el diseño de las dimensiones no partió de cero sin
  contexto del resultado que se esperaba mejorar. Es una amenaza a la validez de "medición ciega",
  reconocida explícitamente, no oculta.
- **La congelación (T8) se verifica por manifiesto de hashes SHA-256, no por historial de git**,
  porque la regla 6 prohíbe commits en esta tarea. La garantía de que nada cambió entre el freeze y
  la medición descansa en el recálculo de hashes antes/después (ambos recálculos coinciden
  exactamente con el manifiesto original, ver `docs/freeze-xss-20261025.json`), no en un commit
  firmado o un log de git verificable independientemente.
- **Probabilidad RF por payload no capturada sistemáticamente:** T9 pedía registrar la probabilidad
  del Random Forest por payload desde `detection_events`. Con 0 fallos de bloqueo en las 3 corridas
  de Config 2, esa cifra no cambia el resultado de cobertura; se verificó una sola vez de forma
  puntual (193 xss / 7 sqli / 3 benign-pass_anomaly, de tráfico ajeno al corpus, en la corrida 1) pero
  no se preservó una copia de la base SQLite de cada corrida antes de reiniciar el contenedor para la
  siguiente, así que el detalle por payload de las 3 corridas no es reconstruible retroactivamente.
  Declarado aquí en vez de inventar o aproximar esa cifra (regla 3).
- **`POST /posts` exige `title` y `content` simultáneamente a nivel de ruta** (`src/routes/posts.js:53`);
  el corpus solo rellena el campo objetivo de la dimensión `campo`, así que las entradas con
  `campo=content`/`campo=title` reciben `400` de la aplicación cuando no hay protección (confirmado
  en Config 1: 136/200 con `400`, consistente con las 68+68 entradas de esos dos campos). Esto no
  afecta la medición de bloqueo (el middleware actúa antes de esa validación), pero si T11 llegara a
  ejecutarse, esas entradas no tendrían un post persistido que verificar en el navegador — declarado,
  no descubierto en T11.
- **T11 y T12 (P1) no se ejecutaron** por la prioridad explícita de la tarea ("P0 primero, P1 solo si
  queda tiempo") — ver sección 8.

## 8. Qué NO cambia / qué no se hizo en esta tarea

- No se tocó la librería, el modelo, el umbral ni el filtro de exclusión original
  (`attack-sim/exclusion_filter.py`) — todo lo nuevo son archivos agregados (regla 7).
- No se midió Config 3a ni Config 3b con este corpus de XSS — T9 solo pedía Config 1 y 2.
- No se ejecutó T11 (explotabilidad en navegador automatizado sobre una submuestra de 40) ni T12
  (ZAP como segunda fuente vía API, filtrado por el mismo criterio) — son P1, no alcanzó el tiempo
  disponible hoy. Quedan completamente pendientes, no parcialmente hechos.
- No se corrigió el hallazgo de T7 (3 coincidencias normalizadas) ni ningún otro defecto encontrado
  durante la tarea — por diseño (regla 2), todo se reporta, nada se corrige en esta tarea.
- No se hizo ningún commit, push ni PR (regla 6). Todo el trabajo está sin confirmar en
  `exp/ronda5-20261025`, en ambos repos tal como quedó documentado en la sección 2.
