# Delta de tesis — las cuatro configuraciones, misma aplicación, ejecutor corregido (2026-10-25)

Insumo para que otra persona corrija y agregue el texto de la tesis. No contiene redacción de
capítulos completos — solo cifras, procedencia y propuestas mínimas por sección.

## 1. Resumen

Se remidieron las cuatro configuraciones con la misma aplicación, la misma imagen, el mismo corpus
(800 payloads: 200 sqli, 200 path_traversal, 200 cmdi, 200 xss) y el mismo ejecutor corregido.
Config 3a, que antes se medía en una rama distinta con cambios en 91 archivos de la aplicación, se
reconstruyó en el mismo árbol activando solo el WAF (`LOGSGUARDIAN_DISABLED=true`). El hallazgo
central: Command Injection en 3a sube de 68.0 % (cifra anterior, ejecutor defectuoso) a 82.0 % —
confirma que el ejecutor defectuoso sí distorsionó la medición del WAF, no solo la de logSguarDian.
Los 68 ataques que antes se atribuían como "solo el WAF no bloqueó" ahora son 51 (1 sqli, 3 path
traversal, 36 cmdi, 11 xss); de esos, la 3b bloquea 48 y la 2 bloquea 44; quedan 3 payloads cmdi que
ninguna de las dos capas bloquea.

## 2. Tabla de procedencia

| Configuración | SHA base / rama | Digest de imagen | Compose | Paquete / hashes | Corpus | Ejecutor |
|---|---|---|---|---|---|---|
| 1 | `exp/ronda5-20261025` @ `07e80ead6a64db5db086216322624bc5bfa4edb0` (= `main`) | `lsgt6final20261025-app:a75c14208ccd` (local build, `Dockerfile` SHA-256 `7f1edcdd...`) | `docker-compose.yml` + `docker-compose.direct.yml`, `LOGSGUARDIAN_DISABLED=true` | n/a (sin protección) | `attack-sim/combined_corpus_round5_20261025.jsonl`, `f1fb0b0a2c552636358785ec323aa10c76519638d0da1cb62ce131be2330263d` | `run_large_corpus_fixed.py` / `send_xss_corpus.py` vía `run_combined_corpus_20261025.py` |
| 2 | idem | idem | `docker-compose.yml` + `docker-compose.direct.yml`, sin `LOGSGUARDIAN_DISABLED` | `logsguardian@0.1.1` (registro npm), tarball SHA-256 `abf8d5c47036d9c3a289bc36158f1caaa91b9504689aa97193e51c6808258d15` (coincide con el documentado), `rf.onnx`=`25b407e6...`, `if.onnx`=`5be28ee8...` (par C) | idem | idem |
| 3a | idem (unificada; antes: `origin/feat/waf-modsecurity-crs`, divergente en 91 archivos) | idem | `docker-compose.yml` + `docker-compose.waf-audit-override.yml` (nuevo, solo redirige el volumen de auditoría), `LOGSGUARDIAN_DISABLED=true` | n/a — confirmado: `detection_events` ni siquiera existe como tabla (la librería nunca se montó) | idem | idem |
| 3b | idem | idem | `docker-compose.yml` + `docker-compose.waf-audit-override.yml`, sin `LOGSGUARDIAN_DISABLED` | `logsguardian@0.1.1`, mismo tarball y mismos hashes de modelo que Config 2 (verificado por separado) | idem | idem |

**WAF (3a y 3b):** imagen `owasp/modsecurity-crs:nginx-alpine`, digest
`sha256:f12da37e72e29d1f06e7e829780f1016606d0799eac2966e58ef3819a3d30a50`. Nginx `1.30.5`,
ModSecurity `v3.0.17` (`libmodsecurity.so.3.0.17`), OWASP CRS `4.30.0`. `SecRuleEngine On`,
`blocking_paranoia_level=1`, `detection_paranoia_level=1`, `inbound_anomaly_score_threshold=5`,
`outbound_anomaly_score_threshold=4`. Exclusiones por defecto: **ninguna activa** — los dos archivos
de exclusión que trae el paquete CRS (`REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example`,
`RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example`) existen solo como `.conf.example`, y el
`Include` real del `setup.conf` solo carga `*.conf`; los plugins en `owasp-crs/plugins/` son los
cuatro `empty-*.conf` de plantilla, sin ninguno real habilitado.

