# Fe de erratas y verificación de la Ronda 4, quinta ronda (2026-10-25)

Este documento no modifica resultados, los documentos delta ni las erratas anteriores (`docs/thesis-delta-errata-20261025.md`, `-b`, `-c` y `-d`). Registra la verificación de la Ronda 4 (A1 a A5, solo lectura) y las correcciones que de ella resultan.

Rama `exp/ronda5-20261025`, HEAD `07e80ead6a64db5db086216322624bc5bfa4edb0`, sin commits ni cambios en archivos con seguimiento. Respaldo previo a la quinta ronda: `docs/evidence/tex-before-round5-20261025/` (24 archivos, sumas en `SHA256SUMS.txt`). Wilson al 95 % con z = 1.959963984540054. Script de la verificación: `docs/evidence/r5-verificacion-ronda4-20261025.py`; salida: `docs/evidence/r5-verificacion-ronda4-20261025.json`.

## 1. A1. Con qué se midieron los 37 de 40 de la Ronda 4

| Elemento | Valor | Fuente |
|---|---|---|
| Fecha y commit | 2026-08-15, `af61eba` ("test: Round 4 - large corpus comparison across all 4 configs") | `git log` |
| Archivos de resultados | `attack-sim/results_config{1,2,3a,3b}.json` en `af61eba`; SHA-256 `7ac78940...` (Config 1), `efad90ab...` (Config 2), `b7ec71bb...` (3a), `77279aa1...` (3b); 590 payloads cada uno. El `results_config2.json` del árbol de trabajo es el de la Ronda 5 (608 entradas); el de la Ronda 4 se extrajo con `git show af61eba:...` | `docs/evidence/r5-verificacion-ronda4-20261025.json` |
| Librería | `package.json` de `af61eba`: `"logsguardian": "file:vendor/logsguardian-0.1.0.tgz"`; tarball local con SHA-256 `e09120006dd17e790838f2ae92bb68ee4c7f3a5e160c2c4c83f5a513909fe359`, presente en el repositorio desde `06316cb` (2026-08-05). No es el archivo publicado en npm (`c5c1a1da...`, publicado el 2026-08-30) y no es la 0.1.1 | `git show`, `git log -- vendor/logsguardian-0.1.0.tgz` |
| Modelos | Los del tarball: `rf.onnx` `180837255dffd596a38bf7c29032ccc313005cd70eca5c6238e23e35bdc0d4ec`, `if.onnx` `5de374a7f1d19176d7c66d3354e972d37b28a7306a87efa0ce8639278f489150` (par A, `rf_v10`/`if_v9`). La aplicación carga `modelDir: ../models`, y los blobs `models/rf.onnx` y `models/if.onnx` de `af61eba` tienen los mismos hashes. Los archivos de resultados no registran modelo ni versión: la atribución se apoya en el estado de git | `git show af61eba:src/server.js`, `docs/config3b-results.md` |
| Ejecutor | `attack-sim/run_large_corpus.py` de `af61eba`, SHA-256 `0c84de551f1138bbeb1ef7a9ed1801d83e4c52a7312c04b873a75de57a286623`, idéntico al ejecutor anterior a la corrección (`00ea3a3^`). Es el ejecutor sin corregir | comparación de hashes |
| Configuración 3a | Rama `feat/waf-modsecurity-crs` (otra versión de la aplicación) | `docs/config3b-results.md`, comentario de `docker-compose.yml` en `af61eba` |
| Totales | Config 1 0/590, Config 2 583/590, Config 3a 550/590, Config 3b 587/590 | recalculado |

Corpus de la Ronda 4: `attack-sim/large_corpus_requests.json.leaked.bak`, SHA-256 `fd51e5974871b56f77a546cce40f7cd34ebbf2a4ce79669307da0cb8189a51eb`, idéntico al de `af61eba`.

## 2. A2. Composición de los 40 y de los 37

| Conjunto | n | Path Traversal | SQLi | XSS | Command Injection |
|---|---|---|---|---|---|
| Ataques que la 3a no bloquea | 40 | 26 | 11 | 3 | 0 |
| De ellos, los que la 3b bloquea (todos con la firma de capa de la aplicación) | 37 | 23 | 11 | 3 | 0 |
| De ellos, los que la Config 2 bloquea | 39 | 25 | 11 | 3 | 0 |
| Pasan ambas capas | 3 | `path_traversal_186`, `_30`, `_36` | 0 | 0 | 0 |

Se confirma que ninguno de los 40 ni de los 37 es de Command Injection.

## 3. A3. Auditoría de fuga de la Ronda 4

