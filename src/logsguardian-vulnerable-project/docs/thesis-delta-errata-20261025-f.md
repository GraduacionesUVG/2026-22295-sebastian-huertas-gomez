# Fe de erratas y verificación del ejecutor, sexta ronda, continuación (2026-10-25)

Este documento no modifica resultados, los documentos delta ni las erratas anteriores (`docs/thesis-delta-errata-20261025.md`, `-b`, `-c`, `-d` y `-e`). Registra la verificación del ejecutor de la Ronda 4 (A1 y A2, solo lectura) y las correcciones de redacción de esta ronda.

Rama `exp/ronda5-20261025`, HEAD `07e80ead6a64db5db086216322624bc5bfa4edb0`, sin commits ni cambios en archivos con seguimiento. Respaldo previo: `docs/evidence/tex-before-round6b-20261025/` (24 archivos, sumas en `SHA256SUMS.txt`). El nombre `tex-before-round6-20261025` ya estaba ocupado por el respaldo del prompt anterior, y por eso este lleva el sufijo `b`; igualmente, la sección del log de ediciones se llama "Sexta ronda, continuación" (ediciones 128 a 141).

## 1. A1. Qué cambia el ejecutor corregido

Diff de `attack-sim/run_large_corpus.py` entre `00ea3a3^` y `00ea3a3` (`git diff`, solo lectura). El ejecutor solo implementa dos transportes: consulta (GET) y formulario `application/x-www-form-urlencoded` (POST). No tiene rutas para JSON ni `multipart/form-data`; el emisor multi-transporte de XSS es `send_xss_corpus.py`, un archivo aparte de la tarea del corpus de XSS que no forma parte de ese commit.

El cambio es uno: se añade `_is_pre_encoded(categoría, valor)`, verdadero si la categoría es `path_traversal` o `cmdi` y el payload contiene al menos una secuencia `%[0-9a-fA-F]{2}`.

| Categoría | Transporte en el ejecutor | Condición | Petición |
|---|---|---|---|
| SQLi | GET (consulta) | cualquiera | Sin cambio (la categoría no está en el conjunto) |
| XSS | POST (formulario) | cualquiera | Sin cambio (la categoría no está en el conjunto) |
| Path Traversal | GET (consulta) | sin `%XX` | Sin cambio |
| Path Traversal | GET (consulta) | con `%XX` | Cambia: el valor se inserta tal cual en la consulta (antes se recodificaba) |
| Command Injection | POST (formulario) | sin `%XX` | Sin cambio |
| Command Injection | POST (formulario) | con `%XX` | Cambia: el valor se inserta tal cual en el cuerpo, y los parámetros extra se codifican con `quote` en lugar de `urlencode` |

El mismo commit eliminó los modelos y los tarballs vendorizados y tocó `src/app.js` y `package.json`; eso cambia la aplicación posterior, no la medición de la Ronda 4, que se hizo con el estado de `af61eba`.

## 2. A2. ¿Pudo la corrección alterar las peticiones de los 40?

Se determinó con datos: se construyeron, sin red, las peticiones de los 590 payloads de la Ronda 4 (corpus de `af61eba`) con el ejecutor anterior (`attack-sim/run_large_corpus_pre_fix_20261025.py`) y con el corregido, y se compararon método, URL, cuerpo y cabeceras. Script `docs/evidence/r6-ejecutor-peticiones-20261025.py`; salida `docs/evidence/r6-ejecutor-peticiones-20261025.json`.

| Categoría | Transporte | n | Idénticas | Distintas |
|---|---|---|---|---|
| SQLi | GET | 77 | 77 | 0 |
| XSS | POST formulario | 113 | 113 | 0 |
| Path Traversal | GET | 200 | 200 | 0 |
| Command Injection | POST formulario | 200 | 0 | 200 |

De los 40 ataques que el WAF no bloqueó (11 de SQLi, 3 de XSS y 26 de Path Traversal), ninguno tiene una petición distinta. Los 200 payloads de Path Traversal de la Ronda 4 no contienen `%XX`, a diferencia del corpus de la Ronda 5, que sí tenía payloads codificados (de ahí el defecto descrito en la Sección 9.4). Los 200 de Command Injection sí cambian de petición y no se remidieron.

Lo que se verificó es la igualdad de las peticiones, no del veredicto: la Ronda 4 no se repitió con el ejecutor corregido.

## 3. Correcciones de redacción (ediciones 128 a 141)

