# Registro de ediciones de la tesis (2026-10-25)

Este documento registra cada edición hecha a los archivos `.tex` de `/Users/xtsebas/Desktop/tesis/tesis final/` para incorporar la Ronda 5 (corpus de XSS n=200 y cuatro configuraciones remedidas el 25 de octubre de 2026). No modifica resultados ni los documentos delta.

Rama de datos: `exp/ronda5-20261025` del repositorio `logSguarDian-vulnerable-project`, HEAD `07e80ead6a64db5db086216322624bc5bfa4edb0`, sin commits. La carpeta de los `.tex` no es un repositorio de git, por lo que no se pudo crear una rama allí; el respaldo previo a las ediciones y sus sumas SHA-256 están en `docs/evidence/tex-before-20261025/`. Las líneas originales se miden sobre ese respaldo; las nuevas, sobre los archivos actuales.

## Ediciones por archivo

| Archivo | Ediciones |
|---|---|
| b-resumen.tex | 1 |
| c-abstract.tex | 1 |
| j-metodologia.tex | 20 |
| k-resultados.tex | 20 |
| l-discusion.tex | 7 |
| m-conclusiones.tex | 2 |
| n-anexos.tex | 1 |
| n-recomendaciones.tex | 7 |
| **Total** | **59** |

Las ediciones con el sufijo de corrección (J-4.4-fecha, J-7.11-proxy-precision, D-defensa-ci, K-8.4.3-ci) afinan texto que introduje en esta misma sesión y no tienen línea original.

## Detalle

### 01. J-enfoque: j-metodologia.tex, línea original 81, línea actual 81

Ubicación: Sec 7.1, variables extrañas (barrido: "misma imagen").

Antes:

```
servidor anfitrión idéntico entre condiciones (misma imagen Docker, misma base de datos
sembrada) controlan
```

Después:

```
servidor anfitrión idéntico entre condiciones (mismo árbol de la aplicación, mismo
\texttt{Dockerfile}, misma base de datos sembrada) controlan
```

Fuente: docs/thesis-delta-configs.md §4 (Sección 7.4.4 / Procedimiento 4.1) y §2 (Dockerfile SHA-256 7f1edcdd...); errata E-12 (la imagen local de la aplicación no se verificó por digest en cada arranque, de ahí que se diga mismo árbol y mismo Dockerfile y no misma imagen).

### 02. J-M2-fila: j-metodologia.tex, línea original 209, línea actual 209

Ubicación: Cuadro de muestras, fila M2.

Antes:

```
M2. Corpus limpio de evaluación (Ronda~5) & 200 SQLi (sqlmap), 200 Path Traversal y 200 Command
Injection (generadores propios); 1 payload de XSS confirmado con OWASP ZAP & Intencional, con filtro de exclusión contra el entrenamiento &
```

Después:

```
M2. Corpus limpio de evaluación (Ronda~5) & 200 SQLi (sqlmap), 200 Path Traversal y 200 Command
Injection (generadores propios), y 200 XSS (generador propio, 25 de octubre de 2026); el payload único de XSS confirmado con OWASP ZAP se conserva aparte como hallazgo & Intencional, con filtro de exclusión contra el entrenamiento &
```

Fuente: docs/thesis-delta-xss.md §1 y §4 (Cuadro 36); attack-sim/xss_corpus_filtered_20261025.jsonl (n=200).

### 03. J-M2-texto: j-metodologia.tex, línea original 229, línea actual 229

Ubicación: Sec 7.3, párrafo posterior al Cuadro de muestras (n=1).

Antes:

```
La categoría XSS de M2 se reduce a un único payload confirmado con OWASP ZAP (n=1); la restricción
correspondiente se declara en la Sección~\ref{sec:met-restricciones}.
```

Después:

```
La categoría XSS de M2 se amplió el 25 de octubre de 2026 con un corpus propio de 200 payloads
(Procedimiento~4.3); el payload único confirmado con OWASP ZAP se conserva como hallazgo de
explotabilidad (n=1), con la restricción declarada en la Sección~\ref{sec:met-restricciones}.
```

Fuente: docs/thesis-delta-xss.md §4 (Procedimiento 4.3 / Sección 7.5; Sección 7.12).

### 04. J-par-C-0.1.1: j-metodologia.tex, línea original 414, línea actual 415

Ubicación: Sec 7.4.2, párrafo de paquetes (3b con 0.1.1).

Antes:

```
Con la 0.1.1 solo se midió la cobertura de la Configuración~2 de la Ronda~5, con el ejecutor
original y con el corregido; las aplicaciones de terceros
```

Después:

```
Con la 0.1.1 se midió la cobertura de la Configuración~2 de la Ronda~5, con el ejecutor
original y con el corregido, y, el 25 de octubre de 2026, la de las Configuraciones 2 y 3b con el
ejecutor corregido; las aplicaciones de terceros
```

Fuente: docs/thesis-delta-configs.md §2 (fila de la Configuración 3b: logsguardian 0.1.1 del registro, tarball SHA-256 abf8d5c4..., rf.onnx 25b407e6..., if.onnx 5be28ee8...) y §6 (verificado byte a byte en 2 y 3b por separado).

### 05. J-par-C-metrica: j-metodologia.tex, línea original 425, línea actual 427

Ubicación: Sec 7.4.2, última frase del párrafo de paquetes.

Antes:

```
de modo que esa métrica existe para los pares A y C, y para la versión 0.1.1 publicada solo en la Configuración~2.
```

Después:

```
de modo que esa métrica existe para los pares A y C, y para la versión 0.1.1 publicada en las Configuraciones 2 y 3b.
```

Fuente: Ídem J-par-C-0.1.1.

### 06. J-cuadro12-C: j-metodologia.tex, línea original 389, línea actual 390

Ubicación: Cuadro 12 (pares de modelos), fila C.

Antes:

```
repetición de la Ronda~5 con el tarball de validación 22550ea; OWASP Juice Shop (copia local) \\ \hline
```

Después:

```
repetición de la Ronda~5 con el tarball de validación 22550ea; OWASP Juice Shop (copia local); Configuraciones 2 y 3b de la medición unificada del 25 de octubre de 2026 (paquete 0.1.1 del registro, archivo \texttt{abf8d5c4...}) \\ \hline
```

Fuente: Ídem J-par-C-0.1.1; docs/thesis-delta-configs.md §4 (Sección 7.4.2 / Cuadro 12).

### 07. J-4.1-c1: j-metodologia.tex, línea original 505, línea actual 507

Ubicación: Procedimiento 4.1, Configuración 1.

Antes:

```
\item \textbf{Configuración 1 (control):} aplicación sin protección, para confirmar que cada
    payload es explotable y establecer la línea base.
```

Después:

```
\item \textbf{Configuración 1 (control):} aplicación sin protección (con
    \texttt{LOGSGUARDIAN\_DISABLED=true}), para confirmar que cada payload es explotable y
    establecer la línea base.
```

Fuente: docs/thesis-delta-configs.md §2 (Configuración 1: docker-compose.yml + docker-compose.direct.yml, LOGSGUARDIAN_DISABLED=true).

### 08. J-4.1-mecanismo: j-metodologia.tex, línea original 515, línea actual 518

Ubicación: Sec 7.4.4 / Procedimiento 4.1, mecanismo y transparencia.

Antes:

```
Se eligió el nivel de paranoia 1 porque es la configuración realista para la población
objetivo:
```

Después:

```
Las cuatro configuraciones se levantan con el mismo árbol de la aplicación, el mismo
\texttt{Dockerfile} y el mismo \texttt{docker-compose.yml}. La librería se desactiva en las
Configuraciones 1 y 3a con la variable de entorno \texttt{LOGSGUARDIAN\_DISABLED=true}, sin
modificar ningún archivo con seguimiento. Las Configuraciones 1 y 2 publican la aplicación
directamente con \texttt{docker-compose.direct.yml}; en la 3a y la 3b el WAF se coloca delante, y
un archivo adicional (\texttt{docker-compose.waf-audit-override.yml}) solo redirige el volumen del
registro de auditoría. El WAF es la imagen \texttt{owasp/modsecurity-crs:nginx-alpine}, con
Nginx 1.30.5, ModSecurity 3.0.17 y OWASP CRS 4.30.0, nivel de paranoia 1,
\texttt{SecRuleEngine On}, umbral de anomalía de entrada de 5 y sin exclusiones activas. La
etiqueta de esa imagen es flotante, por lo que se cita su digest
(\texttt{sha256:f12da37e...}) y no la etiqueta. En las Configuraciones 2 y 3b se verificó, por
separado, que el paquete \texttt{logsguardian} 0.1.1 es el del registro de npm (SHA-256 del
archivo \texttt{abf8d5c4...}) y que los modelos son los del par~C (\texttt{25b407e6...} y
\texttt{5be28ee8...}). Una medición anterior de la Configuración~3a, hecha el 10 de octubre de 2026
en otra rama de la aplicación y con el ejecutor anterior a la corrección, se descartó y se
reemplazó por la de este procedimiento.

Se eligió el nivel de paranoia 1 porque es la configuración realista para la población
objetivo:
```

Fuente: docs/thesis-delta-configs.md §2 (compose por configuración; WAF: Nginx 1.30.5, ModSecurity 3.0.17, CRS 4.30.0, SecRuleEngine On, paranoia 1, umbral de entrada 5, sin exclusiones activas, digest sha256:f12da37e72e29d1f06e7e829780f1016606d0799eac2966e58ef3819a3d30a50) y §6 (paquete verificado); errata V8 (etiqueta flotante), §1 de configs (rama antigua de 3a divergente en 91 archivos); attack-sim/results_config3a-round5-20261010.json (medición descartada).

### 09. J-4.3-semilla: j-metodologia.tex, línea original 535, línea actual 555

Ubicación: Procedimiento 4.3, primer párrafo.

Antes:

```
El corpus M2 se genera con un
script versionado (\texttt{build\_corpus.py}) y semilla fija (20260923), de modo que dos
ejecuciones sobre las mismas entradas producen el mismo corpus:
```

Después:

```
El corpus M2 se genera con
scripts versionados y semilla fija, de modo que dos ejecuciones sobre las mismas entradas
producen el mismo corpus: SQLi, Path Traversal y Command Injection con
\texttt{build\_corpus.py} y la semilla 20260923, y XSS con \texttt{generate\_xss.py} y la semilla
20261025, que difiere de la anterior en la semilla y en la fecha (25 de octubre de 2026):
```

Fuente: docs/thesis-delta-xss.md §2 (generate_xss.py, semilla 20261025, 25 de octubre de 2026); semilla 20260923 ya existente en el texto.

### 10. J-4.3-xss: j-metodologia.tex, línea original 552, línea actual 574

Ubicación: Sec 7.5 / Procedimiento 4.3, viñeta XSS.

Antes:

```
\item \textbf{XSS:} OWASP ZAP \cite{owaspzap}, con un \textit{Active Scan} dirigido por su API REST
    contra \texttt{POST /posts} (campos \texttt{content} y \texttt{title}) y \texttt{POST /profile}
    (campo \texttt{bio}), con sesión autenticada. ZAP reporta una alerta por cada combinación de
    parámetro y técnica confirmada como vulnerable, no cada payload probado; por eso el corpus de
    XSS contiene un solo payload, el confirmado, y no se completó con variantes escritas a mano.
\end{itemize}
```

Después:

```
\item \textbf{XSS:} generador propio determinista (\texttt{generate\_xss.py}, semilla 20261025),
    no derivado de listas públicas, que combina cuatro dimensiones: 8 contextos de inyección, 9
    vectores de ejecución, 7 funciones ejecutadas y 10 codificaciones o evasiones, con un mapeo
    explícito de los vectores válidos en cada contexto. Genera 400 candidatos, de los que
    \texttt{sample\_xss.py} toma 200 por muestreo estratificado. Una quinta dimensión, que se aplica
    al muestrear, combina 3 transportes (\texttt{application/x-www-form-urlencoded}, JSON y
    \texttt{multipart/form-data}) con 3 campos de destino (\texttt{content} y \texttt{title} de
    \texttt{POST /posts}, y \texttt{bio} de \texttt{POST /profile}). Ningún valor de una dimensión
    supera el 30~\% del corpus, salvo el transporte y el campo, que solo tienen tres valores y para
    los que el mínimo posible del valor más frecuente es 33.3~\%; en esas dos dimensiones se fijó un
    tope de 34~\%. El protocolo se congeló antes de la medición (\texttt{docs/protocol-xss.md}). El
    payload único que confirmó OWASP ZAP \cite{owaspzap} con un \textit{Active Scan} dirigido por su
    API REST contra \texttt{POST /posts} (campos \texttt{content} y \texttt{title}) y
    \texttt{POST /profile} (campo \texttt{bio}), con sesión autenticada, se conserva como hallazgo de
    vulnerabilidad real y no como corpus de medición: ZAP reporta una alerta por cada combinación de
    parámetro y técnica confirmada como vulnerable, no cada payload probado.
\end{itemize}
```

Fuente: docs/protocol-xss.md (T4: 8 contextos, 9 vectores, 7 funciones, 10 codificaciones; 3 transportes x 3 destinos; T5: 400 a 200, tope de 30 %, 34 % en transporte y campo, mínimo matemático 33.3 %); docs/thesis-delta-xss.md §7.

### 11. J-4.3-filtro-a: j-metodologia.tex, línea original 559, línea actual 592

Ubicación: Procedimiento 4.3, filtro de exclusión.

Antes:

```
Todo candidato pasa por un filtro de exclusión antes de entrar al corpus: se descarta si su hash
```

Después:

```
Todo candidato de SQLi, Path Traversal y Command Injection pasa por un filtro de exclusión antes de entrar al corpus: se descarta si su hash
```

Fuente: errata V6 (orden en build_corpus.py: generar, filtrar, tomar; XSS: generar, muestrear, filtrar).

### 12. J-4.3-800: j-metodologia.tex, línea original 563, línea actual 596

Ubicación: Procedimiento 4.3, cierre (601 a 800 peticiones; filtro XSS posterior al muestreo).

Antes:

```
De cada
categoría de SQLi, Path Traversal y Command Injection se seleccionan 200 payloads finales; el corpus
resultante tiene 601 peticiones.
```

Después:

```
De cada
categoría se seleccionan 200 payloads finales; el corpus resultante tiene 800 peticiones. En XSS,
el filtro de exclusión (\texttt{exclusion\_filter\_xss.py}) se aplicó sobre los 200 payloads ya
muestreados, es decir, después y no antes del muestreo, y descartó 0. La auditoría posterior de
fuga (\texttt{leakage\_check\_xss.py}), que mide contención de subcadena normalizada, encontró 3
payloads coincidentes que el filtro no había atrapado, y por regla del protocolo no se corrigieron.
```

Fuente: errata V6 (exclusion_report_xss_20261025.json: 0 descartes; leakage_report_xss_20261025.json: 3 coincidencias normalizadas por subcadena) y V7 (600 peticiones idénticas al corpus original).

### 13. J-4.4-3b: j-metodologia.tex, línea original 577, línea actual ver archivo

Ubicación: Sec 7.4.4 / Procedimiento 4.4, cierre (paquete de 3a y 3b).

Antes:

```
Las
cuatro configuraciones del Procedimiento~4.1 se ejecutaron sobre el corpus limpio; la
Configuración~3a, que no incorpora la librería, se ejecutó en una rama distinta de la aplicación
mediante un árbol de trabajo de git, y de las Configuraciones 3a y 3b no consta el paquete exacto: el directorio de dependencias
de su commit contiene el archivo de la 0.1.0 del registro, pero los resultados no registran cuál
se ejecutó. La Configuración~2 se repitió además con el paquete 0.1.1, instalado desde el registro de npm, y con
el ejecutor corregido.
```

Después:

```
En la
Ronda~5 original (10 de octubre de 2026), las cuatro configuraciones del Procedimiento~4.1 se
ejecutaron sobre el corpus limpio de 601 peticiones; la Configuración~3a se midió entonces en una
rama distinta de la aplicación, y esa medición se descartó (Procedimiento~4.1). La Configuración~2
se repitió además con el paquete 0.1.1, instalado desde el registro de npm, y con el ejecutor
corregido. El 25 de octubre de 2026 las cuatro configuraciones se midieron de nuevo sobre el mismo
árbol de la aplicación, con el ejecutor corregido y con el corpus combinado de 800 peticiones (las
600 de SQLi, Path Traversal y Command Injection, idénticas una a una a las del corpus original, más
200 de XSS), en tres corridas por configuración con el contenedor y la base de datos reiniciados
entre una y otra. Los payloads de XSS se envían con un emisor propio
(\texttt{send\_xss\_corpus.py}) en los tres transportes, que aplica la convención del ejecutor
corregido a los payloads ya codificados.
```

Fuente: errata V7 (corpus de 600 peticiones idéntico; SHA-256 del combinado f1fb0b0a...), V9 (tres corridas, 0 cambios de veredicto), docs/thesis-delta-xss.md §2 (send_xss_corpus.py); fechas de los archivos results_config*-round5-20261010.json y results_config2-develop-tarball-20261009.json.

### 14. J-7.5-zap: j-metodologia.tex, línea original 707, línea actual 748

Ubicación: Sec 7.5, párrafo de ZAP.

Antes:

```
Su resultado es un único payload confirmado, por lo que la cobertura de
XSS tiene n=1 (Sección~\ref{sec:met-restricciones}).
```

Después:

```
Su resultado es un único payload confirmado, que se conserva como hallazgo de explotabilidad
(n=1; Sección~\ref{sec:met-restricciones}) y no como corpus de medición: la cobertura de XSS se mide
con el generador propio de 200 payloads (Procedimiento~4.3).
```

Fuente: docs/thesis-delta-xss.md §4 (Procedimiento 4.3 / Sección 7.5).

### 15. J-4.4-fecha: j-metodologia.tex, línea original no aplica, línea actual 614

Ubicación: Procedimiento 4.4, corrección de fecha (correctiva de la edición J-4.4-3b).

Antes:

```
Ronda~5 original (10 de octubre de 2026), las cuatro configuraciones del Procedimiento~4.1 se
```

Después:

```
Ronda~5 original (9 y 10 de octubre de 2026), las cuatro configuraciones del Procedimiento~4.1 se
```

Fuente: Corrección de fecha de J-4.4-3b: los archivos de la Ronda 5 original son del 9 y 10 de octubre (results_config2-develop-tarball-20261009.json, results_config*-round5-20261010.json).

### 16. J-7.11-generaciones: j-metodologia.tex, línea original 1029, línea actual 1071

Ubicación: Sec 7.11, viñeta de generaciones de modelo (3b en par C).

Antes:

```
y la evaluación en OWASP Juice Shop, al par~C
    (Cuadro~\ref{tab:pares-modelos}).
```

Después:

```
la evaluación en OWASP Juice Shop y las Configuraciones 2 y 3b de la medición unificada del 25 de
    octubre de 2026, al par~C (Cuadro~\ref{tab:pares-modelos}).
```

Fuente: docs/thesis-delta-configs.md §2 (3b con el par C).

### 17. J-7.11-ejecutor: j-metodologia.tex, línea original 1050, línea actual 1092

Ubicación: Sec 7.11, viñeta de defectos de recodificación (benchmark/ejecutor anterior de 3a y 3b).

Antes:

```
Todas las
    mediciones de Path Traversal y de Command Injection de la Ronda~5, y las de la Ronda~4 que usaron
    el mismo ejecutor, se hicieron con el ejecutor anterior, salvo la Configuración~2 con el paquete
    0.1.1. No se midió el paquete 0.1.0 con el ejecutor corregido, por lo que no puede separarse
    cuánto de la mejora de 85.0~\% a 100.0~\% se debe al modelo, al middleware y al ejecutor; y las
    Configuraciones 3a y 3b, que incluyen un WAF, tampoco se repitieron, así que su comparación en
    esas dos categorías es provisional.
```

Después:

```
Las mediciones de
    Path Traversal y de Command Injection de la Ronda~5 con el paquete 0.1.0 y con el tarball de
    validación, y las de la Ronda~4 que usaron el mismo ejecutor, se hicieron con el ejecutor
    anterior. La Configuración~2 con el paquete 0.1.1 y las cuatro configuraciones de la medición
    unificada del 25 de octubre de 2026 se hicieron con el ejecutor corregido. No se midió el
    paquete 0.1.0 con el ejecutor corregido, por lo que no puede separarse cuánto de la mejora de
    85.0~\% a 100.0~\% se debe al modelo, al middleware y al ejecutor. Para el WAF sí se aisló el
    efecto del ejecutor: el ejecutor anterior, ejecutado sobre el árbol y la pila actuales,
    reprodujo el 68.0~\% de Command Injection de la medición del 10 de octubre (136 de 200, con el
    mismo veredicto en los 600 payloads de esa medición), y el ejecutor corregido dio 164 de 200
    (82.0~\%); la diferencia se debe a que el ejecutor anterior volvía a codificar los separadores
    ya codificados, y no a la versión de la aplicación.
```

Fuente: errata Fase 2a (docs/evidence/phase2a-summary-20261025.json: ejecutor anterior 136/200, 0 ids distintos en 600 payloads respecto de results_config3a-round5-20261010.json; ejecutor corregido 164/200) y V7.

### 18. J-7.11-nuevas: j-metodologia.tex, línea original 1057, línea actual ver archivo

Ubicación: Sec 7.11, nuevas amenazas a la validez (10 solicitadas + proxy).

Antes:

```
\item \textbf{La medición con el paquete 0.1.1 no es independiente.}
```

Después:

```
\item \textbf{Corpus de XSS construido después de conocer los resultados de la Ronda~5.} El
    corpus propio de XSS se diseñó el 25 de octubre de 2026, con el conocimiento de que la Ronda~5
    original medía XSS con n=1 y de que las otras categorías ya tenían generadores propios. La
    medición no es ciega, y el 200 de 200 no puede leerse como una evaluación independiente.
    \item \textbf{Sesgo del autor en el generador de XSS.} Las cuatro dimensiones, sus valores y el
    mapeo de los vectores válidos en cada contexto los diseñó el autor del generador, no se
    derivaron de una taxonomía publicada; la cobertura medida depende de las combinaciones que se
    consideraron válidas.
    \item \textbf{Coincidencias con el entrenamiento que el filtro no eliminó.} La auditoría de
    subcadena normalizada (\texttt{leakage\_check.py}, sobre las particiones de entrenamiento,
    validación y prueba) encontró 3 de los 200 payloads de XSS (\texttt{xss\_118},
    \texttt{xss\_254} y \texttt{xss\_342}) con coincidencia, que el filtro, con 0 descartes, no
    atrapó porque solo descarta la igualdad exacta de la forma normalizada del campo completo; por
    regla del protocolo no se corrigieron ni se retiraron. Los tres se bloquean en las
    Configuraciones 2, 3a y 3b, y sin ellos la librería sigue bloqueando 197 de 197.
    \item \textbf{Auditoría de subcadena en las cuatro categorías.} Aplicada el 25 de octubre de
    2026 a los cuatro corpus, la misma auditoría encontró coincidencias normalizadas por subcadena
    en 4 de los 200 payloads de SQLi, 7 de Path Traversal, 2 de Command Injection y 3 de XSS (por
    igualdad del campo completo, 4 de SQLi y ninguno en las demás). Es un criterio permisivo, que
    sirve como límite superior y no como medida de solapamiento, y el filtro de exclusión de la
    Ronda~5 no lo aplicaba.
    \item \textbf{Campos de XSS sin vulnerabilidad confirmada.} De los 200 payloads de XSS, 136 (68
    en \texttt{content} y 68 en \texttt{title}) se dirigen a campos de \texttt{POST /posts} donde
    ZAP no confirmó vulnerabilidad, y sin protección la aplicación los rechaza con HTTP 400; miden
    la detección y no la explotabilidad. Solo los 64 dirigidos a \texttt{bio} apuntan a un campo
    con vulnerabilidad confirmada.
    \item \textbf{Congelación del protocolo de XSS sin historial de git.} Que el protocolo y los
    artefactos del corpus de XSS no cambiaron entre su congelación y la medición se verificó con un
    manifiesto de sumas SHA-256 (\texttt{docs/freeze-xss-20261025.json}), recalculado antes y
    después, y no con el historial de git, porque la tarea se ejecutó sin commits; la garantía no
    es verificable por un tercero a partir de un commit.
    \item \textbf{Atribución por capa en la Configuración~3b por categoría.} El registro de eventos
    de la librería no guarda un identificador de petición, por lo que los bloqueos de la 3b se
    atribuyeron a una de las dos capas por método y ruta, es decir, por categoría y no por payload.
    La atribución al WAF coincide, categoría por categoría, con lo medido por separado en la 3a,
    pero no es un cruce determinista.
    \item \textbf{La librería no se comporta igual sola que detrás del proxy.} Cuatro payloads de
    Command Injection (\texttt{cmdi\_112}, \texttt{cmdi\_134}, \texttt{cmdi\_31} y
    \texttt{cmdi\_38}) los bloquea la Configuración~3b y no los bloquean ni la 2 ni la 3a. Se
    comprobó que el cuerpo y el objetivo de la petición llegan idénticos por ambas rutas y que el
    proxy agrega cuatro cabeceras \texttt{X-*} y quita el puerto de \texttt{Host}; no se midió el
    efecto de esas cabeceras en el veredicto de la librería, de modo que la Configuración~2 y la
    librería dentro de la 3b no son la misma medición.
    \item \textbf{Causa del salto de Command Injection en la Configuración~3a.} Con el ejecutor
    anterior sobre la pila actual el WAF solo bloqueó 136 de 200 (68.0~\%), con 52 de 105 payloads
    de separadores ya codificados (49.5~\%); con el ejecutor corregido, 164 de 200 (82.0~\%) y 80 de
    105 (76.2~\%). La diferencia se atribuye a la recodificación de separadores ya codificados, y
    con el ejecutor corregido el WAF sigue bloqueando menos los codificados (76.2~\%) que los
    no codificados (88.4~\%, 84 de 95).
    \item \textbf{Repeticiones de un proceso determinista.} Las tres corridas por configuración
    (9{,}600 envíos de payload en total) no cambiaron el veredicto de ningún payload; confirman que
    el procedimiento es determinista y no estiman la variabilidad entre corpus ni entre
    construcciones del contenedor. La incertidumbre de muestreo la expresan los intervalos de
    Wilson.
    \item \textbf{Etiqueta flotante de la imagen del WAF.} \texttt{docker-compose.yml} referencia la
    imagen \texttt{owasp/modsecurity-crs:nginx-alpine} sin digest; el digest medido
    (\texttt{sha256:f12da37e...}) quedó registrado, pero la etiqueta resuelve hoy a un manifiesto
    distinto, de modo que repetir la medición sin fijar el digest puede cambiar el WAF.
    \item \textbf{La medición con el paquete 0.1.1 no es independiente.}
```

Fuente: XSS corpus posterior a la Ronda 5, sesgo del generador, freeze por manifiesto: docs/thesis-delta-xss.md §7; coincidencias: errata V4 y V6 (attack-sim/leakage_report_round5_all_20261025.json); 136 de 200: errata V3; atribución por capa: docs/thesis-delta-configs.md §3.3 y §7; proxy: errata V2 y Fase 2b (docs/evidence/phase2b-diff-20261025.json); cmdi 3a: errata V7b y Fase 2a; 9,600 envíos: errata V9; etiqueta flotante: errata V8.

### 19. J-7.12-xss: j-metodologia.tex, línea original 1091, línea actual 1197

Ubicación: Sec 7.12, restricción "Cobertura de XSS con n=1".

Antes:

```
\item \textbf{Cobertura de XSS con n=1.} ZAP confirmó una única vulnerabilidad de XSS en la
    aplicación de referencia (\texttt{POST /profile}, campo \texttt{bio}); la cobertura de esa
    categoría descansa en ese caso y no tiene el peso estadístico de las otras tres (n=200 cada
    una). Que ZAP reporte un solo caso refleja la aplicación evaluada, no un límite de la
    herramienta.
```

Después:

```
\item \textbf{Explotabilidad de XSS confirmada en un solo caso.} La cobertura de XSS se midió
    sobre un corpus propio de 200 payloads, 64 de ellos dirigidos al campo vulnerable
    (\texttt{bio}); la explotabilidad confirmada sigue descansando en un único caso (ZAP,
    \texttt{POST /profile}, campo \texttt{bio}), que no se amplió. Que ZAP reporte un solo caso
    refleja la aplicación evaluada, no un límite de la herramienta.
```

Fuente: docs/thesis-delta-xss.md §4 (Sección 7.12) y §5.

### 20. J-7.11-proxy-precision: j-metodologia.tex, línea original no aplica, línea actual 1142

Ubicación: Sec 7.11, precisión de la comprobación de la Fase 2b (correctiva).

Antes:

```
Se
    comprobó que el cuerpo y el objetivo de la petición llegan idénticos por ambas rutas y que el
    proxy agrega cuatro cabeceras \texttt{X-*} y quita el puerto de \texttt{Host}; no se midió el
```

Después:

```
Con
    un servidor de captura y cinco payloads se comprobó que el cuerpo y el objetivo de la petición
    llegan idénticos por ambas rutas y que el proxy agrega cuatro cabeceras \texttt{X-*} y quita el
    puerto de \texttt{Host}; no se midió el
```

Fuente: Precisión de la edición J-7.11-nuevas (errata Fase 2b: servidor de captura de cabeceras, cinco payloads).

### 21. K-intro-par: k-resultados.tex, línea original 44, línea actual 44

Ubicación: Cap. 8, introducción (pares de modelos).

Antes:

```
las métricas sobre el conjunto de prueba y la evaluación en OWASP
Juice Shop corresponden al par~C, que es el contenido del paquete 0.1.1;
```

Después:

```
las métricas sobre el conjunto de prueba, la evaluación en OWASP
Juice Shop y las Configuraciones 2 y 3b de la medición unificada del 25 de octubre de 2026
corresponden al par~C, que es el contenido del paquete 0.1.1;
```

Fuente: docs/thesis-delta-configs.md §2.

### 22. K-smart-oe3: k-resultados.tex, línea original 591, línea actual 595

Ubicación: Cuadro SMART del OE3, fila Medible.

Antes:

```
cobertura entre 92.5~\% y 100~\% en 3 categorías con el paquete 0.1.1 (85.0~\% en Path Traversal con la 0.1.0)
```

Después:

```
cobertura entre 92.5~\% y 100~\% en las 4 categorías con el paquete 0.1.1 (85.0~\% en Path Traversal con la 0.1.0)
```

Fuente: results_combined_config2_run1_20261025.json (XSS 200/200).

### 23. K-c28-fila: k-resultados.tex, línea original 420, línea actual 421

Ubicación: Cuadro 28, fila XSS.

Antes:

```
Payloads clásicos (ZAP no automatizado) \\ \hline
```

Después:

```
Generador propio (semilla 20261025) \\ \hline
```

Fuente: docs/thesis-delta-xss.md §4 (Cuadro 28).

### 24. K-c28-nota: k-resultados.tex, línea original 428, línea actual 429

Ubicación: Cuadro 28, nota (semilla y fecha distintas).

Antes:

```
La asignación de CAPEC-242 a \texttt{xss} es
una decisión de mapeo del dataset, no una equivalencia conceptual.}
```

Después:

```
La asignación de CAPEC-242 a \texttt{xss} es
una decisión de mapeo del dataset, no una equivalencia conceptual. El corpus de XSS lo genera
\texttt{generate\_xss.py} (400 candidatos, muestreo estratificado a 200, filtro de exclusión y
auditoría de fuga) con la semilla 20261025 el 25 de octubre de 2026; la semilla y la fecha difieren
de las de las otras tres categorías (20260923).}
```

Fuente: docs/thesis-delta-xss.md §2 y §4 (Cuadro 28); semilla 20260923 ya existente en el texto.

### 25. K-8.4.2-601: k-resultados.tex, línea original 713, línea actual 717

Ubicación: Sec 8.4.2, composición del corpus.

Antes:

```
El corpus contiene 601
peticiones: 200 por cada una de las categorías SQLi, Path Traversal y Command Injection, y un
payload de XSS confirmado con OWASP ZAP. El filtro de exclusión descartó
```

Después:

```
El corpus de la
Ronda~5 original contenía 601 peticiones: 200 por cada una de las categorías SQLi, Path Traversal y
Command Injection, y un payload de XSS confirmado con OWASP ZAP. El 25 de octubre de 2026 se agregó
un corpus propio de 200 payloads de XSS, con lo que el corpus de cobertura tiene 800 peticiones.
El filtro de exclusión descartó
```

Fuente: errata V7; docs/thesis-delta-xss.md §1.

### 26. K-8.4.2-xss: k-resultados.tex, línea original 736, línea actual 742

