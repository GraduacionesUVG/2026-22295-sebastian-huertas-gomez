# Fe de erratas y experimentos, segunda ronda (2026-10-25)

Este documento no modifica resultados, los documentos delta ni `docs/thesis-delta-errata-20261025.md`. Registra las correcciones que la segunda ronda hizo al texto de la primera, las comprobaciones de preparación de compilación y los resultados de los experimentos E1 y E2.

Rama `exp/ronda5-20261025`, HEAD `07e80ead6a64db5db086216322624bc5bfa4edb0`, sin commits ni cambios en archivos con seguimiento. Respaldo previo a la segunda ronda: `docs/evidence/tex-before-round2-20261025/` (24 archivos, sumas en `SHA256SUMS.txt`). Wilson y Wald al 95 % con z = 1.959963984540054.

## 1. Errores del texto de la primera ronda corregidos

| ID | Dónde | Decía | Problema | Corrección |
|---|---|---|---|---|
| F-01 | Sección 7.7, fila "Corpus limpio (M2)" | "cero coincidencias en el corpus final" | Cierto solo para el hash exacto del filtro; la auditoría de subcadena normalizada da 4, 7, 2 y 3 de 200 | A1 |
| F-02 | Sección 8.4.3, Discusión, nota del Anexo | La diferencia codificados frente a sin codificar del WAF se presentaba con "intervalos de Wilson solapados" | El solapamiento de dos intervalos no es una prueba de hipótesis; la prueba exacta de Fisher da p = 0.028 | A3 |
| F-03 | Sección 8.4.3 | "40 ... 37 ... 33 frente a 68, 65 y 64 antes; esa reducción corresponde al cambio de ejecutor" | Atribuía al ejecutor las cifras 65 y 64, que provienen de otras versiones de la librería (Config 2 anterior con el par A; de la 3b anterior no consta el paquete); además 37 de 40 colisiona con el 37 de 40 de dvws-node | A4 |
| F-04 | Sección 8.4.2 | "se reconfirmó que es explotable sin protección (HTTP 200)" | Solo se verificó que el servidor lo almacena sin escapar; no hay ejecución en navegador | A7 |
| F-05 | Sección 7.11, 8.4.3 y Discusión | "no se midió por qué la librería se comporta distinto detrás del proxy" | Superado por E1: las cabeceras del proxy explican la diferencia | E1 |
| F-06 | Resumen y Abstract | "payloads no vistos" sin calificar | Hay coincidencias residuales por subcadena y el corpus de XSS es posterior a la Ronda 5 | A2 |

## 2. A3. Prueba de hipótesis, 3a codificados frente a sin codificar

Datos: 80 de 105 bloqueados con separadores codificados (76.2 %, Wilson 67.2--83.3 %) y 84 de 95 sin codificar (88.4 %, Wilson 80.4--93.4 %). Resultados (`docs/evidence/a3-fisher-codificacion-20261025.json`, script `docs/evidence/a3-fisher-codificacion-20261025.py`, sin `scipy`: la prueba exacta se calcula con la distribución hipergeométrica):

| Estadístico | Valor |
|---|---|
| Diferencia de proporciones | 12.23 puntos porcentuales |
| Prueba exacta de Fisher bilateral | p = 0.02765 |
| IC95 de Wald de la diferencia | 1.85 a 22.61 puntos |

Coincide con lo esperado (12.2 puntos; p cercano a 0.028; IC de 1.8 a 22.6). Los dos subconjuntos no están controlados por otras características del payload (longitud, familia de separador, comando), de modo que la diferencia no se atribuye a la codificación como causa.

## 3. A11. Preparación de compilación

No hay LaTeX en este equipo. Se comprobó por lectura:

| Comprobación | Resultado |
|---|---|
| `longtable`, `float` (`[H]`), `array` y `\newcolumntype{L}` | Cargados en `0-preambulo_standalone.tex` (líneas 18, 26, 27, 28) y en `main.tex` (líneas 46, 56, 57, 58). No falta ningún paquete |
| `\allowbreak` y `\textsuperscript` | Comandos del núcleo de LaTeX; no requieren paquetes |
| Ruptura de `\texttt` | `hyphenat` con la opción `htt` está cargado en ambos preámbulos |
| Etiquetas | 142 `\label`, 113 `\ref` distintos, 0 referencias sin etiqueta, 0 etiquetas duplicadas |
| Llaves y entornos | Balanceados en los ocho archivos tocados (se excluye `document`, que abre el preámbulo) |
| Comentarios `%` nuevos | 0 |
| Numeración de recomendaciones | Simulada leyendo cada `\setcounter{enumi}` y cada `\item`: 1 a 23 sin saltos ni repeticiones (listado en el registro de ediciones) |