| Pedido | Dónde | Qué se hizo |
|---|---|---|
| B1 | Conclusión 8 (B), Sección 9.5, Recomendación 2 | La tercera razón (bloqueos indebidos y umbral, sin tasa de falsos positivos del WAF) se sustituye por la conexión con el modo `monitor`: la configuración recomendada es `monitor` hasta calibrar con el tráfico propio (recomendaciones 1 y 5), por lo que la librería no puede ser la única capa que bloquea; los bloqueos indebidos medidos (conclusión 9) sustentan esa recomendación pero no demuestran que el WAF tenga menos falsos positivos, cuya tasa no se midió |
| B2 | Los mismos tres lugares | "La librería no sustituye al WAF" pasa a "No se puede afirmar que la librería sustituya al WAF"; "se sostiene en otras razones" pasa a "no descansa en la cobertura medida sino en razones de prudencia, no de medición". La Acción de la Recomendación 2 conserva "y no como su sustituto" |
| B3 | Sección 9.6 | "Confirman el posicionamiento" pasa a "Respaldan en parte el posicionamiento", conservando el resto de la frase |
| B4 | Recomendación 2, Resultado esperado | Se añade que 797, 794 y 749 se midieron con la librería en modo `block` y que una instalación real exige antes la calibración de la recomendación 1 |
| B5 | Sección 9.5 | "ni que ninguna subsuma a la otra" se sustituye por la frase exacta: en Path Traversal, SQL Injection y XSS la librería con cabeceras subsume al WAF; en Command Injection el WAF bloquea 3 payloads que la librería con cabeceras deja pasar, de modo que en el corpus completo ninguna capa subsume a la otra (el WAF aporta 3 y la librería 48) |
| B6 | Secciones 8.4.3 y 9.5 | La frase sobre la corrección del ejecutor se reescribe con el resultado de A1 y A2, nombrando las tres categorías de los 40 |
| B7 | Conclusión 7 | Se añade que en XSS hubo 0 de 200 por igualdad del campo completo y 3 por subcadena normalizada |
| B8 | Recomendación 11 | La repetición de la cobertura con el paquete 0.1.0 se redacta explícitamente "con el ejecutor corregido", para separar el efecto del modelo, del middleware y del ejecutor |

Ediciones adicionales no pedidas, por coherencia: (1) las recomendaciones 1 y 5 reciben las etiquetas `rec:monitor` y `rec:monitor-defecto`, y los tres lugares las citan con `\ref` en lugar de números fijos; (2) la oración inicial de la Sección 9.6 pasa de "confirman dos de sus planteamientos" a "confirman uno, respaldan en parte otro y obligan a matizar un tercero", y su lista de razones sustituye "los bloqueos indebidos" por "la configuración recomendada es el modo monitor hasta calibrar"; (3) el cierre del párrafo de la Ronda 4 en la Sección 9.5 pasa de "no respalda por sí solo que no lo sustituya" a "no permite por sí solo afirmar ni descartar que lo sustituya". Sin ellas, esos tres puntos contradecían la formulación nueva.

No se tocó el Marco Teórico ni la Introducción. Ambos pueden contener formulaciones de "capa complementaria" que no se revisaron.

## 4. Verificaciones

| Comprobación | Resultado |
|---|---|
| `\ref` y `\label` | 147 etiquetas, 118 referencias distintas, 0 referencias sin etiqueta, 0 duplicadas |
| Etiquetas nuevas | `rec:monitor` en la recomendación 1 y `rec:monitor-defecto` en la 5 (comprobado simulando el conteo del `enumerate`) |
| Llaves y entornos | Balanceados en los ocho archivos |
| Comentarios `%` añadidos | 0 |
| Recomendaciones | 1 a 23 sin saltos ni repeticiones |
| Compilación | No hay LaTeX en este equipo |

## 5. Sin verificar

1. El veredicto de la Ronda 4 con el ejecutor corregido (las peticiones de los 40 son idénticas, pero la ronda no se repitió).
2. Los 200 de Command Injection de la Ronda 4 cambian de petición con el ejecutor corregido y no se remidieron; no pertenecen a los 40.
3. Si el Marco Teórico o la Introducción contienen la afirmación "capa complementaria y no sustituto" con el respaldo anterior; no se revisaron por instrucción.

## 6. Decisiones pendientes para el autor

1. Las recomendaciones 1 y 5 dicen que la librería debe estar en modo `monitor` hasta calibrar; la Recomendación 2 pide desplegarla detrás de un WAF, pero las cifras de cobertura del par (797 de 800) son en modo `block`. El texto ya lo declara. Queda como decisión si la tesis debe medir alguna vez la combinación con la librería en `monitor` (en ese modo la librería no bloquea y la cobertura de la combinación sería la del WAF solo, 749 de 800).
2. El Marco Teórico y la Introducción no se revisaron; conviene que el autor los lea con la misma pregunta (¿afirman que la librería no sustituye al WAF?).

## 7. Archivos nuevos de esta ronda

| Archivo | SHA-256 |
|---|---|
| `docs/evidence/r6-ejecutor-peticiones-20261025.py` | `43a3e1fde19bffbecc017243f0bfba047e5c081addc3fdd8aed1d86492ceeadc` |
| `docs/evidence/r6-ejecutor-peticiones-20261025.json` | `404e7f753aefeac1509a3f8ad72fd7819a1b8df2aadfd774142880b565c696e9` |
| `docs/evidence/tex-before-round6b-20261025/SHA256SUMS.txt` | `8760e9d7bee552e53f9d746ac65d2e86d3fcf3ca311fc462bbcb4326e7235b53` |

No se hicieron mediciones nuevas ni se levantó ningún contenedor.