**Ejecutor:** `attack-sim/run_large_corpus_fixed.py`, SHA-256
`422393460dfea808efe411d358166d37b662bbcaad77843ede0247c684c61af1`, extraído del commit `00ea3a3`
("test: verify logsguardian@0.1.1 closes the path_traversal gap to 100%") — ya ancestro de HEAD en
esta rama, byte idéntico al `run_large_corpus.py` trackeado actual. Verificado con tres fuentes
independientes: (1) el log de acceso de Nginx muestra `GET /posts/1/attachment?file=%252e%252e%252f...`
exactamente como lo trae el corpus, sin una capa adicional de codificación; (2) ModSecurity genera
puntajes de anomalía no nulos sobre los cuerpos POST con separadores codificados (`%26`, `%7c`,
`%0a`, `%3b`), señal de que procesó el contenido real, no una forma corrompida; (3) prueba de
captura de bytes (`attack-sim/test_harness_encoding.py`, de la tarea de corpus de XSS) ya había
confirmado fidelidad a nivel de byte para las mismas funciones reutilizadas aquí.

**Comando de reproducción (por configuración/corrida):**
```
COMPOSE_PROJECT_NAME=<propio> LOGSGUARDIAN_DISABLED=<true|unset> \
  docker compose -f docker-compose.yml [-f docker-compose.direct.yml | -f docker-compose.waf-audit-override.yml] \
  up -d --build db app [waf]
python3 attack-sim/run_combined_corpus_20261025.py <config> attack-sim/combined_corpus_round5_20261025.jsonl <run>
```

**Estado de git de esta tarea (sin commits, regla 5):** rama `exp/ronda5-20261025`, HEAD sin cambios
(`07e80ead6a64db5db086216322624bc5bfa4edb0`, idéntico antes y después). `git diff --stat` contra
archivos trackeados: vacío (ningún archivo con seguimiento fue modificado). 22 archivos/directorios
nuevos, todos sin seguimiento — lista completa con SHA-256 en
`docs/evidence/untracked-configs-20261025.txt`. El parche completo de la divergencia entre la rama
histórica de Config 3a (`origin/feat/waf-modsecurity-crs`) y esta rama compartida está en
`docs/evidence/app-diff-configs-20261025.patch` (91 archivos, 95153 líneas). Repositorio `logSguarDian`
(solo lectura): sin cambios propios de esta tarea.

## 3. Resultados

### 3.1 Tabla global k/n, porcentaje e IC95% Wilson (corrida 1, cifra principal)

Fórmula: `p=k/n; centro=(p+z²/2n)/(1+z²/n); margen=z·√(p(1-p)/n+z²/4n²)/(1+z²/n)`, `z=1.959963984540054`.

| Categoría | Config 1 | Config 2 | Config 3a | Config 3b |
|---|---|---|---|---|
| sqli | 0/200 (0.0%) [0.0,1.9] | 199/200 (99.5%) [97.2,99.9] | 199/200 (99.5%) [97.2,99.9] | 200/200 (100.0%) [98.1,100] |
| path_traversal | 0/200 (0.0%) [0.0,1.9] | 200/200 (100.0%) [98.1,100] | 197/200 (98.5%) [95.7,99.5] | 200/200 (100.0%) [98.1,100] |
| cmdi | 0/200 (0.0%) [0.0,1.9] | 185/200 (92.5%) [88.0,95.4] | 164/200 (82.0%) [76.1,86.7] | 197/200 (98.5%) [95.7,99.5] |
| xss | 0/200 (0.0%) [0.0,1.9] | 200/200 (100.0%) [98.1,100] | 189/200 (94.5%) [90.4,96.9] | 200/200 (100.0%) [98.1,100] |

### a) Config 1 — control

0 bloqueos en las 800 peticiones, en las tres corridas. Sin excepciones que reportar.

### b) Defense-in-depth: de los ataques que 3a no bloqueó, cuántos bloquea 3b y cuántos la 2

3a no bloqueó 51 de 800 (1 sqli, 3 path_traversal, 36 cmdi, 11 xss).

| Categoría | 3a no bloqueó | 3b bloqueó | 2 bloqueó |
|---|---|---|---|
| sqli | 1 | 1 | 1 |
| path_traversal | 3 | 3 | 3 |
| cmdi | 36 | 33 | 29 |
| xss | 11 | 11 | 11 |
| **Total** | **51** | **48** | **44** |

### c) Command Injection: separadores ya codificados (105/200) frente a sin codificar (95/200)