Límite de palabras del Resumen: no consta en `1-opciones_adicionales.tex`, en `z-main.tex` ni en las Directrices (el texto extraído de las Directrices no contiene "palabras" ni "resumen"). El Resumen pasa de 259 a 294 palabras y el Abstract de 222 a 251. Si la facultad impone un límite, la parte que se recomienda recortar primero es la tercera (corpus de XSS posterior a la Ronda 5).

## 4. E1. Cabeceras del proxy

Condiciones: Configuración 2 directa, imagen local `lsgt6final20261025-app` (`a75c14208ccd`, la misma de las mediciones del 25 de octubre, sin reconstruir), `logsguardian` 0.1.1 con `rf.onnx` `25b407e6...` e `if.onnx` `5be28ee8...` verificados dentro del contenedor, ejecutor corregido (`run_large_corpus.py`, SHA-256 `42239346...`), proyecto de Compose `lsgt6final20261025`, puerto 3000. Siete payloads (cuatro que solo bloquea la 3b, y `cmdi_6`, `cmdi_184` y `cmdi_185`), tres variantes, tres repeticiones cada una (63 envíos). Variantes: V0 sin cabeceras extra; V1 con `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Port` y `X-Forwarded-Proto` (valores de `docs/evidence/phase2b-diff-20261025.json`); V2 con además `Host: localhost`. Archivos: `docs/evidence/e1-proxy-headers-20261025.json`, script `attack-sim/e1_proxy_headers_20261025.py`, instantánea de `detection_events` en `docs/evidence/e1-events-snapshot-20261025/`.

Cada celda: bloqueados de 3 repeticiones; clase de mayor probabilidad y su probabilidad (`confidence` del evento; la política toma el máximo entre las cinco clases y bloquea si es de ataque y vale 0.35 o más). Las tres repeticiones dieron el mismo resultado en todos los casos.

| Payload | V0 sin cabeceras extra | V1 + cuatro X-* | V2 + cuatro X-* + Host sin puerto |
|---|---|---|---|
| `cmdi_112` | 0/3; benign 0.4000 | 3/3; sqli 0.4000 | 3/3; sqli 0.4000 |
| `cmdi_134` | 0/3; sqli 0.3333 | 3/3; sqli 0.3667 | 3/3; sqli 0.3667 |
| `cmdi_31` | 0/3; benign 0.3333 | 3/3; sqli 0.3667 | 3/3; sqli 0.3667 |
| `cmdi_38` | 0/3; sqli 0.3333 | 3/3; cmdi 0.3667 | 3/3; cmdi 0.3667 |
| `cmdi_6` | 0/3; benign 0.3667 | 0/3; benign 0.3333 | 0/3; benign 0.3333 |
| `cmdi_184` | 0/3; benign 0.3333 | 0/3; sqli 0.3333 | 0/3; sqli 0.3333 |
| `cmdi_185` | 0/3; path_traversal 0.3000 | 0/3; sqli 0.3333 | 0/3; sqli 0.3333 |

Resultado con la regla fijada de antemano: agregar las cabeceras hace bloquear 4 de los 4 payloads (3 de 3 repeticiones en cada uno), sin ellas 0 de 4, y los controles no cambian. Se aplica la redacción A: la diferencia entre la Configuración 2 y la librería dentro de la 3b queda explicada por el proxy. Agregar además `Host` sin puerto no cambia ningún veredicto (V2 igual a V1). Los emparejamientos entre envío y evento se hicieron por orden (un solo cliente secuencial; 63 eventos de `/admin/ping` para 63 envíos; coherencia entre `verdict = block` y HTTP 403 en los 63).

Lectura del extractor (solo lectura, paquete instalado; `docs/evidence/e1-extractor-caracteristicas-20261025.json`):

| Entrada | Características que dependen de ella |
|---|---|
| Cabecera `User-Agent` | `ua_present`, `ua_length`, `ua_suspicious` |
| Cabecera `Content-Type` | `content_type_encoded` |
| Cabecera `Authorization` | `authorization_length` |
| Todas las cabeceras fuera de la lista estándar (host, user-agent, accept, content-type, content-length, authorization, cookie, referer, connection, accept-encoding, accept-language, cache-control) | `unusual_headers_count` |
| Cabecera `Host`, `Referer`, `Cookie` | Ninguna (`Host` está en la lista estándar; `Referer` y `Cookie` se copian a la petición canónica y ninguna característica los usa) |
| IP del cliente | Ninguna (`req.ip` solo se guarda en el evento) |

