# Fe de erratas y sensibilidad, tercera ronda (2026-10-25)

Este documento no modifica resultados, los documentos delta ni las erratas anteriores (`docs/thesis-delta-errata-20261025.md` y `docs/thesis-delta-errata-20261025-b.md`). Registra la recalculación del aporte de cada capa (A1), una corrección a la errata-b, la sensibilidad S1 y las comprobaciones de la fase A.

Rama `exp/ronda5-20261025`, HEAD `07e80ead6a64db5db086216322624bc5bfa4edb0`, sin commits ni cambios en archivos con seguimiento. Respaldo previo a la tercera ronda: `docs/evidence/tex-before-round3-20261025/` (24 archivos, sumas en `SHA256SUMS.txt`). Wilson al 95 % con z = 1.959963984540054.

## 1. A1. Aporte de cada capa, recalculado

Fuente: `attack-sim/results_combined_config{2,3a,3b}_run1_20261025.json` (corrida 1, 800 payloads).

| Cantidad | Esperado | Recalculado |
|---|---|---|
| Bloqueados: Config 2 / 3a / 3b | 784 / 749 / 797 | 784 / 749 / 797 |
| Unión de bloqueados por la Config 2 o la 3a | 793 | 793 (sqli 200, path_traversal 200, cmdi 193, xss 200) |
| 3b menos Config 2 | 13 (1 sqli, 12 cmdi) | 13 (sqli 1, cmdi 12) |
| Aporte del WAF sobre la librería sola (unión menos Config 2; payloads que la 3a bloquea y la Config 2 no) | +9 (1 sqli, 8 cmdi) | +9: `sqli_75`, `cmdi_120`, `cmdi_155`, `cmdi_28`, `cmdi_36`, `cmdi_40`, `cmdi_66`, `cmdi_7`, `cmdi_9` |
| Efecto de las cabeceras del proxy (3b menos la unión) | +4 | +4: `cmdi_112`, `cmdi_134`, `cmdi_31`, `cmdi_38` (los mismos de E1) |
| 3b menos 3a | 48, de los que 4 por cabeceras | 48 (sqli 1, path_traversal 3, cmdi 33, xss 11); 44 son payloads que la Config 2 bloquea y 4 son los de las cabeceras |
| 3a menos 3b | no indicado | 0 |

Las cifras esperadas coinciden con las recalculadas. Se corrigió el texto en la Sección 8.4.3, la Sección 9.5, la Conclusión 8, la Recomendación 2 y la fila de defensa en profundidad del Cuadro 40; una búsqueda de "13 payloads", "agrega 13", "+13" y "12 de Command" no deja ocurrencias de la formulación anterior.

## 2. Corrección a la errata-b

La errata-b (§4) afirma que E1 se corrió con la imagen `a75c14208ccd` "sin reconstruir". Esa afirmación no estaba verificada. Docker Compose 5.5.1 reconstruye la imagen de la aplicación al cambiar el contexto de build (los archivos nuevos del repositorio lo cambian): al levantar la pila en esta ronda la imagen `lsgt6final20261025-app` pasó a `sha256:d9b12672f0007fd4f38672b3141a95b59935a6df99b2d56bff4f425ecd37bf85` (creada el 2026-10-25 23:05:36 UTC), y el identificador usado en la ronda 2 no se registró. Lo que sí se verificó en ambas rondas, dentro del contenedor, es el paquete `logsguardian` 0.1.1 y los hashes de los modelos (`rf.onnx` `25b407e6...`, `if.onnx` `5be28ee8...`). Las conclusiones de E1 no dependen de la imagen; en esta ronda la condición sin cabeceras reprodujo la corrida 1 payload por payload en la imagen reconstruida (ver §4). Es el mismo fenómeno de la errata E-12.

## 3. Comprobaciones de la fase A