Confirmado: 105 de los 200 payloads de cmdi traen al menos un separador ya porcentual-codificado
(`%XX`); 95 no.

| Config | Codificados (n=105) | Sin codificar (n=95) |
|---|---|---|
| 1 | 0/105 (0.0%) | 0/95 (0.0%) |
| 2 | 95/105 (90.5%) [83.4,94.7] | 90/95 (94.7%) [88.3,97.7] |
| 3a | 80/105 (76.2%) [67.2,83.3] | 84/95 (88.4%) [80.5,93.4] |
| 3b | 104/105 (99.0%) [94.8,99.8] | 93/95 (97.9%) [92.7,99.4] |

**Sobre si el ejecutor defectuoso distorsionó el 68.0 % del WAF:** con el ejecutor corregido, el WAF
bloquea 88.4 % de los payloads sin codificar (no afectados por el defecto, ya que el defecto solo
alteraba payloads que el generador entregaba ya codificados) y 76.2 % de los codificados. Si el
68.0 % histórico (136/200) se descompone asumiendo que el subconjunto sin codificar se comportó
igual que ahora (no pudo ser afectado por un defecto que solo tocaba payloads ya codificados), el
subconjunto codificado histórico habría estado cerca de 50 % (136−84=52 de 105 ≈ 49.5 %), muy por
debajo del 76.2 % medido ahora. **Esto es una inferencia aritmética a partir de la cifra agregada
histórica, no una remedición directa del ejecutor defectuoso** — no se reconstruyó esa corrida
antigua ni se desglosó por separador en su momento, así que no hay un número histórico por
subcategoría contra el cual comparar directamente.

### d) Path Traversal: desglose por estilo de codificación

| Estilo | n | Config 1 | Config 2 | Config 3a | Config 3b |
|---|---|---|---|---|---|
| raw | 25 | 0% | 100% | 100% | 100% |
| backslash | 25 | 0% | 100% | 100% | 100% |
| url_single/mixed_case | 43 | 0% | 100% | 100% | 100% |
| url_double_encoded | 23 | 0% | 100% | 100% | 100% |
| overlong_utf8 | 19 | 0% | 100% | 100% | 100% |
| dot_dot_bypass (`....//`) | 21 | 0% | 100% | 90.5% (19/21) | 100% |
| null_byte_suffix | 29 | 0% | 100% | 100% | 100% |
| absolute_no_traversal | 15 | 0% | 100% | 93.3% (14/15) | 100% |

Los 3 fallos de 3a en path_traversal se concentran en dos estilos: 2 de `dot_dot_bypass` y 1 de
`absolute_no_traversal`. Ningún otro estilo de codificación presenta fallos en ninguna configuración
protegida.

### e) Payloads que ni el WAF (3a) ni la librería (2) bloquean

3 de 800, todos cmdi:

| id | payload |
|---|---|
| `cmdi_6` | `127.0.0.1\nnet user` |
| `cmdi_184` | `127.0.0.1;net user` |
| `cmdi_185` | `127.0.0.1%26cat /app/.env %23` |

Los dos primeros usan separadores sin codificar (`\n` y `;` literales); el tercero usa `%26` ya
codificado. 3b sí bloquea los tres (confirmado en la medición de capas, ver §3.3).

### f) Valor anterior frente a valor nuevo

| | Antes (ejecutor defectuoso en PT/cmdi; 3b atribuida al par A) | Ahora (ejecutor corregido; mismo árbol; 0.1.1 en 2 y 3b) |
|---|---|---|
| Config 1 | sqli 0/200, pt 0/200, cmdi 0/200, xss 0/1 | sqli 0/200, pt 0/200, cmdi 0/200, xss 0/200 |
| Config 2 | sqli 199/200, pt 200/200, cmdi 185/200, xss 1/1 | sqli 199/200, pt 200/200, cmdi 185/200, xss 200/200 |
| Config 3a | sqli 199/200, pt 197/200, cmdi 136/200 (68.0%), xss 1/1 | sqli 199/200, pt 197/200, **cmdi 164/200 (82.0%)**, xss 189/200 |
| Config 3b | sqli 200/200, pt 200/200, cmdi 197/200, xss 1/1 | sqli 200/200, pt 200/200, cmdi 197/200, xss 200/200 |
| "68 ataques solo-WAF-no-bloqueó" | 68 (1 sqli, 3 pt, 64 cmdi) | **51 (1 sqli, 3 pt, 36 cmdi, 11 xss)** |
| de esos, 3b bloqueó / 2 bloqueó | 65 / 64 | **48 / 44** |

