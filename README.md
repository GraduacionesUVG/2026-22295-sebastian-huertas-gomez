# logSguarDian

## Descripción

logSguarDian es una librería npm que funciona como middleware RASP (*Runtime Application
Self-Protection*) para aplicaciones Node.js/Express. Se monta en el pipeline de la aplicación y
analiza cada petición HTTP en tiempo de ejecución, sin bloquear el Event Loop, para detectar y
clasificar cuatro vectores de ataque: SQL Injection, Cross-Site Scripting (XSS), Path
Traversal/Local File Inclusion y Command Injection.

La detección usa un modelo híbrido de aprendizaje automático: un Random Forest supervisado
(autoridad de bloqueo) y un Isolation Forest no supervisado (detección de anomalías,
solo registro), ambos serializados en ONNX y ejecutados en `worker_threads` dedicados. El
proyecto está dirigido a startups y pequeñas empresas sin un departamento formal de
ciberseguridad, como una capa de defensa adicional —no un sustituto— de un WAF tradicional.

Este repositorio contiene dos componentes, bajo `src/`:

- **`src/logsguardian/`** — el monorepo de la librería: el pipeline de extracción de
  características, el entrenamiento del modelo y el paquete publicable `logsguardian`
  (publicado en [npmjs.com](https://www.npmjs.com/package/logsguardian)).
- **`src/logsguardian-vulnerable-project/`** — una aplicación de notas deliberadamente
  vulnerable, usada como entorno de referencia para evaluar la librería en los cuatro
  vectores de ataque, con y sin protección, y en conjunto con un WAF (ModSecurity + OWASP CRS).

## Tecnologías Utilizadas

- Node.js / TypeScript
- Express (middleware, peer dependency)
- Random Forest + Isolation Forest (modelo híbrido de clasificación/detección de anomalías)
- ONNX y `onnxruntime-node` (inferencia del modelo en producción)
- `worker_threads` (inferencia asíncrona sin bloquear el Event Loop)
- `better-sqlite3` (registro de eventos de detección)
- pnpm workspaces (monorepo de la librería)
- Jest (pruebas unitarias y end-to-end)
- Python y scikit-learn (entrenamiento del modelo, fuera de la ruta de ejecución en producción)
- Docker y Docker Compose (aplicación de referencia y escenarios de evaluación)
- PostgreSQL (base de datos de la aplicación de referencia)
- Nginx + ModSecurity v3 + OWASP Core Rule Set (WAF, para los escenarios en capas)

## Requisitos Previos

- Node.js v20 o superior
- pnpm (para construir y probar el monorepo de la librería)
- Docker y Docker Compose (para levantar la aplicación de referencia)
- npm (incluido con Node.js, usado dentro de la aplicación de referencia)

## Instalación

El repositorio tiene dos partes independientes: la librería (`src/logsguardian`) y la
aplicación de referencia que la usa (`src/logsguardian-vulnerable-project`).

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/xtsebas/2026-22295-sebastian-huertas-gomez.git
   cd 2026-22295-sebastian-huertas-gomez
   ```

2. Construir y probar la librería:
   ```bash
   cd src/logsguardian
   pnpm install
   pnpm run build
   pnpm run test
   ```

3. Levantar la aplicación de referencia con Docker (desde otra terminal, en la raíz del repo):
   ```bash
   cd src/logsguardian-vulnerable-project
   docker compose -f docker-compose.yml -f docker-compose.direct.yml up -d --build db app
   ```
   La aplicación queda disponible en `http://localhost:3000`. Por defecto corre en modo
   protegido (logSguarDian activo, modo `block`). Para levantarla sin protección, como
   línea base de comparación:
   ```bash
   LOGSGUARDIAN_DISABLED=true docker compose -f docker-compose.yml -f docker-compose.direct.yml up -d --build db app
   ```

Ambos pasos son independientes y reproducibles: el paso 2 no requiere Docker, y el paso 3 no
requiere pnpm (la aplicación de referencia instala `logsguardian` desde el registro de npm
como una dependencia normal, vía `npm install` dentro de su propia imagen).

## Ejecución

Con la aplicación de referencia levantada (paso 3):

- Probar un ataque de SQL Injection (bypass de autenticación) contra `/login`:
  ```bash
  curl -i "http://localhost:3000/login" -X POST \
    --data-urlencode "username=' OR '1'='1' --" --data-urlencode "password=x"
  ```
  Sin protección devuelve una sesión válida; con protección devuelve `403 Forbidden`.

- Ver el catálogo de ataques detectados:
  ```bash
  docker exec logsguardian-vulnerable-project-app-1 npx logsguardian attacks list
  ```

- Bajar el stack al terminar:
  ```bash
  cd src/logsguardian-vulnerable-project
  docker compose -f docker-compose.yml -f docker-compose.direct.yml down
  ```

### Si `attacks list` no muestra nada ("se queda trabada")

`npx logsguardian config init` genera `logsguardian.config.js` con `dbPath: './logsguardian.db'`
por defecto, pero `src/app.js` monta el middleware con su propio `dbPath` fijo
(`/app/logsguardian-events.db`). Son dos archivos distintos: el middleware sí escribe eventos,
pero el CLI lee del otro archivo, vacío — por eso `attacks list` no muestra nada aunque haya
ataques bloqueados. El arreglo es apuntar el config al archivo real, dentro del contenedor:

```bash
docker exec logsguardian-vulnerable-project-app-1 sed -i \
  "s|dbPath: './logsguardian.db'|dbPath: '/app/logsguardian-events.db'|" \
  /app/logsguardian.config.js
```

## Comandos de logSguarDian

Todos los comandos, excepto `config init`, requieren que exista `logsguardian.config.js` en el
directorio actual (se genera con `config init`). Se ejecutan dentro del contenedor de la
aplicación, por ejemplo: `docker exec logsguardian-vulnerable-project-app-1 npx logsguardian <comando>`.

| Grupo | Comando | Qué hace |
|---|---|---|
| config | `config init` | Genera `logsguardian.config.js` con los valores por defecto |
| config | `config show` | Imprime la configuración activa (modo, umbral, modelo, dbPath) |
| config | `config set <clave> <valor>` | Cambia una clave de configuración (`threshold`, `mode`, `model`, `telemetry`) |
| config | `config validate` | Valida que la configuración sea coherente y que los modelos existan |
| attacks | `attacks list` | Catálogo de tipos de ataque detectados, con conteo y última detección |
| attacks | `attacks summary` | Distribución de ataques por endpoint, periodo y severidad |
| attacks | `attacks inspect <clase>` | Tasa de detección, features principales y ejemplos de payloads para una clase |
| endpoints | `endpoints top` | Rutas ordenadas por frecuencia de ataques detectados |
| endpoints | `endpoints profile <ruta>` | Perfil detallado de una ruta: tipos de ataque, distribución horaria, IPs de origen |
| endpoints | `endpoints report` | Exporta el análisis completo de endpoints (JSON o CSV) |
| webhooks | `webhooks add <url>` | Registra un webhook (solo HTTPS) para avisar en cada detección |
| webhooks | `webhooks remove <id>` | Elimina un webhook registrado |
| webhooks | `webhooks test <id>` | Envía un payload de prueba al webhook sin esperar una detección real |
| webhooks | `webhooks list` | Lista los webhooks registrados |

## Capturas

Las capturas de pantalla del proyecto se encuentran en [`/capturas`](./capturas), 10 en total
(`captura-01.png` a `captura-10.png`): instalación y configuración de la librería, un ataque
sin protección y el mismo ataque bloqueado, el registro de detecciones vía CLI, y resultados
de evaluación del modelo.

## Demo

El video demostrativo se encuentra en [`/demo/demo.mp4`](./demo/demo.mp4).

## Documentación

El informe final del proyecto está disponible en
[`/docs/informe_final.pdf`](./docs/informe_final.pdf).

El consentimiento de uso de foto y video firmado se encuentra en
[`/docs/consentimiento_firmado.pdf`](./docs/consentimiento_firmado.pdf).

## Autores

- Sebastián Huertas Gómez — Carnet 22295
- Diego Pablo Valenzuela Palacios - Carnet 22309

## Licencia

MIT
