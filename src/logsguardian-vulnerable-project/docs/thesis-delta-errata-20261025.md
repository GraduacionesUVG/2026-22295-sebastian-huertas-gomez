# Fe de erratas y verificaciones de los documentos delta (2026-10-25)

Este documento no modifica los resultados ni los documentos `docs/thesis-delta-xss.md` y `docs/thesis-delta-configs.md`. Registra las verificaciones V1 a V10 hechas con los archivos existentes, la ejecucion de la Fase 2 y los errores encontrados en los deltas.

Rama `exp/ronda5-20261025`, HEAD `07e80ead6a64db5db086216322624bc5bfa4edb0`, sin commits. Todas las rutas son relativas a la raiz del repositorio `logSguarDian-vulnerable-project`. Los scripts de analisis estan en `docs/evidence/` y `attack-sim/` (archivos nuevos con fecha 20261025). Wilson al 95 % con z = 1.959963984540054.

## 1. Errores e inconsistencias en los deltas

| ID | Donde | Dice | Verdad segun los archivos | Evidencia |
|---|---|---|---|---|
| E-01 | `thesis-delta-configs.md` §3.1(e) | 3 payloads (`cmdi_6`, `cmdi_184`, `cmdi_185`) no los bloquean ni la 3a ni la Config 2, y "3b si bloquea los tres" | La 3b NO bloquea esos tres: son exactamente su conjunto de no bloqueados (197/200). La interseccion de 3a y Config 2 en cmdi tiene 7 ids, no 3 (`cmdi_112`, `cmdi_134`, `cmdi_184`, `cmdi_185`, `cmdi_31`, `cmdi_38`, `cmdi_6`); la 3b bloquea 4 de ellos (`cmdi_112`, `cmdi_134`, `cmdi_31`, `cmdi_38`) | V1, V2 |
| E-02 | `thesis-delta-configs.md` §1 | "quedan 3 payloads cmdi que ninguna de las dos capas bloquea" | Ambiguo: 3 payloads no los bloquea ninguna configuracion (ni 3a, ni 2, ni 3b). Ademas, 4 payloads no los bloquea ninguna capa por separado pero la 3b si | V1, V2 |
| E-03 | `thesis-delta-configs.md` §3.2 | "0 flips sobre 2400 comparaciones payload x run" | Son 4 configuraciones x 800 payloads x 3 corridas = 9600 payload-corridas (6400 comparaciones de las corridas 2 y 3 contra la 1). Cero cambios de veredicto | V9 |
| E-04 | `thesis-delta-xss.md` §1, §6, §7 | los 3 payloads (`xss_118`, `xss_254`, `xss_342`) "coinciden por igualdad normalizada" | La auditoria T7 mide contencion de subcadena normalizada. Por igualdad normalizada de campo completo hay 0 coincidencias en XSS. La comparacion simetrica con las otras categorias es la de subcadena normalizada: sqli 4, path_traversal 7, cmdi 2, xss 3 de 200 | V6 |
| E-05 | `thesis-delta-configs.md` §5 | "La ventaja relativa del WAF en Path Traversal ... se mantiene" | Con la 0.1.1 la libreria (200/200) iguala o supera al WAF (197/200); no hay ventaja del WAF en Path Traversal. La diferencia es de 3 payloads con intervalos de Wilson solapados ([98.1, 100.0] y [95.7, 99.5]) | §3.1 del delta, V1 |
| E-06 | `thesis-delta-configs.md` §5 | "3b supera a ambas individualmente en todas las categorias medidas"; "ninguna subsume a la otra" | En path_traversal y xss la 3b iguala a la Config 2 (200/200 las dos). En xss la libreria sola bloquea los 200 y el WAF falla 11, asi que la libreria subsume al WAF en xss y en path_traversal. En sqli y cmdi ninguna subsume a la otra | V1 |
| E-07 | `thesis-delta-configs.md` §3.1(c) | IC95 de 3a sin codificar [80.5, 93.4] y de 3b sin codificar [92.7, 99.4] | Con z = 1.959963984540054: 84/95 -> [80.446, 93.410], es decir [80.4, 93.4]; 93/95 -> [92.646, 99.421], es decir [92.6, 99.4]. Error de redondeo de 0.1 | calculo propio |
| E-08 | `thesis-delta-configs.md` §3.1(c) | 49.5 % como inferencia aritmetica sin desglose historico | Existe el resultado por payload de la medicion antigua (`attack-sim/results_config3a-round5-20261010.json`): 52/105 = 49.5 % en codificados y 84/95 = 88.4 % en sin codificar. La cifra ya no es una inferencia: es un dato medido (V7) | V7 |
| E-09 | `thesis-delta-configs.md` §1, §5, §6 | el salto de cmdi en 3a se atribuye al ejecutor defectuoso, pero "no se volvio a correr" | Se volvio a correr (Fase 2a): el ejecutor anterior sobre el stack nuevo da 136/200 y el mismo veredicto en los 600 payloads que la medicion antigua. El ejecutor explica por si solo la diferencia | Fase 2a |
| E-10 | `thesis-delta-configs.md` §5 (y §1) | "la 3b bloquea 33 de los 36 y la Config 2 solo 29" tratado como conteo normal | No es error de conteo: 4 payloads (`cmdi_112`, `cmdi_134`, `cmdi_31`, `cmdi_38`) los bloquea la 3b y no los bloquea ni la 3a ni la Config 2. El agregado de la 3b (797) supera a la union de la Config 2 y la 3a (793) en 4 | V2 |
| E-11 | `thesis-delta-xss.md` §4 (fila Cuadro 38) | "3a/3b no se midieron en esta tarea" | Superado por `thesis-delta-configs.md`: las cuatro configuraciones se midieron con el corpus de 200 payloads de XSS | `thesis-delta-configs.md` |
| E-12 | `thesis-delta-configs.md` §7 | "Config 3a y 3b corrieron con --build; no se verifico el digest de imagen arranque por arranque" | Sigue siendo cierto. Ademas, en la Fase 2 la reconstruccion produjo otra imagen local de la aplicacion (`sha256:e22deaa793f0...`, distinta de `a75c14208ccd`) porque el contexto de build incluye archivos nuevos; la imagen del WAF no cambio (`sha256:f12da37e...`) | Fase 2 |

