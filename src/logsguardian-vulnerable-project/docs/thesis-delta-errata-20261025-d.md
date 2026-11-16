# Fe de erratas y repeticiones, cuarta ronda (2026-10-25)

Este documento no modifica resultados, los documentos delta ni las erratas anteriores (`docs/thesis-delta-errata-20261025.md`, `-b` y `-c`). Registra las dos corridas adicionales con cabeceras (A1), la descomposición del aporte de cada capa en condiciones equiparadas (A2) y las correcciones a texto de rondas anteriores.

Rama `exp/ronda5-20261025`, HEAD `07e80ead6a64db5db086216322624bc5bfa4edb0`, sin commits ni cambios en archivos con seguimiento. Respaldo previo a la cuarta ronda: `docs/evidence/tex-before-round4-20261025/` (24 archivos, sumas en `SHA256SUMS.txt`). Wilson al 95 % con z = 1.959963984540054.

## 1. A1. Tres corridas con las cuatro cabeceras del proxy

Condiciones: Configuración 2 directa (`docker-compose.yml` más `docker-compose.direct.yml`, proyecto `lsgt6final20261025`, puerto 3000), `logsguardian` 0.1.1 con `rf.onnx` `25b407e6...` e `if.onnx` `5be28ee8...` verificados dentro del contenedor en cada corrida, ejecutor corregido, corpus combinado de 800 peticiones, cabeceras `X-REAL-IP: 192.168.65.1`, `X-Forwarded-For: 192.168.65.1`, `X-Forwarded-Port: 8080`, `X-Forwarded-Proto: http` en todas las peticiones (los inicios de sesión devolvieron 200). Entre corridas: `docker compose down -v` y `up -d --no-build`, de modo que el contenedor y la base de datos (volúmenes) se recrearon; la imagen fue la misma en las dos corridas nuevas (`sha256:d9b12672f000...`, la de la corrida 1, reconstruida en la ronda 3; `--no-build` evitó otra reconstrucción). Script `attack-sim/s1b_config2_proxy_headers_20261025.py`.

| Corrida | SQLi | Path Traversal | Command Injection | XSS | Total |
|---|---|---|---|---|---|
| 1 (ronda 3) | 200/200 | 200/200 | 194/200 | 200/200 | 794/800 |
| 2 | 200/200 | 200/200 | 194/200 | 200/200 | 794/800 |
| 3 | 200/200 | 200/200 | 194/200 | 200/200 | 794/800 |

Wilson al 95 %: SQLi, Path Traversal y XSS [98.1, 100.0]; Command Injection [93.6, 98.6]; total [98.4, 99.7]. Ids con veredicto distinto entre las tres corridas: ninguno. Ids con status HTTP distinto entre las tres corridas: ninguno. Resultado: la condición con cabeceras tiene ahora tres corridas idénticas, igual que la condición sin cabeceras (`results_combined_config2_run{1,2,3}_20261025.json`, errata V9).

## 2. A2. Descomposición en condiciones equiparadas

Fuente: `attack-sim/results_combined_config{2,3a,3b}_run1_20261025.json` y `attack-sim/results_s1_config2_con_cabeceras_run{1,2,3}_20261025.json`; script `docs/evidence/r4-analisis-20261025.py`, salida `docs/evidence/r4-analisis-20261025.json`.

| Cantidad | Esperado | Calculado |
|---|---|---|
| (a) Config 2 con cabeceras, total y por categoría | 794 | 794: SQLi 200, Path Traversal 200, Command Injection 194, XSS 200 |
| (b) 3b menos Config 2 sin cabeceras | 13 | 13 |
| (b) Efecto de las cabeceras sobre la librería (neto) | 10 | 10 (12 a bloqueado, 2 a no bloqueado) |
| (b) Aporte del WAF en condiciones equiparadas (3b menos Config 2 con cabeceras) | 3 | 3: `cmdi_9`, `cmdi_51`, `cmdi_94` (los tres de Command Injection; los bloquea la 3a y no la Config 2 con cabeceras) |
| (b) Suma | 13 = 10 + 3 | 13 = 10 + 3 (comprobado) |
| (c) De los cambios por cabeceras, entre los 51 que el WAF no bloquea | 4 | 4 netos: `cmdi_112`, `cmdi_134`, `cmdi_31`, `cmdi_38` (4 a bloqueado, 0 a no bloqueado) |
| (c) Entre los que el WAF sí bloquea | 6 | 6 netos: 8 a bloqueado (`cmdi_120`, `cmdi_155`, `cmdi_28`, `cmdi_36`, `cmdi_40`, `cmdi_66`, `cmdi_7`, `sqli_75`) menos 2 a no bloqueado (`cmdi_51`, `cmdi_94`) |
| (d) 51 payloads que el WAF no bloquea: Config 2 con cabeceras frente a 3b | coinciden | Coinciden 51 de 51 en cada una de las tres corridas (ambas bloquean 48) |
| (d) Sobre los 800 | no pedido | La Config 2 con cabeceras y la 3b difieren solo en `cmdi_51`, `cmdi_9` y `cmdi_94` (los tres del aporte del WAF) |