sqli, path_traversal, Config 1 y Config 2 (ya medida con el ejecutor corregido en la Ronda 5
original) no cambian. El cambio real está enteramente en cmdi de Config 3a, y en la incorporación de
xss con un corpus real (antes n=1).

### 3.2 Estabilidad entre corridas

3 corridas por configuración, contenedor y base de datos reiniciados entre cada una (y el directorio
de auditoría del WAF vaciado antes de cada corrida de 3a/3b). **Cero cambios de veredicto por
payload** entre corridas, en las cuatro configuraciones (0 flips sobre 2400 comparaciones
payload×run posibles).

### 3.3 Atribución por capa en Config 3b (corrida 1)

Método: un bloqueo se atribuye a logSguarDian si existe una fila en `detection_events` (snapshot de
la base SQLite del contenedor, preservado antes de reiniciar) con `verdict=block` para ese
método+ruta, excluyendo las filas identificables como los dos *logins* propios del arnés
(`predicted_class=benign`, `verdict=pass_anomaly`, en `/login`). Se atribuye al WAF si la petición
nunca llegó a la aplicación (no hay fila correspondiente). No es un cruce por payload individual
(`detection_events` no guarda un identificador de petición) — es una atribución por categoría.
Detalle completo en `attack-sim/layer_attribution_config3b_run1_20261025.json`.

| Categoría | Total bloqueado (3b) | Atribuido a logSguarDian | Atribuido al WAF |
|---|---|---|---|
| sqli | 200 | 1 | 199 |
| path_traversal | 200 | 3 | 197 |
| cmdi | 197 | 33 | 164 |
| xss | 200 | 11 | 189 |

Los valores "atribuido al WAF" coinciden **exactamente**, categoría por categoría, con los
resultados medidos de forma independiente en Config 3a (WAF solo) — una validación cruzada fuerte de
que la atribución por capa es internamente consistente, no un artefacto del método de conteo.

También se observó, en `/admin/ping`, el mismo patrón de confusión de clase cmdi→sqli ya documentado
en `docs/config2-results-v1.md` y `k-resultados.tex:376-378` (29 de 33 eventos de cmdi bloqueados en
Config 3b se etiquetaron `predicted_class=sqli`). No afecta el conteo de bloqueo.

## 4. Cambios por sección de la tesis