Ubicación: Sec 8.4.2, cierre del párrafo de ZAP y resultado de XSS n=200 y n=64.

Antes:

```
Ese payload fue bloqueado por ambos pares de modelos (1 de 1), de modo que la
cobertura de XSS tiene n=1 y no es comparable en peso estadístico con las otras tres categorías.
```

Después:

```
Ese payload fue bloqueado por ambos pares de modelos (1 de 1), y el 25 de octubre de 2026 se
reconfirmó que es explotable sin protección (HTTP 200) y que la librería lo bloquea (HTTP 403). Los
dos resultados responden preguntas distintas: ZAP (n=1) mide la explotabilidad confirmada, y el
corpus propio (n=200), la cobertura de detección.

La cobertura de XSS sobre el corpus propio, con el paquete 0.1.1 del registro de npm, fue de 200
de 200 payloads bloqueados (100.0~\%; intervalo de Wilson al 95~\%: 98.1--100.0~\%), sin variación
entre las tres corridas ni entre los tres transportes (64 de 64 en
\texttt{application/x-www-form-urlencoded}, 68 de 68 en JSON y 68 de 68 en
\texttt{multipart/form-data}); sin protección se bloquearon 0 de 200. De los 200 payloads, 64 se
dirigen al campo vulnerable \texttt{bio}, y los 64 se bloquearon (94.3--100.0~\%). Los otros 136 se
dirigen a \texttt{content} y \texttt{title}, campos sin vulnerabilidad confirmada: sin protección la
aplicación los rechaza con HTTP 400 porque la ruta exige ambos campos, y con la librería reciben
HTTP 403, de modo que miden la detección y no la explotabilidad. El filtro de exclusión de XSS se
aplicó después del muestreo y descartó 0 candidatos, y la auditoría posterior de fuga encontró 3
payloads con coincidencia normalizada por subcadena con el entrenamiento (Cuadro~\ref{tab:res-corpus});
sin ellos, la librería bloquea 197 de 197.
```

Fuente: errata V3 (docs/evidence/errata-v3-strata-20261025.json: Config 1 0/200 y 0/64; Config 2 200/200 y 64/64 con Wilson; HTTP 400 en los 136 de content y title; transportes 64/68/68); docs/thesis-delta-xss.md §3.6 (ZAP reconfirmado: 200 sin protección, 403 con la librería); errata V4 (197/197).

### 27. K-c36-fila: k-resultados.tex, línea original 814, línea actual 839

Ubicación: Cuadro 36, filas XSS.

Antes:

```
XSS & OWASP ZAP (\textit{Active Scan}, API REST) & 1 alerta confirmada & 0 & 1 \\ \hline
```

Después:

```
XSS (hallazgo de ZAP) & OWASP ZAP (\textit{Active Scan}, API REST) & 1 alerta confirmada & 0 & 1 \\ \hline
XSS (cobertura) & Generador propio (\texttt{generate\_xss.py}) & 400 & 0\textsuperscript{a} & 200 \\ \hline
```

Fuente: docs/thesis-delta-xss.md §4 (Cuadro 36) y §2 (400 candidatos, 200 finales).

### 28. K-c36-caption: k-resultados.tex, línea original 816, línea actual 842

Ubicación: Cuadro 36, título.

Antes:

```
Construcción del corpus limpio de evaluación (Ronda~5, semilla 20260923)}
```

Después:

```
Construcción del corpus limpio de evaluación (Ronda~5, semilla 20260923; XSS, semilla 20261025)}
```

Fuente: Semilla 20261025: docs/thesis-delta-xss.md §2.

### 29. K-c36-nota: k-resultados.tex, línea original 819, línea actual 845

Ubicación: Cuadro 36, nota (filtro posterior al muestreo, 0 descartes, 3 coincidencias).

Antes:

```
{\footnotesize Nota. Elaboración propia con datos de \texttt{docs/config3b-results.md} y
\texttt{attack-sim/exclusion\_report.json} (repositorio \texttt{logSguarDian-vulnerable-project}).}
```

Después:

```
{\footnotesize Nota. Elaboración propia con datos de \texttt{docs/config3b-results.md},
\texttt{attack-sim/exclusion\_report.json}, \texttt{attack-sim/exclusion\_report\_xss\_20261025.json}
y \texttt{attack-sim/leakage\_report\_xss\_20261025.json} (repositorio
\texttt{logSguarDian-vulnerable-project}). \textsuperscript{a}Los 200 payloads finales de XSS son
el resultado del muestreo estratificado de los 400 candidatos, no del filtro. El filtro de exclusión
se aplicó después del muestreo, en orden inverso al de las otras categorías, y descartó 0; la
auditoría posterior de fuga encontró 3 payloads (\texttt{xss\_118}, \texttt{xss\_254} y
\texttt{xss\_342}) con coincidencia normalizada por subcadena con las particiones de entrenamiento y
de prueba, que no se corrigieron.}
```

Fuente: errata V6 y V4; attack-sim/exclusion_report_xss_20261025.json y leakage_report_xss_20261025.json (train 3, val 0, test 3).

### 30. K-c37-fila: k-resultados.tex, línea original 831, línea actual 864

Ubicación: Cuadro 37, filas XSS.

Antes:

```
XSS & 110/113 (97.3~\%) & 1/1 (n=1) & 1/1 (n=1) & 1/1 (n=1) & Cumple, con n=1 \\ \hline
```

Después:

```
XSS (corpus propio, n=200) & 110/113 (97.3~\%) & No medido\textsuperscript{c} & No medido\textsuperscript{c} & 200/200 (100.0~\%)\textsuperscript{c} & Cumple \\ \hline
XSS (ZAP, n=1) & --- & 1/1 (n=1, corpus anterior, no comparable) & 1/1 (n=1, corpus anterior, no comparable) & 1/1 (n=1) & No aplica; explotabilidad confirmada en un caso \\ \hline
```

Fuente: docs/thesis-delta-xss.md §4 (Cuadro 37); results_combined_config2_run1_20261025.json; columnas 0.1.0 y tarball: no medidas con el corpus de XSS.

### 31. K-c37-nota: k-resultados.tex, línea original 843, línea actual 877

Ubicación: Cuadro 37, nota (nota c).

Antes:

```
Las columnas de la Ronda~5 con el ejecutor anterior no
son comparables con ella.}
```

Después:

```
Las columnas de la Ronda~5 con el ejecutor anterior no
son comparables con ella. \textsuperscript{c}La cobertura de XSS sobre el corpus propio se midió el
25 de octubre de 2026 con el paquete 0.1.1 del registro (archivo SHA-256 \texttt{abf8d5c4...}) y el
emisor \texttt{send\_xss\_corpus.py}, en la corrida 1 de tres idénticas
(\texttt{attack-sim/results\_combined\_config2\_run1\_20261025.json}); intervalo de Wilson al 95~\%:
98.1--100.0~\%. No se midió con el paquete 0.1.0 ni con el tarball de validación. El caso de ZAP se
midió con un corpus anterior de un solo payload y no es comparable con el de 200.}
```

Fuente: results_combined_config2_run1_20261025.json (SHA-256 577e6e00...); docs/thesis-delta-configs.md §2 (tarball abf8d5c4...).

### 32. K-8.4.3-parrafo: k-resultados.tex, línea original 877, línea actual ver archivo

Ubicación: Sec 8.4.3, párrafo 3a/3b/"68 ataques" reescrito.

Antes:

```
El Cuadro~\ref{tab:res-ronda5} repite la comparación con el corpus limpio de la Ronda~5, que no
tiene la fuga de la Ronda~4. Sus cifras de Path Traversal y de Command Injection se midieron con el
ejecutor anterior, que alteraba los payloads ya codificados y afecta a las cuatro configuraciones,
incluidas las del WAF; solo la Configuración~2 se repitió con el ejecutor corregido
(Cuadro~\ref{tab:res-cobertura}), de modo que esas dos filas deben leerse como provisionales. La Configuración~1 bloqueó 0 de 601 payloads, lo que confirma que el
corpus y el ejecutor miden lo que declaran. El WAF solo (3a) bloqueó el 99.5~\% de SQLi, una cifra equivalente a la de
\textit{logSguarDian} solo (2, 100~\%), y el 98.5~\% de Path Traversal, más que la librería
(85.0~\%), pero solo el 68.0~\% de Command Injection, frente al 91.5~\% de la librería. La combinación de ambas capas (3b)
bloqueó el 100~\% de SQLi y de Path Traversal y el 98.5~\% de Command Injection. De los 68 ataques
que el WAF solo no bloqueó (1 de SQLi, 3 de Path Traversal y 64 de Command Injection), la
Configuración~3b bloqueó 65 y la Configuración~2, 64. La Configuración~2 se midió con un tarball que contiene el par~A y de la 3b no consta el paquete
exacto; la 3a no incorpora la librería y se midió en una rama distinta de la aplicación. En XSS,
las tres configuraciones protegidas bloquearon el único payload, con n=1.
```

Después:

```
El Cuadro~\ref{tab:res-ronda5} repite la comparación con el corpus limpio de la Ronda~5, que no
tiene la fuga de la Ronda~4, ampliado con el corpus propio de XSS (800 peticiones). A diferencia de
la medición del 10 de octubre de 2026, que se descartó, las cuatro configuraciones se ejecutaron de
nuevo el 25 de octubre de 2026 sobre el mismo árbol de la aplicación, con el mismo
\texttt{Dockerfile} y el ejecutor corregido, y con el paquete 0.1.1 en las Configuraciones 2 y 3b
(Procedimiento~4.1). La Configuración~1 bloqueó 0 de 800 payloads, lo que confirma que el corpus y
el ejecutor miden lo que declaran. En total, la librería sola (2) bloqueó 784 de 800 payloads
(98.0~\%), el WAF solo (3a) 749 (93.6~\%) y ambas capas (3b) 797 (99.6~\%).

Por categoría, el WAF solo bloqueó el 99.5~\% de SQLi, igual que la librería, el 98.5~\% de Path
Traversal, el 82.0~\% de Command Injection (intervalo de Wilson al 95~\%: 76.1--86.7~\%) y el
94.5~\% de XSS. En Path Traversal no hay ventaja del WAF: con el paquete 0.1.1 la librería bloqueó
200 de 200 y el WAF 197 de 200, una diferencia de tres payloads con intervalos de Wilson que se
solapan (98.1--100.0~\% y 95.7--99.5~\%). En Command Injection la librería bloqueó el 92.5~\%, el
WAF el 82.0~\% y la combinación el 98.5~\%. El 68.0~\% que se reportó para el WAF en la medición del
10 de octubre se reprodujo al volver a ejecutar el ejecutor anterior sobre este mismo árbol (136 de
200, con el mismo veredicto en los 600 payloads de esa medición), de modo que la diferencia con el
82.0~\% se debe al ejecutor, que volvía a codificar los separadores ya codificados, y no a la
aplicación. Aun con el ejecutor corregido, el WAF bloquea menos los 105 payloads de Command
Injection con separadores ya codificados (80 de 105, 76.2~\%) que los 95 sin codificar (84 de 95,
88.4~\%) (Cuadro~\ref{tab:anx-cmdi-codificacion}). En XSS, los 11 payloads que el WAF no bloqueó
usan doble codificación URL y se envían como JSON o \texttt{multipart/form-data}; la librería sola
los bloqueó todos.

De los 51 ataques que el WAF solo no bloqueó (1 de SQLi, 3 de Path Traversal, 36 de Command
Injection y 11 de XSS), la Configuración~3b bloqueó 48 y la Configuración~2, 44. Sobre el mismo
denominador de la medición anterior (sin XSS) son 40 ataques no bloqueados por el WAF, de los que la
3b bloqueó 37 y la 2, 33, frente a 68, 65 y 64 antes; esa reducción corresponde al cambio de
ejecutor. Frente a la librería sola, la combinación bloqueó 13 payloads más (1 de SQLi y 12 de
Command Injection), y frente al WAF solo, 48 más. La complementariedad es asimétrica: en Path
Traversal y en XSS la librería sola bloquea todo lo que bloquea la combinación y el WAF no agrega
nada, mientras que en SQLi y en Command Injection cada capa bloquea payloads que la otra no. Tres
payloads de Command Injection (\texttt{cmdi\_6}, \texttt{cmdi\_184} y \texttt{cmdi\_185}) no los
bloquea ninguna configuración. Cuatro payloads de la misma categoría (\texttt{cmdi\_112},
\texttt{cmdi\_134}, \texttt{cmdi\_31} y \texttt{cmdi\_38}) los bloquea la 3b y no los bloquean ni la
3a ni la Configuración~2: con un servidor de captura se comprobó que el cuerpo y el objetivo de la
petición llegan idénticos por ambas rutas y que el proxy agrega cuatro cabeceras \texttt{X-*}, pero
no se midió el efecto de esas cabeceras en el veredicto de la librería, de modo que la
Configuración~2 y la librería dentro de la 3b no deben tratarse como la misma medición
(Sección~\ref{sec:met-validez}).
```

Fuente: errata V1 (conjuntos), V2 (4 payloads solo de la 3b), V3 (11 de XSS en 3a), V5 (51/48/44; 40/37/33 frente a 68/65/64; agregados 784/749/797; +13 y +48), V7b (76.2 % y 88.4 %), Fase 2a (136/200 reproducido), Fase 2b (cabeceras); Wilson calculados con z=1.959963984540054.

### 33. K-c38-tabla: k-resultados.tex, línea original 894, línea actual 960

Ubicación: Cuadro 38, tabla reconstruida.

Antes:

```
\begin{tabular}{|L{2.7cm}|L{2.0cm}|L{2.5cm}|L{2.5cm}|L{2.5cm}|}
\hline
\textbf{Categoría} & \textbf{Config.~1 (sin protección)} & \textbf{Config.~2 (solo \textit{logSguarDian})} & \textbf{Config.~3a (solo WAF)} & \textbf{Config.~3b (ambas capas)} \\ \hline
SQLi & 0/200 (0.0~\%) & 200/200 (100.0~\%) & 199/200 (99.5~\%) & 200/200 (100.0~\%) \\ \hline
Path Traversal & 0/200 (0.0~\%) & 170/200 (85.0~\%) & 197/200 (98.5~\%) & 200/200 (100.0~\%) \\ \hline
Command Injection & 0/200 (0.0~\%) & 183/200 (91.5~\%) & 136/200 (68.0~\%) & 197/200 (98.5~\%) \\ \hline
XSS (n=1) & 0/1 & 1/1 & 1/1 & 1/1 \\ \hline
\end{tabular}
\caption[Cuatro configuraciones sobre el corpus limpio de la Ronda 5]{Payloads bloqueados por configuración sobre el corpus limpio de la Ronda~5 (601 peticiones)}
```

Después:

```
\begin{tabular}{|L{2.7cm}|L{2.0cm}|L{2.6cm}|L{2.6cm}|L{2.6cm}|}
\hline
\textbf{Categoría} & \textbf{Config.~1 (sin protección)} & \textbf{Config.~2 (solo \textit{logSguarDian}, 0.1.1)} & \textbf{Config.~3a (solo WAF)} & \textbf{Config.~3b (ambas capas, 0.1.1)} \\ \hline
SQLi & 0/200 (0.0~\%) & 199/200 (99.5~\%) & 199/200 (99.5~\%) & 200/200 (100.0~\%) \\ \hline
Path Traversal & 0/200 (0.0~\%) & 200/200 (100.0~\%) & 197/200 (98.5~\%) & 200/200 (100.0~\%) \\ \hline
Command Injection & 0/200 (0.0~\%) & 185/200 (92.5~\%) & 164/200 (82.0~\%) & 197/200 (98.5~\%) \\ \hline
XSS & 0/200 (0.0~\%) & 200/200 (100.0~\%) & 189/200 (94.5~\%) & 200/200 (100.0~\%) \\ \hline
\textbf{Total} & 0/800 (0.0~\%) & 784/800 (98.0~\%) & 749/800 (93.6~\%) & 797/800 (99.6~\%) \\ \hline
\end{tabular}
\caption[Cuatro configuraciones sobre el corpus limpio de la Ronda 5 con XSS]{Payloads bloqueados por configuración sobre el corpus limpio de la Ronda~5 ampliado con XSS (800 peticiones)}
```

Fuente: results_combined_config{1,2,3a,3b}_run1_20261025.json; docs/thesis-delta-configs.md §3.1 (tabla global); totales por suma de categorías (784, 749, 797, 0) y Wilson calculados aparte.

### 34. K-c38-nota: k-resultados.tex, línea original 905, línea actual 972

Ubicación: Cuadro 38, nota reemplazada (paquete de 3b, ejecutor, medición unificada).

Antes:

```
{\footnotesize Nota. Elaboración propia con datos de
\texttt{attack-sim/results\_config\{1,2-published-with-real-xss,3a,3b\}-round5-20261010.json}
(repositorio \texttt{logSguarDian-vulnerable-project}); conteos recalculados a partir de los
archivos de resultados. Configuración~2: tarball con el par~A (ver Sección~\ref{subsec:met-f2}); de la Configuración~3b no consta el paquete exacto (los resultados no lo registran), y se atribuye al par~A. Medido con el ejecutor
anterior a la corrección; las Configuraciones 3a y 3b no se repitieron con el ejecutor corregido.}
```

Después:

```
{\footnotesize Nota. Elaboración propia con datos de
\texttt{attack-sim/results\_combined\_config\{1,2,3a,3b\}\_run1\_20261025.json} (repositorio
\texttt{logSguarDian-vulnerable-project}); conteos recalculados a partir de los archivos de
resultados. Medición del 25 de octubre de 2026, corrida 1 de tres idénticas, con el mismo árbol de
la aplicación y el mismo \texttt{Dockerfile} en las cuatro configuraciones, el ejecutor corregido y
el corpus combinado de 800 peticiones (SHA-256 \texttt{f1fb0b0a...}). Configuraciones 2 y 3b con el
paquete 0.1.1 del registro de npm (archivo SHA-256 \texttt{abf8d5c4...}; modelos \texttt{25b407e6...}
y \texttt{5be28ee8...}, par~C; ver Sección~\ref{subsec:met-f2}). Intervalos de Wilson al 95~\% en
SQLi, Path Traversal, Command Injection y XSS: Configuración~2, 97.2--99.9, 98.1--100.0,
88.0--95.4 y 98.1--100.0~\%; Configuración~3a, 97.2--99.9, 95.7--99.5, 76.1--86.7 y 90.4--96.9~\%;
Configuración~3b, 98.1--100.0, 98.1--100.0, 95.7--99.5 y 98.1--100.0~\%. Las mediciones anteriores
de la Configuración~2 con el paquete 0.1.0 (Cuadro~\ref{tab:res-cobertura}) no se incluyen ni se
comparan con la Configuración~3a.}
```

Fuente: Archivos results_combined_*; corpus combinado SHA-256 f1fb0b0a...; docs/thesis-delta-configs.md §2; Wilson por categoría de docs/thesis-delta-configs.md §3.1 y calculados con z=1.959963984540054.

### 35. K-c40-xss: k-resultados.tex, línea original 968, línea actual 1043

Ubicación: Cuadro 40 (resumen de indicadores), filas XSS.

Antes:

```
Cobertura XSS & OE3 & $\geq$80~\% & 1/1 (n=1, ZAP) & Cumple, con n=1 \\ \hline
```

Después:

```
Cobertura XSS (corpus propio, paquete 0.1.1) & OE3 & $\geq$80~\% & 200/200 (100.0~\%; IC 95~\%: 98.1--100.0~\%); 64/64 en \texttt{bio} (IC 95~\%: 94.3--100.0~\%) & Cumple en cobertura (n=200) \\ \hline
Explotabilidad de XSS confirmada (ZAP) & OE3 & Descriptivo & 1 caso (\texttt{POST /profile}, \texttt{bio}; n=1) & --- \\ \hline
```

Fuente: errata V3; docs/thesis-delta-xss.md §3.1.

### 36. K-c40-dp: k-resultados.tex, línea original 977, línea actual 1053

Ubicación: Cuadro 40 (resumen de indicadores), fila de defensa en profundidad.

Antes:

```
Contribución en defensa en profundidad (Ronda~5, ejecutor anterior) & OG & Descriptivo & 65 de 68 ataques no bloqueados por el WAF (provisional) & --- \\ \hline
```

Después:

```
Contribución en defensa en profundidad (Ronda~5, 25 de octubre de 2026) & OG & Descriptivo & La 3b bloqueó 48 de los 51 ataques no bloqueados por el WAF; la Configuración~2, 44 de 51 & --- \\ \hline
```

Fuente: errata V5 (51, 48, 44).

### 37. K-8.4.2-corrida: k-resultados.tex, línea original 727, línea actual 733

Ubicación: Sec 8.4.2, corridas por medición.

Antes:

```
Cada medición corresponde a una sola corrida.
```

Después:

```
Cada medición corresponde a una sola corrida, salvo la de XSS, que se midió en tres corridas idénticas.
```

Fuente: docs/thesis-delta-xss.md §3.4 (tres corridas idénticas).

### 38. K-8.4.2-ejecutor: k-resultados.tex, línea original 787, línea actual 808

Ubicación: Sec 8.4.2, alcance de la corrección del ejecutor.

Antes:

```
La corrección del ejecutor afecta también a las demás mediciones de Path Traversal y Command
Injection de este capítulo con el ejecutor anterior, que no se repitieron.
```

Después:

```
La corrección del ejecutor afecta también a las demás mediciones de Path Traversal y Command
Injection de este capítulo con el ejecutor anterior (paquete 0.1.0 y tarball de validación), que no
se repitieron; las cuatro configuraciones se midieron de nuevo con el ejecutor corregido el 25 de
octubre de 2026 (Cuadro~\ref{tab:res-ronda5}).
```

Fuente: docs/thesis-delta-configs.md §1 (cuatro configuraciones remedidas con el ejecutor corregido).

### 39. K-8.4.2-subcadena: k-resultados.tex, línea original 798, línea actual 821

Ubicación: Sec 8.4.2, auditoría de subcadena en las cuatro categorías.

Antes:

```
Path
Traversal alcanza 7 coincidencias y Command Injection 2. La cobertura de SQLi reportada incluye,
```

Después:

```
Path
Traversal alcanza 7 coincidencias y Command Injection 2. La auditoría de subcadena repetida el 25 de
octubre de 2026 sobre los cuatro corpus da 4 coincidencias en SQLi, 7 en Path Traversal, 2 en
Command Injection y 3 en XSS, de 200 payloads cada uno. La cobertura de SQLi reportada incluye,
```

Fuente: errata V6 (attack-sim/leakage_report_round5_all_20261025.json: sqli 4, pt 7, cmdi 2, xss 3 por subcadena normalizada).

### 40. D-libreria: l-discusion.tex, línea original 66, línea actual 66

Ubicación: Cap. 9, Librería y pipeline (0.1.1 en 2 y 3b).

Antes:

```
Con la 0.1.1 solo se midió la cobertura de la Configuración~2 de la Ronda~5; las aplicaciones de
terceros y el rendimiento no se midieron con ella,
```

Después:

```
Con la 0.1.1 se midió la cobertura de las Configuraciones 2 y 3b de la Ronda~5; las aplicaciones de
terceros y el rendimiento no se midieron con ella,
```

Fuente: docs/thesis-delta-configs.md §2.

### 41. D-variantes: l-discusion.tex, línea original 94, línea actual 94

Ubicación: Cap. 9, Variantes desconocidas (XSS n=200).

Antes:

```
Con esas salvedades, el sistema reconoce variantes no vistas
de los vectores cubiertos en una proporción superior al criterio de cobertura del 80~\%.
```

Después:

```
El corpus propio de 200 payloads de XSS, medido con el paquete 0.1.1, se bloqueó en su
totalidad (200 de 200; intervalo de Wilson al 95~\%: 98.1--100.0~\%); se construyó después de
conocer los resultados de la Ronda~5, y 3 de sus payloads coinciden con el entrenamiento por
subcadena normalizada, de modo que no es una evaluación ciega. Con esas salvedades, el sistema
reconoce variantes no vistas de los vectores cubiertos en una proporción superior al criterio de
cobertura del 80~\%.
```

Fuente: errata V3 y V6.

### 42. D-oe3-xss: l-discusion.tex, línea original 196, línea actual 200

Ubicación: Cap. 9, OE3, párrafo de XSS (n=1 a n=200).

Antes:

```
En XSS,
la detección se sustenta en el F1 de 0.9877 sobre el conjunto de prueba, en el 98~\% de la suite
extremo a extremo, en el 97.3~\% de la Ronda~4 y en el único caso que ZAP confirmó sobre la
aplicación de referencia (\texttt{POST /profile}, bloqueado por todos los paquetes evaluados), un
resultado real pero con n=1 que no tiene el peso estadístico de las otras tres categorías. El OE3
se cumple, sin reservas en las métricas de clasificación y con dos reservas en la cobertura: el
n=1 de XSS y que la medición vigente de Path Traversal y de Command Injection no es independiente
del corpus que motivó las correcciones.
```

Después:

```
En XSS,
la detección se sustenta en el F1 de 0.9877 sobre el conjunto de prueba, en el 98~\% de la suite
extremo a extremo, en el 97.3~\% de la Ronda~4 y, desde el 25 de octubre de 2026, en la cobertura
del corpus propio de 200 payloads: 200 de 200 (intervalo de Wilson al 95~\%: 98.1--100.0~\%) y 64
de 64 en el campo vulnerable \texttt{bio} (94.3--100.0~\%). El criterio de cobertura del 80~\% se
cumple para XSS con evidencia estadística. Esa cobertura tiene límites declarados: el corpus se
construyó después de conocer los resultados de la Ronda~5, 136 de sus 200 payloads apuntan a
campos sin vulnerabilidad confirmada y 3 coinciden con el entrenamiento por subcadena normalizada.
La explotabilidad confirmada sigue descansando en el único caso que ZAP confirmó sobre la
aplicación de referencia (\texttt{POST /profile}, bloqueado por todos los paquetes evaluados), con
n=1. El OE3 se cumple, sin reservas en las métricas de clasificación y con reservas en la
cobertura: que la medición vigente de Path Traversal y de Command Injection no es independiente
del corpus que motivó las correcciones, y que la de XSS se hizo sobre un corpus construido después
de conocer los resultados de la Ronda~5.
```

Fuente: errata V3, V4, V6; docs/thesis-delta-xss.md §3.1 y §5.

### 43. D-defensa: l-discusion.tex, línea original 220, línea actual ver archivo

Ubicación: Cap. 9, Defensa en profundidad, párrafo de la Ronda 5 reescrito.

Antes:

```
La comparación sobre el corpus limpio de la Ronda~5, que no tiene la fuga de la Ronda~4, apunta
en la misma dirección, con una reserva importante: sus cifras de Path Traversal y de Command
Injection se midieron con el ejecutor anterior, que alteraba los payloads ya codificados y afecta
también al WAF, y no se repitieron con el ejecutor corregido, de modo que esas dos categorías son
provisionales. Con esa reserva, el WAF solo y la librería sola tienen perfiles distintos: en SQL Injection son
prácticamente equivalentes (99.5~\% y 100~\%, una diferencia de un payload); en Path Traversal el
WAF bloquea más (98.5~\% frente a 85.0~\%); y en Command Injection la librería bloquea más
(91.5~\% frente a 68.0~\%), la categoría en la que las firmas del WAF son más débiles.
Las dos capas combinadas bloquean el 100~\% de SQL Injection y de Path Traversal y el 98.5~\% de
Command Injection, más que cualquiera por separado en esa última, y de los 68 ataques que el WAF
no bloqueó, la combinación bloqueó 65. Esto indica que las capas detectan cosas distintas y que
una no subsume a la otra, con la salvedad de que la ventaja del WAF en Path Traversal queda
descartada para la librería con el paquete 0.1.1 (200 de 200), y de que la desventaja del WAF en
Command Injection (68.0~\%) debe confirmarse repitiendo las configuraciones con el ejecutor
corregido, porque la alteración de los separadores codificados pudo afectarla. Las Rondas 1 a 3 aportaron
```

Después:

```
La comparación sobre el corpus limpio de la Ronda~5, que no tiene la fuga de la Ronda~4, se repitió
el 25 de octubre de 2026 con las cuatro configuraciones sobre el mismo árbol de la aplicación, con
el ejecutor corregido y con 800 payloads, 200 de ellos de XSS. El WAF solo y la librería sola tienen
perfiles distintos. En SQL Injection son equivalentes (99.5~\% ambos, 199 de 200). En Path
Traversal no hay ventaja del WAF: con el paquete 0.1.1 la librería bloqueó 200 de 200 y el WAF
197 de 200, una diferencia de tres payloads con intervalos de Wilson solapados. En Command
Injection la librería bloquea más (92.5~\% frente a 82.0~\%); la cifra del WAF, con intervalo de
Wilson al 95~\% de 76.1 a 86.7~\%, no permite afirmar que supere el 80~\%. El 68.0~\% que se había
reportado para el WAF era un efecto del ejecutor anterior: al volver a ejecutarlo sobre el mismo
árbol reprodujo 136 de 200, y el ejecutor corregido dio 164. Aun así, el WAF bloquea menos los
payloads de Command Injection con separadores ya codificados (76.2~\%) que los no codificados
(88.4~\%), una diferencia que se mantiene con el ejecutor corregido y que no se debe a la
medición. En XSS, el WAF bloqueó 189 de 200 (94.5~\%) y falló en 11 payloads con doble
codificación URL enviados como JSON o \texttt{multipart/form-data}; la librería bloqueó los 200.

En conjunto, la librería sola bloqueó 784 de 800 payloads, el WAF solo 749 y la combinación 797: la
combinación agrega 13 payloads a la librería (1 de SQL Injection y 12 de Command Injection) y 48
al WAF. De los 51 ataques que el WAF no bloqueó, la combinación bloqueó 48 y la librería sola 44. La
complementariedad es asimétrica: en Path Traversal y en XSS la librería sola bloquea todo lo que
bloquea la combinación, y solo en SQL Injection y en Command Injection cada capa detiene payloads
que la otra deja pasar. Por eso no puede afirmarse que la combinación supere a ambas capas en todas
las categorías, ni que ninguna subsuma a la otra. Cuatro payloads de Command Injection los bloquea
la combinación y no los bloquean ni la librería sola ni el WAF solo; no se midió por qué la librería
se comporta distinto detrás del proxy, de modo que la Configuración~2 y la librería dentro de la 3b
no son la misma medición. Tres payloads de Command Injection (\texttt{cmdi\_6}, \texttt{cmdi\_184}
y \texttt{cmdi\_185}) no los bloquea ninguna configuración, y su causa no se investigó. Las Rondas 1 a 3 aportaron
```

Fuente: errata V1, V2, V3, V5, V7b y Fase 2a; no se usó la afirmación de ventaja del WAF en Path Traversal ni las de 3b supera a ambas e ninguna subsume a la otra (errata E-05 y E-06).

### 44. D-c41-oe3: l-discusion.tex, línea original 324, línea actual 345

Ubicación: Cuadro 41 (cumplimiento), fila OE3.

Antes:

```
cobertura sobre payloads no vistos de 92.5 a 100~\% con el paquete vigente 0.1.1 y el ejecutor corregido (Path Traversal 200/200, intervalo 98.1--100.0~\%). Reservas: XSS con n=1, y que esa medición se hizo sobre el corpus que reveló los defectos de medición. \\ \hline
```

Después:

```
cobertura sobre payloads no vistos de 92.5 a 100~\% en las cuatro categorías con el paquete vigente 0.1.1 y el ejecutor corregido (Path Traversal 200/200, intervalo 98.1--100.0~\%; XSS 200/200, 98.1--100.0~\%). XSS: cumplido en cobertura (n=200); la explotabilidad confirmada sigue siendo n=1. Reservas: la medición de Path Traversal y de Command Injection se hizo sobre el corpus que reveló los defectos de medición, y la de XSS sobre un corpus construido después de conocer los resultados de la Ronda~5. \\ \hline
```

Fuente: errata V3; docs/thesis-delta-xss.md §4 (Cuadros 40 y 41).

### 45. D-limitaciones: l-discusion.tex, línea original 376, línea actual 397

Ubicación: Cap. 9, Limitaciones.

Antes:

```
La cobertura de
Path Traversal y de Command Injection con el paquete 0.1.1 se midió sobre el corpus que reveló los
defectos y solo para la Configuración~2; las mediciones con el ejecutor anterior, entre ellas la
comparación con el WAF, no se repitieron; la de XSS descansa en un único caso confirmado, y quedó
pendiente la validación con una startup en producción.
```

Después:

```
La cobertura de
Path Traversal y de Command Injection con el paquete 0.1.1 se midió sobre el corpus que reveló los
defectos; las mediciones del paquete 0.1.0 y del tarball de validación se hicieron con el ejecutor
anterior y no se repitieron; la cobertura de XSS se midió sobre un corpus construido después de
conocer los resultados de la Ronda~5 y la explotabilidad confirmada descansa en un único caso; y
quedó pendiente la validación con una startup en producción.
```

Fuente: Ídem J-7.11-nuevas.

### 46. C-cobertura: m-conclusiones.tex, línea original 64, línea actual 64

Ubicación: Conclusión conc:cobertura, reservas y XSS.

Antes:

```
Las reservas son dos: la
    cobertura de XSS descansa en un único caso confirmado con OWASP ZAP (1 de 1 en las
    Configuraciones 2, 3a y 3b, n=1), que no permite afirmar el criterio del 80~\% para esa
    categoría y que carece de un corpus limpio; y la medición con el paquete 0.1.1 se hizo solo en
    la Configuración~2 y sobre el corpus que reveló los defectos, por lo que no es independiente.
```

Después:

```
Sobre un corpus propio de 200
    payloads de XSS, el paquete 0.1.1 bloqueó 200 de 200 (intervalo de Wilson al 95~\% de 98.1 a
    100.0~\%; 64 de 64 en el campo vulnerable), de modo que el criterio del 80~\% se cumple para
    XSS en cobertura. Las reservas son dos: la medición con el paquete 0.1.1 de Path Traversal y de
    Command Injection se hizo sobre el corpus que reveló los defectos, por lo que no es
    independiente; y el corpus de XSS se construyó después de conocer los resultados de la Ronda~5,
    136 de sus 200 payloads apuntan a campos sin vulnerabilidad confirmada, y la explotabilidad
    confirmada sigue descansando en un único caso de OWASP ZAP (n=1).
```

Fuente: errata V3; docs/thesis-delta-xss.md §4.

### 47. C-waf: m-conclusiones.tex, línea original 98, línea actual 101

Ubicación: Conclusión conc:waf, cifras de la Ronda 5.

Antes:

```
En la Ronda~5, sobre un corpus sin esa fuga,
    el WAF solo bloqueó el 68.0~\% de Command Injection frente al 91.5~\% de la librería, y ambas
    capas el 98.5~\%. Las cifras de Path Traversal y de Command Injection de la Ronda~5 se midieron
    con el ejecutor anterior a la corrección, que alteraba los payloads ya codificados y afecta
    también al WAF, y no se repitieron con el ejecutor corregido; son provisionales. La evidencia
    respalda el uso de la librería como capa complementaria a un WAF y no como su sustituto.
```

Después:

```
En la Ronda~5, sobre un corpus sin esa fuga y ampliado
    con 200 payloads de XSS, medido el 25 de octubre de 2026 con las cuatro configuraciones sobre
    el mismo árbol de la aplicación y el ejecutor corregido, la librería sola bloqueó 784 de 800
    payloads, el WAF solo 749 y ambas capas 797. El WAF bloqueó el 82.0~\% de Command Injection
    (intervalo de Wilson al 95~\%: 76.1--86.7~\%) frente al 92.5~\% de la librería, y el 68.0~\%
    reportado antes se debió al ejecutor anterior y no a la aplicación. De los 51 ataques que el WAF
    no bloqueó, ambas capas bloquearon 48 y la librería sola 44. La complementariedad es asimétrica:
    la combinación agrega 13 payloads a la librería y 48 al WAF, en Path Traversal y en XSS la
    librería sola iguala a la combinación, y solo en SQL Injection y en Command Injection cada capa
    bloquea payloads que la otra no. La evidencia respalda el uso de la librería como capa
    complementaria a un WAF y no como su sustituto.
```

Fuente: errata V1, V2, V5, V7b y Fase 2a.

### 48. R-waf: n-recomendaciones.tex, línea original 36, línea actual 36

Ubicación: Recomendación 2 (capa complementaria detrás de un WAF).

Antes:

```
bloqueó 37 de los 40 ataques que ModSecurity con OWASP CRS dejó pasar en la Ronda~4, y en
    Command Injection el WAF solo bloqueó el 68.0~\% frente al 91.5~\% de la librería en la
    Ronda~5, una comparación provisional (Conclusión~\ref{conc:waf}). \textit{Resultado esperado:}
    mayor cobertura que la de cada capa por separado.
```

Después:

```
bloqueó 37 de los 40 ataques que ModSecurity con OWASP CRS dejó pasar en la Ronda~4, y en la
    Ronda~5 la combinación bloqueó 48 de los 51 ataques que el WAF solo no bloqueó, frente a 44 de la
    librería sola; en Command Injection el WAF solo bloqueó el 82.0~\% frente al 92.5~\% de la
    librería (Conclusión~\ref{conc:waf}). \textit{Resultado esperado:} mayor cobertura agregada que la
    de cada capa por separado (797 de 800 payloads frente a 784 y 749).
```

Fuente: errata V5; resultados de los archivos results_combined_*.

### 49. R-repetir-accion: n-recomendaciones.tex, línea original 118, línea actual 119

Ubicación: Recomendación 11, acción (3a y 3b ya remedidas).

Antes:

```
Acción:} con el paquete 0.1.1 del registro y el ejecutor corregido, repetir las cuatro
    configuraciones de la Ronda~5 (incluidas la 3a y la 3b), la cobertura con el paquete 0.1.0,
    las aplicaciones de terceros y el benchmark de rendimiento; repetir también la cobertura con
    un corpus nuevo, generado con otra semilla y el mismo filtro de exclusión.
```

Después:

```
Acción:} con el paquete 0.1.1 del registro y el ejecutor corregido, repetir la cobertura con
    el paquete 0.1.0, las aplicaciones de terceros y el benchmark de rendimiento; repetir también
    las cuatro configuraciones de la Ronda~5 con un corpus nuevo, generado con otra semilla y el
    mismo filtro de exclusión, y fijar el digest de la imagen del WAF.
```

Fuente: docs/thesis-delta-configs.md §1 (3a y 3b ya remedidas); errata V8 (digest).

### 50. R-repetir-just: n-recomendaciones.tex, línea original 124, línea actual 125

Ubicación: Recomendación 11, justificación y resultado esperado.

Antes:

```
\textit{Justificación:} con la 0.1.1 solo se midió la Configuración~2, sobre el
    corpus que reveló los defectos, y de las Configuraciones 1, 3a y 3b no consta el paquete
    (Conclusión~\ref{conc:cobertura}). \textit{Resultado esperado:} cifras independientes y atadas
    al archivo exacto evaluado, que confirmen o corrijan el 100.0~\% en Path Traversal y el
    92.5~\% en Command Injection, y una comparación con el WAF definitiva.
```

Después:

```
\textit{Justificación:} las cuatro configuraciones se midieron con la 0.1.1 sobre el corpus
    que reveló los defectos (en Path Traversal y Command Injection) y sobre un corpus de XSS
    construido después de conocer los resultados de la Ronda~5, y las aplicaciones de terceros y
    el benchmark no se midieron con ella (Conclusión~\ref{conc:cobertura}). \textit{Resultado
    esperado:} cifras independientes y atadas al archivo exacto evaluado, que confirmen o corrijan
    el 100.0~\% en Path Traversal, el 92.5~\% en Command Injection y el 100.0~\% en XSS, y una
    comparación con el WAF sobre un corpus independiente.
```

Fuente: docs/thesis-delta-configs.md §2; docs/thesis-delta-xss.md §7.

### 51. R-xss-cmdi: n-recomendaciones.tex, línea original 130, línea actual 133

Ubicación: Recomendaciones 12 y 13 (XSS más allá de un caso; payloads cmdi no bloqueados).

Antes:

```
\item \textbf{Construir un corpus limpio de XSS.} \textit{Acción:} generar payloads de XSS
    con OWASP ZAP u otras herramientas sobre más endpoints o aplicaciones, filtrarlos contra el
    entrenamiento, definir para cada payload su forma exacta en el cable para que el ejecutor no la
    altere, y repetir la comparación con el WAF sobre ambos corpus. \textit{Justificación:} la
    cobertura de XSS descansa en un único payload confirmado por ZAP (1 de 1), que no permite
    afirmar el criterio del 80~\% (Conclusión~\ref{conc:cobertura}). \textit{Resultado esperado:}
    una cobertura de XSS con intervalo de confianza comparable al de las otras categorías.
```

Después:

```
\item \textbf{Ampliar la explotabilidad confirmada de XSS más allá de un caso.}
    \textit{Acción:} confirmar con OWASP ZAP u otras herramientas, sobre más endpoints o
    aplicaciones, la explotabilidad de payloads del corpus propio, en particular los dirigidos a
    \texttt{content} y \texttt{title}, cuya vulnerabilidad no se confirmó, y repetir el filtrado
    contra el entrenamiento con el criterio de subcadena normalizada. \textit{Justificación:} la
    cobertura de XSS se midió sobre 200 payloads (200 de 200), pero la explotabilidad confirmada
    descansa en un único caso (1 de 1, ZAP) y 136 de los 200 payloads apuntan a campos sin
    vulnerabilidad confirmada (Conclusión~\ref{conc:cobertura}). \textit{Resultado esperado:} una
    medición de explotabilidad de XSS con más de un caso confirmado, que permita separar la
    detección de la explotabilidad.

    \item \textbf{Investigar los payloads de Command Injection que la combinación no bloquea.}
    \textit{Acción:} analizar por qué \texttt{cmdi\_6}, \texttt{cmdi\_184} y \texttt{cmdi\_185} no
    los bloquea ninguna configuración, y por qué otros cuatro payloads de la misma categoría
    (\texttt{cmdi\_112}, \texttt{cmdi\_134}, \texttt{cmdi\_31} y \texttt{cmdi\_38}) solo los bloquea
    la combinación y no la librería sola, comparando el vector de características y la
    probabilidad del Random Forest de cada petición con y sin el proxy. \textit{Justificación:} en
    la medición del 25 de octubre de 2026 esos tres son los únicos payloads que la combinación
    no bloquea, y la causa de ambos hallazgos no se investigó
    (Conclusión~\ref{conc:waf}). \textit{Resultado esperado:} saber si los tres payloads son una
    evasión real de las dos capas y si las cabeceras que agrega el proxy alteran el veredicto de la
    librería.
```

Fuente: errata V1 (cmdi_6, cmdi_184, cmdi_185), V2 (cmdi_112, cmdi_134, cmdi_31, cmdi_38) y V3 (136 de 200).

### 52. R-cnt-1: n-recomendaciones.tex, línea original 159, línea actual 177

Ubicación: Contador de la sección "Reproducibilidad y entrega de datos".

Antes:

```
\setcounter{enumi}{14}
```

Después:

```
\setcounter{enumi}{15}
```

Fuente: Consecuencia de añadir una recomendación en la sección anterior (el contador manual pasa de 14 a 15).

### 53. R-cnt-2: n-recomendaciones.tex, línea original 182, línea actual 200

Ubicación: Contador de la sección "Ampliación del alcance".

Antes:

```
\setcounter{enumi}{16}
```

Después:

```
\setcounter{enumi}{17}
```

Fuente: Ídem (de 16 a 17).

### 54. R-cnt-3: n-recomendaciones.tex, línea original 205, línea actual 223

Ubicación: Contador de la sección "Para trabajos de investigación similares".

Antes:

```
\setcounter{enumi}{18}
```

Después:

```
\setcounter{enumi}{19}
```

Fuente: Ídem (de 18 a 19).

### 55. A-anexos: n-anexos.tex, línea original 160, línea actual 160

Ubicación: Anexos: nuevas secciones (estratos de XSS; cmdi codificado; procedencia).

Antes:

```
\ifdefined\modoensamble
\else
	\section*{Referencias}
```

Después:

```
\section{Cobertura de XSS por estrato}
\label{anx:xss-estratos}

El Cuadro~\ref{tab:anx-xss-estratos} desglosa la cobertura del corpus propio de XSS por cada
dimensión de su generador, y el Cuadro~\ref{tab:anx-xss-bio} repite el desglose para los 64
payloads dirigidos al campo \texttt{bio}, el único con vulnerabilidad confirmada. Las
Configuraciones 2 y 3b bloquearon todos los payloads de cada estrato. La Configuración 3a falló en
11 payloads, todos con doble codificación URL (\texttt{url\_double}, 14 de 25 bloqueados) y
enviados como JSON o \texttt{multipart/form-data}. Los intervalos son de Wilson al 95~\%; en un
estrato con pocos payloads, el límite inferior es amplio aun con 100~\% de bloqueo.

\begin{longtable}{|L{4.2cm}|L{0.9cm}|L{3.4cm}|L{4.0cm}|}
\hline
\textbf{Estrato} & \textbf{n} & \textbf{Configuraciones 2 y 3b: bloqueados e IC 95~\%} & \textbf{Configuración 3a: bloqueados e IC 95~\%} \\ \hline
\endfirsthead
\multicolumn{4}{l}{\footnotesize\textit{(continuación)}} \\ \hline
\textbf{Estrato} & \textbf{n} & \textbf{Configuraciones 2 y 3b: bloqueados e IC 95~\%} & \textbf{Configuración 3a: bloqueados e IC 95~\%} \\ \hline
\endhead
\multicolumn{4}{r}{\footnotesize\textit{Continúa en la página siguiente}} \\
\endfoot
\endlastfoot
\multicolumn{4}{|l|}{\textit{Contexto de inyección}} \\ \hline
\texttt{attr\_double} & 41 & 41/41 (100.0~\%) [91.4--100.0] & 39/41 (95.1~\%) [83.9--98.7] \\ \hline
\texttt{attr\_single} & 44 & 44/44 (100.0~\%) [92.0--100.0] & 41/44 (93.2~\%) [81.8--97.7] \\ \hline
\texttt{attr\_unquoted} & 23 & 23/23 (100.0~\%) [85.7--100.0] & 22/23 (95.7~\%) [79.0--99.2] \\ \hline
\texttt{html\_body} & 47 & 47/47 (100.0~\%) [92.4--100.0] & 44/47 (93.6~\%) [82.8--97.8] \\ \hline
\texttt{html\_comment} & 16 & 16/16 (100.0~\%) [80.6--100.0] & 15/16 (93.8~\%) [71.7--98.9] \\ \hline
\texttt{js\_string} & 7 & 7/7 (100.0~\%) [64.6--100.0] & 7/7 (100.0~\%) [64.6--100.0] \\ \hline
\texttt{svg} & 13 & 13/13 (100.0~\%) [77.2--100.0] & 12/13 (92.3~\%) [66.7--98.6] \\ \hline
\texttt{url\_href\_src} & 9 & 9/9 (100.0~\%) [70.1--100.0] & 9/9 (100.0~\%) [70.1--100.0] \\ \hline
\multicolumn{4}{|l|}{\textit{Vector de ejecución}} \\ \hline
\texttt{event\_onerror} & 37 & 37/37 (100.0~\%) [90.6--100.0] & 34/37 (91.9~\%) [78.7--97.2] \\ \hline
\texttt{event\_onfocus\_autofocus} & 15 & 15/15 (100.0~\%) [79.6--100.0] & 14/15 (93.3~\%) [70.2--98.8] \\ \hline
\texttt{event\_onload\_body} & 15 & 15/15 (100.0~\%) [79.6--100.0] & 14/15 (93.3~\%) [70.2--98.8] \\ \hline
\texttt{event\_onmouseover} & 36 & 36/36 (100.0~\%) [90.4--100.0] & 33/36 (91.7~\%) [78.2--97.1] \\ \hline
\texttt{event\_ontoggle} & 25 & 25/25 (100.0~\%) [86.7--100.0] & 23/25 (92.0~\%) [75.0--97.8] \\ \hline
\texttt{iframe\_srcdoc} & 6 & 6/6 (100.0~\%) [61.0--100.0] & 6/6 (100.0~\%) [61.0--100.0] \\ \hline
\texttt{javascript\_uri} & 9 & 9/9 (100.0~\%) [70.1--100.0] & 9/9 (100.0~\%) [70.1--100.0] \\ \hline
\texttt{script} & 21 & 21/21 (100.0~\%) [84.5--100.0] & 21/21 (100.0~\%) [84.5--100.0] \\ \hline
\texttt{svg\_onload} & 36 & 36/36 (100.0~\%) [90.4--100.0] & 35/36 (97.2~\%) [85.8--99.5] \\ \hline
\multicolumn{4}{|l|}{\textit{Función ejecutada}} \\ \hline
\texttt{alert} & 28 & 28/28 (100.0~\%) [87.9--100.0] & 23/28 (82.1~\%) [64.4--92.1] \\ \hline
\texttt{confirm} & 31 & 31/31 (100.0~\%) [89.0--100.0] & 29/31 (93.5~\%) [79.3--98.2] \\ \hline
\texttt{document\_cookie} & 18 & 18/18 (100.0~\%) [82.4--100.0] & 18/18 (100.0~\%) [82.4--100.0] \\ \hline
\texttt{eval\_atob} & 32 & 32/32 (100.0~\%) [89.3--100.0] & 32/32 (100.0~\%) [89.3--100.0] \\ \hline
\texttt{fetch\_externo} & 40 & 40/40 (100.0~\%) [91.2--100.0] & 38/40 (95.0~\%) [83.5--98.6] \\ \hline
\texttt{fromcharcode} & 29 & 29/29 (100.0~\%) [88.3--100.0] & 29/29 (100.0~\%) [88.3--100.0] \\ \hline
\texttt{prompt} & 22 & 22/22 (100.0~\%) [85.1--100.0] & 20/22 (90.9~\%) [72.2--97.5] \\ \hline
\multicolumn{4}{|l|}{\textit{Codificación o evasión}} \\ \hline
\texttt{html\_entities\_dec} & 23 & 23/23 (100.0~\%) [85.7--100.0] & 23/23 (100.0~\%) [85.7--100.0] \\ \hline
\texttt{html\_entities\_hex} & 21 & 21/21 (100.0~\%) [84.5--100.0] & 21/21 (100.0~\%) [84.5--100.0] \\ \hline
\texttt{inline\_comment} & 23 & 23/23 (100.0~\%) [85.7--100.0] & 23/23 (100.0~\%) [85.7--100.0] \\ \hline
\texttt{mixed\_case} & 15 & 15/15 (100.0~\%) [79.6--100.0] & 15/15 (100.0~\%) [79.6--100.0] \\ \hline
\texttt{raw} & 14 & 14/14 (100.0~\%) [78.5--100.0] & 14/14 (100.0~\%) [78.5--100.0] \\ \hline
\texttt{slash\_for\_space} & 16 & 16/16 (100.0~\%) [80.6--100.0] & 16/16 (100.0~\%) [80.6--100.0] \\ \hline
\texttt{unicode\_escape} & 18 & 18/18 (100.0~\%) [82.4--100.0] & 18/18 (100.0~\%) [82.4--100.0] \\ \hline
\texttt{url\_double} & 25 & 25/25 (100.0~\%) [86.7--100.0] & 14/25 (56.0~\%) [37.1--73.3] \\ \hline
\texttt{url\_single} & 25 & 25/25 (100.0~\%) [86.7--100.0] & 25/25 (100.0~\%) [86.7--100.0] \\ \hline
\texttt{whitespace\_tab\_newline} & 20 & 20/20 (100.0~\%) [83.9--100.0] & 20/20 (100.0~\%) [83.9--100.0] \\ \hline
\multicolumn{4}{|l|}{\textit{Transporte}} \\ \hline
\texttt{json} & 68 & 68/68 (100.0~\%) [94.7--100.0] & 63/68 (92.6~\%) [83.9--96.8] \\ \hline
\texttt{multipart} & 68 & 68/68 (100.0~\%) [94.7--100.0] & 62/68 (91.2~\%) [82.1--95.9] \\ \hline
\texttt{urlencoded} & 64 & 64/64 (100.0~\%) [94.3--100.0] & 64/64 (100.0~\%) [94.3--100.0] \\ \hline
\multicolumn{4}{|l|}{\textit{Campo de destino}} \\ \hline
\texttt{bio} & 64 & 64/64 (100.0~\%) [94.3--100.0] & 59/64 (92.2~\%) [83.0--96.6] \\ \hline
\texttt{content} & 68 & 68/68 (100.0~\%) [94.7--100.0] & 63/68 (92.6~\%) [83.9--96.8] \\ \hline
\texttt{title} & 68 & 68/68 (100.0~\%) [94.7--100.0] & 67/68 (98.5~\%) [92.1--99.7] \\ \hline
\multicolumn{4}{|l|}{\textit{Subcadena literal \texttt{alert} en el payload}} \\ \hline
Con la subcadena & 17 & 17/17 (100.0~\%) [81.6--100.0] & 12/17 (70.6~\%) [46.9--86.7] \\ \hline
Sin la subcadena & 183 & 183/183 (100.0~\%) [97.9--100.0] & 177/183 (96.7~\%) [93.0--98.5] \\ \hline
\caption[Cobertura de XSS por estrato, corpus completo]{Cobertura de XSS por estrato sobre los 200 payloads del corpus propio (corrida 1, paquete 0.1.1 en las Configuraciones 2 y 3b)}
\label{tab:anx-xss-estratos}
\end{longtable}
{\footnotesize Nota. Elaboración propia con datos de
\texttt{attack-sim/results\_combined\_config\{2,3a,3b\}\_run1\_20261025.json} y de
\texttt{attack-sim/xss\_corpus\_filtered\_20261025.jsonl} (repositorio
\texttt{logSguarDian-vulnerable-project}); cálculo en
\texttt{docs/evidence/errata-v3-strata-20261025.py}. Las Configuraciones 2 y 3b coinciden en todos
los estratos.}

\begin{longtable}{|L{4.2cm}|L{0.9cm}|L{3.4cm}|L{4.0cm}|}
\hline
\textbf{Estrato} & \textbf{n} & \textbf{Configuraciones 2 y 3b: bloqueados e IC 95~\%} & \textbf{Configuración 3a: bloqueados e IC 95~\%} \\ \hline
\endfirsthead
\multicolumn{4}{l}{\footnotesize\textit{(continuación)}} \\ \hline
\textbf{Estrato} & \textbf{n} & \textbf{Configuraciones 2 y 3b: bloqueados e IC 95~\%} & \textbf{Configuración 3a: bloqueados e IC 95~\%} \\ \hline
\endhead
\multicolumn{4}{r}{\footnotesize\textit{Continúa en la página siguiente}} \\
\endfoot
\endlastfoot
\multicolumn{4}{|l|}{\textit{Contexto de inyección}} \\ \hline
\texttt{attr\_double} & 13 & 13/13 (100.0~\%) [77.2--100.0] & 12/13 (92.3~\%) [66.7--98.6] \\ \hline
\texttt{attr\_single} & 13 & 13/13 (100.0~\%) [77.2--100.0] & 12/13 (92.3~\%) [66.7--98.6] \\ \hline
\texttt{attr\_unquoted} & 9 & 9/9 (100.0~\%) [70.1--100.0] & 8/9 (88.9~\%) [56.5--98.0] \\ \hline
\texttt{html\_body} & 17 & 17/17 (100.0~\%) [81.6--100.0] & 15/17 (88.2~\%) [65.7--96.7] \\ \hline
\texttt{html\_comment} & 3 & 3/3 (100.0~\%) [43.9--100.0] & 3/3 (100.0~\%) [43.9--100.0] \\ \hline
\texttt{js\_string} & 2 & 2/2 (100.0~\%) [34.2--100.0] & 2/2 (100.0~\%) [34.2--100.0] \\ \hline
\texttt{svg} & 4 & 4/4 (100.0~\%) [51.0--100.0] & 4/4 (100.0~\%) [51.0--100.0] \\ \hline
\texttt{url\_href\_src} & 3 & 3/3 (100.0~\%) [43.9--100.0] & 3/3 (100.0~\%) [43.9--100.0] \\ \hline
\multicolumn{4}{|l|}{\textit{Vector de ejecución}} \\ \hline
\texttt{event\_onerror} & 15 & 15/15 (100.0~\%) [79.6--100.0] & 13/15 (86.7~\%) [62.1--96.3] \\ \hline
\texttt{event\_onfocus\_autofocus} & 2 & 2/2 (100.0~\%) [34.2--100.0] & 2/2 (100.0~\%) [34.2--100.0] \\ \hline
\texttt{event\_onload\_body} & 5 & 5/5 (100.0~\%) [56.6--100.0] & 5/5 (100.0~\%) [56.6--100.0] \\ \hline
\texttt{event\_onmouseover} & 14 & 14/14 (100.0~\%) [78.5--100.0] & 12/14 (85.7~\%) [60.1--96.0] \\ \hline
\texttt{event\_ontoggle} & 8 & 8/8 (100.0~\%) [67.6--100.0] & 7/8 (87.5~\%) [52.9--97.8] \\ \hline
\texttt{iframe\_srcdoc} & 1 & 1/1 (100.0~\%) [20.7--100.0] & 1/1 (100.0~\%) [20.7--100.0] \\ \hline
\texttt{javascript\_uri} & 3 & 3/3 (100.0~\%) [43.9--100.0] & 3/3 (100.0~\%) [43.9--100.0] \\ \hline
\texttt{script} & 7 & 7/7 (100.0~\%) [64.6--100.0] & 7/7 (100.0~\%) [64.6--100.0] \\ \hline
\texttt{svg\_onload} & 9 & 9/9 (100.0~\%) [70.1--100.0] & 9/9 (100.0~\%) [70.1--100.0] \\ \hline
\multicolumn{4}{|l|}{\textit{Función ejecutada}} \\ \hline
\texttt{alert} & 12 & 12/12 (100.0~\%) [75.8--100.0] & 10/12 (83.3~\%) [55.2--95.3] \\ \hline
\texttt{confirm} & 8 & 8/8 (100.0~\%) [67.6--100.0] & 8/8 (100.0~\%) [67.6--100.0] \\ \hline
\texttt{document\_cookie} & 5 & 5/5 (100.0~\%) [56.6--100.0] & 5/5 (100.0~\%) [56.6--100.0] \\ \hline
\texttt{eval\_atob} & 8 & 8/8 (100.0~\%) [67.6--100.0] & 8/8 (100.0~\%) [67.6--100.0] \\ \hline
\texttt{fetch\_externo} & 16 & 16/16 (100.0~\%) [80.6--100.0] & 14/16 (87.5~\%) [64.0--96.5] \\ \hline
\texttt{fromcharcode} & 8 & 8/8 (100.0~\%) [67.6--100.0] & 8/8 (100.0~\%) [67.6--100.0] \\ \hline
\texttt{prompt} & 7 & 7/7 (100.0~\%) [64.6--100.0] & 6/7 (85.7~\%) [48.7--97.4] \\ \hline
\multicolumn{4}{|l|}{\textit{Codificación o evasión}} \\ \hline
\texttt{html\_entities\_dec} & 6 & 6/6 (100.0~\%) [61.0--100.0] & 6/6 (100.0~\%) [61.0--100.0] \\ \hline
\texttt{html\_entities\_hex} & 6 & 6/6 (100.0~\%) [61.0--100.0] & 6/6 (100.0~\%) [61.0--100.0] \\ \hline
\texttt{inline\_comment} & 9 & 9/9 (100.0~\%) [70.1--100.0] & 9/9 (100.0~\%) [70.1--100.0] \\ \hline
\texttt{mixed\_case} & 6 & 6/6 (100.0~\%) [61.0--100.0] & 6/6 (100.0~\%) [61.0--100.0] \\ \hline
\texttt{raw} & 5 & 5/5 (100.0~\%) [56.6--100.0] & 5/5 (100.0~\%) [56.6--100.0] \\ \hline
\texttt{slash\_for\_space} & 4 & 4/4 (100.0~\%) [51.0--100.0] & 4/4 (100.0~\%) [51.0--100.0] \\ \hline
\texttt{unicode\_escape} & 7 & 7/7 (100.0~\%) [64.6--100.0] & 7/7 (100.0~\%) [64.6--100.0] \\ \hline
\texttt{url\_double} & 9 & 9/9 (100.0~\%) [70.1--100.0] & 4/9 (44.4~\%) [18.9--73.3] \\ \hline
\texttt{url\_single} & 8 & 8/8 (100.0~\%) [67.6--100.0] & 8/8 (100.0~\%) [67.6--100.0] \\ \hline
\texttt{whitespace\_tab\_newline} & 4 & 4/4 (100.0~\%) [51.0--100.0] & 4/4 (100.0~\%) [51.0--100.0] \\ \hline
\multicolumn{4}{|l|}{\textit{Transporte}} \\ \hline
\texttt{json} & 21 & 21/21 (100.0~\%) [84.5--100.0] & 18/21 (85.7~\%) [65.4--95.0] \\ \hline
\texttt{multipart} & 17 & 17/17 (100.0~\%) [81.6--100.0] & 15/17 (88.2~\%) [65.7--96.7] \\ \hline
\texttt{urlencoded} & 26 & 26/26 (100.0~\%) [87.1--100.0] & 26/26 (100.0~\%) [87.1--100.0] \\ \hline
\multicolumn{4}{|l|}{\textit{Campo de destino}} \\ \hline
\texttt{bio} & 64 & 64/64 (100.0~\%) [94.3--100.0] & 59/64 (92.2~\%) [83.0--96.6] \\ \hline
\caption[Cobertura de XSS por estrato, campo bio]{Cobertura de XSS por estrato sobre los 64 payloads dirigidos al campo \texttt{bio} (corrida 1, paquete 0.1.1 en las Configuraciones 2 y 3b)}
\label{tab:anx-xss-bio}
\end{longtable}
{\footnotesize Nota. Elaboración propia con las mismas fuentes del Cuadro~\ref{tab:anx-xss-estratos}.
Los 5 payloads que la Configuración 3a no bloqueó en \texttt{bio} reciben HTTP 200 de la aplicación.}

\section{Command Injection con separadores codificados y sin codificar}
\label{anx:cmdi-codificacion}

De los 200 payloads de Command Injection, 105 traen al menos un separador ya codificado
(\texttt{\%XX}) y 95 no. El Cuadro~\ref{tab:anx-cmdi-codificacion} los separa por configuración y
por versión del ejecutor. El ejecutor anterior volvía a codificar los separadores ya codificados,
por lo que solo alteraba el primer grupo; el segundo da el mismo resultado con ambos ejecutores.
Con el ejecutor corregido, el WAF sigue bloqueando menos los payloads con separadores codificados
(76.2~\%) que los no codificados (88.4~\%), una diferencia de 12.2 puntos porcentuales cuyos
intervalos de Wilson se solapan parcialmente.

\begin{table}[H]
\centering
\small
\begin{tabular}{|L{3.7cm}|L{3.6cm}|L{3.6cm}|L{2.5cm}|}
\hline
\textbf{Configuración y ejecutor} & \textbf{Separadores codificados (n=105): bloqueados e IC 95~\%} & \textbf{Sin codificar (n=95): bloqueados e IC 95~\%} & \textbf{Total (n=200)} \\ \hline
Configuración 1 (sin protección) & 0/105 (0.0~\%) [0.0--3.5] & 0/95 (0.0~\%) [0.0--3.9] & 0/200 (0.0~\%) \\ \hline
Configuración 2 (0.1.1), ejecutor corregido & 95/105 (90.5~\%) [83.4--94.7] & 90/95 (94.7~\%) [88.3--97.7] & 185/200 (92.5~\%) \\ \hline
Configuración 2 (0.1.1), ejecutor anterior (10 de octubre) & 102/105 (97.1~\%) [91.9--99.0] & 90/95 (94.7~\%) [88.3--97.7] & 192/200 (96.0~\%) \\ \hline
Configuración 3a, ejecutor corregido (25 de octubre) & 80/105 (76.2~\%) [67.2--83.3] & 84/95 (88.4~\%) [80.4--93.4] & 164/200 (82.0~\%) \\ \hline
Configuración 3a, ejecutor anterior (10 de octubre; reproducido el 25) & 52/105 (49.5~\%) [40.1--58.9] & 84/95 (88.4~\%) [80.4--93.4] & 136/200 (68.0~\%) \\ \hline
Configuración 3b (0.1.1), ejecutor corregido & 104/105 (99.0~\%) [94.8--99.8] & 93/95 (97.9~\%) [92.6--99.4] & 197/200 (98.5~\%) \\ \hline
\end{tabular}
\caption[Command Injection con separadores codificados y sin codificar]{Command Injection: payloads con separadores ya codificados y sin codificar, por configuración y por versión del ejecutor}
\label{tab:anx-cmdi-codificacion}
\end{table}
{\footnotesize Nota. Elaboración propia con datos de
\texttt{attack-sim/results\_combined\_config\{1,2,3a,3b\}\_run1\_20261025.json},
\texttt{attack-sim/results\_config3a-round5-20261010.json},
\texttt{attack-sim/results\_phase2a\_prefixexecutor\_config3a\_run1\_20261025.json} y los archivos
de resultados de la Configuración~2 del 10 de octubre de 2026; cálculo en
\texttt{docs/evidence/errata-v7b-cmdi-encoding-20261025.py}. Un payload se cuenta como codificado
si contiene al menos un \texttt{\%XX}.}

\section{Procedencia de la medición unificada del 25 de octubre de 2026}
\label{anx:ronda5-procedencia}

El Cuadro~\ref{tab:anx-ronda5-procedencia} identifica los archivos y las versiones de la medición
de las cuatro configuraciones con el corpus combinado de 800 peticiones. Las rutas son relativas a
la raíz del repositorio \texttt{logSguarDian-vulnerable-project}, rama
\texttt{exp/ronda5-20261025}, sin commits propios.

\begin{table}[H]
\centering
\small
\begin{tabular}{|L{4.2cm}|L{9.3cm}|}
\hline
\textbf{Elemento} & \textbf{Valor} \\ \hline
SHA base de la rama & {\scriptsize\texttt{07e80ead6a64db5db086216322624bc5bfa4edb0}} \\ \hline
Candidatos de XSS (400), SHA-256 & {\scriptsize\texttt{98d6e846899feedb0e736f3cb842d13c8d506751fb60911318bf840137883614}} \\ \hline
Corpus de XSS (200), SHA-256 & {\scriptsize\texttt{ef67ffd34d09a59c4cf8212722f78d5a2e8894f8d6a38d6e63a2f4598b6fae0d}} \\ \hline
Corpus combinado (800), SHA-256 & {\scriptsize\texttt{f1fb0b0a2c552636358785ec323aa10c76519638d0da1cb62ce131be2330263d}} \\ \hline
Protocolo de XSS, SHA-256 & {\scriptsize\texttt{ae52abc3227feb00650e98e0e1e81185fc76a56d8bd6b93ba1ca5cb3cc53134f}} \\ \hline
Manifiesto de congelación de XSS, SHA-256 & {\scriptsize\texttt{b3ccb69cc6329b520d4b0e91e28e9c1030940afedbdfe3915408ca31faee0496}} \\ \hline
Ejecutor corregido (\texttt{run\_large\_corpus.py}, commit \texttt{00ea3a3}), SHA-256 & {\scriptsize\texttt{422393460dfea808efe411d358166d37b662bbcaad77843ede0247c684c61af1}} \\ \hline
Ejecutor anterior (\texttt{00ea3a3\^{}}), SHA-256 & {\scriptsize\texttt{0c84de551f1138bbeb1ef7a9ed1801d83e4c52a7312c04b873a75de57a286623}} \\ \hline
Emisor de XSS (\texttt{send\_xss\_corpus.py}), SHA-256 & {\scriptsize\texttt{18c645527d1c6944734edb899ce10279928285abef1a627691c06223dcaa75ee}} \\ \hline
Paquete \texttt{logsguardian@0.1.1}, SHA-256 del archivo & {\scriptsize\texttt{abf8d5c47036d9c3a289bc36158f1caaa91b9504689aa97193e51c6808258d15}} \\ \hline
Modelo \texttt{rf.onnx} (par~C), SHA-256 & {\scriptsize\texttt{25b407e649283606a231665a5a8c8ea1c2c7ad4fd0374a8945b3f119651b0870}} \\ \hline
Modelo \texttt{if.onnx} (par~C), SHA-256 & {\scriptsize\texttt{5be28ee8437643b2f13708eee1ac3175348a350ea6fb8f8daeb09bd5717f797e}} \\ \hline
Imagen del WAF, digest & {\scriptsize\texttt{sha256:\allowbreak f12da37e72e29d1f06e7e829780f1016606d0799eac2966e58ef3819a3d30a50}} \\ \hline
Versiones del WAF & Nginx 1.30.5, ModSecurity 3.0.17, OWASP CRS 4.30.0; paranoia 1; \texttt{SecRuleEngine On}; umbral de anomalía de entrada 5; sin exclusiones activas \\ \hline
\texttt{Dockerfile} de la aplicación, SHA-256 & {\scriptsize\texttt{7f1edcdd31b1bd63b3d84d71a49f91b6a2cb63c8435413b6bab3e4e09d84203d}} \\ \hline
Resultados de la Configuración~1, corrida 1, SHA-256 & {\scriptsize\texttt{d88f968d203762aa469998968a79801018992f444c8ad7ff1bfef65986610903}} \\ \hline
Resultados de la Configuración~2, corrida 1, SHA-256 & {\scriptsize\texttt{577e6e002fb4989c719562a63a4db06482e40bff46ad68eb1faefcbb3b9b59aa}} \\ \hline
Resultados de la Configuración~3a, corrida 1, SHA-256 & {\scriptsize\texttt{1cf8badbbcc7f92f633aabd07d5d208355d94a97802587d510ff7f51818b502c}} \\ \hline
Resultados de la Configuración~3b, corrida 1, SHA-256 & {\scriptsize\texttt{1cfd0b5ec657d7fdc6816d10eb2b3f8992cf687d3c22d0a0d957db3b1048ba8e}} \\ \hline
\end{tabular}
\caption[Procedencia de la medición unificada]{Procedencia de la medición unificada de las cuatro configuraciones del 25 de octubre de 2026}
\label{tab:anx-ronda5-procedencia}
\end{table}
{\footnotesize Nota. Elaboración propia con datos de \texttt{docs/thesis-delta-xss.md},
\texttt{docs/thesis-delta-configs.md} y \texttt{docs/thesis-delta-errata-20261025.md}; las sumas
se recalcularon el 25 de octubre de 2026. La etiqueta de la imagen del WAF es flotante y hoy
resuelve a otro manifiesto, por lo que se cita el digest medido. La imagen local de la aplicación
tuvo el identificador \texttt{a75c14208ccd}; su digest no se verificó en cada arranque.}

\ifdefined\modoensamble
\else
	\section*{Referencias}
```