Las cifras esperadas coinciden con las calculadas. Aclaración sobre (c): los "10 que cambian" son un neto; hay 14 payloads con veredicto distinto (12 a bloqueado y 2 a no bloqueado), y el 6 de los que el WAF sí bloquea es 8 menos 2.

Discrepancias del cruce de verificación: ninguna. Las cabeceras bastan para explicar la diferencia entre la Configuración 2 y la librería dentro de la 3b en esos 51 payloads. Esto no prueba la causa en los demás: sobre los 800, la 3b se diferencia de la Config 2 con cabeceras solo por el aporte del WAF.

## 3. Correcciones a texto de rondas anteriores

| ID | Dónde | Decía | Problema | Corrección |
|---|---|---|---|---|
| F-07 | Secciones 8.4.3, 9.5, Conclusión 8, Recomendación 2, Cuadro 40, Anexo 13.8 (ronda 3) | "13 = 9 por el WAF + 4 por las cabeceras" | La descomposición mezclaba una unión calculada contra la Config 2 sin cabeceras: de los 9 payloads que "aporta el WAF", ocho los bloquea también la librería con cabeceras. En condiciones equiparadas el WAF aporta 3 | B3: 13 = 10 + 3 |
| F-08 | Secciones 8.4.3, 9.5 y Conclusión 8 | "en SQL Injection y en Command Injection cada capa bloquea payloads que la otra no" | Con cabeceras, la librería bloquea 200/200 de SQLi y el WAF no agrega nada; solo en Command Injection cada capa bloquea payloads que la otra no (3 el WAF, 33 la librería) | Corregido en las tres |
| F-09 | Pedido B7 | "las probabilidades del Random Forest son múltiplos de 1/30" | No es general: en las 66 filas de `detection_events` de E1 hay dos filas benignas (`GET /login` y `GET /posts`) con 0.9812 y 0.8867, que no son múltiplos de 1/30 (la tercera fila no ping, `POST /login` con 0.8000, sí lo es dentro de la precisión de float32). Los árboles tienen profundidad máxima 25, así que las hojas pueden no ser puras. En las 63 peticiones de `/admin/ping` de E1 los valores observados son 0.3000, 0.3333, 0.3667 y 0.4000, todos múltiplos de 1/30 | El texto se restringe a "los casos límite medidos" y a 30 árboles (`n_estimators = 30` en `training/retrain_v11_contract69.py`, línea 51; no se inspeccionó el ONNX) |
| F-10 | Sección 9 (Contraste con el Marco Teórico) | "la librería y el WAF perimetral detectan conjuntos parcialmente distintos" | Solo vale para la Ronda 4; en la Ronda 5 equiparada el WAF agrega 3 de 800 | Se aclara que el respaldo es el de la Ronda 4 |
| F-11 | Anexo 13.8 (ronda 3) | "La condición sin cabeceras se repitió en el mismo contenedor" | Había tres corridas de la medición unificada sin cabeceras (errata V9) más el control | Descripción de las corridas corregida |

## 4. Verificaciones de la fase B