## 2. Verificaciones V1 a V10

### V1. Conjuntos de payloads no bloqueados (corrida 1)

Fuente: `attack-sim/results_combined_config{2,3a,3b}_run1_20261025.json`; script `docs/evidence/errata-v1-v5-v9-20261025.py`; salida `docs/evidence/errata-v1-v5-v9-20261025.json`.

| Categoria | abs(M3a) | abs(M2) | abs(M3b) | abs(M3a interseccion M2) | abs(M3a interseccion M2 interseccion M3b) |
|---|---|---|---|---|---|
| sqli | 1 | 1 | 0 | 0 | 0 |
| path_traversal | 3 | 0 | 0 | 0 | 0 |
| cmdi | 36 | 15 | 3 | 7 | 3 |
| xss | 11 | 0 | 0 | 0 | 0 |
| Total | 51 | 16 | 3 | 7 | 3 |

Ids: interseccion de 3a y Config 2 en cmdi: `cmdi_112`, `cmdi_134`, `cmdi_184`, `cmdi_185`, `cmdi_31`, `cmdi_38`, `cmdi_6`. Interseccion triple en cmdi: `cmdi_184`, `cmdi_185`, `cmdi_6` (son los tres no bloqueados de la 3b). Los ids de sqli y path_traversal no bloqueados por la 3a no coinciden con los de la Config 2 (en sqli la 3a y la Config 2 fallan cada una en un id distinto). La verdad: tres payloads no los bloquea ninguna configuracion (`cmdi_6`, `cmdi_184`, `cmdi_185`); siete no los bloquean ni la 3a ni la Config 2; de esos siete la 3b bloquea cuatro.

### V2. Payloads que la 3b bloquea y la libreria sola no

| Categoria | 3a no bloquea y la 3b si | 3a no bloquea y la Config 2 si | 3b si, Config 2 no (entre los que 3a no bloquea) |
|---|---|---|---|
| sqli | 1 | 1 | 0 |
| path_traversal | 3 | 3 | 0 |
| cmdi | 33 | 29 | 4: `cmdi_112`, `cmdi_134`, `cmdi_31`, `cmdi_38` |
| xss | 11 | 11 | 0 |

No es un error de conteo del delta. No hay ningun payload que bloquee la Config 2 y no bloquee la 3b. Ver Fase 2b.

### V3. XSS por configuracion, por campo y por transporte (corrida 1)

Fuentes: `attack-sim/results_combined_config*_run1_20261025.json` y `attack-sim/combined_corpus_round5_20261025.jsonl`; scripts `docs/evidence/errata-v3-strata-20261025.py`; salida `docs/evidence/errata-v3-strata-20261025.json` (incluye las tablas por contexto, vector, funcion y codificacion).