Fuente: Tablas generadas por script a partir de docs/evidence/errata-v3-strata-20261025.json y docs/evidence/errata-v7b-cmdi-encoding-20261025.json; hashes recalculados con shasum -a 256 el 25 de octubre de 2026; docs/thesis-delta-xss.md §2, docs/thesis-delta-configs.md §2.

### 56. RS-resumen: b-resumen.tex, línea original 7, línea actual 7

Ubicación: Resumen, cobertura de XSS.

Antes:

```
92.5~\% en inyección de comandos; en Cross-Site Scripting solo se confirmó un caso.
```

Después:

```
92.5~\% en inyección de comandos y 100.0~\% en Cross-Site Scripting (200 de 200 payloads de un corpus propio); la explotabilidad de Cross-Site Scripting se confirmó en un solo caso.
```

Fuente: docs/thesis-delta-xss.md §3.1.

### 57. RS-abstract: c-abstract.tex, línea original 7, línea actual 7

Ubicación: Abstract, cobertura de XSS (sincronizado con el Resumen).

Antes:

```
100.0\% of Path Traversal and 92.5\% of command injection; only one cross-site scripting case was confirmed.
```

Después:

```
100.0\% of Path Traversal, 92.5\% of command injection and 100.0\% of cross-site scripting (200 of 200 payloads from an own corpus); cross-site scripting exploitability was confirmed in a single case only.
```

Fuente: Sincronizado con RS-resumen.

### 58. D-defensa-ci: l-discusion.tex, línea original no aplica, línea actual 240

Ubicación: Cap. 9, Defensa en profundidad, precisión sobre el solapamiento de intervalos (correctiva).

Antes:

```
payloads de Command Injection con separadores ya codificados (76.2~\%) que los no codificados
(88.4~\%), una diferencia que se mantiene con el ejecutor corregido y que no se debe a la
medición.
```

Después:

```
payloads de Command Injection con separadores ya codificados (76.2~\%) que los no codificados
(88.4~\%), una diferencia de 12.2 puntos porcentuales que se mantiene con el ejecutor corregido,
aunque sus intervalos de Wilson se solapan parcialmente (67.2--83.3~\% y 80.4--93.4~\%).
```

Fuente: errata V7b (Wilson).

### 59. K-8.4.3-ci: k-resultados.tex, línea original no aplica, línea actual 935

Ubicación: Sec 8.4.3, precisión sobre el solapamiento de intervalos (correctiva).

Antes:

```
Injection con separadores ya codificados (80 de 105, 76.2~\%) que los 95 sin codificar (84 de 95,
88.4~\%) (Cuadro~\ref{tab:anx-cmdi-codificacion}).
```

Después:

```
Injection con separadores ya codificados (80 de 105, 76.2~\%) que los 95 sin codificar (84 de 95,
88.4~\%), con intervalos de Wilson parcialmente solapados (Cuadro~\ref{tab:anx-cmdi-codificacion}).
```

Fuente: errata V7b (Wilson 67.2--83.3 y 80.4--93.4).


## Barrido de valores obsoletos (punto 17)

Búsqueda en todos los `.tex` del directorio (se excluyen las líneas de comentario completas). Se informan los conteos antes y después de las ediciones, las líneas actuales de cada hit y su disposición.

### `68.0`: antes 6, después 6

Líneas actuales: j-metodologia.tex:1100, j-metodologia.tex:1149, k-resultados.tex:930, l-discusion.tex:237, m-conclusiones.tex:105, n-anexos.tex:321

Disposición: Se conserva y se corrige el sentido: es la cifra histórica del ejecutor anterior (136 de 200) que ahora se explica y se contrasta con 82.0 % (Cuadro 38, Secciones 8.4.3 y 7.11, Discusión, Conclusión de defensa en profundidad, Anexo). Las menciones que la presentaban como medición vigente del WAF en Discusión, Conclusiones y Recomendaciones se reescribieron.

### `68,0`: antes 0, después 0

Disposición: Sin hits.

### `136/200`: antes 1, después 1

Líneas actuales: n-anexos.tex:321

Disposición: Cuadro 38 reconstruido (ya no aparece como celda del WAF). El único hit actual es la fila histórica del Anexo, rotulada como ejecutor anterior.

### `65 de 68`: antes 1, después 0

Disposición: Corregido: la fila del Cuadro 40 ahora dice 48 de 51 (3b) y 44 de 51 (Configuración 2).

### `65/68`: antes 0, después 0

Disposición: Sin hits.

### `37/40`: antes 4, después 4

Líneas actuales: k-resultados.tex:332, k-resultados.tex:334, k-resultados.tex:349, k-resultados.tex:366

Disposición: Sin relación: cifras de dvws-node (37 de 40 bloqueados con User-Agent de navegador). No se tocan.

### `64 de`: antes 1, después 5

Líneas actuales: j-metodologia.tex:1101, j-metodologia.tex:1150, j-metodologia.tex:1198, k-resultados.tex:749, m-conclusiones.tex:66

Disposición: Antes: 64 ataques de Command Injection no bloqueados por el WAF (corregido, ahora 36 de Command Injection y 51 en total). Los hits actuales son 164 de 200 (WAF, ejecutor corregido) y los 64 payloads de XSS dirigidos a bio (64 de 64 bloqueados); correctos.

### `n=1`: antes 12, después 9

Líneas actuales: j-metodologia.tex:231, j-metodologia.tex:749, j-metodologia.tex:1106, k-resultados.tex:744, k-resultados.tex:865, k-resultados.tex:1044, l-discusion.tex:210, l-discusion.tex:345, m-conclusiones.tex:71

Disposición: Cada hit restante se refiere a la explotabilidad confirmada por ZAP (correcto) o al hecho histórico de que la Ronda 5 original medía XSS con n=1. Se corrigieron los que decían que la cobertura de XSS tenía n=1.

### `n = 1`: antes 0, después 0

Disposición: Sin hits.

### `una sola alerta`: antes 0, después 0

Disposición: Sin hits (la frase vigente es una sola es de XSS, hecho de ZAP).

### `1/1`: antes 3, después 2

Líneas actuales: k-resultados.tex:865, n-anexos.tex:265

Disposición: Quedan: la fila de ZAP del Cuadro 37 (rotulada n=1, corpus anterior, no comparable) y estratos de n=1 en las tablas del Anexo. Corregidos: el Cuadro 38 y el Cuadro 40.

### `0/1`: antes 1, después 0

Disposición: Corregido: Cuadro 38 (XSS 0/1 pasó a 0/200). La búsqueda descarta los falsos positivos 70/15/15 y 0/105.

### `538`: antes 1, después 1

Líneas actuales: k-resultados.tex:737

Disposición: Se conserva como hecho (alertas de ZAP, n=1), según lo indicado.

### `no permite afirmar`: antes 1, después 1

Líneas actuales: l-discusion.tex:237

Disposición: Corregido en Conclusiones (criterio del 80 % de XSS). El hit restante está en Discusión y se refiere a que el 82.0 % del WAF en Command Injection no permite afirmar que supere el 80 %.

### `payloads clásicos`: antes 0, después 0

Disposición: Corregido (Cuadro 28).

### `no automatizado`: antes 1, después 0

Disposición: Corregido (Cuadro 28).

### `misma imagen`: antes 1, después 0

Disposición: Corregido (Sección 7.1): ahora dice mismo árbol de la aplicación y mismo Dockerfile, porque la imagen local no se verificó por digest en cada arranque (errata E-12).

### `misma aplicación`: antes 1, después 1

Líneas actuales: j-metodologia.tex:503

Disposición: Se conserva (Procedimiento 4.1): ahora es cierto para las cuatro configuraciones, con el mecanismo documentado.

### `feat/waf`: antes 0, después 0

Disposición: Sin hits.

### `par A`: antes 24, después 22

Líneas actuales: j-metodologia.tex:399, j-metodologia.tex:401, j-metodologia.tex:410, j-metodologia.tex:420, j-metodologia.tex:609, j-metodologia.tex:1068, j-metodologia.tex:1069, j-metodologia.tex:1072, j-metodologia.tex:1080, k-resultados.tex:48, k-resultados.tex:49, k-resultados.tex:317, k-resultados.tex:375, k-resultados.tex:723, k-resultados.tex:727, k-resultados.tex:735, k-resultados.tex:762, k-resultados.tex:784, k-resultados.tex:860, k-resultados.tex:1012, l-discusion.tex:394, n-anexos.tex:46

Disposición: Se revisó cada hit: son atribuciones históricas del paquete 0.1.0 y del estudio de User-Agent, correctas. Se eliminó la atribución de la Configuración 3b al par A (Cuadro 38 y Procedimiento 4.4) y la de la 3a a una rama distinta; la 3b se atribuye al par C.

### `0.1.0`: antes 43, después 47

Líneas actuales: j-metodologia.tex:254, j-metodologia.tex:388, j-metodologia.tex:400, j-metodologia.tex:409, j-metodologia.tex:414, j-metodologia.tex:418, j-metodologia.tex:421, j-metodologia.tex:425, j-metodologia.tex:426, j-metodologia.tex:609, j-metodologia.tex:671, j-metodologia.tex:1067, j-metodologia.tex:1076, j-metodologia.tex:1093, j-metodologia.tex:1097, k-resultados.tex:46, k-resultados.tex:72, k-resultados.tex:83, k-resultados.tex:94, k-resultados.tex:104, k-resultados.tex:316, k-resultados.tex:595, k-resultados.tex:723, k-resultados.tex:762, k-resultados.tex:784, k-resultados.tex:793, k-resultados.tex:809, k-resultados.tex:860, k-resultados.tex:882, k-resultados.tex:983, k-resultados.tex:1040, l-discusion.tex:55, l-discusion.tex:61, l-discusion.tex:66, l-discusion.tex:81, l-discusion.tex:90, l-discusion.tex:183, l-discusion.tex:189, l-discusion.tex:198, l-discusion.tex:394, l-discusion.tex:399, m-conclusiones.tex:23, m-conclusiones.tex:31, m-conclusiones.tex:57, n-anexos.tex:46, n-anexos.tex:58, n-recomendaciones.tex:120

Disposición: Se revisó cada hit: nombre del paquete publicado el 30 de agosto de 2026 y mediciones rotuladas como 0.1.0 (Cuadro 37, resumen de indicadores, Discusión). Ninguna cifra de 0.1.0 se compara ya con la Configuración 3a.

### `170/200`: antes 2, después 1

Líneas actuales: k-resultados.tex:862

Disposición: Cuadro 37 (columna 0.1.0, rotulada). Eliminado del Cuadro 38.

### `183/200`: antes 2, después 1

Líneas actuales: k-resultados.tex:863

Disposición: Cuadro 37 (columna 0.1.0, rotulada). Eliminado del Cuadro 38.


## Cifras nuevas y su fuente

| Cifra | Archivo y clave |
|---|---|
| Config 1: 0/800 (0/200 por categoría) | `attack-sim/results_combined_config1_run1_20261025.json`; `docs/thesis-delta-configs.md` §3.1(a) |
| Config 2: 199, 200, 185, 200 de 200; total 784 | `results_combined_config2_run1_20261025.json`; recuento por conjuntos en `docs/evidence/errata-v1-v5-v9-20261025.json` (V1, V5) |
| Config 3a: 199, 197, 164, 189 de 200; total 749 | `results_combined_config3a_run1_20261025.json`; V1, V5 |
| Config 3b: 200, 200, 197, 200 de 200; total 797 | `results_combined_config3b_run1_20261025.json`; V1, V5 |
| Wilson por categoría y configuración | `docs/thesis-delta-configs.md` §3.1; recalculados con z = 1.959963984540054 |
| 51 ataques que la 3a no bloquea (1, 3, 36, 11); 3b bloquea 48; Config 2 bloquea 44 | V1, V2, V5 |
| Sin XSS: 40, 37, 33 frente a 68, 65, 64 | V5 |
| +13 (1 sqli, 12 cmdi) sobre la Config 2 y +48 sobre la 3a | V5 (agregados 784, 749, 797) |
| Tres payloads que ninguna configuración bloquea (`cmdi_6`, `cmdi_184`, `cmdi_185`) | V1 (interseccion triple) |
| Cuatro payloads solo de la 3b (`cmdi_112`, `cmdi_134`, `cmdi_31`, `cmdi_38`) | V2; Fase 2b (`docs/evidence/phase2b-diff-20261025.json`) |
| cmdi codificado 80/105 (76.2 %) y sin codificar 84/95 (88.4 %) en la 3a; 52/105 (49.5 %) con el ejecutor anterior | V7b (`docs/evidence/errata-v7b-cmdi-encoding-20261025.json`); Fase 2a (`docs/evidence/phase2a-summary-20261025.json`) |
| 136/200 reproducido con el ejecutor anterior; 164/200 con el corregido | Fase 2a (`attack-sim/results_phase2a_prefixexecutor_config3a_run{1,2}_20261025.json`) |
| XSS 200/200 [98.1, 100.0] y bio 64/64 [94.3, 100.0] (Config 2 y 3b); 3a 189/200 [90.4, 96.9] y bio 59/64 [83.0, 96.6] | V3 (`docs/evidence/errata-v3-strata-20261025.json`) |
| 136 de 200 con HTTP 400 sin protección | V3 (Config 1) |
| 197/197 sin los tres payloads con coincidencia | V4 |
| Subcadena normalizada: sqli 4, pt 7, cmdi 2, xss 3 de 200 | V6 (`attack-sim/leakage_report_round5_all_20261025.json`) |
| 9,600 envíos sin cambio de veredicto | V9 |
| Hashes del anexo | `shasum -a 256` recalculados el 25 de octubre de 2026 sobre los archivos del repositorio |

## Decisiones pendientes para el autor y afirmaciones que no se pudieron verificar

1. Afirmaciones de los deltas que no se usaron, por contradecir los archivos (errata E-01, E-02, E-05, E-06, E-10): que la 3b bloquea los tres payloads de cmdi que ninguna capa bloquea (no los bloquea); que el WAF tiene ventaja en Path Traversal (con la 0.1.1 la librería iguala o supera al WAF); que la 3b supera a ambas capas en todas las categorías y que ninguna subsume a la otra (en Path Traversal y XSS la librería sola iguala a la 3b).
2. Se eliminó del Cuadro 38 la columna de Config 2 con el paquete 0.1.0 (170/200 y 183/200), para no compararla con la 3a. Esas cifras siguen en el Cuadro 37 rotuladas como 0.1.0. Si se prefiere conservarlas en el Cuadro 38 como fila aparte, hay que rotularlas y no compararlas.
3. Se añadió una recomendación nueva (investigar los payloads de cmdi que la combinación no bloquea), de modo que las recomendaciones pasan de 22 a 23 y se renumeran las posteriores (los contadores manuales de `\setcounter` suben una unidad). No hay referencias numéricas a recomendaciones en otros capítulos; las referencias usan etiquetas.
4. La recomendación 12 (Construir un corpus limpio de XSS) se reorientó a ampliar la explotabilidad confirmada, porque el corpus ya existe. Es un cambio de sentido, no solo de cifras.
5. El texto de la Sección 7.7 (fila "Corpus limpio (M2)" del cuadro de datos) todavía dice "reporte de exclusión con cero coincidencias en el corpus final". Es cierto para el criterio exacto del filtro, pero convive con las 4, 7, 2 y 3 coincidencias por subcadena de la auditoría posterior. No se modificó por quedar fuera de las 17 ubicaciones; conviene decidir si se matiza.
6. El Resumen y el Abstract dicen "payloads no vistos" también para XSS, aunque 3 de los 200 coinciden con el entrenamiento por subcadena normalizada y el corpus se construyó tras conocer los resultados de la Ronda 5. Está declarado en el cuerpo (Secciones 7.11 y 9), no en el resumen.
7. La diferencia del WAF entre separadores codificados (76.2 %) y sin codificar (88.4 %) es de 12.2 puntos porcentuales y sus intervalos de Wilson se solapan parcialmente; el texto lo declara así y no la presenta como diferencia significativa.
8. No se investigó por qué cuatro payloads de cmdi solo los bloquea la 3b ni por qué los tres restantes evaden todo (Fase 2b se limitó a comparar cuerpo, objetivo y cabeceras). Las cuatro cabeceras `X-*` y el `Host` sin puerto son diferencias observadas, no causa demostrada.
9. La versión de ModSecurity y de Nginx de la medición antigua de la 3a no consta en los archivos (V8), por lo que el texto no la compara con la nueva; se dice solo que la medición antigua se descartó.
10. En la Fase 2 la reconstrucción produjo otra imagen local de la aplicación (`sha256:e22deaa793f0...`, frente a `a75c14208ccd` de las mediciones del 25 de octubre); no cambió ningún veredicto en los 600 payloads, pero el texto no afirma que la imagen sea la misma.
11. T11 y T12 del delta de XSS (explotabilidad en navegador y ZAP como segunda fuente) no se ejecutaron; por eso la explotabilidad confirmada sigue en n=1.
12. Pendientes de tareas anteriores que no dependen de esta: abrir las URL de `mastercard2025` y `cloudflaredefenseindepth`, confirmar la URL de `torrano2010csic`, obtener la versión de Juice Shop con Diego, y confirmar si el nombre del examinador lleva "Ing. Ma.".

## Compilación

No hay una distribución de LaTeX instalada en este equipo (`pdflatex`, `xelatex`, `latexmk`, `tectonic` y `lualatex` no existen), por lo que no se pudo compilar. Comprobaciones hechas en su lugar: todas las referencias `\ref` tienen su `\label` y no hay etiquetas duplicadas; las llaves están balanceadas en los ocho archivos tocados; los entornos `begin`/`end` están balanceados (la única diferencia es `document`, esperada porque el `\begin{document}` lo aporta el preámbulo); ninguna línea añadida contiene comentarios `%`. Para compilar en Overleaf: `main.tex`, motor pdfLaTeX, biber y `makeglossaries`. Puntos a mirar en el registro: avisos de `Overfull \hbox` en los cuadros nuevos del Anexo (hashes en `\scriptsize\texttt`), y la longitud de los cuadros `longtable` de estratos.

## Estado de git

Rama `exp/ronda5-20261025`, HEAD `07e80ead6a64db5db086216322624bc5bfa4edb0` antes y después. Sin commits, sin `add`, sin cambios en archivos con seguimiento. Los `.tex` están en una carpeta que no es un repositorio; sus cambios se pueden revisar contra `docs/evidence/tex-before-20261025/` con `diff`.


## Segunda ronda (ediciones 60 a 79)

Ediciones de la segunda ronda, con respaldo previo en `docs/evidence/tex-before-round2-20261025/` (sumas en `SHA256SUMS.txt`). Las líneas originales se miden sobre ese respaldo y las nuevas sobre los archivos actuales. Los resultados de los experimentos E1 y E2 y de las comprobaciones de la fase A están en `docs/thesis-delta-errata-20261025-b.md`.

| Archivo | Ediciones |
|---|---|
| b-resumen.tex | 1 |
| c-abstract.tex | 1 |
| j-metodologia.tex | 4 |
| k-resultados.tex | 4 |
| l-discusion.tex | 2 |
| m-conclusiones.tex | 1 |
| n-anexos.tex | 5 |
| n-recomendaciones.tex | 2 |
| **Total** | **20** |

### 60. A1: j-metodologia.tex, línea original 835, línea actual 835

Ubicación: Sec 7.7, fila "Corpus limpio (M2)" del cuadro de datos.

Antes:

```
Reporte de exclusión con cero
coincidencias en el corpus final; reproducibilidad (dos ejecuciones con igual resultado)
```

Después:

```
Sin coincidencias por hash exacto
tras el filtro, por construcción; la auditoría posterior por subcadena normalizada encontró 4
(SQLi), 7 (Path Traversal), 2 (Command Injection) y 3 (XSS) coincidencias de 200, y cinco de las
siete de Path Traversal son también literales; reproducibilidad (dos ejecuciones con igual resultado)
```

Fuente: attack-sim/leakage_report_round5_all_20261025.json, por_categoria.*.union_particiones: subcadena_normalizada sqli 4, path_traversal 7, cmdi 2, xss 3; path_traversal.subcadena_exacta 5 (ids path_traversal_26, _40, _57, _119, _198, todos dentro de los 7 normalizados).

### 61. A2-es: b-resumen.tex, línea original 7, línea actual 7

Ubicación: Resumen, calificación de "payloads no vistos".

Antes:

```
Sobre payloads no vistos, la versión 0.1.1 bloqueó
```

Después:

```
Sobre payloads no vistos (excluidos del entrenamiento por coincidencia exacta, con coincidencias residuales por subcadena normalizada de entre 1.0 y 3.5~\% por categoría y, en Cross-Site Scripting, con un corpus construido después de conocer los resultados de la Ronda~5), la versión 0.1.1 bloqueó
```

Fuente: Mismo archivo: 2/200 = 1.0 % (cmdi) y 7/200 = 3.5 % (Path Traversal) como extremos; 4/200 = 2.0 % (SQLi) y 3/200 = 1.5 % (XSS). Corpus de XSS posterior a la Ronda 5: docs/thesis-delta-xss.md §7. Palabras del Resumen: 259 antes, 294 después; no se encontró límite en la plantilla ni en las Directrices (ver errata-b).

### 62. A2-en: c-abstract.tex, línea original 7, línea actual 7

Ubicación: Abstract, calificación de "unseen payloads" (sincronizado con el Resumen).

Antes:

```
On unseen payloads, version 0.1.1 blocked
```

Después:

```
On unseen payloads (excluded from training by exact match, with residual normalized-substring overlaps of 1.0\% to 3.5\% per category and, for cross-site scripting, a corpus built after the Round~5 results were known), version 0.1.1 blocked
```

Fuente: Ídem A2-es. Palabras del Abstract: 222 antes, 251 después.

### 63. A3-k: k-resultados.tex, línea original 936, línea actual 937

Ubicación: Sec 8.4.3, codificados frente a sin codificar.

Antes:

```
88.4~\%), con intervalos de Wilson parcialmente solapados (Cuadro~\ref{tab:anx-cmdi-codificacion}).
```

Después:

```
88.4~\%); la diferencia es de 12.2 puntos porcentuales (prueba exacta de Fisher bilateral,
$p = 0.028$; intervalo de confianza de Wald al 95~\% de la diferencia, de 1.8 a 22.6 puntos;
Cuadro~\ref{tab:anx-cmdi-codificacion}). Los dos subconjuntos no están controlados por otras
características del payload, por lo que la diferencia no se atribuye a la codificación como causa.
```

Fuente: docs/evidence/a3-fisher-codificacion-20261025.json: Fisher exacto bilateral p = 0.02765 (80/105 frente a 84/95), diferencia 12.23 puntos, IC95 de Wald 1.85 a 22.61 puntos (z = 1.959963984540054); script docs/evidence/a3-fisher-codificacion-20261025.py. Wilson de cada grupo: docs/evidence/errata-v7b-cmdi-encoding-20261025.json.

### 64. A3-l: l-discusion.tex, línea original 240, línea actual 240

Ubicación: Cap. 9, Defensa en profundidad, codificados frente a sin codificar.

Antes:

```
payloads de Command Injection con separadores ya codificados (76.2~\%) que los no codificados
(88.4~\%), una diferencia de 12.2 puntos porcentuales que se mantiene con el ejecutor corregido,
aunque sus intervalos de Wilson se solapan parcialmente (67.2--83.3~\% y 80.4--93.4~\%).
```

Después:

```
payloads de Command Injection con separadores ya codificados (76.2~\%; intervalo de Wilson al
95~\%: 67.2--83.3~\%) que los no codificados (88.4~\%; 80.4--93.4~\%), una diferencia de 12.2
puntos porcentuales que se mantiene con el ejecutor corregido (prueba exacta de Fisher bilateral,
$p = 0.028$; intervalo de confianza de Wald al 95~\% de la diferencia, de 1.8 a 22.6 puntos). Los
dos subconjuntos no están controlados por otras características del payload, por lo que la
diferencia no se atribuye a la codificación como causa.
```

Fuente: Ídem A3-k.

### 65. A3-anexo-texto: n-anexos.tex, línea original 308, línea actual 308

Ubicación: Anexo de cmdi codificado, párrafo introductorio.

Antes:

```
una diferencia de 12.2 puntos porcentuales cuyos
intervalos de Wilson se solapan parcialmente.
```

Después:

```
una diferencia de 12.2 puntos porcentuales (prueba exacta de
Fisher bilateral sobre 80 de 105 frente a 84 de 95, $p = 0.028$; intervalo de confianza de Wald al
95~\% de la diferencia, de 1.8 a 22.6 puntos). Los dos subconjuntos no están controlados por otras
características del payload, por lo que la diferencia no se atribuye a la codificación como causa.
El cuadro conserva los intervalos de Wilson de cada grupo.
```

Fuente: Ídem A3-k.

### 66. A3-A10-anexo-nota: n-anexos.tex, línea original 332, línea actual 335

Ubicación: Anexo de cmdi codificado, nota (prueba de hipótesis y 4 frente a 32 payloads).

Antes:

```
Un payload se cuenta como codificado
si contiene al menos un \texttt{\%XX}.}
```

Después:

```
Un payload se cuenta como codificado
si contiene al menos un \texttt{\%XX}. La prueba de Fisher y el intervalo de Wald se calcularon en
\texttt{docs/evidence/a3-fisher-codificacion-20261025.py}. Con el ejecutor corregido, 4 payloads de
Command Injection dejaron de bloquearse en la Configuración~3a (\texttt{cmdi\_22},
\texttt{cmdi\_38}, \texttt{cmdi\_52} y \texttt{cmdi\_179}) y 32 pasaron a bloquearse, de modo que el
defecto no sesgaba todos los payloads en la misma dirección.}
```

Fuente: A3: ídem A3-k. A10: docs/thesis-delta-errata-20261025.md, Fase 2a (4 payloads dejan de bloquearse: cmdi_22, cmdi_38, cmdi_52, cmdi_179; 32 pasan a bloquearse; neto +28), docs/evidence/phase2a-summary-20261025.json.

### 67. A3-j: j-metodologia.tex, línea original 1152, línea actual 1160

Ubicación: Sec 7.11, viñeta de causa del salto de cmdi en la 3a.

Antes:

```
el WAF sigue bloqueando menos los codificados (76.2~\%) que los
    no codificados (88.4~\%, 84 de 95).
```

Después:

```
el WAF sigue bloqueando menos los codificados (76.2~\%) que los
    no codificados (88.4~\%, 84 de 95), una diferencia de 12.2 puntos porcentuales (prueba exacta de
    Fisher bilateral, $p = 0.028$) que no se atribuye a la codificación como causa, porque los dos
    subconjuntos no están controlados por otras características del payload.
```

Fuente: Ídem A3-k.

### 68. A4: k-resultados.tex, línea original 941, línea actual 945

Ubicación: Sec 8.4.3, comparación con la medición anterior (solo WAF; sin 37/40 ni 33/40).