| Ubicación | Valor/texto actual | Qué cambia | Propuesta mínima |
|---|---|---|---|
| Cuadro 38 y su nota | Config 3a cmdi 136/200 (68.0%); nota de "68 ataques solo-WAF-no-bloqueó, 3b bloqueó 65, 2 bloqueó 64" | Config 3a cmdi sube a 164/200 (82.0%); el total de ataques solo-WAF-no-bloqueó baja a 51, con desglose por categoría distinto | Reemplazar la fila de Config 3a y la nota con las cifras de §3.1/§3.1(f) de este documento; agregar la columna xss (antes ausente del cuadro por n=1). |
| Sección 8.4.3 (texto sobre 3a, 3b y los 68 ataques) | Describe 68 ataques y la cifra 65/64 | Debe describir 51 ataques y 48/44, con la aclaración de que la medición anterior de 3a venía de una rama con la aplicación en otra versión | Reescribir el párrafo citando §3.1(b) y §3.1(f); agregar una frase explicando que esta ronda unificó las cuatro configuraciones en el mismo árbol de trabajo. |
| Cuadro 37 | Cifras de Config 2 (ya correctas, ejecutor corregido, 0.1.1) | Sin cambio en Config 2; si el cuadro incluye Config 3a/3b, esas filas sí cambian igual que el Cuadro 38 | Sin cambio en la fila de Config 2; actualizar 3a/3b si están presentes ahí también. |
| Sección 7.4.4 / Procedimiento 4.1 (misma aplicación e imagen en las 4 configs) | Afirma que las cuatro usan la misma aplicación e imagen | Antes esto **no era cierto** para 3a (medida en `feat/waf-modsecurity-crs`, divergente en 91 archivos); ahora sí lo es, con el mecanismo documentado (`LOGSGUARDIAN_DISABLED` sobre el mismo `docker-compose.yml`) | "Las cuatro configuraciones corren sobre la misma rama, el mismo Dockerfile y el mismo árbol de trabajo (confirmado en esta ronda); 3a y 3b comparten exactamente el mismo stack de Compose, distinguidas solo por la variable `LOGSGUARDIAN_DISABLED`." |
| Sección 7.11 (amenazas a la validez: "benchmark no repetido", ejecutor anterior) | Señala el ejecutor defectuoso como amenaza pendiente de resolver para 3a/3b | Resuelta para este corpus y esta ronda — agregar el resultado, no solo la advertencia | "Resuelto en esta ronda: las cuatro configuraciones se remidieron con el ejecutor corregido sobre el mismo árbol de la aplicación; ver [sección]." |
| Sección 7.12 | Puede listar la falta de corpus de XSS o la medición cruzada entre ramas como restricción | Ya no aplica en los mismos términos | Actualizar según lo que diga exactamente esa sección — revisar contra §3 de este documento. |
| Discusión | Probablemente cita el 68.0% de 3a en cmdi como evidencia de debilidad del WAF frente a cmdi | El WAF es más fuerte de lo reportado (82.0%), aunque sigue siendo la capa más débil para cmdi frente a logSguarDian (92.5-98.5%) | "El WAF solo, con el ejecutor corregido, bloquea 82.0% de Command Injection (antes reportado 68.0% por un defecto del arnés de medición) — sigue siendo el punto más débil del WAF frente a las otras tres categorías, pero la brecha con logSguarDian es menor de lo que se pensaba." |
| Conclusiones sobre defensa en profundidad | Cita 37/40 o 65/68 como el valor de complementariedad | Ahora es 48/51 (3b) y 44/51 (2 sola) sobre lo que el WAF no detecta | Actualizar la cifra citando §3.1(b); la conclusión cualitativa (las capas se complementan, ninguna subsume a la otra) se mantiene — ver §5. |
| Cuadros 40 y 41 (indicadores y cumplimiento de OE3) | Si citan el 68.0% o la medición cruzada de 3a | Actualizar a 82.0% y a "medido en el mismo árbol" | Reemplazar la cifra y la nota de procedencia. |
| Resumen y abstract | Si mencionan explícitamente la cifra de 68.0% o "65 de 68" | Ya no son exactos | Revisar si el resumen/abstract cita estas cifras puntuales; si no lo hace, sin cambio. |

## 5. Afirmaciones que dejan de ser ciertas / que siguen siendo ciertas

**Dejan de ser ciertas (tal como estaban escritas):**
- "El WAF bloquea 68.0% de Command Injection" — era un artefacto del ejecutor defectuoso; la cifra
  real, con el mismo árbol y el ejecutor corregido, es 82.0%.
- "Las cuatro configuraciones usan la misma aplicación y la misma imagen Docker" — no era cierto
  para 3a tal como se midió originalmente (rama `feat/waf-modsecurity-crs`, divergente en 91
  archivos, incluidas rutas, vistas y middleware). Ahora sí es cierto, con esta remedición.
- "De los 68 ataques que el WAF solo no bloqueó, la 3b bloqueó 65 y la 2 bloqueó 64" — las cifras
  correctas son 51/48/44.

**Siguen siendo ciertas, sin cambio:**
- La ventaja relativa del WAF en Path Traversal y SQLi sobre logSguarDian solo (Config 2) **se
  mantiene**: 3a iguala a 2 en sqli (199/200 ambas) y queda muy cerca en path_traversal (197 vs 200).
  No fue una distorsión del ejecutor — los payloads de sqli/path_traversal no dependen de los
  separadores que el defecto corrompía.
- La complementariedad de las capas (ninguna subsume a la otra, 3b supera a ambas individualmente en
  todas las categorías medidas) **se mantiene**, con cifras más bajas pero la misma conclusión
  cualitativa: 48 de 51 ataques que el WAF solo no detecta sí los detecta la capa combinada.
- El patrón de confusión de clase cmdi→sqli en los eventos de logSguarDian **se mantiene**,
  reproducido de forma independiente en esta ronda.

## 6. Hechos verificados frente a hipótesis

**Hechos verificados (medidos en esta sesión, con evidencia en archivo):**
- Config 3a (mismo árbol): cmdi 164/200 (82.0%), path_traversal 197/200, sqli 199/200, xss 189/200.
  Tres corridas idénticas, cero flips.
- `detection_events` no existe como tabla en el contenedor de Config 3a — la librería nunca se montó.
- Paquete 0.1.1 verificado byte a byte (tarball y ambos modelos) en Config 2 y Config 3b por
  separado, mismos hashes en ambas.