| Configuracion | n=200: k/n | Wilson 95 % | bio n=64: k/n | Wilson 95 % |
|---|---|---|---|---|
| Config 1 | 0/200 | [0.0, 1.9] | 0/64 | [0.0, 5.7] |
| Config 2 | 200/200 | [98.1, 100.0] | 64/64 | [94.3, 100.0] |
| Config 3a | 189/200 | [90.4, 96.9] | 59/64 | [83.0, 96.6] |
| Config 3b | 200/200 | [98.1, 100.0] | 64/64 | [94.3, 100.0] |

Config 1 (HTTP status): los 136 payloads dirigidos a `/posts` (68 en `content`, 68 en `title`) reciben 400, en los tres transportes; los 64 dirigidos a `bio` reciben 200. Confirmado.

Config 2 y Config 3b: los 200 reciben 403 (campo `bio` 64, `content` 68, `title` 68; transporte urlencoded 64, json 68, multipart 68).

Config 3a, HTTP status por campo y transporte:

| Estrato | 403 | 400 | 200 |
|---|---|---|---|
| bio (n=64) | 59 | 0 | 5 |
| content (n=68) | 63 | 5 | 0 |
| title (n=68) | 67 | 1 | 0 |
| urlencoded (n=64) | 64 | 0 | 0 |
| json (n=68) | 63 | 2 | 3 |
| multipart (n=68) | 62 | 4 | 2 |

Los 11 payloads que la 3a no bloquea (todos con codificacion `url_double`, todos en transporte json o multipart; ninguno en urlencoded):

| id | contexto | vector | funcion | codificacion | transporte | campo | status |
|---|---|---|---|---|---|---|---|
| xss_132 | attr_single | event_onmouseover | confirm | url_double | json | title | 400 |
| xss_156 | html_body | event_onload_body | alert | url_double | multipart | content | 400 |
| xss_249 | attr_unquoted | event_onmouseover | prompt | url_double | multipart | bio | 200 |
| xss_275 | attr_double | event_onfocus_autofocus | alert | url_double | multipart | content | 400 |
| xss_295 | svg | svg_onload | alert | url_double | multipart | content | 400 |
| xss_333 | html_body | event_onerror | fetch_externo | url_double | json | bio | 200 |
| xss_372 | attr_double | event_ontoggle | alert | url_double | multipart | bio | 200 |
| xss_380 | attr_single | event_onerror | fetch_externo | url_double | json | bio | 200 |
| xss_381 | html_comment | event_onerror | confirm | url_double | json | content | 400 |
| xss_394 | html_body | event_onmouseover | alert | url_double | json | bio | 200 |
| xss_55 | attr_single | event_ontoggle | prompt | url_double | multipart | content | 400 |

Por codificacion en la 3a: `url_double` 14/25 (Wilson [37.1, 73.3]); las otras nueve codificaciones, 100 % de bloqueo. Con y sin la subcadena `alert`: 12/17 y 177/183. Seis de los once llegan a la aplicacion con status 400 porque `content` y `title` no vulneran (la ruta exige ambos campos); cinco llegan con 200 a `bio`. No se investigo el mecanismo por el cual el WAF no bloquea la doble codificacion en json y multipart.

### V4. Sensibilidad: sin `xss_118`, `xss_254`, `xss_342`

Fuente: `docs/evidence/errata-v1-v5-v9-20261025.json`.

| Configuracion | n=197: k/n | Wilson 95 % | bio n=63: k/n | Wilson 95 % |
|---|---|---|---|---|
| Config 1 | 0/197 | [0.0, 1.9] | 0/63 | [0.0, 5.7] |
| Config 2 | 197/197 | [98.1, 100.0] | 63/63 | [94.3, 100.0] |
| Config 3a | 186/197 (94.4 %) | [90.3, 96.9] | 58/63 | [82.7, 96.6] |
| Config 3b | 197/197 | [98.1, 100.0] | 63/63 | [94.3, 100.0] |

Los tres ids estan bloqueados en las configuraciones 2, 3a y 3b. Ninguna conclusion cambia.

### V5. Denominadores equiparables (solo sqli, path_traversal y cmdi: 600 payloads)

| | Antes (documentado) | Ahora (600 payloads) | Ahora (800 payloads) |
|---|---|---|---|
| Ataques que 3a no bloquea | 68 | 40 (1 sqli, 3 pt, 36 cmdi) | 51 (1, 3, 36, 11 xss) |
| De esos, los que bloquea la 3b | 65 | 37 | 48 |
| De esos, los que bloquea la Config 2 | 64 | 33 | 44 |