| Comprobación | Resultado |
|---|---|
| A2 | El Resumen tenía "100.0 % en Path Traversal y 92.5 % en inyección de comandos y 100.0 % en Cross-Site Scripting" (doble "y" introducida por la edición A2 de la segunda ronda). Corregido. El Abstract ("100.0% of Path Traversal, 92.5% of command injection and 100.0% of cross-site scripting") no tiene el defecto |
| A3 | Las clases del Random Forest son `benign`, `cmdi`, `path_traversal`, `sqli`, `xss` (`parity_report.json` del paquete), las mismas cuatro clases de ataque del corpus. No existe un archivo que mida la distancia entre las distribuciones, y el texto lo dice |
| A5 `\ref` y `\label` | 144 etiquetas, 115 referencias distintas, 0 referencias sin etiqueta, 0 etiquetas duplicadas (incluida la nueva `anx:sensibilidad` y `tab:anx-sensibilidad`) |
| A5 llaves y entornos | Balanceados en los ocho archivos tocados (se excluye `document`) |
| A5 comentarios `%` | 0 añadidos |
| Recomendaciones | Siguen de 1 a 23 sin saltos (no se añadió ninguna) |
| Compilación | No hay LaTeX en este equipo; la compilación en Overleaf de la ronda anterior (main-10.pdf, 160 páginas) es la última verificada |

## 4. S1. Sensibilidad de la Configuración 2 a las cabeceras del proxy

Condiciones: Configuración 2 directa (`docker-compose.yml` más `docker-compose.direct.yml`, proyecto `lsgt6final20261025`, puerto 3000), `logsguardian` 0.1.1 con modelos del par C verificados por hash, ejecutor corregido (`run_large_corpus.py` y `send_xss_corpus.py`), corpus combinado de 800 peticiones, una corrida por condición. Cabeceras (valores de `docs/evidence/phase2b-capture-20261025.json`): `X-REAL-IP: 192.168.65.1`, `X-Forwarded-For: 192.168.65.1`, `X-Forwarded-Port: 8080`, `X-Forwarded-Proto: http`, añadidas a todas las peticiones, incluidos los inicios de sesión (ambos devolvieron 200). Script `attack-sim/s1_config2_proxy_headers_20261025.py`; resultados `attack-sim/results_s1_config2_{sin,con}_cabeceras_run1_20261025.json`; análisis `docs/evidence/s1-analisis-20261025.py` y `.json`.

Desviación del encargo: además de la corrida con cabeceras se hizo una corrida de control sin cabeceras en el mismo contenedor, porque la imagen se había reconstruido (§2). El control reprodujo la corrida 1 (`results_combined_config2_run1_20261025.json`) sin ningún id con veredicto o status distinto. Fue una corrida de 9 segundos y no se hizo ninguna otra.

| Categoría | Sin cabeceras | Con cuatro cabeceras | A bloqueado | A no bloqueado |
|---|---|---|---|---|
| SQLi | 199/200 [97.2, 99.9] | 200/200 [98.1, 100.0] | 1 | 0 |
| Path Traversal | 200/200 [98.1, 100.0] | 200/200 [98.1, 100.0] | 0 | 0 |
| Command Injection | 185/200 [88.0, 95.4] | 194/200 [93.6, 98.6] | 11 | 2 |
| XSS | 200/200 [98.1, 100.0] | 200/200 [98.1, 100.0] | 0 | 0 |
| Total | 784/800 [96.8, 98.8] | 794/800 [98.4, 99.7] | 12 | 2 |

Cambios de veredicto frente a la corrida 1 sin cabeceras:

| Dirección | ids |
|---|---|
| No bloqueado a bloqueado (12) | `cmdi_112`, `cmdi_120`, `cmdi_134`, `cmdi_155`, `cmdi_28`, `cmdi_31`, `cmdi_36`, `cmdi_38`, `cmdi_40`, `cmdi_66`, `cmdi_7`, `sqli_75` |
| Bloqueado a no bloqueado (2) | `cmdi_51` (`sleep 10`) y `cmdi_94` (`sleep 5`): ambos terminan por tiempo de espera, lo que se cuenta como no detectado |

Prueba exacta de McNemar sobre los 14 discordantes (12 frente a 2): p = 0.0129.

Relación con la 3b: de los 13 payloads que la 3b bloquea y la Config 2 sin cabeceras no, la Config 2 con cabeceras bloquea 12 (todos salvo `cmdi_9`). La unión de la Config 2 con cabeceras y la 3a es de 797 payloads, igual que la 3b, y 3b menos Config 2 con cabeceras son exactamente 3 payloads (`cmdi_9`, `cmdi_51`, `cmdi_94`). Dicho de otro modo, con las cabeceras la librería sola bloquea 48 de los 51 ataques que la 3a no bloquea (sin ellas, 44).