- WAF: Nginx 1.30.5, ModSecurity 3.0.17, CRS 4.30.0, sin exclusiones activas por defecto.
- Los valores "atribuido al WAF" en la medición por capas de 3b coinciden exactamente con los
  valores medidos de forma independiente en 3a, categoría por categoría.

**Hipótesis / interpretación (no medidas directamente):**
- Que el 68.0% histórico de cmdi en 3a corresponde a un subconjunto codificado cercano al 50% — es
  una inferencia aritmética a partir de la cifra agregada histórica (§3.1c), no una remedición del
  ejecutor defectuoso. No se volvió a correr la versión con el defecto para confirmarlo directamente.
- Que los 3 payloads que ninguna capa bloquea (`cmdi_6`, `cmdi_184`, `cmdi_185`) representan una
  categoría real de evasión (separadores sin codificar y `/app/.env` como objetivo) y no un
  artefacto — es razonable dado el patrón, pero no se investigó la causa exacta en el middleware ni
  en las reglas de CRS.

## 7. Desviaciones, limitaciones y amenazas nuevas

- **Sin commits (regla 5):** todo el trabajo de esta tarea vive sin confirmar en
  `exp/ronda5-20261025`. El estado se reconstruye con el SHA base (`07e80ead6a64db5db086216322624bc5bfa4edb0`,
  igual antes y después), el parche de divergencia (`docs/evidence/app-diff-configs-20261025.patch`)
  y los hashes de cada archivo nuevo (`docs/evidence/untracked-configs-20261025.txt`), no con
  historial de git.
- **Rama compartida con la tarea de corpus de XSS:** esta tarea reutilizó sin modificar
  `attack-sim/xss_corpus_filtered_20261025.jsonl`, `generate_xss.py`, `send_xss_corpus.py` y
  `run_large_corpus_fixed.py` que esa tarea dejó en el mismo árbol de trabajo. Verificado que el
  hash del corpus de XSS coincide con `docs/freeze-xss-20261025.json` antes de usarlo.
- **`waf/audit/audit.log` está trackeado por git** (598 líneas) y el WAF lo sigue escribiendo en
  cada arranque — correr 3a/3b sin redirigirlo habría modificado un archivo con seguimiento,
  prohibido por la regla 7. Se resolvió con `docker-compose.waf-audit-override.yml` (archivo nuevo,
  no modifica `docker-compose.yml`), que redirige el volumen a `attack-sim/waf-audit-20261025/`
  (directorio nuevo). El archivo trackeado se verificó sin cambios (598 líneas, antes y después).
- **Atribución por capa en 3b es por categoría, no por payload individual** — `detection_events` no
  guarda un identificador de petición que permita unir cada fila con un id exacto del corpus; la
  unión se hizo por método+ruta, excluyendo los dos logins del arnés por `predicted_class=benign`.
  Es un método razonable (validado cruzando contra 3a, que coincide exactamente), pero no es un
  join determinista payload-por-payload.
- **El 68.0% histórico no se puede descomponer directamente por separador** — no existe un registro
  por-payload de esa corrida antigua con el desglose codificado/sin-codificar; la comparación de
  §3.1(c) es una inferencia aritmética sobre la cifra agregada, declarada como tal.
- **No se investigó la causa exacta de los 3 payloads que evaden ambas capas** ni se tocó el modelo,
  el umbral, el filtro de CRS o la librería para intentar cerrarlos — por la regla 1 del protocolo
  (no ajustar nada para mejorar resultados).
- **Config 3a y 3b corrieron con `--build` en cada arranque**, reutilizando la caché de capas de
  Docker dado que el contexto de build no cambió entre corridas; no se verificó el digest de imagen
  arranque por arranque, solo al final (`a75c14208ccd`, consistente con una única imagen cacheada).

## 8. Qué NO cambia

- No se tocó la librería, el modelo, el umbral, ninguna regla de CRS ni el filtro de exclusión de
  payloads — regla 1 cumplida.
- No se modificó `docker-compose.yml` para construir Config 3a: la unificación se logró con la
  variable de entorno `LOGSGUARDIAN_DISABLED`, ya soportada por el archivo existente.
- Config 1 y Config 2 no cambian respecto a lo ya reportado con el ejecutor corregido (Cuadro 37);
  solo se confirmaron de nuevo como parte de la corrida unificada.
- No se hizo ningún commit, push ni PR. Todo el trabajo está sin confirmar en
  `exp/ronda5-20261025`, en ambos repos, documentado en la sección 2.