Método: `training/leakage_check.py` (repositorio `logSguarDian`, solo lectura) contra train, val y test, con tres criterios: igualdad normalizada del campo completo, subcadena normalizada y subcadena literal. Script `attack-sim/leakage_check_round4_20261025.py`; salida `attack-sim/leakage_report_round4_20261025.json`. Reproduce las cifras de Diego Valenzuela (sección VIII.3.5): cmdi 200/200 por igualdad y 63 literales; XSS 7/113 por igualdad y 13 por subcadena; SQLi 0/77 por igualdad y 26 por subcadena; Path Traversal 0/200.

| Categoría | n | Igualdad normalizada | Subcadena normalizada | Subcadena literal |
|---|---|---|---|---|
| SQLi | 77 | 0 | 26 | 0 |
| XSS | 113 | 7 | 13 | 12 |
| Path Traversal | 200 | 0 | 0 | 0 |
| Command Injection | 200 | 200 | 200 | 63 |

Cruce con los ataques que importan:

| Conjunto | Igualdad normalizada | Subcadena normalizada | Subcadena literal |
|---|---|---|---|
| Los 40 (11 SQLi, 3 XSS, 26 Path Traversal) | 0 | SQLi: `sqli_15`, `_17`, `_3`, `_50`, `_54`, `_71`, `_76` (7 de 11); XSS: `xss_25` (1 de 3); Path Traversal: 0 | `xss_25` |
| Los 37 | 0 | los mismos 7 de SQLi y `xss_25` | `xss_25` |

Las categorías de los 40 sí se auditaron (las cuatro lo fueron). Por igualdad normalizada no se detectó coincidencia en ninguno de los 40; la regla de subcadena es permisiva (límite superior). La auditoría detecta coincidencias y no demuestra su ausencia, por lo que el texto dice "no se detectó". El informe `logSguarDian/training/results/leakage_report.json` (auditoría anterior, rama `develop`) da cifras por partición con otra regla (por ejemplo, 21 de 77 de SQLi con train y 10 de 113 de XSS con coincidencia exacta en train); no se reconcilió con las anteriores y no se usa en la tesis.

## 4. A4. ¿Afecta la corrección del ejecutor a los 40?

La diferencia entre los dos ejecutores (`diff` de los archivos) es una sola: la petición se construye distinto cuando la categoría es `path_traversal` o `cmdi` y el payload contiene al menos un `%XX`. Para cualquier otro payload las peticiones son idénticas byte a byte.

| Categoría de la Ronda 4 | Payloads con `%XX` en categorías afectadas |
|---|---|
| SQLi | 0 (categoría no afectada) |
| XSS | 0 (categoría no afectada) |
| Path Traversal | 0 de 200 |
| Command Injection | 200 de 200 |

Ninguno de los 40 ni de los 37 es afectado: la corrección no altera sus peticiones. Esto establece que las peticiones habrían sido las mismas; no se volvió a medir la Ronda 4 con el ejecutor corregido, de modo que el veredicto con el ejecutor corregido es esperable pero no verificado. Los 200 de Command Injection sí cambian de petición y no se remidieron (los bloqueó el 100 % de cada configuración con el ejecutor anterior); no afecta a los 40.

## 5. A5. Wilson al 95 % y verificación de los 51

| Cantidad | k / n | Porcentaje | Wilson |
|---|---|---|---|
| Ronda 4: la librería bloquea de los que el WAF no bloquea | 37 / 40 | 92.5 | [80.1, 97.4] |
| Ronda 5: la 3b bloquea de los que el WAF no bloquea | 48 / 51 | 94.1 | [84.1, 98.0] |
| Ronda 5: payloads que la librería suma al WAF solo (3b menos 3a) | 48 / 800 | 6.0 | [4.6, 7.9] |
| Ronda 5: payloads que el WAF suma a la librería en condiciones equiparadas | 3 / 800 | 0.4 | [0.1, 1.1] |
| Ronda 5: ataques que el WAF no bloquea | 51 / 800 | 6.4 | [4.9, 8.3] |

Verificación con los archivos: de los 51 ataques que la 3a no bloquea en la Ronda 5, la 3b bloquea 48 (los tres que no bloquea son `cmdi_184`, `cmdi_185` y `cmdi_6`); la 3b menos la 3a son también 48; la Config 2 con cabeceras bloquea 48 de los 51.

## 6. Correcciones