**Aviso expreso:** en Command Injection la diferencia con la corrida sin cabeceras es de 9 payloads (11 a bloqueado, 2 a no bloqueado), más de 2, y el total difiere en 10. La regla fijada de antemano se cumplió en lo principal: los Cuadros 37 y 38, el Resumen y el Abstract no cambian, y la sensibilidad se reporta en la nueva sección 13.8 del Anexo (`anx:sensibilidad`) y en la Sección 7.11. Se añadió además una referencia a esa sección en la descomposición de la Sección 8.4.3, la Sección 9.5, la Conclusión 8 y la nota del Cuadro 38, porque la descomposición "9 por el WAF y 4 por las cabeceras" solo vale para la Configuración 2 sin cabeceras.

## 5. Archivos nuevos de esta ronda

| Archivo | SHA-256 |
|---|---|
| `attack-sim/s1_config2_proxy_headers_20261025.py` | `46dd7a736079d0e956000f11e4abca77b4a283cecd3ab2d682729c93dd7e3eb2` |
| `attack-sim/results_s1_config2_sin_cabeceras_run1_20261025.json` | `a76cce52c7fa6d23a6ddf12c144739de1318d3b082c636df0dbd01357d3dee9a` |
| `attack-sim/results_s1_config2_con_cabeceras_run1_20261025.json` | `51f57d54539782e0279673285bc448fa6ca9aaf10769887be73d437865dcc3b3` |
| `docs/evidence/s1-analisis-20261025.py` | `40746e5e4baaffd61b87eba16c34faff51c04516a11d862b9bfbeba166e9c47a` |
| `docs/evidence/s1-analisis-20261025.json` | `8b8bf7688636bd15e1afadfc423774f0aabdc9a66e8ce08b3f92b1183aaf8113` |
| `docs/evidence/tex-before-round3-20261025/SHA256SUMS.txt` | `af990527cbf1c30cbcac447d204e3ff9a27982bd4cdfbcd0f0b45c52356654d7` |

También nuevo: `docs/evidence/tex-before-round3-20261025/` (copia de los 24 archivos previos a la ronda) y este documento. Pila `lsgt6final20261025` bajada con `docker compose down -v`; sin contenedores en ejecución; puerto 3000 libre.

## 6. Decisiones pendientes para el autor

1. La comparación de defensa en profundidad mezcla dos condiciones: la 3b recibe las cuatro cabeceras del proxy y la Config 2 no. Con las cabeceras, la librería sola bloquea 794 de 800 y el WAF agrega 3 (de los cuales 2 son órdenes `sleep` que, sin bloqueo, llegan a la aplicación y terminan por tiempo de espera). La complementariedad sigue siendo asimétrica, pero el aporte del WAF depende de la condición: 13 payloads sobre la Config 2 sin cabeceras, 3 sobre la Config 2 con ellas. Se mantuvo el texto pedido (9 por el WAF y 4 por las cabeceras) con la salvedad y la referencia a la 13.8; el autor decide si la Config 2 con cabeceras debe pasar a ser la referencia de la comparación.
2. La Config 2 de los Cuadros 37 y 38 describe un despliegue sin proxy. Una aplicación real detrás de un proxy inverso entrega cabeceras que la medición no incluyó. Por el efecto observado (+10 en total, +9 en Command Injection) no es un detalle menor; la regla fijada de antemano impidió cambiar las cifras principales.
3. El efecto de las cabeceras pasa por una única característica, `unusual_headers_count` (errata-b §4). Ya se anotó como hallazgo para el componente de IA.
4. Para S1 se hizo una corrida por condición. La condición sin cabeceras ya tenía tres corridas idénticas (errata anterior), pero la condición con cabeceras no se repitió.
5. El número "13.8" depende de que el capítulo de Anexos sea el 13 en la compilación; la referencia es automática (`\ref{anx:sensibilidad}`).
6. Corrección a la errata-b (§2 de este documento): la imagen de E1 no se puede afirmar como `a75c14208ccd`.