Antes:

```
Sobre el mismo
denominador de la medición anterior (sin XSS) son 40 ataques no bloqueados por el WAF, de los que la
3b bloqueó 37 y la 2, 33, frente a 68, 65 y 64 antes; esa reducción corresponde al cambio de
ejecutor.
```

Después:

```
Para el WAF, los
ataques no bloqueados pasan de 68 a 40 en las tres categorías comparables con la medición anterior
(de 64 a 36 en Command Injection), y la reejecución del ejecutor anterior sobre el mismo árbol
muestra que esa reducción se debe al ejecutor. No se compara con las mediciones anteriores la
Configuración~3b ni la 2, porque provienen de otras versiones de la librería: la Configuración~2
anterior usó el par~A y de la 3b anterior no consta el paquete.
```

Fuente: docs/thesis-delta-errata-20261025.md V5 (68 a 40 en 600 payloads; cmdi 64 a 36) y Fase 2a (el ejecutor anterior reproduce 136/200 y el mismo veredicto en los 600); par de modelos de la Config 2 anterior: Cuadro 12 (tarball con el par A); de la 3b anterior no consta el paquete: texto original de la tesis y errata V8.

### 69. A5: n-recomendaciones.tex, línea original 121, línea actual 121

Ubicación: Recomendación 11, filtro de exclusión.

Antes:

```
generado con otra semilla y el
    mismo filtro de exclusión, y fijar
```

Después:

```
generado con otra semilla y un
    filtro de exclusión que incorpore, además de la igualdad exacta, la auditoría de subcadena
    normalizada, y fijar
```

Fuente: docs/protocol-xss.md (T6 y T7: el filtro exacto no atrapó 3 coincidencias que la auditoría de subcadena sí) y errata V6.

### 70. A6-j: j-metodologia.tex, línea original 1154, línea actual 1164

Ubicación: Sec 7.11, nueva amenaza: comparación con el WAF no neutral.

Antes:

```
\item \textbf{Repeticiones de un proceso determinista.}
```

Después:

```
\item \textbf{Comparación con el WAF no neutral.} El corpus se construyó a partir de familias
    de payload que también están representadas en el entrenamiento de la librería, mientras que el
    WAF es un conjunto de reglas genérico en nivel de paranoia 1; la comparación entre ambos no es
    neutral y favorece a la librería por construcción. No se midieron otros niveles de paranoia ni
    un corpus ajeno al entrenamiento.
    \item \textbf{Repeticiones de un proceso determinista.}
```

Fuente: Instrucción del autor (A6). No hay archivo de resultados que mida la neutralidad de la comparación; la redacción se acotó a familias de payload representadas en el entrenamiento, que la auditoría de subcadena respalda en parte (V6). Los niveles de paranoia distintos de 1 no se midieron (docs/thesis-delta-configs.md §2).

### 71. A6-c: m-conclusiones.tex, línea original 110, línea actual 110

Ubicación: Conclusión conc:waf, cláusula sobre la limitación de la comparación.

Antes:

```
La evidencia respalda el uso de la librería como capa
    complementaria a un WAF y no como su sustituto.
```

Después:

```
La evidencia respalda el uso de la librería como capa
    complementaria a un WAF y no como su sustituto, con la limitación de que el corpus se construyó
    a partir de familias de payload representadas en el entrenamiento de la librería y de que no se
    midieron otros niveles de paranoia del WAF, por lo que la comparación no es neutral
    (Sección~\ref{sec:met-validez}).
```

Fuente: Ídem A6-j.

### 72. A7: k-resultados.tex, línea original 742, línea actual 742

Ubicación: Sec 8.4.2, reconfirmación del payload de ZAP.

Antes:

```
el 25 de octubre de 2026 se
reconfirmó que es explotable sin protección (HTTP 200) y que la librería lo bloquea (HTTP 403).
```

Después:

```
el 25 de octubre de 2026 se
reconfirmó que el servidor lo almacena sin escapar (HTTP 200) sin protección y que la librería lo
bloquea (HTTP 403); la ejecución en un navegador no se verificó.
```

Fuente: docs/thesis-delta-xss.md §3.6 (Config 1: 200, persiste sin escapar; Config 2: 403). No hay verificación en navegador (T11 no se ejecutó, §8 del mismo documento).

### 73. A8-fila: n-anexos.tex, línea original 354, línea actual 361

Ubicación: Anexo de procedencia, rótulo del manifiesto.

Antes:

```
Manifiesto de congelación de XSS, SHA-256 &
```

Después:

```
Manifiesto de congelación de XSS (versión final), SHA-256 &
```

Fuente: docs/freeze-xss-20261025.json (SHA-256 b3ccb69c...; claves recalculo_pre_medicion, recalculo_post_medicion, nota_congelacion).

### 74. A8-nota: n-anexos.tex, línea original 374, línea actual 381

Ubicación: Anexo de procedencia, nota sobre el alcance de la garantía de congelación.

Antes:

```
La etiqueta de la imagen del WAF es flotante y hoy
resuelve a otro manifiesto, por lo que se cita el digest medido.
```

Después:

```
El manifiesto de congelación es el de su versión
final: incluye los recálculos posteriores a la medición, y la garantía de congelación descansa en
los hashes de los archivos congelados que contiene, no en el del manifiesto. La etiqueta de la
imagen del WAF es flotante y hoy resuelve a otro manifiesto, por lo que se cita el digest medido.
```

Fuente: Ídem A8-fila.

### 75. A9: n-anexos.tex, línea original varias, línea actual varias

Ubicación: Anexos: todas las celdas con hashes de 64 caracteres (26).

Antes:

```
\texttt{<64 caracteres hexadecimales>}
```

Después:

```
\texttt{<32 caracteres>\allowbreak{}<32 caracteres>}
```

Fuente: Cambio tipográfico sin cifras; 26 hashes de 64 caracteres.

### 76. E1-j: j-metodologia.tex, línea original 1145, línea actual 1147

Ubicación: Sec 7.11, viñeta de la librería sola frente a detrás del proxy (resultado de E1).

Antes:

```
puerto de \texttt{Host}; no se midió el
    efecto de esas cabeceras en el veredicto de la librería, de modo que la Configuración~2 y la
    librería dentro de la 3b no son la misma medición.
```

Después:

```
puerto de \texttt{Host}; al
    enviar los cuatro payloads a la Configuración~2 con esas cabeceras, el paquete 0.1.1 los
    bloqueó en las tres repeticiones, y sin ellas no bloqueó ninguno, mientras que agregar además
    el \texttt{Host} sin puerto no cambió ningún veredicto. Con las cabeceras, la única
    característica del vector que cambia es el recuento de cabeceras fuera de la lista estándar
    (\texttt{unusual\_headers\_count}, de 0 a 4), que usa el Random Forest. La diferencia queda
    explicada por el proxy: la Configuración~2 y la librería dentro de la 3b no son la misma
    medición, y el veredicto de la librería depende en parte de las cabeceras que agrega el
    despliegue.
```

Fuente: docs/evidence/e1-proxy-headers-20261025.json (63 envíos: 7 payloads x 3 variantes x 3 repeticiones, Config 2, 0.1.1, ejecutor corregido; V0 0/3 en los cuatro, V1 y V2 3/3 en los cuatro), docs/evidence/e1-extractor-caracteristicas-20261025.json (única característica que cambia: unusual_headers_count 0 a 4; usada por el RF, no por el IF), attack-sim/e1_proxy_headers_20261025.py.

### 77. E1-k: k-resultados.tex, línea original 952, línea actual 958

Ubicación: Sec 8.4.3, payloads que solo bloquea la 3b (resultado de E1).

Antes:

```
pero
no se midió el efecto de esas cabeceras en el veredicto de la librería, de modo que la
Configuración~2 y la librería dentro de la 3b no deben tratarse como la misma medición
(Sección~\ref{sec:met-validez}).
```

Después:

```
y al
enviar los cuatro payloads a la Configuración~2 con esas cabeceras el paquete 0.1.1 los bloqueó en
las tres repeticiones, y sin ellas no bloqueó ninguno. La diferencia queda explicada por el proxy
(el recuento de cabeceras fuera de la lista estándar que lee el extractor pasa de 0 a 4), de modo
que la Configuración~2 y la librería dentro de la 3b no son la misma medición
(Sección~\ref{sec:met-validez}).
```

Fuente: Ídem E1-j.

### 78. E1E2-l: l-discusion.tex, línea original 252, línea actual 255

Ubicación: Cap. 9, Defensa en profundidad (resultados de E1 y E2).

Antes:

```
no se midió por qué la librería
se comporta distinto detrás del proxy, de modo que la Configuración~2 y la librería dentro de la 3b
no son la misma medición. Tres payloads de Command Injection (\texttt{cmdi\_6}, \texttt{cmdi\_184}
y \texttt{cmdi\_185}) no los bloquea ninguna configuración, y su causa no se investigó.
```

Después:

```
las cuatro cabeceras
\texttt{X-*} que agrega el proxy lo explican: al enviar esos payloads a la Configuración~2 con las
cabeceras, la librería los bloqueó en las tres repeticiones, y sin ellas ninguno, porque las
cabeceras elevan de 0 a 4 el recuento de cabeceras fuera de la lista estándar que usa el Random
Forest. La Configuración~2 y la librería dentro de la 3b no son, por tanto, la misma medición, y el
veredicto de la librería depende en parte de las cabeceras que agrega el despliegue. Tres payloads
de Command Injection (\texttt{cmdi\_6}, \texttt{cmdi\_184} y \texttt{cmdi\_185}) no los bloquea
ninguna configuración: el WAF no activa ninguna regla de CRS sobre ellos (puntaje de entrada 0
frente al umbral de 5) y, en la Configuración~2, la clase de mayor probabilidad del Random Forest
es benigna en \texttt{cmdi\_6} y, con las cabeceras del proxy, de ataque con probabilidad 0.3333 en
\texttt{cmdi\_184} y \texttt{cmdi\_185}, a 0.0167 del umbral de 0.35 (a 0.05 en \texttt{cmdi\_185}
sin cabeceras); no se investigó por qué.
```

Fuente: E1: ídem E1-j. E2: docs/evidence/e2-waf-probe-20261025.json y docs/evidence/e2-waf-audit-20261025/audit.log (ninguna regla de CRS sobre cmdi_6, cmdi_184 y cmdi_185 con Host localhost:3000; control cmdi_0 bloqueado por 932235, umbral 5); probabilidades del RF: e1-proxy-headers-20261025.json, campo evento.confidence (probabilidad de la clase de mayor probabilidad; múltiplos de 1/30).

### 79. E1E2-r: n-recomendaciones.tex, línea original 145, línea actual 146

Ubicación: Recomendación 13, acción, justificación y resultado esperado (E1 y E2).

Antes:

```
\textit{Acción:} analizar por qué \texttt{cmdi\_6}, \texttt{cmdi\_184} y \texttt{cmdi\_185} no
    los bloquea ninguna configuración, y por qué otros cuatro payloads de la misma categoría
    (\texttt{cmdi\_112}, \texttt{cmdi\_134}, \texttt{cmdi\_31} y \texttt{cmdi\_38}) solo los bloquea
    la combinación y no la librería sola, comparando el vector de características y la
    probabilidad del Random Forest de cada petición con y sin el proxy. \textit{Justificación:} en
    la medición del 25 de octubre de 2026 esos tres son los únicos payloads que la combinación
    no bloquea, y la causa de ambos hallazgos no se investigó
    (Conclusión~\ref{conc:waf}). \textit{Resultado esperado:} saber si los tres payloads son una
    evasión real de las dos capas y si las cabeceras que agrega el proxy alteran el veredicto de la
    librería.
```

Después:

```
\textit{Acción:} analizar por qué \texttt{cmdi\_6}, \texttt{cmdi\_184} y \texttt{cmdi\_185} no
    los bloquea ninguna configuración, y evaluar si el veredicto de la librería debe depender de
    las cabeceras que agrega la infraestructura, repitiendo las mediciones con y sin ellas.
    \textit{Justificación:} en la medición del 25 de octubre de 2026 esos tres son los únicos
    payloads que la combinación no bloquea (el WAF no activa ninguna regla sobre ellos, y con las
    cabeceras del proxy la probabilidad de la clase de ataque más probable del Random Forest queda
    en 0.3333 o menos), y cuatro payloads de la misma categoría solo se bloquean cuando el proxy
    agrega cuatro cabeceras \texttt{X-*} (Conclusión~\ref{conc:waf}). \textit{Resultado esperado:}
    saber si los tres payloads son una evasión real de las dos capas y cuánto cambia el veredicto
    de la librería según las cabeceras del despliegue.
```

Fuente: Ídem E1E2-l; texto de la recomendación: errata-b §4 y §5.


### Numeración de las recomendaciones (A11)

Simulada leyendo cada `\setcounter{enumi}` y cada `\item` de `n-recomendaciones.tex`:

| N.º | Línea | Título |
|---|---|---|
| 1 | 26 | Instalar primero en modo \texttt{monitor |
| 2 | 34 | Usar la librería como capa complementaria detrás de un WAF. |
| 3 | 42 | Montar el middleware después de todos los analizadores de cuerpo. |
| 4 | 50 | No desplegar la versión actual en rutas de alto volumen de datos. |
| 5 | 62 | Usar el modo \texttt{monitor |
| 6 | 68 | Verificar y, si se confirma, corregir el sesgo de la cabecera |
| 7 | 80 | Proteger al servidor ante saturación. |
| 8 | 88 | Reducir el costo fijo de memoria y CPU. |
| 9 | 97 | Reducir la confusión entre categorías en los eventos registrados. |
| 10 | 110 | Validar la librería en el entorno productivo de una startup guatemalteca. |
| 11 | 118 | Repetir las mediciones con el paquete vigente y con un corpus nuevo. |
| 12 | 134 | Ampliar la explotabilidad confirmada de XSS más allá de un caso. |
| 13 | 145 | Investigar los payloads de Command Injection que la combinación no bloquea. |
| 14 | 157 | Monitorear la memoria en un escenario sostenido de condición única. |
| 15 | 163 | Medir la contribución del Isolation Forest con las pruebas de penetración. |
| 16 | 179 | Publicar los vectores derivados y depurar el conjunto de pruebas extremo a |
| 17 | 190 | Versionar el generador de los conjuntos sintéticos de Command Injection. |
| 18 | 202 | Desacoplar la detección de Node.js y de npm. |
| 19 | 212 | Exponer la librería como servidor del Protocolo de Contexto de Modelo (MCP). |
| 20 | 225 | Definir un conjunto de evaluación externo desde el inicio. |
| 21 | 232 | Medir y tratar los casi-duplicados antes de particionar. |
| 22 | 240 | Bloquear el conjunto de prueba una sola vez y versionar cada medición. |
| 23 | 250 | Construir los corpus de evaluación con un generador versionado y un filtro de |

Resultado: 23 recomendaciones, de 1 a 23, sin saltos ni repeticiones. La etiqueta `rec:cola` corresponde a la recomendación 7.

### Barrido de valores obsoletos (A12)

Búsqueda en todos los `.tex` del directorio (se excluyen las líneas de comentario completas). Se informan los conteos antes y después de las ediciones de la segunda ronda (respaldo tex-before-round2-20261025), las líneas actuales de cada hit y su disposición.

### `68.0`: antes 6, después 6

Líneas actuales: j-metodologia.tex:1102, j-metodologia.tex:1157, k-resultados.tex:931, l-discusion.tex:237, m-conclusiones.tex:105, n-anexos.tex:324

Disposición: Se conserva y se corrige el sentido: es la cifra histórica del ejecutor anterior (136 de 200) que ahora se explica y se contrasta con 82.0 % (Cuadro 38, Secciones 8.4.3 y 7.11, Discusión, Conclusión de defensa en profundidad, Anexo). Las menciones que la presentaban como medición vigente del WAF en Discusión, Conclusiones y Recomendaciones se reescribieron.

### `68,0`: antes 0, después 0

Disposición: Sin hits.

### `136/200`: antes 1, después 1

Líneas actuales: n-anexos.tex:324

Disposición: Cuadro 38 reconstruido (ya no aparece como celda del WAF). El único hit actual es la fila histórica del Anexo, rotulada como ejecutor anterior.

### `65 de 68`: antes 0, después 0

Disposición: Corregido: la fila del Cuadro 40 ahora dice 48 de 51 (3b) y 44 de 51 (Configuración 2).

### `65/68`: antes 0, después 0

Disposición: Sin hits.

### `37/40`: antes 4, después 4

Líneas actuales: k-resultados.tex:332, k-resultados.tex:334, k-resultados.tex:349, k-resultados.tex:366

Disposición: Sin relación: cifras de dvws-node (37 de 40 bloqueados con User-Agent de navegador). No se tocan.

### `64 de`: antes 5, después 5

Líneas actuales: j-metodologia.tex:1103, j-metodologia.tex:1158, j-metodologia.tex:1213, k-resultados.tex:750, m-conclusiones.tex:66

Disposición: Antes: 64 ataques de Command Injection no bloqueados por el WAF (corregido, ahora 36 de Command Injection y 51 en total). Los hits actuales son 164 de 200 (WAF, ejecutor corregido) y los 64 payloads de XSS dirigidos a bio (64 de 64 bloqueados); correctos.

### `n=1`: antes 9, después 9

Líneas actuales: j-metodologia.tex:231, j-metodologia.tex:749, j-metodologia.tex:1108, k-resultados.tex:745, k-resultados.tex:866, k-resultados.tex:1052, l-discusion.tex:210, l-discusion.tex:356, m-conclusiones.tex:71

Disposición: Cada hit restante se refiere a la explotabilidad confirmada por ZAP (correcto) o al hecho histórico de que la Ronda 5 original medía XSS con n=1. Se corrigieron los que decían que la cobertura de XSS tenía n=1.

### `n = 1`: antes 0, después 0

Disposición: Sin hits.

### `una sola alerta`: antes 0, después 0

Disposición: Sin hits (la frase vigente es una sola es de XSS, hecho de ZAP).

### `1/1`: antes 2, después 2

Líneas actuales: k-resultados.tex:866, n-anexos.tex:265

Disposición: Quedan: la fila de ZAP del Cuadro 37 (rotulada n=1, corpus anterior, no comparable) y estratos de n=1 en las tablas del Anexo. Corregidos: el Cuadro 38 y el Cuadro 40.

### `0/1`: antes 0, después 0

Disposición: Corregido: Cuadro 38 (XSS 0/1 pasó a 0/200). La búsqueda descarta los falsos positivos 70/15/15 y 0/105.

### `538`: antes 1, después 1

Líneas actuales: k-resultados.tex:737

Disposición: Se conserva como hecho (alertas de ZAP, n=1), según lo indicado.

### `no permite afirmar`: antes 1, después 1

Líneas actuales: l-discusion.tex:237

Disposición: Corregido en Conclusiones (criterio del 80 % de XSS). El hit restante está en Discusión y se refiere a que el 82.0 % del WAF en Command Injection no permite afirmar que supere el 80 %.

### `payloads clásicos`: antes 0, después 0

Disposición: Corregido (Cuadro 28).

### `no automatizado`: antes 0, después 0

Disposición: Corregido (Cuadro 28).

### `misma imagen`: antes 0, después 0

Disposición: Corregido (Sección 7.1): ahora dice mismo árbol de la aplicación y mismo Dockerfile, porque la imagen local no se verificó por digest en cada arranque (errata E-12).

### `misma aplicación`: antes 1, después 1

Líneas actuales: j-metodologia.tex:503

Disposición: Se conserva (Procedimiento 4.1): ahora es cierto para las cuatro configuraciones, con el mecanismo documentado.

### `feat/waf`: antes 0, después 0

Disposición: Sin hits.

### `par A`: antes 22, después 23

Líneas actuales: j-metodologia.tex:399, j-metodologia.tex:401, j-metodologia.tex:410, j-metodologia.tex:420, j-metodologia.tex:609, j-metodologia.tex:1070, j-metodologia.tex:1071, j-metodologia.tex:1074, j-metodologia.tex:1082, k-resultados.tex:48, k-resultados.tex:49, k-resultados.tex:317, k-resultados.tex:375, k-resultados.tex:723, k-resultados.tex:727, k-resultados.tex:735, k-resultados.tex:763, k-resultados.tex:785, k-resultados.tex:861, k-resultados.tex:950, k-resultados.tex:1020, l-discusion.tex:405, n-anexos.tex:46

Disposición: Se revisó cada hit: son atribuciones históricas del paquete 0.1.0 y del estudio de User-Agent, correctas. Se eliminó la atribución de la Configuración 3b al par A (Cuadro 38 y Procedimiento 4.4) y la de la 3a a una rama distinta; la 3b se atribuye al par C.

### `0.1.0`: antes 47, después 47

Líneas actuales: j-metodologia.tex:254, j-metodologia.tex:388, j-metodologia.tex:400, j-metodologia.tex:409, j-metodologia.tex:414, j-metodologia.tex:418, j-metodologia.tex:421, j-metodologia.tex:425, j-metodologia.tex:426, j-metodologia.tex:609, j-metodologia.tex:671, j-metodologia.tex:1069, j-metodologia.tex:1078, j-metodologia.tex:1095, j-metodologia.tex:1099, k-resultados.tex:46, k-resultados.tex:72, k-resultados.tex:83, k-resultados.tex:94, k-resultados.tex:104, k-resultados.tex:316, k-resultados.tex:595, k-resultados.tex:723, k-resultados.tex:763, k-resultados.tex:785, k-resultados.tex:794, k-resultados.tex:810, k-resultados.tex:861, k-resultados.tex:883, k-resultados.tex:991, k-resultados.tex:1048, l-discusion.tex:55, l-discusion.tex:61, l-discusion.tex:66, l-discusion.tex:81, l-discusion.tex:90, l-discusion.tex:183, l-discusion.tex:189, l-discusion.tex:198, l-discusion.tex:405, l-discusion.tex:410, m-conclusiones.tex:23, m-conclusiones.tex:31, m-conclusiones.tex:57, n-anexos.tex:46, n-anexos.tex:58, n-recomendaciones.tex:120

Disposición: Se revisó cada hit: nombre del paquete publicado el 30 de agosto de 2026 y mediciones rotuladas como 0.1.0 (Cuadro 37, resumen de indicadores, Discusión). Ninguna cifra de 0.1.0 se compara ya con la Configuración 3a.

### `170/200`: antes 1, después 1

Líneas actuales: k-resultados.tex:863

Disposición: Cuadro 37 (columna 0.1.0, rotulada). Eliminado del Cuadro 38.

### `183/200`: antes 1, después 1

Líneas actuales: k-resultados.tex:864

Disposición: Cuadro 37 (columna 0.1.0, rotulada). Eliminado del Cuadro 38.



## Tercera ronda (ediciones 80 a 90)

Ediciones de la tercera ronda, con respaldo previo en `docs/evidence/tex-before-round3-20261025/` (sumas en `SHA256SUMS.txt`). Las líneas originales se miden sobre ese respaldo y las nuevas sobre los archivos actuales. Resultados de la recalculación de A1, de la sensibilidad S1 y de las comprobaciones en `docs/thesis-delta-errata-20261025-c.md`.

| Archivo | Ediciones |
|---|---|
| b-resumen.tex | 1 |
| j-metodologia.tex | 2 |
| k-resultados.tex | 3 |
| l-discusion.tex | 1 |
| m-conclusiones.tex | 2 |
| n-anexos.tex | 1 |
| n-recomendaciones.tex | 1 |
| **Total** | **11** |

### 80. T-A1-k: k-resultados.tex, línea original 950, línea actual 950

Ubicación: Sec 8.4.3, aporte de la combinación descompuesto.

Antes:

```
Frente a la librería sola, la combinación bloqueó 13 payloads más (1 de SQLi y 12 de
Command Injection), y frente al WAF solo, 48 más.
```

Después:

```
Frente a la librería sola, la combinación bloqueó 13 payloads más (1 de SQLi y 12 de
Command Injection), de los que 9 los bloquea el WAF y 4 los bloquea la librería por las cabeceras
que agrega el proxy; frente al WAF solo bloqueó 48 más, de los que 4 se deben a esas cabeceras. Esta
descomposición parte de la Configuración~2 sin esas cabeceras: con ellas, la librería sola bloquea
794 de 800 y el WAF suma 3 (Sección~\ref{anx:sensibilidad}).
```

Fuente: attack-sim/results_combined_config{2,3a,3b}_run1_20261025.json, recalculado en la tercera ronda: unión Config 2 o 3a = 793; 3b menos Config 2 = 13 (sqli 1, cmdi 12); unión menos Config 2 = 9 (sqli_75 y ocho de cmdi); 3b menos unión = 4 (cmdi_112, cmdi_134, cmdi_31, cmdi_38); 3b menos 3a = 48. Condición con cabeceras: docs/evidence/s1-analisis-20261025.json (794 de 800; 3b menos Config 2 con cabeceras = 3).

### 81. T-A1-l: l-discusion.tex, línea original 248, línea actual 248

Ubicación: Cap. 9, Defensa en profundidad, aporte de la combinación descompuesto.

Antes:

```
la
combinación agrega 13 payloads a la librería (1 de SQL Injection y 12 de Command Injection) y 48
al WAF.
```

Después:

```
la
combinación bloqueó 13 payloads más que la librería sola (1 de SQL Injection y 12 de Command
Injection), de los que 9 los bloquea el WAF y 4 los bloquea la librería por las cabeceras que agrega
el proxy, y 48 más que el WAF solo, de los que 4 se deben a esas cabeceras. Esta descomposición
parte de la Configuración~2 sin las cabeceras del proxy; con ellas, la librería sola bloquea 794 de
800 y el WAF agrega 3 (Sección~\ref{anx:sensibilidad}).
```

Fuente: Ídem T-A1-k.

### 82. T-A1-c: m-conclusiones.tex, línea original 108, línea actual 108

Ubicación: Conclusión conc:waf, aporte de la combinación descompuesto.

Antes:

```
la combinación agrega 13 payloads a la librería y 48 al WAF, en Path Traversal y en XSS la
    librería sola iguala a la combinación,
```

Después:

```
la combinación bloqueó 13 payloads más que la librería sola, de los que 9 los bloquea el WAF y 4
    la librería por las cabeceras del proxy, y 48 más que el WAF solo, de los que 4 se deben a esas
    cabeceras (descomposición medida con la Configuración~2 sin ellas; Sección~\ref{anx:sensibilidad}); en
    Path Traversal y en XSS la librería sola iguala a la combinación,
```

Fuente: Ídem T-A1-k.

### 83. T-A1-r: n-recomendaciones.tex, línea original 40, línea actual 40

Ubicación: Recomendación 2, resultado esperado.

Antes:

```
de cada capa por separado (797 de 800 payloads frente a 784 y 749).
```

Después:

```
de cada capa por separado (797 de 800 payloads frente a 784 y 749); la combinación suma 13
    payloads a la librería sola, 9 por el WAF y 4 por las cabeceras que agrega el proxy.
```

Fuente: Ídem T-A1-k.

### 84. T-A1-c40: k-resultados.tex, línea original 1061, línea actual 1067

Ubicación: Cuadro 40, fila de defensa en profundidad.

Antes:

```
La 3b bloqueó 48 de los 51 ataques no bloqueados por el WAF; la Configuración~2, 44 de 51 & --- \\ \hline
```

Después:

```
La 3b bloqueó 48 de los 51 ataques no bloqueados por el WAF y la Configuración~2, 44; frente a la Configuración~2, la 3b bloqueó 13 más (9 por el WAF y 4 por las cabeceras del proxy) & --- \\ \hline
```

Fuente: Ídem T-A1-k.

### 85. T-A2: b-resumen.tex, línea original 7, línea actual 7

Ubicación: Resumen, enumeración de coberturas (sobraba una "y").

Antes:

```
100.0~\% en Path Traversal y 92.5~\% en inyección de comandos y 100.0~\% en Cross-Site Scripting
```

Después:

```
100.0~\% en Path Traversal, 92.5~\% en inyección de comandos y 100.0~\% en Cross-Site Scripting
```

Fuente: b-resumen.tex antes de la edición (doble "y" introducida en la edición A2 de la segunda ronda). El Abstract se revisó y no tiene el defecto.

### 86. T-A3-j: j-metodologia.tex, línea original 1164, línea actual 1169

Ubicación: Sec 7.11, viñeta "Comparación con el WAF no neutral".

Antes:

```
El corpus se construyó a partir de familias
    de payload que también están representadas en el entrenamiento de la librería, mientras que el
    WAF es un conjunto de reglas genérico en nivel de paranoia 1; la comparación entre ambos no es
    neutral
```

Después:

```
La librería se entrenó con payloads de las
    mismas cuatro clases de ataque que el corpus de evaluación (el corpus excluye coincidencias
    exactas, pero no se midió la distancia entre ambas distribuciones), mientras que el WAF es un
    conjunto de reglas genérico en nivel de paranoia 1 que no se calibró con ellos; la comparación
    entre ambos no es neutral
```

Fuente: Clases del Random Forest: node_modules/logsguardian/models/parity_report.json (rf_classes: benign, cmdi, path_traversal, sqli, xss); exclusión de coincidencias exactas y auditoría de subcadena: attack-sim/leakage_report_round5_all_20261025.json; configuración del WAF: docs/thesis-delta-configs.md §2 (paranoia 1, sin exclusiones). La distancia entre distribuciones no se midió (no hay archivo).

### 87. T-A3-c: m-conclusiones.tex, línea original 111, línea actual 113

Ubicación: Conclusión conc:waf, limitación de la comparación.

Antes:

```
con la limitación de que el corpus se construyó
    a partir de familias de payload representadas en el entrenamiento de la librería y de que no se
    midieron otros niveles de paranoia del WAF, por lo que la comparación no es neutral
```

Después:

```
con la limitación de que la librería se entrenó
    con payloads de las mismas cuatro clases de ataque que el corpus de evaluación (que excluye
    coincidencias exactas, pero cuya distancia respecto del entrenamiento no se midió), mientras que
    el WAF no se calibró con ellos y no se midieron otros niveles de paranoia, por lo que la
    comparación no es neutral
```

Fuente: Ídem T-A3-j.

### 88. T-A4-j: j-metodologia.tex, línea original 1152, línea actual 1152

Ubicación: Sec 7.11, viñeta de la librería frente al proxy: condición de la Config 2 y resultado de S1.

Antes:

```
La diferencia queda
    explicada por el proxy: la Configuración~2 y la librería dentro de la 3b no son la misma
    medición, y el veredicto de la librería depende en parte de las cabeceras que agrega el
    despliegue.
```

Después:

```
La diferencia queda
    explicada por el proxy: la Configuración~2 y la librería dentro de la 3b no son la misma
    medición, y el veredicto de la librería depende en parte de las cabeceras que agrega el
    despliegue. La Configuración~2 se midió sin esas cuatro cabeceras, de modo que sus cifras
    describen un despliegue sin proxy. Una corrida de sensibilidad de las 800 peticiones con las
    cuatro cabeceras dio 794 de 800 bloqueadas (784 sin ellas): 12 payloads pasan a bloquearse
    (SQLi 1, Command Injection 11) y 2 dejan de bloquearse (órdenes con \texttt{sleep} que llegan a
    la aplicación y terminan por tiempo de espera), sin cambios en Path Traversal ni en XSS
    (Sección~\ref{anx:sensibilidad}).
```

Fuente: docs/evidence/s1-analisis-20261025.json (por_categoria, a_bloqueado, a_no_bloqueado, status_de_los_que_cambian: cmdi_51 y cmdi_94 terminan en error por tiempo de espera); attack-sim/results_s1_config2_{sin,con}_cabeceras_run1_20261025.json; attack-sim/s1_config2_proxy_headers_20261025.py.

### 89. T-A4-k: k-resultados.tex, línea original 990, línea actual 993

Ubicación: Cuadro 38, nota: condición de la Config 2 y resultado de S1.

Antes:

```
Las mediciones anteriores
de la Configuración~2 con el paquete 0.1.0 (Cuadro~\ref{tab:res-cobertura}) no se incluyen ni se
comparan con la Configuración~3a.}
```

Después:

```
Las mediciones anteriores
de la Configuración~2 con el paquete 0.1.0 (Cuadro~\ref{tab:res-cobertura}) no se incluyen ni se
comparan con la Configuración~3a. La Configuración~2 se midió sin las cuatro cabeceras
\texttt{X-*} que agrega el proxy, por lo que sus cifras describen un despliegue sin proxy; con esas
cabeceras, una corrida de sensibilidad dio 794 de 800 (SQLi 200, Path Traversal 200, Command
Injection 194 y XSS 200), y las cifras de este cuadro no cambian (Sección~\ref{anx:sensibilidad}).}
```

Fuente: Ídem T-A4-j.

### 90. T-A4-anexo: n-anexos.tex, línea original 387, línea actual 387

Ubicación: Anexo 13.8: sensibilidad de la Configuración 2 a las cabeceras del proxy (nueva sección y cuadro).

Antes:

```
\ifdefined\modoensamble
\else
	\section*{Referencias}
```

Después:

```
\section{Sensibilidad de la Configuración 2 a las cabeceras del proxy}
\label{anx:sensibilidad}

El Cuadro~\ref{tab:anx-sensibilidad} compara la Configuración~2 con el paquete 0.1.1 en dos
condiciones, ambas sobre el corpus combinado de 800 peticiones y con el ejecutor corregido: sin
cabeceras extra (corrida 1 de la medición unificada) y con las cuatro cabeceras
\texttt{X-Real-IP}, \texttt{X-Forwarded-For}, \texttt{X-Forwarded-Port} y
\texttt{X-Forwarded-Proto} que agrega el proxy, con los valores de la captura de la Fase 2b
(192.168.65.1, 192.168.65.1, 8080 y http). Es una sensibilidad: las cifras principales del
Capítulo~\ref{cap:resultados} no cambian. La condición sin cabeceras se repitió en el mismo
contenedor y reprodujo la corrida 1 sin diferencias en ningún payload.

\begin{table}[H]
\centering
\small
\begin{tabular}{|L{2.7cm}|L{3.7cm}|L{3.7cm}|L{1.6cm}|L{1.6cm}|}
\hline
\textbf{Categoría} & \textbf{Sin cabeceras: bloqueados e IC 95~\%} & \textbf{Con cuatro cabeceras: bloqueados e IC 95~\%} & \textbf{A bloqueado} & \textbf{A no bloqueado} \\ \hline
SQLi & 199/200 (99.5~\%) [97.2--99.9] & 200/200 (100.0~\%) [98.1--100.0] & 1 & 0 \\ \hline
Path Traversal & 200/200 (100.0~\%) [98.1--100.0] & 200/200 (100.0~\%) [98.1--100.0] & 0 & 0 \\ \hline
Command Injection & 185/200 (92.5~\%) [88.0--95.4] & 194/200 (97.0~\%) [93.6--98.6] & 11 & 2 \\ \hline
XSS & 200/200 (100.0~\%) [98.1--100.0] & 200/200 (100.0~\%) [98.1--100.0] & 0 & 0 \\ \hline
\textbf{Total} & 784/800 (98.0~\%) [96.8--98.8] & 794/800 (99.2~\%) [98.4--99.7] & 12 & 2 \\ \hline
\end{tabular}
\caption[Sensibilidad de la Configuración 2 a las cabeceras del proxy]{Sensibilidad de la Configuración 2 (paquete 0.1.1) a las cuatro cabeceras que agrega el proxy, sobre 800 peticiones}
\label{tab:anx-sensibilidad}
\end{table}
{\footnotesize Nota. Elaboración propia con datos de
\texttt{attack-sim/results\_combined\_config2\_run1\_20261025.json} (sin cabeceras) y de
\texttt{attack-sim/results\_s1\_config2\_con\_cabeceras\_run1\_20261025.json} (con cabeceras); cálculo
en \texttt{docs/evidence/s1-analisis-20261025.py}. Una corrida por condición. Pasan a bloqueado: \texttt{cmdi\_112}, \texttt{cmdi\_120}, \texttt{cmdi\_134}, \texttt{cmdi\_155}, \texttt{cmdi\_28}, \texttt{cmdi\_31}, \texttt{cmdi\_36}, \texttt{cmdi\_38}, \texttt{cmdi\_40}, \texttt{cmdi\_66}, \texttt{cmdi\_7}, \texttt{sqli\_75}. Dejan de bloquearse: \texttt{cmdi\_51}, \texttt{cmdi\_94}, órdenes con \texttt{sleep} que llegan a la aplicación y terminan por tiempo de
espera, lo que se cuenta como no detectado. Prueba exacta de McNemar sobre los 14 payloads
discordantes (12 frente a 2): $p = 0.013$. De los 13 payloads que la Configuración~3b bloquea y la
Configuración~2 sin cabeceras no, la Configuración~2 con cabeceras bloquea 12 (todos salvo
\texttt{cmdi\_9}); la unión de la Configuración~2 con cabeceras y la 3a es de 797 payloads, igual que
la 3b, y el WAF suma 3 (\texttt{cmdi\_9}, \texttt{cmdi\_51} y \texttt{cmdi\_94}) a la librería con
cabeceras. La imagen local de la aplicación de esta sensibilidad (\texttt{sha256:d9b12672f000...}) se
reconstruyó porque cambió el contexto de build; el paquete 0.1.1 y los modelos se verificaron por
hash dentro del contenedor.}

\ifdefined\modoensamble
\else
	\section*{Referencias}
```

Fuente: Ídem T-A4-j; McNemar exacto bilateral p = 0.01294 (12 frente a 2); imagen local sha256:d9b12672f0007fd4f38672b3141a95b59935a6df99b2d56bff4f425ecd37bf85 (docker image inspect); hashes de paquete y modelos verificados dentro del contenedor.



## Cuarta ronda (ediciones 91 a 108)

Ediciones de la cuarta ronda, con respaldo previo en `docs/evidence/tex-before-round4-20261025/` (sumas en `SHA256SUMS.txt`). Las líneas originales se miden sobre ese respaldo y las nuevas sobre los archivos actuales. Resultados de A1 y A2 y correcciones en `docs/thesis-delta-errata-20261025-d.md`. Las ediciones con sufijo "corr" afinan texto de esta misma ronda y no tienen línea original.

| Archivo | Ediciones |
|---|---|
| b-resumen.tex | 1 |
| c-abstract.tex | 1 |
| j-metodologia.tex | 1 |
| k-resultados.tex | 4 |
| l-discusion.tex | 4 |
| m-conclusiones.tex | 1 |
| n-anexos.tex | 3 |
| n-recomendaciones.tex | 3 |
| **Total** | **18** |

### 91. Q-B3-k: k-resultados.tex, línea original 950, línea actual 950

Ubicación: Sec 8.4.3, descomposición 13 = 10 + 3 en lugar de 9 + 4.

Antes:

```
Frente a la librería sola, la combinación bloqueó 13 payloads más (1 de SQLi y 12 de
Command Injection), de los que 9 los bloquea el WAF y 4 los bloquea la librería por las cabeceras
que agrega el proxy; frente al WAF solo bloqueó 48 más, de los que 4 se deben a esas cabeceras. Esta
descomposición parte de la Configuración~2 sin esas cabeceras: con ellas, la librería sola bloquea
794 de 800 y el WAF suma 3 (Sección~\ref{anx:sensibilidad}). La complementariedad es asimétrica: en Path
Traversal y en XSS la librería sola bloquea todo lo que bloquea la combinación y el WAF no agrega
nada, mientras que en SQLi y en Command Injection cada capa bloquea payloads que la otra no.
```

Después:

```
Frente a la Configuración~2 sin las cabeceras del proxy, la combinación bloqueó 13 payloads
más (1 de SQLi y 12 de Command Injection), pero esa diferencia mezcla dos condiciones: la librería
dentro de la 3b recibe las cabeceras que agrega el proxy y la Configuración~2 no. La descomposición
es 13 = 10 + 3: las cabeceras elevan en 10 los payloads que bloquea la librería sola (794 de 800
en la Configuración~2 con cabeceras, frente a 784), y en condiciones equiparadas el WAF suma 3 de
800 payloads a la librería (\texttt{cmdi\_9}, \texttt{cmdi\_51} y \texttt{cmdi\_94}, de Command
Injection y bloqueados por la 3a). La librería suma 48 payloads sobre el WAF solo
(Sección~\ref{anx:sensibilidad}). La complementariedad es asimétrica: en Path Traversal, SQLi y XSS
la librería sola, con cabeceras, bloquea todo lo que bloquea la combinación y el WAF no agrega
nada, y solo en Command Injection cada capa bloquea payloads que la otra no (3 el WAF y 33 la
librería).
```

Fuente: docs/evidence/r4-analisis-20261025.json (A2.b_descomposicion: 3b menos Config 2 sin cabeceras = 13, efecto neto de cabeceras = 10, aporte del WAF en condiciones equiparadas = 3: cmdi_9, cmdi_51, cmdi_94; A2.c_cambios_por_cabeceras: 4 netos entre los 51 que el WAF no bloquea, 6 netos entre los que sí bloquea; A2.d: 51 de 51 coinciden con la 3b en las tres corridas); docs/evidence/s1-analisis-20261025.json. 3b menos 3a = 48 y 33 de Command Injection: errata-c §1.

### 92. Q-B2-k: k-resultados.tex, línea original 995, línea actual 999

Ubicación: Cuadro 38, nota: condiciones equiparadas y aporte del WAF.

Antes:

```
La Configuración~2 se midió sin las cuatro cabeceras
\texttt{X-*} que agrega el proxy, por lo que sus cifras describen un despliegue sin proxy; con esas
cabeceras, una corrida de sensibilidad dio 794 de 800 (SQLi 200, Path Traversal 200, Command
Injection 194 y XSS 200), y las cifras de este cuadro no cambian (Sección~\ref{anx:sensibilidad}).}
```

Después:

```
La Configuración~2 de este cuadro se midió sin las
cuatro cabeceras \texttt{X-*} que agrega el proxy, por lo que sus cifras describen un despliegue
directo, sin proxy. Con esas cabeceras, en tres corridas, dio 794 de 800 (SQLi 200, Path Traversal
200, Command Injection 194 y XSS 200), y en condiciones equiparadas (Configuración~2 con cabeceras)
el aporte del WAF sobre la librería es de 3 payloads. Las cifras de este cuadro no cambian
(Sección~\ref{anx:sensibilidad}).}
```

Fuente: docs/evidence/r4-analisis-20261025.json (A2.b_descomposicion: 3b menos Config 2 sin cabeceras = 13, efecto neto de cabeceras = 10, aporte del WAF en condiciones equiparadas = 3: cmdi_9, cmdi_51, cmdi_94; A2.c_cambios_por_cabeceras: 4 netos entre los 51 que el WAF no bloquea, 6 netos entre los que sí bloquea; A2.d: 51 de 51 coinciden con la 3b en las tres corridas); docs/evidence/s1-analisis-20261025.json.

### 93. Q-B3-c40: k-resultados.tex, línea original 1067, línea actual 1073

Ubicación: Cuadro 40, fila de defensa en profundidad.

Antes:

```
La 3b bloqueó 48 de los 51 ataques no bloqueados por el WAF y la Configuración~2, 44; frente a la Configuración~2, la 3b bloqueó 13 más (9 por el WAF y 4 por las cabeceras del proxy) & --- \\ \hline
```

Después:

```
La 3b bloqueó 48 de los 51 ataques no bloqueados por el WAF; la Configuración~2, 44 sin las cabeceras del proxy y 48 con ellas. En condiciones equiparadas el WAF suma 3 de 800 payloads a la librería (13 = 10 por las cabeceras + 3 por el WAF) & --- \\ \hline
```

Fuente: docs/evidence/r4-analisis-20261025.json (A2.b_descomposicion: 3b menos Config 2 sin cabeceras = 13, efecto neto de cabeceras = 10, aporte del WAF en condiciones equiparadas = 3: cmdi_9, cmdi_51, cmdi_94; A2.c_cambios_por_cabeceras: 4 netos entre los 51 que el WAF no bloquea, 6 netos entre los que sí bloquea; A2.d: 51 de 51 coinciden con la 3b en las tres corridas); docs/evidence/s1-analisis-20261025.json.

### 94. Q-B3-l: l-discusion.tex, línea original 248, línea actual 248

Ubicación: Cap. 9, Defensa en profundidad, descomposición 13 = 10 + 3.

Antes:

```
la
combinación bloqueó 13 payloads más que la librería sola (1 de SQL Injection y 12 de Command
Injection), de los que 9 los bloquea el WAF y 4 los bloquea la librería por las cabeceras que agrega
el proxy, y 48 más que el WAF solo, de los que 4 se deben a esas cabeceras. Esta descomposición
parte de la Configuración~2 sin las cabeceras del proxy; con ellas, la librería sola bloquea 794 de
800 y el WAF agrega 3 (Sección~\ref{anx:sensibilidad}). De los 51 ataques que el WAF no bloqueó, la combinación bloqueó 48 y la librería sola 44. La
complementariedad es asimétrica: en Path Traversal y en XSS la librería sola bloquea todo lo que
bloquea la combinación, y solo en SQL Injection y en Command Injection cada capa detiene payloads
que la otra deja pasar.
```

Después:

```
la
combinación bloqueó 13 payloads más que la librería sola sin las cabeceras del proxy, pero esa
comparación mezcla condiciones, porque la librería dentro de la 3b las recibe. La descomposición es
13 = 10 + 3: las cabeceras elevan en 10 los payloads que bloquea la librería sola (794 de 800 con
cabeceras, frente a 784) y, en condiciones equiparadas, el WAF suma 3 de 800 payloads a la
librería, todos de Command Injection, mientras que la librería suma 48 al WAF solo
(Sección~\ref{anx:sensibilidad}). De los 51 ataques que el WAF no bloqueó, la combinación bloqueó
48, igual que la librería con cabeceras (44 sin ellas). La complementariedad es asimétrica: en Path
Traversal, SQL Injection y XSS la librería sola, con cabeceras, bloquea todo lo que bloquea la
combinación, y solo en Command Injection cada capa detiene payloads que la otra deja pasar.
```

Fuente: docs/evidence/r4-analisis-20261025.json (A2.b_descomposicion: 3b menos Config 2 sin cabeceras = 13, efecto neto de cabeceras = 10, aporte del WAF en condiciones equiparadas = 3: cmdi_9, cmdi_51, cmdi_94; A2.c_cambios_por_cabeceras: 4 netos entre los 51 que el WAF no bloquea, 6 netos entre los que sí bloquea; A2.d: 51 de 51 coinciden con la 3b en las tres corridas); docs/evidence/s1-analisis-20261025.json.

### 95. Q-B4-l: l-discusion.tex, línea original 269, línea actual 270

Ubicación: Cap. 9, Defensa en profundidad, reencuadre de la ganancia del WAF.

Antes:

```
no se investigó por qué. Las Rondas 1 a 3 aportaron
```

Después:

```
no se investigó por qué. En condiciones equiparadas, la ganancia de cobertura de añadir el WAF a
la librería en la Ronda~5 es de 3 de 800 payloads, de modo que la recomendación de desplegar la
librería detrás de un WAF no descansa en esa ganancia, sino en la Ronda~4 (la librería bloqueó 37 de
los 40 ataques que el WAF dejó pasar), en los bloqueos indebidos y la falta de calibración de la
librería, y en que el corpus favorece a la librería por construcción. Las Rondas 1 a 3 aportaron
```

Fuente: Ronda 4: texto vigente de la Sección 8.4.3 (37 de 40); 3 de 800: docs/evidence/r4-analisis-20261025.json (A2.b_descomposicion: 3b menos Config 2 sin cabeceras = 13, efecto neto de cabeceras = 10, aporte del WAF en condiciones equiparadas = 3: cmdi_9, cmdi_51, cmdi_94; A2.c_cambios_por_cabeceras: 4 netos entre los 51 que el WAF no bloquea, 6 netos entre los que sí bloquea; A2.d: 51 de 51 coinciden con la 3b en las tres corridas); docs/evidence/s1-analisis-20261025.json. Sesgo del corpus y paranoia: Sección 7.11 (viñeta de la comparación no neutral).

### 96. Q-B3-l2: l-discusion.tex, línea original 291, línea actual 296

Ubicación: Cap. 9, Contraste con el Marco Teórico: respaldo de la capa complementaria.

Antes:

```
la librería, que analiza la petición dentro del proceso, y el WAF perimetral detectan
conjuntos parcialmente distintos (Sección~\ref{sec:dis-defensa}).
```

Después:

```
en la Ronda~4, la librería, que analiza la petición dentro del proceso, y el WAF perimetral
detectan conjuntos parcialmente distintos; en la Ronda~5, en condiciones equiparadas, el WAF agrega
solo 3 de 800 payloads a la librería, de modo que el respaldo es el de la Ronda~4
(Sección~\ref{sec:dis-defensa}).
```

Fuente: docs/evidence/r4-analisis-20261025.json (A2.b_descomposicion: 3b menos Config 2 sin cabeceras = 13, efecto neto de cabeceras = 10, aporte del WAF en condiciones equiparadas = 3: cmdi_9, cmdi_51, cmdi_94; A2.c_cambios_por_cabeceras: 4 netos entre los 51 que el WAF no bloquea, 6 netos entre los que sí bloquea; A2.d: 51 de 51 coinciden con la 3b en las tres corridas); docs/evidence/s1-analisis-20261025.json.

### 97. Q-B7-l: l-discusion.tex, línea original 341, línea actual 348

Ubicación: Cap. 9, Condiciones de despliegue: artefacto de cabeceras (nuevo párrafo).

Antes:

```
calibración, sin cambiar la arquitectura, y define la configuración recomendada para la población
objetivo: instalación en modo \texttt{monitor} y calibración del umbral con el tráfico propio antes
de activar el bloqueo.
```

Después:

```
calibración, sin cambiar la arquitectura, y define la configuración recomendada para la población
objetivo: instalación en modo \texttt{monitor} y calibración del umbral con el tráfico propio antes
de activar el bloqueo.

\textbf{Cabeceras que agrega el despliegue.} El Random Forest se compone de 30 árboles y, en los
casos límite medidos, sus probabilidades son múltiplos de 1/30 (0.3333 y 0.3667); como el umbral de
0.35 cae entre 10 y 11 árboles, en esos casos un solo árbol, movido por el recuento de cabeceras
fuera de la lista estándar (\texttt{unusual\_headers\_count}), decide el bloqueo
(Sección~\ref{anx:sensibilidad}). Es un artefacto de despliegue análogo al sesgo de la cabecera
\texttt{User-Agent}, y no se midió la importancia de esa característica en el modelo.
```

Fuente: n_estimators = 30: training/retrain_v11_contract69.py:51 y training/evaluate_test.py:384 (repositorio logSguarDian); valores 0.3333 y 0.3667 de docs/evidence/e1-proxy-headers-20261025.json; umbral 0.35: node_modules/logsguardian/dist/middleware.js (RF_THRESHOLD); unusual_headers_count: docs/evidence/e1-extractor-caracteristicas-20261025.json. La generalización "todas las probabilidades son múltiplos de 1/30" no se usó: hay contraejemplos (errata-d F-09).

### 98. Q-B4-c: m-conclusiones.tex, línea original 106, línea actual 106

Ubicación: Conclusión conc:waf, descomposición 13 = 10 + 3 y reencuadre.

Antes:

```
De los 51 ataques que el WAF
    no bloqueó, ambas capas bloquearon 48 y la librería sola 44. La complementariedad es asimétrica:
    la combinación bloqueó 13 payloads más que la librería sola, de los que 9 los bloquea el WAF y 4
    la librería por las cabeceras del proxy, y 48 más que el WAF solo, de los que 4 se deben a esas
    cabeceras (descomposición medida con la Configuración~2 sin ellas; Sección~\ref{anx:sensibilidad}); en
    Path Traversal y en XSS la librería sola iguala a la combinación, y solo en SQL Injection y en Command Injection cada capa
    bloquea payloads que la otra no. La evidencia respalda el uso de la librería como capa
    complementaria a un WAF y no como su sustituto, con la limitación de que la librería se entrenó
    con payloads de las mismas cuatro clases de ataque que el corpus de evaluación (que excluye
    coincidencias exactas, pero cuya distancia respecto del entrenamiento no se midió), mientras que
    el WAF no se calibró con ellos y no se midieron otros niveles de paranoia, por lo que la
    comparación no es neutral
    (Sección~\ref{sec:met-validez}).
```

Después:

```
De los 51 ataques que el WAF
    no bloqueó, ambas capas bloquearon 48 y la librería sola, 44 sin las cabeceras del proxy y 48 con
    ellas. La combinación bloqueó 13 payloads más que la librería sola sin esas cabeceras, una
    comparación que mezcla condiciones: 13 = 10 (efecto de las cabeceras que agrega el proxy, que
    elevan la librería sola a 794 de 800) + 3 (aporte del WAF en condiciones equiparadas, todos de
    Command Injection), y la librería suma 48 al WAF solo (Sección~\ref{anx:sensibilidad}). La
    complementariedad es asimétrica: en Path Traversal, SQL Injection y XSS la librería sola, con
    cabeceras, iguala a la combinación, y solo en Command Injection cada capa bloquea payloads que la
    otra no. En condiciones equiparadas, la ganancia de cobertura de añadir el WAF a la librería en
    la Ronda~5 es de 3 de 800 payloads, de modo que la recomendación de usar la librería como capa
    complementaria a un WAF y no como su sustituto no descansa en esa ganancia, sino en la Ronda~4
    (37 de 40), en los bloqueos indebidos y la falta de calibración de la librería
    (conclusión~\ref{conc:fp}) y en que el corpus favorece a la librería por construcción: la
    librería se entrenó con payloads de las mismas cuatro clases de ataque que el corpus de
    evaluación (que excluye coincidencias exactas, pero cuya distancia respecto del entrenamiento no
    se midió), mientras que el WAF no se calibró con ellos y no se midieron otros niveles de
    paranoia, por lo que la comparación no es neutral (Sección~\ref{sec:met-validez}).
```

Fuente: docs/evidence/r4-analisis-20261025.json (A2.b_descomposicion: 3b menos Config 2 sin cabeceras = 13, efecto neto de cabeceras = 10, aporte del WAF en condiciones equiparadas = 3: cmdi_9, cmdi_51, cmdi_94; A2.c_cambios_por_cabeceras: 4 netos entre los 51 que el WAF no bloquea, 6 netos entre los que sí bloquea; A2.d: 51 de 51 coinciden con la 3b en las tres corridas); docs/evidence/s1-analisis-20261025.json. Ronda 4 (37 de 40): texto vigente de la Conclusión 8.

### 99. Q-B4-r: n-recomendaciones.tex, línea original 36, línea actual 36

Ubicación: Recomendación 2, justificación y resultado esperado.

Antes:

```
bloqueó 37 de los 40 ataques que ModSecurity con OWASP CRS dejó pasar en la Ronda~4, y en la
    Ronda~5 la combinación bloqueó 48 de los 51 ataques que el WAF solo no bloqueó, frente a 44 de la
    librería sola; en Command Injection el WAF solo bloqueó el 82.0~\% frente al 92.5~\% de la
    librería (Conclusión~\ref{conc:waf}). \textit{Resultado esperado:} mayor cobertura agregada que la
    de cada capa por separado (797 de 800 payloads frente a 784 y 749); la combinación suma 13
    payloads a la librería sola, 9 por el WAF y 4 por las cabeceras que agrega el proxy.
```

Después:

```
bloqueó 37 de los 40 ataques que ModSecurity con OWASP CRS dejó pasar en la Ronda~4. En la
    Ronda~5, en condiciones equiparadas, el WAF suma solo 3 de 800 payloads a la librería, de modo
    que esta recomendación no descansa en esa ganancia de cobertura, sino en la Ronda~4, en los
    bloqueos indebidos y la falta de calibración de la librería
    (Conclusión~\ref{conc:fp}) y en que el corpus favorece a la librería por construcción
    (Conclusión~\ref{conc:waf}). \textit{Resultado esperado:} cobertura agregada no inferior a la de
    cada capa por separado (797 de 800 payloads con ambas capas, frente a 794 de la librería con las
    cabeceras del proxy y 749 del WAF solo).
```

Fuente: docs/evidence/r4-analisis-20261025.json (A2.b_descomposicion: 3b menos Config 2 sin cabeceras = 13, efecto neto de cabeceras = 10, aporte del WAF en condiciones equiparadas = 3: cmdi_9, cmdi_51, cmdi_94; A2.c_cambios_por_cabeceras: 4 netos entre los 51 que el WAF no bloquea, 6 netos entre los que sí bloquea; A2.d: 51 de 51 coinciden con la 3b en las tres corridas); docs/evidence/s1-analisis-20261025.json. Ronda 4: texto vigente de la Recomendación 2.

### 100. Q-B8-r-a: n-recomendaciones.tex, línea original 69, línea actual 71

Ubicación: Recomendación 6, acción.

Antes:

```
\item \textbf{Verificar y, si se confirma, corregir el sesgo de la cabecera
    \texttt{User-Agent}.} \textit{Acción:} reunir tráfico legítimo de navegadores y clientes HTTP
    diversos (incluidos cURL y los \texttt{User-Agent} por defecto de Node.js), evaluarlo con la
    configuración vigente, recalibrar el umbral de bloqueo con tráfico de varias aplicaciones y
    repetir las mediciones del Cuadro~\ref{tab:res-terceros-ua}.
```

Después:

```
\item \textbf{Verificar y, si se confirma, corregir el sesgo de la cabecera
    \texttt{User-Agent} y del recuento de cabeceras no estándar.} \textit{Acción:} reunir tráfico
    legítimo de navegadores y clientes HTTP diversos (incluidos cURL y los \texttt{User-Agent} por
    defecto de Node.js), evaluarlo con la configuración vigente, recalibrar el umbral de bloqueo con
    tráfico de varias aplicaciones, repetir las mediciones del Cuadro~\ref{tab:res-terceros-ua} y
    repetir la evaluación con la librería detrás de un proxy inverso, con y sin las cabeceras que este
    agrega.
```

Fuente: Pedido del autor (B8); no se añadió una recomendación (siguen 23).

### 101. Q-B8-r-b: n-recomendaciones.tex, línea original 77, línea actual 81

Ubicación: Recomendación 6, justificación y resultado esperado.

Antes:

```
la hipótesis
    no se verificó con un corpus legítimo alternativo. \textit{Resultado esperado:} una reducción
    medible de los bloqueos indebidos o, si no se produce, el descarte de esa hipótesis.
```

Después:

```
la hipótesis
    no se verificó con un corpus legítimo alternativo. Además, cuatro cabeceras de proxy elevaron de
    0 a 4 el recuento de cabeceras fuera de la lista estándar y cambiaron el veredicto de 14 de los
    800 payloads en la Configuración~2 (Sección~\ref{sec:met-validez}); no se midió la importancia de
    esa característica en el modelo. \textit{Resultado esperado:} una reducción medible de los
    bloqueos indebidos o, si no se produce, el descarte de esa hipótesis, y la medida del efecto de
    las cabeceras del despliegue sobre el veredicto.
```

Fuente: docs/evidence/r4-analisis-20261025.json (12 a bloqueado y 2 a no bloqueado = 14 de 800 payloads); docs/evidence/e1-extractor-caracteristicas-20261025.json (unusual_headers_count de 0 a 4).

### 102. Q-B3-k2: k-resultados.tex, línea original 945, línea actual 945

Ubicación: Sec 8.4.3, 51 ataques: Configuración 2 con cabeceras.

Antes:

```
la Configuración~3b bloqueó 48 y la Configuración~2, 44. Para el WAF, los
```

Después:

```
la Configuración~3b bloqueó 48 y la Configuración~2, 44 (48 con las cabeceras del proxy). Para el WAF, los
```

Fuente: docs/evidence/r4-analisis-20261025.json (A2.d: Config 2 con cabeceras bloquea 48 de los 51).

### 103. Q-B5-j: j-metodologia.tex, línea original 1155, línea actual 1155

Ubicación: Sec 7.11, viñeta de la librería sola frente a detrás del proxy: tres corridas y desglose.

Antes:

```
La Configuración~2 se midió sin esas cuatro cabeceras, de modo que sus cifras
    describen un despliegue sin proxy. Una corrida de sensibilidad de las 800 peticiones con las
    cuatro cabeceras dio 794 de 800 bloqueadas (784 sin ellas): 12 payloads pasan a bloquearse
    (SQLi 1, Command Injection 11) y 2 dejan de bloquearse (órdenes con \texttt{sleep} que llegan a
    la aplicación y terminan por tiempo de espera), sin cambios en Path Traversal ni en XSS
    (Sección~\ref{anx:sensibilidad}).
```

Después:

```
Las cifras de la Configuración~2 describen un despliegue directo, sin proxy: se
    midió sin esas cuatro cabeceras. La condición con cabeceras se midió en tres corridas, con el
    contenedor y la base de datos reiniciados entre ellas y sin ningún payload con veredicto
    distinto: con cabeceras la librería sola bloquea 794 de 800 frente a 784 sin ellas (+10; 12
    payloads pasan a bloquearse, SQLi 1 y Command Injection 11, y 2 dejan de bloquearse, órdenes con
    \texttt{sleep} que llegan a la aplicación y terminan por tiempo de espera). De esos 10, 4
    corresponden a payloads que el WAF no bloquea y 6 a payloads que el WAF sí bloquea (8 pasan a
    bloquearse y 2 dejan de bloquearse). En condiciones equiparadas, el WAF suma 3 de 800 payloads a
    la librería (Sección~\ref{anx:sensibilidad}).
```

Fuente: docs/evidence/r4-analisis-20261025.json (A1: tres corridas con cabeceras, 794 en cada una, 0 ids con veredicto distinto; A2.c: 12 a bloqueado y 2 a no bloqueado; 4 netos entre los 51 y 6 netos entre los que el WAF sí bloquea: 8 a bloqueado y 2 a no bloqueado); attack-sim/results_s1_config2_con_cabeceras_run{1,2,3}_20261025.json.

### 104. Q-B6-es: b-resumen.tex, línea original 7, línea actual 7

Ubicación: Resumen, condición de despliegue.

Antes:

```
la versión 0.1.1 bloqueó
```

Después:

```
la versión 0.1.1, en despliegue directo, bloqueó
```

Fuente: Pedido del autor (B6); sin cambio de cifras. Palabras del Resumen: 294 antes (296 después, incluida la corrección de la doble "y").

### 105. Q-B6-en: c-abstract.tex, línea original 7, línea actual 7

Ubicación: Abstract, condición de despliegue (sincronizado con el Resumen).

Antes:

```
version 0.1.1 blocked
```

Después:

```
version 0.1.1, in direct deployment, blocked
```

Fuente: Pedido del autor (B6); sin cambio de cifras. Palabras del Abstract: 251 antes, 254 después.

### 106. Q-B1-anexo: n-anexos.tex, línea original 387, línea actual varias

Ubicación: Anexo 13.8: sensibilidad con tres corridas, descomposición 13 = 10 + 3 y cruce de verificación.

Antes:

```
\section{Sensibilidad de la Configuración 2 a las cabeceras del proxy}
\label{anx:sensibilidad}

El Cuadro~\ref{tab:anx-sensibilidad} compara la Configuración~2 con el paquete 0.1.1 en dos
condiciones, ambas sobre el corpus combinado de 800 peticiones y con el ejecutor corregido: sin
cabeceras extra (corrida 1 de la medición unificada) y con las cuatro cabeceras
\texttt{X-Real-IP}, \texttt{X-Forwarded-For}, \texttt{X-Forwarded-Port} y
\texttt{X-Forwarded-Proto} que agrega el proxy, con los valores de la captura de la Fase 2b
(192.168.65.1, 192.168.65.1, 8080 y http). Es una sensibilidad: las cifras principales del
Capítulo~\ref{cap:resultados} no cambian. La condición sin cabeceras se repitió en el mismo
contenedor y reprodujo la corrida 1 sin diferencias en ningún payload.

\begin{table}[H]
\centering
\small
\begin{tabular}{|L{2.7cm}|L{3.7cm}|L{3.7cm}|L{1.6cm}|L{1.6cm}|}
\hline
\textbf{Categoría} & \textbf{Sin cabeceras: bloqueados e IC 95~\%} & \textbf{Con cuatro cabeceras: bloqueados e IC 95~\%} & \textbf{A bloqueado} & \textbf{A no bloqueado} \\ \hline
SQLi & 199/200 (99.5~\%) [97.2--99.9] & 200/200 (100.0~\%) [98.1--100.0] & 1 & 0 \\ \hline
Path Traversal & 200/200 (100.0~\%) [98.1--100.0] & 200/200 (100.0~\%) [98.1--100.0] & 0 & 0 \\ \hline
Command Injection & 185/200 (92.5~\%) [88.0--95.4] & 194/200 (97.0~\%) [93.6--98.6] & 11 & 2 \\ \hline
XSS & 200/200 (100.0~\%) [98.1--100.0] & 200/200 (100.0~\%) [98.1--100.0] & 0 & 0 \\ \hline
\textbf{Total} & 784/800 (98.0~\%) [96.8--98.8] & 794/800 (99.2~\%) [98.4--99.7] & 12 & 2 \\ \hline
\end{tabular}
\caption[Sensibilidad de la Configuración 2 a las cabeceras del proxy]{Sensibilidad de la Configuración 2 (paquete 0.1.1) a las cuatro cabeceras que agrega el proxy, sobre 800 peticiones}
\label{tab:anx-sensibilidad}
\end{table}
{\footnotesize Nota. Elaboración propia con datos de
\texttt{attack-sim/results\_combined\_config2\_run1\_20261025.json} (sin cabeceras) y de
\texttt{attack-sim/results\_s1\_config2\_con\_cabeceras\_run1\_20261025.json} (con cabeceras); cálculo
en \texttt{docs/evidence/s1-analisis-20261025.py}. Una corrida por condición. Pasan a bloqueado: \texttt{cmdi\_112}, \texttt{cmdi\_120}, \texttt{cmdi\_134}, \texttt{cmdi\_155}, \texttt{cmdi\_28}, \texttt{cmdi\_31}, \texttt{cmdi\_36}, \texttt{cmdi\_38}, \texttt{cmdi\_40}, \texttt{cmdi\_66}, \texttt{cmdi\_7}, \texttt{sqli\_75}. Dejan de bloquearse: \texttt{cmdi\_51}, \texttt{cmdi\_94}, órdenes con \texttt{sleep} que llegan a la aplicación y terminan por tiempo de
espera, lo que se cuenta como no detectado. Prueba exacta de McNemar sobre los 14 payloads
discordantes (12 frente a 2): $p = 0.013$. De los 13 payloads que la Configuración~3b bloquea y la
Configuración~2 sin cabeceras no, la Configuración~2 con cabeceras bloquea 12 (todos salvo
\texttt{cmdi\_9}); la unión de la Configuración~2 con cabeceras y la 3a es de 797 payloads, igual que
la 3b, y el WAF suma 3 (\texttt{cmdi\_9}, \texttt{cmdi\_51} y \texttt{cmdi\_94}) a la librería con
cabeceras. La imagen local de la aplicación de esta sensibilidad (\texttt{sha256:d9b12672f000...}) se
reconstruyó porque cambió el contexto de build; el paquete 0.1.1 y los modelos se verificaron por
hash dentro del contenedor.}

\ifdefined\modoensamble
\else
	\section*{Referencias}
```

Después:

```
\section{Sensibilidad de la Configuración 2 a las cabeceras del proxy}
\label{anx:sensibilidad}

El Cuadro~\ref{tab:anx-sensibilidad} compara la Configuración~2 con el paquete 0.1.1 en dos
condiciones, ambas sobre el corpus combinado de 800 peticiones y con el ejecutor corregido: sin
cabeceras extra y con las cuatro cabeceras \texttt{X-Real-IP}, \texttt{X-Forwarded-For},
\texttt{X-Forwarded-Port} y \texttt{X-Forwarded-Proto} que agrega el proxy, con los valores de la
captura de la Fase 2b (192.168.65.1, 192.168.65.1, 8080 y http). Es una sensibilidad: las cifras
principales del Capítulo~\ref{cap:resultados} no cambian, y la Configuración~2 sin cabeceras sigue
siendo la cifra principal de la librería. Cada condición se midió en tres corridas: la sin
cabeceras, la corrida 1 de la medición unificada y una repetición que la reprodujo sin diferencias;
la con cabeceras, tres corridas con el contenedor y la base de datos reiniciados entre ellas, con
los mismos resultados en las tres y ningún payload con veredicto distinto.

\begin{table}[H]
\centering
\small
\begin{tabular}{|L{2.7cm}|L{3.7cm}|L{3.7cm}|L{1.6cm}|L{1.6cm}|}
\hline
\textbf{Categoría} & \textbf{Sin cabeceras: bloqueados e IC 95~\%} & \textbf{Con cuatro cabeceras: bloqueados e IC 95~\%} & \textbf{A bloqueado} & \textbf{A no bloqueado} \\ \hline
SQLi & 199/200 (99.5~\%) [97.2--99.9] & 200/200 (100.0~\%) [98.1--100.0] & 1 & 0 \\ \hline
Path Traversal & 200/200 (100.0~\%) [98.1--100.0] & 200/200 (100.0~\%) [98.1--100.0] & 0 & 0 \\ \hline
Command Injection & 185/200 (92.5~\%) [88.0--95.4] & 194/200 (97.0~\%) [93.6--98.6] & 11 & 2 \\ \hline
XSS & 200/200 (100.0~\%) [98.1--100.0] & 200/200 (100.0~\%) [98.1--100.0] & 0 & 0 \\ \hline
\textbf{Total} & 784/800 (98.0~\%) [96.8--98.8] & 794/800 (99.2~\%) [98.4--99.7] & 12 & 2 \\ \hline
\end{tabular}
\caption[Sensibilidad de la Configuración 2 a las cabeceras del proxy]{Sensibilidad de la Configuración 2 (paquete 0.1.1) a las cuatro cabeceras que agrega el proxy, sobre 800 peticiones}
\label{tab:anx-sensibilidad}
\end{table}
{\footnotesize Nota. Elaboración propia con datos de
\texttt{attack-sim/results\_combined\_config2\_run1\_20261025.json} (sin cabeceras) y de
\texttt{attack-sim/results\_s1\_config2\_con\_cabeceras\_run\{1,2,3\}\_20261025.json} (con cabeceras);
cálculo en \texttt{docs/evidence/s1-analisis-20261025.py} y
\texttt{docs/evidence/r4-analisis-20261025.py}. Pasan a bloqueado: \texttt{cmdi\_112}, \texttt{cmdi\_120}, \texttt{cmdi\_134}, \texttt{cmdi\_155}, \texttt{cmdi\_28}, \texttt{cmdi\_31}, \texttt{cmdi\_36}, \texttt{cmdi\_38}, \texttt{cmdi\_40}, \texttt{cmdi\_66}, \texttt{cmdi\_7}, \texttt{sqli\_75}. Dejan de bloquearse: \texttt{cmdi\_51}, \texttt{cmdi\_94}, órdenes con \texttt{sleep} que llegan a la aplicación y terminan por tiempo de
espera, lo que se cuenta como no detectado. Prueba exacta de McNemar sobre los 14 payloads
discordantes (12 frente a 2): $p = 0.013$. La imagen local de la aplicación de esta sensibilidad
(\texttt{sha256:d9b12672f000...}) se reconstruyó porque cambió el contexto de build; el paquete
0.1.1 y los modelos se verificaron por hash dentro del contenedor en cada corrida.}

El Cuadro~\ref{tab:anx-descomposicion} descompone la diferencia de 13 payloads entre la
Configuración~3b y la Configuración~2 sin cabeceras. La librería dentro de la 3b siempre recibe las
cabeceras del proxy, por lo que la comparación equiparada es la de la 3b con la Configuración~2 con
cabeceras: 13 = 10 (efecto de las cabeceras sobre la librería) + 3 (aporte del WAF).

\begin{table}[H]
\centering
\small
\begin{tabular}{|L{5.2cm}|L{1.6cm}|L{6.3cm}|}
\hline
\textbf{Concepto} & \textbf{Payloads} & \textbf{Detalle} \\ \hline
Configuración~2 sin cabeceras & 784 & Cifra principal de la librería \\ \hline
Efecto de las cabeceras sobre la librería & +10 & 12 pasan a bloqueado y 2 dejan de bloquearse \\ \hline
\hspace{0.4cm}entre los 51 que el WAF no bloquea & +4 & \texttt{cmdi\_112}, \texttt{cmdi\_134}, \texttt{cmdi\_31}, \texttt{cmdi\_38} \\ \hline
\hspace{0.4cm}entre los que el WAF sí bloquea & +6 & 8 a bloqueado (Command Injection 7, SQLi 1) y 2 a no bloqueado (\texttt{cmdi\_51}, \texttt{cmdi\_94}) \\ \hline
Configuración~2 con cabeceras & 794 & Referencia para la defensa en profundidad \\ \hline
Aporte del WAF en condiciones equiparadas (3b menos 2 con cabeceras) & +3 & \texttt{cmdi\_51}, \texttt{cmdi\_9}, \texttt{cmdi\_94} (Command Injection; los bloquea la 3a) \\ \hline
Configuración~3b & 797 & \\ \hline
\textbf{3b menos 2 sin cabeceras} & \textbf{+13} & \textbf{10 + 3} \\ \hline
\end{tabular}
\caption[Descomposición del aporte de la combinación]{Descomposición de la diferencia entre la Configuración 3b y la Configuración 2 sin cabeceras}
\label{tab:anx-descomposicion}
\end{table}
{\footnotesize Nota. Elaboración propia con datos de
\texttt{attack-sim/results\_combined\_config\{2,3a,3b\}\_run1\_20261025.json} y de
\texttt{attack-sim/results\_s1\_config2\_con\_cabeceras\_run1\_20261025.json}; cálculo en
\texttt{docs/evidence/r4-analisis-20261025.py}. Los +10 son un neto: 12 payloads a bloqueado menos 2
a no bloqueado.}

Cruce de verificación: de los 51 ataques que el WAF solo no bloquea, la Configuración~2 con
cabeceras bloquea 48 y la 3b bloquea 48, y los veredictos coinciden payload por payload (51 de 51)
en cada una de las tres corridas. Sobre los 800 payloads, la Configuración~2 con cabeceras y la 3b
difieren únicamente en los tres que aporta el WAF. Con las cabeceras del proxy, por lo tanto, el
efecto del proxy sobre la librería queda explicado por las cabeceras y no por otra diferencia entre
la Configuración~2 y la librería dentro de la 3b.

\ifdefined\modoensamble
\else
	\section*{Referencias}
```

Fuente: docs/evidence/r4-analisis-20261025.json (A2.b_descomposicion: 3b menos Config 2 sin cabeceras = 13, efecto neto de cabeceras = 10, aporte del WAF en condiciones equiparadas = 3: cmdi_9, cmdi_51, cmdi_94; A2.c_cambios_por_cabeceras: 4 netos entre los 51 que el WAF no bloquea, 6 netos entre los que sí bloquea; A2.d: 51 de 51 coinciden con la 3b en las tres corridas); docs/evidence/s1-analisis-20261025.json. Tres corridas con cabeceras: attack-sim/results_s1_config2_con_cabeceras_run{1,2,3}_20261025.json; sin cabeceras: attack-sim/results_combined_config2_run{1,2,3}_20261025.json (errata V9, 0 cambios de veredicto) y el control S1.

### 107. Q-B1-anexo-corr1: n-anexos.tex, línea original no aplica, línea actual 396

Ubicación: Anexo 13.8, descripción de las corridas por condición (correctiva).

Antes:

```
Cada condición se midió en tres corridas: la sin
cabeceras, la corrida 1 de la medición unificada y una repetición que la reprodujo sin diferencias;
la con cabeceras, tres corridas con el contenedor y la base de datos reiniciados entre ellas, con
los mismos resultados en las tres y ningún payload con veredicto distinto.
```

Después:

```
Cada condición se midió en tres corridas: la sin
cabeceras, las tres de la medición unificada, sin ningún payload con veredicto distinto, y un
control en el mismo contenedor que reprodujo la corrida 1; la con cabeceras, tres corridas con el
contenedor y la base de datos reiniciados entre ellas, con los mismos resultados en las tres y
ningún payload con veredicto distinto.
```

Fuente: Corrige la descripción de las corridas sin cabeceras: las tres de la medición unificada (errata V9) y el control S1.

### 108. Q-B1-anexo-corr2: n-anexos.tex, línea original no aplica, línea actual 459

Ubicación: Anexo 13.8, cruce de verificación: redacción acotada (correctiva).

Antes:

```
Con las cabeceras del proxy, por lo tanto, el
efecto del proxy sobre la librería queda explicado por las cabeceras y no por otra diferencia entre
la Configuración~2 y la librería dentro de la 3b.
```

Después:

```
Con las cabeceras del proxy, por lo tanto, la
Configuración~2 reproduce el veredicto de la librería dentro de la 3b en esos 51 payloads, de modo
que las cabeceras bastan para explicar la diferencia observada entre ambas.
```

Fuente: docs/evidence/r4-analisis-20261025.json (A2.d y d_cruce_todos_los_800: la Config 2 con cabeceras y la 3b difieren solo en cmdi_51, cmdi_9 y cmdi_94).



## Quinta ronda (ediciones 109 a 125)

Ediciones de la quinta ronda, con respaldo previo en `docs/evidence/tex-before-round5-20261025/` (sumas en `SHA256SUMS.txt`). Las líneas originales se miden sobre ese respaldo y las nuevas sobre los archivos actuales. Verificaciones de la Ronda 4 (A1 a A5) y correcciones en `docs/thesis-delta-errata-20261025-e.md`. Las ediciones cuyo nombre termina en un número o en `b` afinan texto de esta misma ronda y no tienen línea original.

| Archivo | Ediciones |
|---|---|
| j-metodologia.tex | 3 |
| k-resultados.tex | 6 |
| l-discusion.tex | 4 |
| m-conclusiones.tex | 2 |
| n-recomendaciones.tex | 2 |
| **Total** | **17** |

### 109. V-B1-tabla: k-resultados.tex, línea original 975, línea actual 982

Ubicación: Cuadro 38: columna "2 con cabeceras (post hoc)" separada por doble filete; anchos ajustados con \tabcolsep.

Antes:

```
\begin{tabular}{|L{2.7cm}|L{2.0cm}|L{2.6cm}|L{2.6cm}|L{2.6cm}|}
\hline
\textbf{Categoría} & \textbf{Config.~1 (sin protección)} & \textbf{Config.~2 (solo \textit{logSguarDian}, 0.1.1)} & \textbf{Config.~3a (solo WAF)} & \textbf{Config.~3b (ambas capas, 0.1.1)} \\ \hline
SQLi & 0/200 (0.0~\%) & 199/200 (99.5~\%) & 199/200 (99.5~\%) & 200/200 (100.0~\%) \\ \hline
Path Traversal & 0/200 (0.0~\%) & 200/200 (100.0~\%) & 197/200 (98.5~\%) & 200/200 (100.0~\%) \\ \hline
Command Injection & 0/200 (0.0~\%) & 185/200 (92.5~\%) & 164/200 (82.0~\%) & 197/200 (98.5~\%) \\ \hline
XSS & 0/200 (0.0~\%) & 200/200 (100.0~\%) & 189/200 (94.5~\%) & 200/200 (100.0~\%) \\ \hline
\textbf{Total} & 0/800 (0.0~\%) & 784/800 (98.0~\%) & 749/800 (93.6~\%) & 797/800 (99.6~\%) \\ \hline
\end{tabular}
```

Después:

```
\setlength{\tabcolsep}{4pt}
\begin{tabular}{|L{2.2cm}|L{1.7cm}|L{2.1cm}||L{2.2cm}||L{2.2cm}|L{2.2cm}|}
\hline
\textbf{Categoría} & \textbf{Config.~1 (sin protección)} & \textbf{Config.~2 (solo \textit{logSguarDian}, 0.1.1)} & \textbf{Config.~2 con cabeceras (post hoc)} & \textbf{Config.~3a (solo WAF)} & \textbf{Config.~3b (ambas capas, 0.1.1)} \\ \hline
SQLi & 0/200 (0.0~\%) & 199/200 (99.5~\%) & 200/200 (100.0~\%) & 199/200 (99.5~\%) & 200/200 (100.0~\%) \\ \hline
Path Traversal & 0/200 (0.0~\%) & 200/200 (100.0~\%) & 200/200 (100.0~\%) & 197/200 (98.5~\%) & 200/200 (100.0~\%) \\ \hline
Command Injection & 0/200 (0.0~\%) & 185/200 (92.5~\%) & 194/200 (97.0~\%) & 164/200 (82.0~\%) & 197/200 (98.5~\%) \\ \hline
XSS & 0/200 (0.0~\%) & 200/200 (100.0~\%) & 200/200 (100.0~\%) & 189/200 (94.5~\%) & 200/200 (100.0~\%) \\ \hline
\textbf{Total} & 0/800 (0.0~\%) & 784/800 (98.0~\%) & 794/800 (99.2~\%) & 749/800 (93.6~\%) & 797/800 (99.6~\%) \\ \hline
\end{tabular}
```

Fuente: Columna con cabeceras: docs/evidence/r4-analisis-20261025.json (A1.por_corrida, tres corridas idénticas: 200, 200, 194, 200; total 794) y attack-sim/results_s1_config2_con_cabeceras_run{1,2,3}_20261025.json; demás columnas sin cambio (results_combined_config{1,2,3a,3b}_run1_20261025.json).

### 110. V-B1-wilson: k-resultados.tex, línea original 995, línea actual 1003

Ubicación: Cuadro 38, nota: intervalos de Wilson de la nueva columna.

Antes:

```
Configuración~2, 97.2--99.9, 98.1--100.0,
88.0--95.4 y 98.1--100.0~\%;
```

Después:

```
Configuración~2, 97.2--99.9, 98.1--100.0,
88.0--95.4 y 98.1--100.0~\%; Configuración~2 con cabeceras, 98.1--100.0, 98.1--100.0, 93.6--98.6 y
98.1--100.0~\%;
```

Fuente: Wilson de la columna con cabeceras: docs/evidence/r4-analisis-20261025.json (SQLi, Path Traversal y XSS [98.1, 100.0]; Command Injection [93.6, 98.6]).

### 111. V-B1-nota: k-resultados.tex, línea original 999, línea actual 1008

Ubicación: Cuadro 38, nota: columna principal fijada antes; columna con cabeceras post hoc.

Antes:

```
La Configuración~2 de este cuadro se midió sin las
cuatro cabeceras \texttt{X-*} que agrega el proxy, por lo que sus cifras describen un despliegue
directo, sin proxy. Con esas cabeceras, en tres corridas, dio 794 de 800 (SQLi 200, Path Traversal
200, Command Injection 194 y XSS 200), y en condiciones equiparadas (Configuración~2 con cabeceras)
el aporte del WAF sobre la librería es de 3 payloads. Las cifras de este cuadro no cambian
(Sección~\ref{anx:sensibilidad}).}
```

Después:

```
La columna Config.~2 se midió sin las cuatro cabeceras
\texttt{X-*} que agrega el proxy, por lo que describe un despliegue directo, sin proxy; se fijó
antes de conocer el efecto de esas cabeceras y es la cifra principal de la librería. La columna
Config.~2 con cabeceras es una sensibilidad añadida después de observar que la 3b bloqueaba
payloads que la Configuración~2 no (análisis post hoc); se midió en tres corridas idénticas y es la
comparable con la 3a y la 3b, porque la librería dentro de la 3b recibe esas cabeceras. En
condiciones equiparadas (3b frente a esa columna) el aporte del WAF sobre la librería es de 3
payloads (Sección~\ref{anx:sensibilidad}).}
```

Fuente: Decisión del autor (columna post hoc); docs/evidence/r4-analisis-20261025.json (A2.b: 3b menos Config 2 con cabeceras = 3).

### 112. V-B5-k: k-resultados.tex, línea original 900, línea actual varias

Ubicación: Sec 8.4.3, Ronda 4: versión, ejecutor, composición de los 40 y auditoría de fuga.

Antes:

```
De los 40 ataques que el WAF no bloqueó, \textit{logSguarDian} bloqueó 37. Los resultados
```

Después:

```
De los 40 ataques que el WAF no bloqueó, \textit{logSguarDian} bloqueó 37 (92.5~\%;
intervalo de Wilson al 95~\%: 80.1--97.4~\%). Esta ronda se midió el 15 de agosto de 2026 con el
tarball local de la 0.1.0 (par~A) y con el ejecutor anterior a la corrección, de modo que no es un
resultado de la 0.1.1. Ninguno de esos 40 ataques es de Command Injection (fueron 11 de SQLi, 3 de
XSS y 26 de Path Traversal); por igualdad normalizada no se detectó coincidencia con el
entrenamiento en ninguno de ellos, aunque por la regla permisiva de subcadena coinciden 7 de los 11
de SQLi y 1 de los 3 de XSS. La corrección del ejecutor no altera las peticiones de esas
categorías, pero la ronda no se repitió con el ejecutor corregido. Los resultados
```

Fuente: docs/evidence/r5-verificacion-ronda4-20261025.json (A1: commit af61eba, 2026-08-15; vendor/logsguardian-0.1.0.tgz con SHA-256 e09120006dd1...; ejecutor 0c84de55... = el anterior; A2: 40 = pt 26, sqli 11, xss 3, cmdi 0; A3: igualdad normalizada 0 en los 40, subcadena normalizada 7 de 11 sqli y 1 de 3 xss; A4: ninguna petición de los 40 cambia con la corrección; A5: Wilson 37/40 [80.1, 97.4]).

### 113. V-B3-c40: k-resultados.tex, línea original 1073, línea actual 1084

Ubicación: Cuadro 40, fila de defensa en profundidad: afirmaciones A y B.

Antes:

```
La 3b bloqueó 48 de los 51 ataques no bloqueados por el WAF; la Configuración~2, 44 sin las cabeceras del proxy y 48 con ellas. En condiciones equiparadas el WAF suma 3 de 800 payloads a la librería (13 = 10 por las cabeceras + 3 por el WAF) & --- \\ \hline
```

Después:

```
La librería suma 48 de 800 payloads al WAF solo (la 3b bloqueó 48 de los 51 ataques que el WAF no bloquea); en condiciones equiparadas (3b frente a la Configuración~2 con cabeceras) el WAF suma 3 de 800 a la librería & --- \\ \hline
```

Fuente: docs/evidence/r5-verificacion-ronda4-20261025.json (A5: 48/51, 48/800, 3/800); docs/evidence/r4-analisis-20261025.json (A2.b y A2.d).

### 114. V-B5-j-tarball: j-metodologia.tex, línea original 419, línea actual varias

Ubicación: Sec 7.4.2, origen del tarball local de la 0.1.0 (corrige "construido en a3aada0").

Antes:

```
se hicieron con un tarball construido en el commit \texttt{a3aada0} (SHA-256 \texttt{e09120006dd1...}),
que contiene el par~A
```

Después:

```
se hicieron con el tarball local de la 0.1.0 que el repositorio de la aplicación incluye desde el
5 de agosto de 2026 (commit \texttt{06316cb}; SHA-256 \texttt{e09120006dd1...}) y que ya se usó en
la Ronda~4, que contiene el par~A
```

Fuente: git log -- vendor/logsguardian-0.1.0.tgz: el archivo con SHA-256 e09120006dd1... está en el repositorio desde el commit 06316cb (2026-08-05) y es el mismo de af61eba (Ronda 4); a3aada0 es solo el commit de la Ronda 5 que lo usó.

### 115. V-B4-j: j-metodologia.tex, línea original 1172, línea actual 1173

Ubicación: Sec 7.11, sesgo del corpus: inferencia marcada, sin "por construcción".

Antes:

```
\item \textbf{Comparación con el WAF no neutral.} La librería se entrenó con payloads de las
    mismas cuatro clases de ataque que el corpus de evaluación (el corpus excluye coincidencias
    exactas, pero no se midió la distancia entre ambas distribuciones), mientras que el WAF es un
    conjunto de reglas genérico en nivel de paranoia 1 que no se calibró con ellos; la comparación
    entre ambos no es neutral y favorece a la librería por construcción. No se midieron otros niveles de paranoia ni
    un corpus ajeno al entrenamiento.
```

Después:

```
\item \textbf{Posible sesgo del corpus en la comparación con el WAF.} La librería se entrenó con
    payloads de las mismas cuatro clases de ataque que el corpus de evaluación (el corpus excluye
    coincidencias exactas, pero no se midió la distancia entre ambas distribuciones), mientras que el
    WAF es un conjunto de reglas genérico en nivel de paranoia 1 que no se calibró con ellos. Es
    plausible que el corpus favorezca a la librería, por lo que las cifras de la librería (48 de 800
    sobre el WAF; 37 de 40 en la Ronda~4) pueden ser optimistas y los 3 de 800 del WAF pueden ser
    una cota inferior de su aporte; es una inferencia, no una medición. No se midieron otros niveles
    de paranoia ni un corpus ajeno al entrenamiento.
```

Fuente: Pedido del autor (B4): inferencia marcada como tal; Wilson y cifras: docs/evidence/r5-verificacion-ronda4-20261025.json (A5).

### 116. V-B5-j-tarball2: j-metodologia.tex, línea original no aplica, línea actual 420

Ubicación: Sec 7.4.2, redacción del origen del tarball (correctiva).

Antes:

```
(commit \texttt{06316cb}; SHA-256 \texttt{e09120006dd1...}) y que ya se usó en
la Ronda~4, que contiene el par~A pero no es el archivo publicado en el registro (SHA-256
\texttt{c5c1a1da57cf...}); se les llama paquete 0.1.0 por contener el mismo par de modelos.
```

Después:

```
(commit \texttt{06316cb}; SHA-256 \texttt{e09120006dd1...}). Ese tarball, que ya se
usó en la Ronda~4, contiene el par~A pero no es el archivo publicado en el registro (SHA-256
\texttt{c5c1a1da57cf...}); se les llama paquete 0.1.0 por contener el mismo par de modelos.
```

Fuente: Ídem V-B5-j-tarball (redacción).

### 117. V-B5-l1: l-discusion.tex, línea original 219, línea actual varias

Ubicación: Cap. 9, Defensa en profundidad, Ronda 4: versión, ejecutor, Wilson, auditoría y alcance de la corroboración.

Antes:

```
En la Ronda~4, ModSecurity con OWASP CRS en nivel de paranoia 1 bloqueó el 93.2~\% de los ataques,
\textit{logSguarDian} el 98.8~\% y ambas capas el 99.5~\%; de los 40 ataques que el WAF dejó pasar,
la librería bloqueó 37. Ese corpus tiene fuga confirmada en Command Injection, pero ninguno de los
40 ataques que el WAF no bloqueó pertenece a esa categoría (fueron 11 de SQL Injection, 3 de XSS y
26 de Path Traversal). Por igualdad normalizada, 7 de los 113 payloads de XSS y ninguno de los 77
de SQL Injection ni de los 200 de Path Traversal coinciden con alguna partición; por subcadena,
26 de SQL Injection y 13 de XSS, un criterio permisivo que el trabajo de graduación de Diego
Valenzuela \cite{valenzuela2026ia} (sección VIII.3.5) califica de límite superior. Con esa salvedad, el resultado apunta al
posicionamiento de \textit{logSguarDian} definido en el Marco Teórico: una capa complementaria al
WAF, que detiene la mayor parte de lo que supera la primera capa, y no un sustituto.
```

Después:

```
En la Ronda~4 (15 de agosto de 2026, con el tarball local de la 0.1.0, par~A, y el ejecutor anterior
a la corrección, de modo que no es un resultado de la 0.1.1), ModSecurity con OWASP CRS en nivel de
paranoia 1 bloqueó el 93.2~\% de los ataques, \textit{logSguarDian} el 98.8~\% y ambas capas el
99.5~\%; de los 40 ataques que el WAF dejó pasar, la librería bloqueó 37 (92.5~\%; intervalo de
Wilson al 95~\%: 80.1--97.4~\%). Ese corpus tiene fuga confirmada en Command Injection, pero
ninguno de los 40 ataques que el WAF no bloqueó pertenece a esa categoría (fueron 11 de SQL
Injection, 3 de XSS y 26 de Path Traversal). Por igualdad normalizada, 7 de los 113 payloads de XSS
y ninguno de los 77 de SQL Injection ni de los 200 de Path Traversal coinciden con alguna partición;
por subcadena, 26 de SQL Injection y 13 de XSS, un criterio permisivo que el trabajo de graduación
de Diego Valenzuela \cite{valenzuela2026ia} (sección VIII.3.5) califica de límite superior. Entre
esos 40 ataques no se detectó coincidencia por igualdad normalizada, pero por subcadena coinciden 7
de los 11 de SQL Injection y 1 de los 3 de XSS; el ejecutor anterior no altera las peticiones de
esas categorías, aunque la ronda no se repitió con el ejecutor corregido. Con esas salvedades, este
resultado corrobora, con una muestra pequeña, que la librería agrega cobertura a un WAF; no respalda
por sí solo que no lo sustituya.
```

Fuente: docs/evidence/r5-verificacion-ronda4-20261025.json (A1 a A5); Diego Valenzuela, trabajo de graduación, sección VIII.3.5 (7/113 xss por igualdad; 26 sqli y 13 xss por subcadena), reproducido con attack-sim/leakage_report_round4_20261025.json.

### 118. V-B3-l: l-discusion.tex, línea original 270, línea actual 276

Ubicación: Cap. 9, Defensa en profundidad: afirmaciones A y B separadas.

Antes:

```
En condiciones equiparadas, la ganancia de cobertura de añadir el WAF a
la librería en la Ronda~5 es de 3 de 800 payloads, de modo que la recomendación de desplegar la
librería detrás de un WAF no descansa en esa ganancia, sino en la Ronda~4 (la librería bloqueó 37 de
los 40 ataques que el WAF dejó pasar), en los bloqueos indebidos y la falta de calibración de la
librería, y en que el corpus favorece a la librería por construcción. Las Rondas 1 a 3 aportaron
```

Después:

```
Los resultados respaldan dos afirmaciones con soportes distintos. La primera es que la librería
agrega cobertura a un WAF: en la Ronda~5, que tiene filtrado contra el entrenamiento, la librería
suma 48 de 800 payloads al WAF solo (6.0~\%; intervalo de Wilson al 95~\%: 4.6--7.9~\%) y bloquea
48 de los 51 ataques que este no bloquea (94.1~\%; 84.1--98.0~\%); la Ronda~4 la corrobora con una
muestra de 40 (37 de 40; 80.1--97.4~\%), con las salvedades de versión, ejecutor y solapamiento
indicadas arriba. La segunda es que la librería no sustituye al WAF, y la cobertura de la Ronda~5
casi no la respalda: en condiciones equiparadas el WAF suma 3 de 800 payloads a la librería
(0.4~\%; 0.1--1.1~\%), y los 37 de 40 de la Ronda~4 miden la primera afirmación y no esta. Se
sostiene en otras razones: la librería se evaluó solo en cuatro clases de ataque, de modo que no hay
evidencia de cobertura fuera de ellas; su veredicto depende de un voto de árbol y de las cabeceras
que agrega el despliegue (arriba); y los bloqueos indebidos medidos en aplicaciones de terceros y
el umbral calibrado sobre la partición de validación y la aplicación de referencia, no con el
tráfico de cada aplicación (Sección~\ref{sec:dis-despliegue}), sin que se haya medido la tasa de
falsos positivos del WAF. Las Rondas 1 a 3 aportaron
```

Fuente: docs/evidence/r5-verificacion-ronda4-20261025.json (A5: Wilson 48/800 [4.6, 7.9], 48/51 [84.1, 98.0], 3/800 [0.1, 1.1], 37/40 [80.1, 97.4]); E1 y E2 (errata-b); docs/evidence/s1-analisis-20261025.json; alcance de cuatro clases: parity_report.json del paquete (rf_classes); calibración: Sección 7.11 (viñeta de calibración en una sola aplicación).

### 119. V-B3-l2: l-discusion.tex, línea original 295, línea actual 310

Ubicación: Cap. 9, Contraste con el Marco Teórico: capa complementaria.

Antes:

```
Confirman el posicionamiento de un RASP como capa complementaria al WAF y no como su
sustituto: en la Ronda~4, la librería, que analiza la petición dentro del proceso, y el WAF perimetral
detectan conjuntos parcialmente distintos; en la Ronda~5, en condiciones equiparadas, el WAF agrega
solo 3 de 800 payloads a la librería, de modo que el respaldo es el de la Ronda~4
(Sección~\ref{sec:dis-defensa}).
```

Después:

```
Confirman el posicionamiento de un RASP como capa complementaria al WAF y no como su
sustituto, con una salvedad: la Ronda~5 respalda que la librería, que analiza la petición dentro del
proceso, agrega cobertura a un WAF perimetral (48 de 800 payloads), pero no que el WAF agregue
cobertura a la librería (3 de 800 en condiciones equiparadas); que no la sustituya se sostiene en el
alcance de cuatro clases de ataque, en la fragilidad del veredicto y en los bloqueos indebidos
(Sección~\ref{sec:dis-defensa}).
```

Fuente: Ídem V-B3-l.

### 120. V-B3-c: m-conclusiones.tex, línea original 98, línea actual varias

Ubicación: Conclusión conc:waf: afirmaciones A y B separadas.

Antes:

```
En la Ronda~4, ModSecurity con OWASP CRS
    bloqueó el 93.2~\% de 590 payloads, la librería el 98.8~\% y ambas capas el 99.5~\%; la librería
    bloqueó 37 de los 40 ataques que el WAF dejó pasar, ninguno de ellos de Command Injection, la
    categoría con fuga de datos confirmada en ese corpus. En la Ronda~5, sobre un corpus sin esa fuga y ampliado
    con 200 payloads de XSS, medido el 25 de octubre de 2026 con las cuatro configuraciones sobre
    el mismo árbol de la aplicación y el ejecutor corregido, la librería sola bloqueó 784 de 800
    payloads, el WAF solo 749 y ambas capas 797. El WAF bloqueó el 82.0~\% de Command Injection
    (intervalo de Wilson al 95~\%: 76.1--86.7~\%) frente al 92.5~\% de la librería, y el 68.0~\%
    reportado antes se debió al ejecutor anterior y no a la aplicación. De los 51 ataques que el WAF
    no bloqueó, ambas capas bloquearon 48 y la librería sola, 44 sin las cabeceras del proxy y 48 con
    ellas. La combinación bloqueó 13 payloads más que la librería sola sin esas cabeceras, una
    comparación que mezcla condiciones: 13 = 10 (efecto de las cabeceras que agrega el proxy, que
    elevan la librería sola a 794 de 800) + 3 (aporte del WAF en condiciones equiparadas, todos de
    Command Injection), y la librería suma 48 al WAF solo (Sección~\ref{anx:sensibilidad}). La
    complementariedad es asimétrica: en Path Traversal, SQL Injection y XSS la librería sola, con
    cabeceras, iguala a la combinación, y solo en Command Injection cada capa bloquea payloads que la
    otra no. En condiciones equiparadas, la ganancia de cobertura de añadir el WAF a la librería en
    la Ronda~5 es de 3 de 800 payloads, de modo que la recomendación de usar la librería como capa
    complementaria a un WAF y no como su sustituto no descansa en esa ganancia, sino en la Ronda~4
    (37 de 40), en los bloqueos indebidos y la falta de calibración de la librería
    (conclusión~\ref{conc:fp}) y en que el corpus favorece a la librería por construcción: la
    librería se entrenó con payloads de las mismas cuatro clases de ataque que el corpus de
    evaluación (que excluye coincidencias exactas, pero cuya distancia respecto del entrenamiento no
    se midió), mientras que el WAF no se calibró con ellos y no se midieron otros niveles de
    paranoia, por lo que la comparación no es neutral (Sección~\ref{sec:met-validez}).
```

Después:

```
Dos afirmaciones, con soportes
    distintos. (A) La librería agrega cobertura a un WAF. En la Ronda~5, sobre un corpus filtrado
    contra el entrenamiento y ampliado con 200 payloads de XSS, medido el 25 de octubre de 2026 con
    las cuatro configuraciones sobre el mismo árbol de la aplicación y el ejecutor corregido, la
    librería sola bloqueó 784 de 800 payloads, el WAF solo 749 y ambas capas 797: la librería suma
    48 de 800 payloads al WAF solo (6.0~\%; intervalo de Wilson al 95~\%: 4.6--7.9~\%) y bloquea 48
    de los 51 ataques que este no bloquea (94.1~\%; 84.1--98.0~\%). El WAF bloqueó el 82.0~\% de
    Command Injection (76.1--86.7~\%) frente al 92.5~\% de la librería, y el 68.0~\% reportado antes
    se debió al ejecutor anterior y no a la aplicación. Como corroboración con una muestra pequeña,
    en la Ronda~4 (15 de agosto de 2026, tarball local de la 0.1.0 con el par~A y ejecutor anterior a
    la corrección, de modo que no es un resultado de la 0.1.1) la librería bloqueó 37 de los 40
    ataques que el WAF dejó pasar (92.5~\%; 80.1--97.4~\%), ninguno de ellos de Command Injection,
    la categoría con fuga de datos confirmada en ese corpus; en esos 40 no se detectó coincidencia
    por igualdad normalizada con el entrenamiento, aunque por subcadena coinciden 7 de los 11 de SQL
    Injection y 1 de los 3 de XSS. (B) La librería no sustituye al WAF. La cobertura de la Ronda~5
    casi no respalda esta afirmación: en condiciones equiparadas, la 3b frente a la Configuración~2
    con las cabeceras del proxy (794 de 800), el WAF suma solo 3 de 800 payloads (0.4~\%; 0.1--1.1~\%),
    todos de Command Injection. La combinación bloqueó 13 payloads más que la Configuración~2 sin
    esas cabeceras, una comparación que mezcla condiciones: 13 = 10 (efecto de las cabeceras que
    agrega el proxy) + 3 (aporte del WAF) (Sección~\ref{anx:sensibilidad}). La afirmación se sostiene
    en otras razones: la librería se evaluó solo en cuatro clases de ataque, de modo que no hay
    evidencia de cobertura fuera de ellas; su veredicto depende de un voto de árbol y de las
    cabeceras del despliegue, pues cuatro cabeceras de proxy cambiaron el veredicto de 14 de los 800
    payloads y dos de los tres payloads de Command Injection que ninguna configuración bloquea quedan
    a 0.0167 del umbral; y los bloqueos indebidos medidos en aplicaciones de terceros
    (conclusión~\ref{conc:fp}), con un umbral calibrado sobre la partición de validación y la
    aplicación de referencia, sin que se haya medido la tasa de falsos positivos del WAF. Es
    plausible que el corpus favorezca a la librería, por lo que sus cifras pueden ser optimistas y
    los 3 de 800 del WAF una cota inferior de su aporte; es una inferencia, no una medición
    (Sección~\ref{sec:met-validez}).
```

Fuente: Ídem V-B3-l; 14 payloads: docs/evidence/r4-analisis-20261025.json (12 a bloqueado y 2 a no bloqueado); 0.0167: docs/evidence/e1-proxy-headers-20261025.json (cmdi_184 y cmdi_185, 0.3333; cmdi_6 es benigno y su probabilidad de ataque no se registra).

### 121. V-B3-r: n-recomendaciones.tex, línea original 36, línea actual varias

Ubicación: Recomendación 2: justificación en dos afirmaciones.

Antes:

```
bloqueó 37 de los 40 ataques que ModSecurity con OWASP CRS dejó pasar en la Ronda~4. En la
    Ronda~5, en condiciones equiparadas, el WAF suma solo 3 de 800 payloads a la librería, de modo
    que esta recomendación no descansa en esa ganancia de cobertura, sino en la Ronda~4, en los
    bloqueos indebidos y la falta de calibración de la librería
    (Conclusión~\ref{conc:fp}) y en que el corpus favorece a la librería por construcción
    (Conclusión~\ref{conc:waf}). \textit{Resultado esperado:}
```

Después:

```
(A) la librería agrega cobertura a un WAF: en la Ronda~5, sobre un corpus filtrado contra el
    entrenamiento, suma 48 de 800 payloads al WAF solo (intervalo de Wilson al 95~\%: 4.6--7.9~\%) y
    bloquea 48 de los 51 ataques que este no bloquea (84.1--98.0~\%); la Ronda~4 lo corrobora con una
    muestra de 40 (37 de 40; 80.1--97.4~\%), pero se midió con el tarball local de la 0.1.0 y el
    ejecutor anterior, de modo que no es un resultado de la 0.1.1 (Conclusión~\ref{conc:waf}). (B) La
    librería no sustituye al WAF: en condiciones equiparadas el WAF suma solo 3 de 800 payloads a la
    librería (0.1--1.1~\%), por lo que la cobertura de la Ronda~5 no respalda esta parte; se sostiene
    en que la librería se evaluó solo en cuatro clases de ataque, en que su veredicto depende de un
    voto de árbol y de las cabeceras del despliegue y en los bloqueos indebidos medidos
    (Conclusión~\ref{conc:fp}), sin que se haya medido la tasa de falsos positivos del WAF.
    \textit{Resultado esperado:}
```

Fuente: Ídem V-B3-l.

### 122. V-B5-k2: k-resultados.tex, línea original no aplica, línea actual 902

Ubicación: Sec 8.4.3, Ronda 4: la 3a se midió en otra rama de la aplicación.

Antes:

```
y con el ejecutor anterior a la corrección, de modo que no es un
resultado de la 0.1.1.
```

Después:

```
y con el ejecutor anterior a la corrección, y la Configuración~3a se midió
en una rama distinta de la aplicación, de modo que no es un resultado de la 0.1.1.
```

Fuente: docs/config3b-results.md (Round 4: Config 3a runs on feat/waf-modsecurity-crs) y docker-compose.yml en af61eba (comentario de la rama).

### 123. V-B5-l1b: l-discusion.tex, línea original no aplica, línea actual 220

Ubicación: Cap. 9, Ronda 4: la 3a se midió en otra rama de la aplicación.

Antes:

```
a la corrección, de modo que no es un resultado de la 0.1.1),
```

Después:

```
a la corrección, y la 3a en una rama distinta de la aplicación, de modo que no es un resultado
de la 0.1.1),
```

Fuente: Ídem V-B5-k2.

### 124. V-B3-c2: m-conclusiones.tex, línea original no aplica, línea actual 108

Ubicación: Conclusión conc:waf, Ronda 4: la 3a se midió en otra rama de la aplicación.

Antes:

```
la corrección, de modo que no es un resultado de la 0.1.1) la librería bloqueó 37 de los 40
```

Después:

```
la corrección, y la 3a en una rama distinta de la aplicación, de modo que no es un resultado de
    la 0.1.1) la librería bloqueó 37 de los 40
```

Fuente: Ídem V-B5-k2.

### 125. V-B3-r2: n-recomendaciones.tex, línea original no aplica, línea actual 40

Ubicación: Recomendación 2, Ronda 4: la 3a se midió en otra rama de la aplicación.

Antes:

```
ejecutor anterior, de modo que no es un resultado de la 0.1.1
```

Después:

```
ejecutor anterior, y la 3a en otra rama de la aplicación, de modo que no es un resultado de la 0.1.1
```

Fuente: Ídem V-B5-k2.



## Sexta ronda (ediciones 126 a 127)

Dos ajustes finales pedidos por el autor (Cuadro 12 y partición de la Conclusión 8). Respaldo previo en `docs/evidence/tex-before-round6-20261025/`. Sin mediciones nuevas.

### 126. W-12-filaA: j-metodologia.tex, línea original 388, línea actual 388

Ubicación: Cuadro 12, fila A: la Ronda 4 y la medición principal de la Ronda 5 usaron el tarball local.

Antes:

```
Paquete \texttt{logsguardian@0.1.0} (commit \texttt{c3d591a}); Ronda~4 (Configuraciones 2, 3a y 3b sobre los 590 payloads)\textsuperscript{c}; medición principal de la Ronda~5;
```

Después:

```
Paquete \texttt{logsguardian@0.1.0} (commit \texttt{c3d591a}); con el tarball local de la 0.1.0 (SHA-256 \texttt{e09120006dd1...}), no con el archivo publicado: Ronda~4 (Configuraciones 2 y 3b sobre los 590 payloads; la 3a no lleva la librería)\textsuperscript{c} y medición principal de la Ronda~5;
```

Fuente: docs/thesis-delta-errata-20261025-e.md §1 (vendor/logsguardian-0.1.0.tgz, SHA-256 e09120006dd1..., en el repo desde 06316cb; usado en af61eba) y §3 de la errata-e; la 3a no lleva la librería (docs/thesis-delta-configs.md §2).

### 127. W-C8-split: m-conclusiones.tex, línea original 113, línea actual 113

Ubicación: Conclusión conc:waf: la afirmación B pasa a un párrafo aparte.

Antes:

```
Injection y 1 de los 3 de XSS. (B) La librería no sustituye al WAF.
```

Después:

```
Injection y 1 de los 3 de XSS.

    (B) La librería no sustituye al WAF.
```

Fuente: Solo estructura: un párrafo aparte para la afirmación B; sin cambio de contenido ni de etiquetas.



## Sexta ronda, continuación (ediciones 128 a 141)

Segundo prompt rotulado "sexta ronda" (solo redacción). La carpeta `tex-before-round6-20261025` ya existía con el respaldo del prompt anterior, por lo que el respaldo de este prompt está en `docs/evidence/tex-before-round6b-20261025/` (sumas en `SHA256SUMS.txt`) y la sección del log se llama "continuación". Verificación del ejecutor y correcciones en `docs/thesis-delta-errata-20261025-f.md`.

| Archivo | Ediciones |
|---|---|
| k-resultados.tex | 1 |
| l-discusion.tex | 6 |
| m-conclusiones.tex | 3 |
| n-recomendaciones.tex | 4 |
| **Total** | **14** |

### 128. X-label1: n-recomendaciones.tex, línea original 26, línea actual 26

Ubicación: Recomendación 1: etiqueta rec:monitor (para referenciar sin número fijo).

Antes:

```
\item \textbf{Instalar primero en modo \texttt{monitor}.}
```

Después:

```
\item \label{rec:monitor}\textbf{Instalar primero en modo \texttt{monitor}.}
```

Fuente: Sin cifras: etiqueta para referenciar la recomendación 1 sin número fijo.

### 129. X-label5: n-recomendaciones.tex, línea original 70, línea actual 75

Ubicación: Recomendación 5: etiqueta rec:monitor-defecto.

Antes:

```
\item \textbf{Usar el modo \texttt{monitor} por defecto.}
```

Después:

```
\item \label{rec:monitor-defecto}\textbf{Usar el modo \texttt{monitor} por defecto.}
```

Fuente: Sin cifras: etiqueta para referenciar la recomendación 5 sin número fijo.

### 130. X-B1-l: l-discusion.tex, línea original 281, línea actual 288

Ubicación: Cap. 9.5, afirmación B: formulación de prudencia y conexión con el modo monitor.

Antes:

```
La segunda es que la librería no sustituye al WAF, y la cobertura de la Ronda~5
casi no la respalda: en condiciones equiparadas el WAF suma 3 de 800 payloads a la librería
(0.4~\%; 0.1--1.1~\%), y los 37 de 40 de la Ronda~4 miden la primera afirmación y no esta. Se
sostiene en otras razones: la librería se evaluó solo en cuatro clases de ataque, de modo que no hay
evidencia de cobertura fuera de ellas; su veredicto depende de un voto de árbol y de las cabeceras
que agrega el despliegue (arriba); y los bloqueos indebidos medidos en aplicaciones de terceros y
el umbral calibrado sobre la partición de validación y la aplicación de referencia, no con el
tráfico de cada aplicación (Sección~\ref{sec:dis-despliegue}), sin que se haya medido la tasa de
falsos positivos del WAF.
```

Después:

```
La segunda es que no se puede afirmar que la librería sustituya al WAF: en condiciones
equiparadas el WAF suma 3 de 800 payloads a la librería (0.4~\%; 0.1--1.1~\%), y los 37 de 40 de la
Ronda~4 miden la primera afirmación y no esta. Esa cautela no descansa en la cobertura medida sino
en razones de prudencia, no de medición: la librería se evaluó solo en cuatro clases de ataque, de
modo que no hay evidencia de cobertura fuera de ellas; su veredicto depende de un voto de árbol y de
las cabeceras que agrega el despliegue (arriba); y la configuración recomendada para la población
objetivo es el modo \texttt{monitor} hasta calibrar el umbral con el tráfico propio
(recomendaciones~\ref{rec:monitor} y~\ref{rec:monitor-defecto}), por lo que la librería no puede ser
la única capa que bloquea. Los bloqueos indebidos medidos en aplicaciones de terceros
(Sección~\ref{sec:dis-despliegue}) sustentan esa recomendación, pero no demuestran que el WAF tenga
menos falsos positivos, cuya tasa no se midió.
```

Fuente: Pedido B1 y B2 del autor; cifras de docs/evidence/r4-analisis-20261025.json y docs/evidence/r5-verificacion-ronda4-20261025.json (sin cambio); la conclusión 9 (conc:fp) ya cita los bloqueos indebidos medidos; la tasa de falsos positivos del WAF no se midió.

### 131. X-B5-l: l-discusion.tex, línea original 263, línea actual 268

Ubicación: Cap. 9.5, subsunción por categoría y en el corpus completo.

Antes:

```
Por eso no puede afirmarse que la combinación supere a ambas capas en todas
las categorías, ni que ninguna subsuma a la otra.
```

Después:

```
Por eso no puede afirmarse que la combinación supere a ambas capas en todas
las categorías. En Path Traversal, SQL Injection y XSS la librería con cabeceras subsume al WAF; en
Command Injection el WAF bloquea 3 payloads que la librería con cabeceras deja pasar, de modo que en
el corpus completo ninguna capa subsume a la otra (el WAF aporta 3 y la librería 48).
```

Fuente: docs/evidence/r4-analisis-20261025.json: Config 2 con cabeceras bloquea todo lo que bloquea la 3b salvo cmdi_9, cmdi_51 y cmdi_94 (A2.d y d_cruce_todos_los_800); 3b menos 3a = 48.

### 132. X-B6-l: l-discusion.tex, línea original 231, línea actual 231

Ubicación: Cap. 9.5, efecto de la corrección del ejecutor en los 40 ataques de la Ronda 4.

Antes:

```
el ejecutor anterior no altera las peticiones de
esas categorías, aunque la ronda no se repitió con el ejecutor corregido.
```

Después:

```
la corrección del ejecutor solo cambia la
petición de los payloads de Path Traversal y de Command Injection que ya traen una secuencia
\texttt{\%XX}, y ninguno de los 40 ataques (11 de SQL Injection, 3 de XSS y 26 de Path Traversal)
la cambia: los 26 de Path Traversal no contienen \texttt{\%XX}, de modo que el ejecutor anterior,
que recodificaba los payloads ya codificados (Sección~\ref{sec:dis-oe3}), no los alteraba. Se
comprobó construyendo las peticiones de los 590 payloads con ambos ejecutores; solo difieren las de
los 200 de Command Injection, y la ronda no se repitió con el ejecutor corregido.
```

Fuente: docs/evidence/r6-ejecutor-peticiones-20261025.json (590 peticiones de la Ronda 4 construidas con ambos ejecutores sin red: distintas solo las 200 de Command Injection; los 40 ataques: 0 distintas) y diff de attack-sim/run_large_corpus.py entre 00ea3a3^ y 00ea3a3.

### 133. X-B6-k: k-resultados.tex, línea original 906, línea actual 906

Ubicación: Sec 8.4.3, efecto de la corrección del ejecutor en los 40 ataques de la Ronda 4.

Antes:

```
La corrección del ejecutor no altera las peticiones de esas
categorías, pero la ronda no se repitió con el ejecutor corregido.
```

Después:

```
La corrección del ejecutor solo cambia la petición de los payloads de Path
Traversal y de Command Injection que ya traen una secuencia \texttt{\%XX}; en los 40 ataques (11 de
SQLi, 3 de XSS y 26 de Path Traversal) no cambia ninguna, porque los 26 de Path Traversal no
contienen \texttt{\%XX} y el ejecutor anterior solo recodificaba los payloads ya codificados
(Sección~\ref{subsec:res-oe3-cobertura}). Se comprobó construyendo las peticiones de los 590
payloads con ambos ejecutores (solo difieren las de los 200 de Command Injection), y la ronda no se
repitió con el ejecutor corregido.
```

Fuente: docs/evidence/r6-ejecutor-peticiones-20261025.json (590 peticiones de la Ronda 4 construidas con ambos ejecutores sin red: distintas solo las 200 de Command Injection; los 40 ataques: 0 distintas) y diff de attack-sim/run_large_corpus.py entre 00ea3a3^ y 00ea3a3.

### 134. X-B3-l: l-discusion.tex, línea original 309, línea actual 318

Ubicación: Cap. 9.6, "Confirman" pasa a "Respaldan en parte".

Antes:

```
los resultados confirman dos de sus planteamientos y obligan a matizar un
tercero. Confirman el posicionamiento de un RASP como capa complementaria al WAF y no como su
sustituto, con una salvedad:
```

Después:

```
los resultados confirman uno de sus planteamientos, respaldan en parte otro
y obligan a matizar un tercero. Respaldan en parte el posicionamiento de un RASP como capa
complementaria al WAF y no como su sustituto, con una salvedad:
```

Fuente: Pedido B3 del autor (solo redacción); recuento de planteamientos ajustado en la oración inicial.

### 135. X-B3-l2: l-discusion.tex, línea original 313, línea actual 322

Ubicación: Cap. 9.6, razones de la cautela alineadas con 9.5 (consistencia).

Antes:

```
que no la sustituya se sostiene en el
alcance de cuatro clases de ataque, en la fragilidad del veredicto y en los bloqueos indebidos
(Sección~\ref{sec:dis-defensa}).
```

Después:

```
que no pueda afirmarse su sustitución se
sostiene en el alcance de cuatro clases de ataque, en la fragilidad del veredicto y en que la
configuración recomendada es el modo \texttt{monitor} hasta calibrar
(Sección~\ref{sec:dis-defensa}).
```

Fuente: Coherencia con X-B1-l (la tercera razón ya no son los bloqueos indebidos).

### 136. X-B2-c1: m-conclusiones.tex, línea original 115, línea actual 116

Ubicación: Conclusión conc:waf (B): formulación de prudencia.

Antes:

```
(B) La librería no sustituye al WAF. La cobertura de la Ronda~5
    casi no respalda esta afirmación: en condiciones equiparadas, la 3b frente a la Configuración~2
    con las cabeceras del proxy (794 de 800), el WAF suma solo 3 de 800 payloads (0.4~\%; 0.1--1.1~\%),
    todos de Command Injection.
```

Después:

```
(B) No se puede afirmar que la librería sustituya al WAF. La cobertura de la
    Ronda~5 no obliga a mantener el WAF: en condiciones equiparadas, la 3b frente a la
    Configuración~2 con las cabeceras del proxy (794 de 800), el WAF suma solo 3 de 800 payloads
    (0.4~\%; 0.1--1.1~\%), todos de Command Injection.
```

Fuente: Pedido B2 del autor; cifras sin cambio (docs/evidence/r4-analisis-20261025.json).

### 137. X-B1-c: m-conclusiones.tex, línea original 120, línea actual 121

Ubicación: Conclusión conc:waf (B): tercera razón sustituida por la conexión con el modo monitor.

Antes:

```
La afirmación se sostiene
    en otras razones: la librería se evaluó solo en cuatro clases de ataque, de modo que no hay
    evidencia de cobertura fuera de ellas; su veredicto depende de un voto de árbol y de las
    cabeceras del despliegue, pues cuatro cabeceras de proxy cambiaron el veredicto de 14 de los 800
    payloads y dos de los tres payloads de Command Injection que ninguna configuración bloquea quedan
    a 0.0167 del umbral; y los bloqueos indebidos medidos en aplicaciones de terceros
    (conclusión~\ref{conc:fp}), con un umbral calibrado sobre la partición de validación y la
    aplicación de referencia, sin que se haya medido la tasa de falsos positivos del WAF.
```

Después:

```
Esa cautela no descansa en la
    cobertura medida sino en razones de prudencia, no de medición: la librería se evaluó solo en
    cuatro clases de ataque, de modo que no hay evidencia de cobertura fuera de ellas; su veredicto
    depende de un voto de árbol y de las cabeceras del despliegue, pues cuatro cabeceras de proxy
    cambiaron el veredicto de 14 de los 800 payloads y dos de los tres payloads de Command Injection
    que ninguna configuración bloquea quedan a 0.0167 del umbral; y la configuración recomendada
    para la población objetivo es el modo \texttt{monitor} hasta calibrar el umbral con el tráfico
    propio (recomendaciones~\ref{rec:monitor} y~\ref{rec:monitor-defecto}), por lo que la librería no
    puede ser la única capa que bloquea. Los bloqueos indebidos medidos en aplicaciones de terceros
    (conclusión~\ref{conc:fp}) sustentan esa recomendación, pero no demuestran que el WAF tenga menos
    falsos positivos, cuya tasa no se midió.
```

Fuente: Pedido B1 del autor; 14 payloads y 0.0167: docs/evidence/r4-analisis-20261025.json y docs/evidence/e1-proxy-headers-20261025.json.

### 138. X-B7-c: m-conclusiones.tex, línea original 90, línea actual 90

Ubicación: Conclusión conc:variantes: XSS.

Antes:

```
(4 de los 200 payloads de SQL
    Injection coinciden por igualdad normalizada con alguna partición; ninguno de Path Traversal ni
    de Command Injection).
```

Después:

```
(4 de los 200 payloads de SQL
    Injection coinciden por igualdad normalizada con alguna partición; ninguno de Path Traversal ni
    de Command Injection; en XSS, 0 de 200 por igualdad del campo completo y 3 por subcadena
    normalizada).
```

Fuente: attack-sim/leakage_report_round5_all_20261025.json: xss, igualdad normalizada del campo completo 0 de 200; subcadena normalizada 3 de 200.

### 139. X-B2-r: n-recomendaciones.tex, línea original 40, línea actual 40

Ubicación: Recomendación 2: justificación B, resultado esperado en modo block y calibración previa.

Antes:

```
(B) La
    librería no sustituye al WAF: en condiciones equiparadas el WAF suma solo 3 de 800 payloads a la
    librería (0.1--1.1~\%), por lo que la cobertura de la Ronda~5 no respalda esta parte; se sostiene
    en que la librería se evaluó solo en cuatro clases de ataque, en que su veredicto depende de un
    voto de árbol y de las cabeceras del despliegue y en los bloqueos indebidos medidos
    (Conclusión~\ref{conc:fp}), sin que se haya medido la tasa de falsos positivos del WAF.
    \textit{Resultado esperado:} cobertura agregada no inferior a la de
    cada capa por separado (797 de 800 payloads con ambas capas, frente a 794 de la librería con las
    cabeceras del proxy y 749 del WAF solo).
```

Después:

```
(B) No se
    puede afirmar que la librería sustituya al WAF: en condiciones equiparadas el WAF suma solo 3 de
    800 payloads a la librería (0.1--1.1~\%), por lo que esta parte no descansa en la cobertura
    medida sino en razones de prudencia, no de medición: la librería se evaluó solo en cuatro clases
    de ataque, su veredicto depende de un voto de árbol y de las cabeceras del despliegue, y la
    configuración recomendada es el modo \texttt{monitor} hasta calibrar el umbral con el tráfico
    propio (recomendaciones~\ref{rec:monitor} y~\ref{rec:monitor-defecto}), por lo que la librería
    no puede ser la única capa que bloquea; los bloqueos indebidos medidos en aplicaciones de
    terceros (Conclusión~\ref{conc:fp}) sustentan esa configuración, pero no demuestran que el WAF
    tenga menos falsos positivos, cuya tasa no se midió. \textit{Resultado esperado:} cobertura
    agregada no inferior a la de cada capa por separado (797 de 800 payloads con ambas capas, frente
    a 794 de la librería con las cabeceras del proxy y 749 del WAF solo). Esas cifras se midieron con
    la librería en modo \texttt{block}; una instalación real exige antes la calibración de la
    recomendación~\ref{rec:monitor}.
```

Fuente: Pedido B1, B2 y B4 del autor; 797, 794 y 749: results_combined_config{3a,3b}_run1_20261025.json y results_s1_config2_con_cabeceras_run{1,2,3}_20261025.json; modo block: docs/evidence/r4-analisis-20261025.json (condiciones de las corridas, errata-d §1).

### 140. X-B8-r: n-recomendaciones.tex, línea original 133, línea actual 138

Ubicación: Recomendación 11: la repetición con el paquete 0.1.0 se redacta explícitamente con el ejecutor corregido.

Antes:

```
\textit{Acción:} con el paquete 0.1.1 del registro y el ejecutor corregido, repetir la cobertura con
    el paquete 0.1.0, las aplicaciones de terceros y el benchmark de rendimiento; repetir también
    las cuatro configuraciones
```

Después:

```
\textit{Acción:} con el paquete 0.1.1 del registro y el ejecutor corregido, repetir las
    aplicaciones de terceros y el benchmark de rendimiento, que no se midieron con ella; repetir con
    el ejecutor corregido la cobertura que se midió con el paquete 0.1.0, para separar el efecto del
    modelo, del middleware y del ejecutor; y repetir también las cuatro configuraciones
```

Fuente: Pedido B8 del autor; Sección 7.11 (no se midió el paquete 0.1.0 con el ejecutor corregido).

### 141. X-B2-l1: l-discusion.tex, línea original 233, línea actual 238

Ubicación: Cap. 9.5, cierre del párrafo de la Ronda 4 alineado con la formulación de prudencia (consistencia).

Antes:

```
no respalda
por sí solo que no lo sustituya.
```

Después:

```
no permite
por sí solo afirmar ni descartar que lo sustituya.
```

Fuente: Coherencia con X-B2-c1.



## Sexta ronda, retoques (ediciones 142 a 144)

Dos retoques de redacción. Respaldo previo en `docs/evidence/tex-before-round6c-20261025/` (24 archivos, sumas en `SHA256SUMS.txt`). Sin mediciones nuevas.

Evidencia de la comparación de las peticiones de los ejecutores (590 payloads de la Ronda 4), registrada para las ediciones 131 y 132 y para estas:

| Archivo | SHA-256 |
|---|---|
| `docs/evidence/r6-ejecutor-peticiones-20261025.py` | `43a3e1fde19bffbecc017243f0bfba047e5c081addc3fdd8aed1d86492ceeadc` |
| `docs/evidence/r6-ejecutor-peticiones-20261025.json` | `404e7f753aefeac1509a3f8ad72fd7819a1b8df2aadfd774142880b565c696e9` |

Verificación de los `.tex` tras todas las rondas: 0 líneas nuevas con comentarios `%` en los ocho archivos modificados (frente al respaldo `tex-before-20261025`), 147 etiquetas y 118 referencias sin huecos ni duplicados, llaves y entornos balanceados. No hay advertencias de compilación que informar porque no hay LaTeX en este equipo.

### 142. Y-c8: m-conclusiones.tex, línea original 121, línea actual 121

Ubicación: Conclusión conc:waf (B): "Esa cautela" pasa a "Mantener el WAF" (referente roto).

Antes:

```
Esa cautela no descansa en la
    cobertura medida
```

Después:

```
Mantener el WAF no descansa en la
    cobertura medida
```

Fuente: Solo redacción: el referente de "Esa cautela" era "no obliga a mantener el WAF".

### 143. Y-k: k-resultados.tex, línea original 911, línea actual 911

Ubicación: Sec 8.4.3: "solo difieren peticiones de Command Injection" y cita del script.

Antes:

```
payloads con ambos ejecutores (solo difieren las de los 200 de Command Injection), y la ronda no se
repitió con el ejecutor corregido.
```

Después:

```
payloads con ambos ejecutores (solo difieren peticiones de Command Injection; script
\texttt{docs/evidence/r6-ejecutor-peticiones-20261025.py} del repositorio
\texttt{logSguarDian-vulnerable-project}), y la ronda no se repitió con el ejecutor corregido.
```

Fuente: Evidencia de la verificación de los 590 payloads: docs/evidence/r6-ejecutor-peticiones-20261025.py y .json (SHA-256 abajo); resultado: distintas solo peticiones de Command Injection (200 de 200); SQLi, XSS y Path Traversal 390 de 390 idénticas; los 40: 0 distintas.

### 144. Y-l: l-discusion.tex, línea original 236, línea actual 236

Ubicación: Cap. 9.5: "solo difieren peticiones de Command Injection".

Antes:

```
solo difieren las de
los 200 de Command Injection, y la ronda no se repitió con el ejecutor corregido.
```

Después:

```
solo difieren peticiones
de Command Injection, y la ronda no se repitió con el ejecutor corregido.
```

Fuente: Ídem Y-k.



## Prefacio (edición 145)

Pedido del autor (2026-10-26): párrafo inicial adaptado del Prefacio del trabajo del componente de IA (sección Prefacio de DIEGOFINAL.pdf) y párrafo de agradecimientos. Solo se modificó `a-prefacio.tex`; respaldo en `docs/evidence/tex-before-prefacio-20261026/` (SHA-256 del respaldo en `SHA256SUMS.txt`). Se eliminaron las dos líneas de comentario que decían que el tomo no tenía agradecimientos, por haber quedado obsoletas. Sin cifras ni mediciones nuevas; 0 líneas nuevas con comentarios `%`.


## Portada (edición 146)

Pedido del autor (2026-10-26): activar `plantilla/portadacit.jpg` en la cubierta. `portada.tex` sobreescribía `\imagenportada` con `plantilla/fondologo_grande.png` (verde liso); se eliminó esa línea y su comentario, de modo que la portada usa la imagen definida en `0-datos_estudiante.tex` (`plantilla/portadacit.jpg`, idéntica a la de la plantilla oficial). Solo se modificó `portada.tex`; respaldo en `docs/evidence/tex-before-portada-20261026/`. `caratula.tex` (hoja blanca con el escudo) no se tocó. No se compiló (sin LaTeX en este equipo).