| Comprobación | Resultado |
|---|---|
| `\ref` y `\label` | 145 etiquetas, 116 referencias distintas, 0 referencias sin etiqueta, 0 etiquetas duplicadas (nuevas: `tab:anx-descomposicion`) |
| Llaves y entornos | Balanceados en los ocho archivos tocados (se excluye `document`) |
| Comentarios `%` añadidos | 0 |
| Recomendaciones | 23, de 1 a 23, sin saltos ni repeticiones (no se añadió ninguna) |
| Residuos de la descomposición anterior | Una búsqueda de "9 los bloquea", "9 por el WAF", "4 por las cabeceras", "4 los bloquea", "4 se deben", "8 de Command", "+4" y "agrega 13" no deja ocurrencias; las menciones de "13 payloads" son la formulación nueva |
| Resumen y Abstract | Cifras sin cambio; se añadió "en despliegue directo" / "in direct deployment". Palabras: Resumen 296 (294 antes de esta ronda; incluye quitar una "y"), Abstract 254 (251). La oración sigue siendo larga por la calificación de "payloads no vistos"; es legible pero conviene vigilar el límite de palabras, que no consta en la plantilla |
| Compilación | No hay LaTeX en este equipo; la última compilación verificada es la de Overleaf previa a la ronda 3 |

## 5. Limpieza

Pila `lsgt6final20261025` bajada con `docker compose down -v` tras la última corrida; sin contenedores en ejecución; puerto 3000 libre. HEAD y `git status` de archivos con seguimiento sin cambios.

## 6. Archivos nuevos de esta ronda

| Archivo | SHA-256 |
|---|---|
| `attack-sim/s1b_config2_proxy_headers_20261025.py` | `98c1676e90df65528e495a787548f6d566b68dc205a5a86ce84b5351bb660b74` |
| `attack-sim/results_s1_config2_con_cabeceras_run2_20261025.json` | `67431ecf4168ceec40324877fec11b100cb198c800215c16bc5da6b1211b5613` |
| `attack-sim/results_s1_config2_con_cabeceras_run3_20261025.json` | `19f874a45012f95b645186f27547d1be75cd60b523e825fcc5a7a7e614481a4a` |
| `docs/evidence/r4-analisis-20261025.py` | `e80251d14afabae5fc381fa47a32cb01de4eb10776cac8885bd3e678a71b86b2` |
| `docs/evidence/r4-analisis-20261025.json` | `40c17435604be9852ce5df792d966b9d05147dc6f4e50ab7008a48dfdc2fe7f9` |
| `docs/evidence/tex-before-round4-20261025/SHA256SUMS.txt` | `c4fbfa2ce723d06571dc8d1a5dd9ba8b4b4d5afdc7e106d48f16b113a0c416fe` |

## 7. Decisiones pendientes para el autor

1. El Cuadro 38 sigue mostrando la Config 2 sin cabeceras junto a la 3b, que recibe las cabeceras del proxy; la nota lo declara y remite al Anexo 13.8, pero un lector que no lea la nota compara condiciones distintas. Por la regla fijada de antemano no se añadió una columna "Config 2 con cabeceras" al cuadro; es la opción más clara y queda a decisión del autor.
2. Con condiciones equiparadas, la Ronda 5 deja de respaldar con cobertura el posicionamiento de capa complementaria (el WAF suma 3 de 800 y la librería suma 48). La recomendación y la conclusión quedaron apoyadas en la Ronda 4, los bloqueos indebidos y el sesgo del corpus; el argumento del sesgo del corpus es una limitación declarada por el propio autor (Sección 7.11), no una medición. Un jurado puede objetar que la Ronda 4 tiene fuga confirmada en Command Injection (aunque ninguno de los 40 ataques que el WAF no bloqueó es de esa categoría).
3. Dos de los tres payloads que aporta el WAF en condiciones equiparadas (`cmdi_51` y `cmdi_94`) son órdenes `sleep`: con la librería sola y las cabeceras no se bloquean, llegan a la aplicación vulnerable y la petición termina por tiempo de espera. Cuentan como no detectados.
4. El texto afirma 30 árboles por el guion de entrenamiento (`retrain_v11_contract69.py`), no por inspección del ONNX; si se necesita certeza, hay que leer el número de árboles del archivo `rf.onnx`.
5. El número "13.8" depende de que el capítulo de Anexos sea el 13 al compilar.
6. Sigue pendiente compilar en Overleaf y revisar avisos `Overfull \hbox` en los cuadros del Anexo, ahora con un cuadro más (`tab:anx-descomposicion`).