Confirmado con los archivos. Los valores "antes" son los del texto actual de la tesis (`k-resultados.tex`, Cuadro 38 y su nota).

Agregados sobre 800 payloads (corrida 1): libreria sola (Config 2) 784, WAF solo (3a) 749, combinacion (3b) 797. Aporte del WAF sobre la libreria: 797 - 784 = +13 (1 sqli, 12 cmdi). Aporte de la libreria sobre el WAF: 797 - 749 = +48 (1 sqli, 3 pt, 33 cmdi, 11 xss). Union de payloads bloqueados por la Config 2 o la 3a: 793; la 3b bloquea 4 mas (V2).

### V6. Orden de operaciones y auditorias de fuga

`attack-sim/build_corpus.py`: para sqli genera los candidatos, los deduplica, los filtra con `exclusion_filter.py` (`filter_and_record`), los mezcla con semilla y toma los primeros 200. Para path_traversal y cmdi genera `2 x 200` candidatos, los filtra y toma los primeros 200. El orden es: generar, filtrar, tomar. XSS: `generate_xss.py` (400 candidatos), `sample_xss.py` (estratificado a 200) y luego `exclusion_filter_xss.py` sobre los 200 muestreados (0 descartes). El orden es: generar, muestrear, filtrar. Es el inverso.

Auditorias de fuga previas: `training/results/leakage_report.json` (repo `logSguarDian`) cubre el corpus de la Ronda 4 y el conjunto E2E, no el corpus de la Ronda 5. No hay en `docs/` ni `training/` de ninguno de los dos repositorios un reporte de subcadena normalizada para sqli, pt y cmdi de la Ronda 5. Se ejecuto la misma auditoria que `leakage_check_xss.py` (reutiliza `training/leakage_check.py`, solo lectura) sobre los cuatro corpus: `attack-sim/leakage_check_round5_all_20261025.py`, salida `attack-sim/leakage_report_round5_all_20261025.json`.

| Categoria (n=200) | Subcadena exacta | Subcadena normalizada | Igualdad normalizada de campo completo |
|---|---|---|---|
| sqli | 0 | 4 (`sqli_103`, `sqli_138`, `sqli_145`, `sqli_175`) | 4 |
| path_traversal | 5 | 7 (`path_traversal_119`, `_163`, `_198`, `_26`, `_29`, `_40`, `_57`) | 0 |
| cmdi | 0 | 2 (`cmdi_14`, `cmdi_78`) | 0 |
| xss | 0 | 3 (`xss_118`, `xss_254`, `xss_342`) | 0 |

(Union de las particiones train, val y test.) Los conteos de sqli (4 por igualdad normalizada), path_traversal (7 por subcadena, 0 por igualdad) y cmdi (2 por subcadena, 0 por igualdad) coinciden con los que reporta el trabajo de graduacion de Diego Valenzuela para la Ronda 5. Cinco payloads de path_traversal son ademas subcadena literal (exacta) de texto de entrenamiento.

### V7. Corpus combinado frente a la Ronda 5 original, y medicion antigua

Fuente: `attack-sim/large_corpus_requests.json`, `attack-sim/combined_corpus_round5_20261025.jsonl`; script `docs/evidence/errata-v7-20261025.py`.

Las 600 peticiones de sqli, pt y cmdi son identicas una a una: 0 con hash distinto, mismos ids, mismo orden. Hash global (SHA-256 de los hashes por peticion ordenados por id, sin el campo `schema`): `e3729614601db7999961b1c5c9bb4bc6a347f2207b0f621414c5d937d9c1aea7` en ambos. SHA-256 de `large_corpus_requests.json`: `68af7d2b071393c594f9a7587d925adad6dd9430e52b651122f2368cf5aaa3f5`; del corpus combinado: `f1fb0b0a2c552636358785ec323aa10c76519638d0da1cb62ce131be2330263d`.

Existen resultados por payload de las mediciones antiguas (`attack-sim/results_config{1,3a,3b}-round5-20261010.json`). Desglose de cmdi con la definicion del delta (payload con al menos un `%XX`; 105 codificados, 95 sin codificar); script `docs/evidence/errata-v7b-cmdi-encoding-20261025.py`, salida `docs/evidence/errata-v7b-cmdi-encoding-20261025.json`:

| Medicion | Codificados (n=105) | Sin codificar (n=95) | Total |
|---|---|---|---|
| 3a antigua (20261010, ejecutor defectuoso, otra rama) | 52 (49.5 %) [40.1, 58.9] | 84 (88.4 %) [80.4, 93.4] | 136 |
| 3a nueva (20261025, ejecutor corregido) | 80 (76.2 %) [67.2, 83.3] | 84 (88.4 %) [80.4, 93.4] | 164 |
| 3b antigua (20261010) | 104 (99.0 %) [94.8, 99.8] | 93 (97.9 %) [92.6, 99.4] | 197 |
| 3b nueva | 104 (99.0 %) [94.8, 99.8] | 93 (97.9 %) [92.6, 99.4] | 197 |
| Config 2 nueva (0.1.1) | 95 (90.5 %) [83.4, 94.7] | 90 (94.7 %) [88.3, 97.7] | 185 |
| Config 2 antigua (tarball par A, 0.1.0, ejecutor defectuoso) | 97 (92.4 %) [85.7, 96.1] | 86 (90.5 %) [83.0, 94.9] | 183 |
| Config 2 con 0.1.1 y ejecutor defectuoso (20261010) | 102 (97.1 %) [91.9, 99.0] | 90 (94.7 %) [88.3, 97.7] | 192 |

### V8. Imagen del WAF

Digest local de `owasp/modsecurity-crs:nginx-alpine`: `sha256:f12da37e72e29d1f06e7e829780f1016606d0799eac2966e58ef3819a3d30a50` (creada 2026-10-05, arquitectura arm64). El tag es flotante: `docker-compose.yml` lo usa sin digest, y hoy `docker buildx imagetools inspect owasp/modsecurity-crs:nginx-alpine` resuelve a un indice con digest `sha256:873ce68a658d2e3b61484a8a24d215f7d15456e7ce5aec5e7114bf000d743365`, cuyo manifiesto arm64 es `sha256:6d195d62b0866a2bd7437aca8f3ca1623668c77877a38e7fb1b16837914476cb`, distinto del digest medido. La medicion antigua tambien uso el tag sin digest (`origin/feat/waf-modsecurity-crs`, `docker-compose.yml:47`). El registro de auditoria antiguo versionado (`waf/audit/audit.log`, commit `00ea3a3`) reporta `OWASP_CRS/4.30.0`, igual que el nuevo. La version de ModSecurity y de nginx de la medicion antigua no se puede determinar con los archivos del repositorio (no se guardo digest ni version).

### V9. Estabilidad

4 configuraciones x 800 payloads x 3 corridas = 9600 payload-corridas; 6400 comparaciones contra la corrida 1. Payloads con veredicto distinto entre corridas: 0 en las cuatro configuraciones. Script `docs/evidence/errata-v1-v5-v9-20261025.py`.

### V10. Fidelidad del emisor de XSS a traves de nginx

Fuente: `attack-sim/waf-audit-20261025/audit-config3b-run1-20261025.jsonl` (registro de auditoria de la 3b, corrida 1; el de 3a no se conservo porque el directorio se vacio entre corridas; es el mismo WAF); script `docs/evidence/errata-v10-20261025.py`, salida `docs/evidence/errata-v10-20261025.json`.

El registro de ModSecurity no contiene cuerpos de peticion (0 de 797 registros). Comprobaciones posibles: los 200 registros de XSS se alinean por orden con los 200 payloads del corpus; el `Content-Length` registrado coincide con el largo en bytes del cuerpo que construye el emisor en los 200 (200/200), el `Content-Type` en 200/200 y la URI en 200/200. El valor de la variable `ARGS` que ModSecurity registra coincide con el esperado (o su prefijo, cuando el registro lo trunca con "characters omitted") en todos los registros que lo traen: urlencoded 64/64; json 63/63 (5 sin valor); multipart 62/62 (6 sin valor). Muestra de tres por transporte en el archivo de salida. Sin discrepancias.

## 3. Fase 2

### 2a. Aislar el ejecutor

Commit que corrigio la re-codificacion: `00ea3a3` (`git log --follow -- attack-sim/run_large_corpus.py`). Version anterior extraida con `git show 00ea3a3^:attack-sim/run_large_corpus.py` a `attack-sim/run_large_corpus_pre_fix_20261025.py`, SHA-256 `0c84de551f1138bbeb1ef7a9ed1801d83e4c52a7312c04b873a75de57a286623` (el ejecutor corregido es `422393460dfea808efe411d358166d37b662bbcaad77843ede0247c684c61af1`).