`unusual_headers_count` entra al Random Forest (69 características) y está excluida del Isolation Forest (63). Con el cuerpo de cada uno de los siete payloads, agregar las cuatro cabeceras `X-*` cambia una sola característica del vector de 76: `unusual_headers_count`, de 0 a 4 (el cuerpo se aproximó como `host=<payload>` sin codificar; ambas variantes comparten el mismo cuerpo). Las probabilidades registradas son múltiplos de 1/30 (0.3, 0.3333, 0.3667, 0.4): los cambios de veredicto de E1 son de un voto de árbol, de 0.3333 a 0.3667 en `cmdi_134`, `cmdi_31` y `cmdi_38`.

Implicación: el veredicto de la librería depende en parte de una característica que mide el despliegue y no el contenido del payload. Una aplicación detrás de un proxy inverso entrega al extractor cabeceras que la Configuración 2 directa no tiene. La Configuración 2 de la tesis describe un despliegue sin proxy; no se midió la Configuración 2 con las cabeceras para las 800 peticiones (fuera del alcance de E1), de modo que se desconoce el efecto sobre las demás categorías.

## 5. E2. Triaje de `cmdi_6`, `cmdi_184` y `cmdi_185`

Random Forest: ver la tabla de E1 (Configuración 2 directa, con y sin cabeceras del proxy). Para `cmdi_184` y `cmdi_185`, con las cabeceras del proxy, la clase de mayor probabilidad es `sqli` con 0.3333, a 0.0167 del umbral de 0.35 (dentro de 0.05 por debajo). Sin las cabeceras, `cmdi_185` queda en `path_traversal` con 0.3000, a 0.05 exactos del umbral, y `cmdi_184` en `benign` con 0.3333. Para `cmdi_6` la clase de mayor probabilidad es `benign` (0.3667 sin cabeceras, 0.3333 con ellas); la probabilidad de la clase de ataque más probable no se registra cuando el máximo es la clase benigna, solo se sabe que no supera ese valor (salvo empate, que la política resuelve a favor de `benign`).

WAF: el registro de auditoría de `attack-sim/waf-audit-20261025/` solo contiene transacciones interrumpidas o con respuesta 4xx/5xx (797 registros, todos 403); los tres payloads no están en él. Para leer su puntaje se levantó un contenedor del mismo WAF (`owasp/modsecurity-crs:nginx-alpine`, imagen `sha256:f12da37e72e29d1f06e7e829780f1016606d0799eac2966e58ef3819a3d30a50`, paranoia 1, `SecRuleEngine On`) delante del servidor de captura de cabeceras, con una única diferencia de configuración: el motor de auditoría en `On` (registra todas las transacciones) en lugar de `RelevantOnly`. No se cambió ninguna regla. Se enviaron con el ejecutor corregido y `Host: localhost:3000`, el mismo `Host` del registro de la 3b. Archivos: `docs/evidence/e2-waf-probe-20261025.json`, `docs/evidence/e2-waf-audit-20261025/audit.log`, script `attack-sim/e2_waf_probe_20261025.py`.

| Payload | HTTP | Interrumpida | Reglas de CRS disparadas (Host localhost:3000) | Reglas con Host numerico (intento 1) |
|---|---|---|---|---|
| `cmdi_6` | 200 | False | ninguna | 920350 (severidad 4) |
| `cmdi_184` | 200 | False | ninguna | 920350 (severidad 4) |
| `cmdi_185` | 200 | False | ninguna | 920350 (severidad 4) |
| `cmdi_112` | 200 | False | ninguna | 920350 (severidad 4) |
| `cmdi_134` | 200 | False | ninguna | 920350 (severidad 4) |
| `cmdi_31` | 200 | False | ninguna | 920350 (severidad 4) |
| `cmdi_38` | 200 | False | ninguna | 920350 (severidad 4) |
| `cmdi_0` | 403 | True | 932235 (severidad 2), 949110 (severidad 0) | 920350 (severidad 4), 932235 (severidad 2), 949110 (severidad 0) |

Con el `Host` de las mediciones, ninguna regla de CRS se dispara sobre ninguno de los siete payloads (puntaje de entrada 0 frente al umbral 5). El control `cmdi_0` se bloquea con la regla 932235 (severidad crítica, 5 puntos). El primer intento usó el `Host` numérico `127.0.0.1:9312` y disparó la regla 920350 (severidad 4, 3 puntos) en todas las peticiones, un artefacto de la sonda y no de los payloads; se conserva en `docs/evidence/e2-waf-probe-intento1-host-ip-20261025.json` y `docs/evidence/e2-waf-audit-20261025/audit-intento1-host-ip-20261025.log`.

Texto añadido a la tesis: Sección 7.11 (viñeta de la librería frente al proxy), Discusión (defensa en profundidad) y justificación de la Recomendación 13.

## 6. Limpieza