| ID | Dónde | Decía | Problema | Corrección |
|---|---|---|---|---|
| F-12 | Sección 7.4.2 | "tarball construido en el commit `a3aada0`" | `a3aada0` es el commit de la Ronda 5 que usó el tarball; el archivo con SHA-256 `e09120006dd1...` está en el repositorio desde `06316cb` (2026-08-05) y ya lo usó la Ronda 4 | Redactado con el commit `06316cb` y la mención de la Ronda 4 |
| F-13 | Pedido B3 (ii) | "los tres payloads que ninguna configuración bloquea están a 0.0167 del umbral" | Solo dos: `cmdi_184` y `cmdi_185` (0.3333). En `cmdi_6` la clase de mayor probabilidad es benigna y la probabilidad de la clase de ataque no se registra | El texto dice "dos de los tres" |
| F-14 | Pedido B5 | "en las demás categorías de esos 40 la auditoría no detectó coincidencias" | Cierto por igualdad normalizada; por la regla de subcadena coinciden 7 de los 11 de SQLi y 1 de los 3 de XSS | El texto declara ambos resultados |
| F-15 | Sección 8.4.3, 9.5, Conclusión 8, Recomendación 2 | La Ronda 4 se presentaba con versión y ejecutor | Faltaba que la Configuración 3a se midió en otra rama de la aplicación (`feat/waf-modsecurity-crs`), la misma razón por la que se descartó la 3a antigua de la Ronda 5; los 40 salen de esa medición | Se añadió junto a la cifra |

## 7. Verificaciones de la fase B

| Comprobación | Resultado |
|---|---|
| `\ref` y `\label` | 145 etiquetas, 116 referencias distintas, 0 sin etiqueta, 0 duplicadas |
| Llaves y entornos | Balanceados en los ocho archivos tocados |
| Comentarios `%` añadidos | 0 |
| Recomendaciones | 1 a 23, sin saltos ni repeticiones |
| "por construcción" y "favorece a la librería" como sustento | Eliminados; queda una sola frase marcada como inferencia en la Sección 7.11 |
| Cuadro 38 | 6 columnas, 6 celdas por fila; la columna con cabeceras va entre filetes dobles; anchos de columna 12.6 cm en total con `\tabcolsep` de 4 pt solo dentro del cuadro (ancho total estimado de 14.4 cm frente a 15.24 cm de texto; el cuadro anterior medía unos 14.7 cm). Fuente y `\small` iguales a los demás cuadros; no se usó `\resizebox`. No se pudo comprobar en el PDF (no hay LaTeX) |
| Compilación | No hay LaTeX en este equipo |

## 8. Archivos nuevos de esta ronda

| Archivo | SHA-256 |
|---|---|
| `attack-sim/leakage_check_round4_20261025.py` | `508e953e5ed8887290dcabcd2b63c1de4d38ed8e1530983338b31aa8f7fb5ff7` |
| `attack-sim/leakage_report_round4_20261025.json` | `a66d43d5321ed6630a2e48fd18f5e62c724370d58523fc17c6f3afe43be730e5` |
| `docs/evidence/r5-verificacion-ronda4-20261025.py` | `ace92288a39eea848427cb16cedb115a424ac25f9758e84f31fb492f5b5f29ff` |
| `docs/evidence/r5-verificacion-ronda4-20261025.json` | `9ea0453bcf586054062a11e2e092c661cc1f2c6fc9698f39dd6dad93a69b2248` |
| `docs/evidence/tex-before-round5-20261025/SHA256SUMS.txt` | `91407e8f3311b76e7770b86a2ab52b046516f014041890f3dca4b7447b94af87` |

No se hicieron mediciones nuevas ni se levantó ningún contenedor en esta ronda.

## 9. Sin verificar

1. El modelo y la versión de la Ronda 4 se atribuyen por el estado de git de `af61eba` (los resultados no los registran).
2. La versión del WAF y de CRS de la Ronda 4 (15 de agosto) no consta; la imagen era la etiqueta flotante.
3. El veredicto de la Ronda 4 con el ejecutor corregido (las peticiones de los 40 son idénticas, pero no se remidió; los 200 de Command Injection sí cambian de petición).
4. La distancia entre la distribución del corpus y la del entrenamiento (no se midió; la inferencia de sesgo del corpus queda marcada como tal).
5. La tasa de falsos positivos del WAF (no se midió) y la de la librería detrás de él.
6. La importancia de `unusual_headers_count` en el modelo (no se midió).

## 10. Decisiones pendientes para el autor

1. La Ronda 4 comparte con la 3a antigua de la Ronda 5 el defecto que llevó a descartar esta última (otra rama de la aplicación, ejecutor anterior). El texto ya lo declara junto a los 37 de 40; el autor puede decidir si conviene mantener esa cifra como corroboración o retirarla.
2. La fila A del Cuadro 12 agrupa la Ronda 4 bajo "Paquete `logsguardian@0.1.0` (commit `c3d591a`)", pero la Ronda 4 usó el tarball local, no el publicado; el texto de 7.4.2 lo distingue y el cuadro no se tocó.
3. La nueva columna "2 con cabeceras" es post hoc y así se declara en la nota; el autor decide si el Cuadro 37 también debe llevarla.
4. El cuadro 38 no se pudo ver compilado: hay que comprobar en el PDF que no desborda el margen.