Stack: mismo arbol, `LOGSGUARDIAN_DISABLED=true`, `docker-compose.yml` mas `docker-compose.waf-audit-phase2a-override.yml` (archivo nuevo que solo redirige el volumen de auditoria a `attack-sim/waf-audit-phase2a-20261025/`), `COMPOSE_PROJECT_NAME=lsgp2a20261025`, puerto 3000 (publicado por el compose; no habia otro servicio usandolo). Imagen del WAF `sha256:f12da37e...`; imagen de la aplicacion reconstruida `sha256:e22deaa793f0...`. Corpus: las 600 peticiones de sqli, pt y cmdi del corpus combinado (identicas a las de la Ronda 5, V7), en `attack-sim/phase2a_legacy_corpus_input_20261025.json`. Dos corridas con el contenedor reiniciado. Resultados: `attack-sim/results_phase2a_prefixexecutor_config3a_run{1,2}_20261025.json` (SHA-256 identico entre ambas: `4cfefdf173e69b8ad79dc5a048745e1c7ca589fe94712943bba679fabd72fb40`); resumen en `docs/evidence/phase2a-summary-20261025.json`.

| Categoria | Ejecutor anterior, corrida 1 | Ejecutor anterior, corrida 2 | Ejecutor corregido (control en el mismo stack) |
|---|---|---|---|
| sqli | 199/200 | 199/200 | 199/200 |
| path_traversal | 197/200 | 197/200 | 197/200 |
| cmdi | 136/200 (68.0 %) | 136/200 (68.0 %) | 164/200 (82.0 %) |
| cmdi codificados | 52/105 (49.5 %) | 52/105 | 80/105 (76.2 %) |
| cmdi sin codificar | 84/95 (88.4 %) | 84/95 | 84/95 |

El veredicto de cada uno de los 600 payloads con el ejecutor anterior sobre el stack nuevo es igual al de la medicion antigua (`results_config3a-round5-20261010.json`): 0 ids distintos. El control con el ejecutor corregido en el mismo stack reproduce la corrida unificada (0 ids distintos). Del ejecutor anterior al corregido, 32 payloads de cmdi pasan de no bloqueados a bloqueados y 4 dejan de bloquearse (`cmdi_22`, `cmdi_38`, `cmdi_52`, `cmdi_179`), neto +28.

Interpretacion con la regla fijada de antemano: cmdi = 136, sqli y pt sin cambio, por lo tanto el ejecutor explica el salto (redaccion A). Corolario: la diferencia de aplicacion de la medicion antigua (rama distinta, 91 archivos) no produjo ningun cambio de veredicto en estos 600 payloads.

### 2b. Entrega de los payloads que solo bloquea la 3b

V2 confirmo cuatro payloads (`cmdi_112`, `cmdi_134`, `cmdi_31`, `cmdi_38`) que la 3b bloquea y la Config 2 y la 3a no. Se enviaron esos cuatro (y `cmdi_6` como control) con el ejecutor corregido a un servidor de captura de cabeceras nuevo (`attack-sim/capture_server_headers_20261025.py`; `attack-sim/capture_server.py` no registra cabeceras y no se modifico): una vez directo (ruta de la Config 2) y una vez a traves de un contenedor del mismo WAF (`owasp/modsecurity-crs:nginx-alpine`, PL1, reglas en On) cuyo backend es el servidor de captura (ruta de la 3b). Script `docs/evidence/phase2b-compare-20261025.py`; capturas `docs/evidence/phase2b-capture-20261025.json`; diferencias `docs/evidence/phase2b-diff-20261025.json`.

Para los cinco payloads, el cuerpo y el objetivo de la peticion son identicos por las dos rutas. Por el WAF llegan cuatro cabeceras adicionales (`X-REAL-IP`, `X-Forwarded-For`, `X-Forwarded-Port`, `X-Forwarded-Proto`) y la cabecera `Host` sin puerto. No se investigo mas alla ni se midio el efecto de esas cabeceras sobre el veredicto de la libreria.

## 4. Estado de git

HEAD `07e80ead6a64db5db086216322624bc5bfa4edb0` antes y despues; `git status` sin archivos con seguimiento modificados; solo archivos nuevos sin seguimiento. Los `.tex` de la tesis estan en `/Users/xtsebas/Desktop/tesis/tesis final`, que no es un repositorio de git (por eso no se creo una rama alli); su respaldo previo a las ediciones y las sumas SHA-256 estan en `docs/evidence/tex-before-20261025/`.