Contenedor `e2waf20261025` eliminado, servidor de captura detenido, pila `lsgt6final20261025` bajada con `docker compose down -v` (los volúmenes los creó esta ejecución). Sin contenedores en ejecución del proyecto; puertos 3000, 9311 y 9312 libres. HEAD y `git status` de archivos con seguimiento sin cambios. T11 y T12 no se ejecutaron.

## 7. Archivos nuevos de esta ronda

| Archivo | SHA-256 |
|---|---|
| `attack-sim/e1_proxy_headers_20261025.py` | `7bfa1c79528dbfcdcf57ce74adafffad1f1443b0e6cebce650da4522adb9bf82` |
| `attack-sim/e2_waf_probe_20261025.py` | `04f1e9b78e25c06f32b4800d58fa9dabfa0c61b03ae279dfe1138d850621e04a` |
| `docs/evidence/a3-fisher-codificacion-20261025.py` | `17b0b8ae4038e043402f4259b2565e6d33910638493875ef67d1e23ff4690fd1` |
| `docs/evidence/a3-fisher-codificacion-20261025.json` | `27484703895f15dd92a43fad7dc366be5558cfadd16aa33bee68f33fabff2d85` |
| `docs/evidence/e1-proxy-headers-20261025.json` | `1928b9d6e5d9fa9e1cf4f1bb8bc1ed31a3d7481f516c02663e63cc340da1bc15` |
| `docs/evidence/e1-extractor-caracteristicas-20261025.json` | `5335dd79ce579d7ea5ac93aeeaa5db23abdfc9f3f74918754332c3e555358959` |
| `docs/evidence/e2-waf-probe-20261025.json` | `ef8968bb3498325d88161b78c260235f6c045fd30553fecf9efca7ff452b275b` |
| `docs/evidence/e2-waf-probe-intento1-host-ip-20261025.json` | `1f2ee65ccf0dd6d473afcc8b6de2a51ffd64fba201c647ff531c2f1104e62800` |
| `docs/evidence/e2-waf-audit-20261025/audit.log` | `0fdb0ecb5aa06be3fd1d1a75285e5ccdf5810b4d0cd856fae7fa1d45865ad160` |
| `docs/evidence/e2-waf-audit-20261025/audit-intento1-host-ip-20261025.log` | `97d3634f00e0a812ed17d6d444e37234d79a981b2bc9497f1cbd8b3dd36fdf9d` |
| `docs/evidence/e2-capture-20261025.jsonl` | `f7f7aff022937e553d036bb84d469e13245a55cde67a48437f1fcdd53d6e60d7` |
| `docs/evidence/e1-events-snapshot-20261025/logsguardian-events.db` | `df7b90008644de1131c4eeedd6e38f21743e01225e353fa231724e4e1c92e309` |
| `docs/evidence/tex-before-round2-20261025/SHA256SUMS.txt` | `4d4e0a4e8ffaa8e1c8f6a7f65884987060bd0e5ef5f13a97294186a0b8a509c3` |

También nuevo: `docs/evidence/tex-before-round2-20261025/` (copia de los 24 archivos de la tesis previa a esta ronda) y este documento. Los archivos del repositorio con seguimiento no se modificaron.

## 8. Decisiones pendientes y observaciones para el autor

1. La Configuración 2 de la tesis se midió sin proxy. Para las 800 peticiones no se midió con las cuatro cabeceras `X-*`; en los siete payloads de E1 el efecto fue de un voto de árbol y favoreció el bloqueo en cuatro. Si el autor quiere afirmar que la cobertura de la librería es la misma detrás de un proxy, falta esa medición (no se hizo por el límite de E1).
2. `unusual_headers_count` es una característica del Random Forest que mide el despliegue y no el payload. Es un hallazgo para el componente de Inteligencia Artificial, análogo al sesgo de `User-Agent`; no se evaluó su importancia en el modelo ni su distribución en el corpus de entrenamiento.
3. La amenaza de comparación no neutral con el WAF (A6) parte de una instrucción del autor: no hay un archivo de resultados que mida cuánto del corpus procede de familias presentes en el entrenamiento; el texto se acotó a "familias de payload representadas en el entrenamiento", respaldado en parte por la auditoría de subcadena. Conviene que el autor confirme esa redacción.
4. El Resumen creció a 294 palabras y el Abstract a 251; no se encontró límite en la plantilla ni en las Directrices, pero un límite de 250 palabras es habitual y habría que recortar.
5. El primer intento de E2 mostró que un `Host` numérico dispara la regla 920350 de CRS (3 puntos); en las mediciones el `Host` era `localhost:3000`. No afecta a la tesis, pero el WAF no debe medirse con `Host` numérico sin declararlo.
6. Sigue sin compilarse: hay que compilar en Overleaf (pdfLaTeX, biber, `makeglossaries`) y revisar los avisos de `Overfull \hbox` en los cuadros del Anexo.
