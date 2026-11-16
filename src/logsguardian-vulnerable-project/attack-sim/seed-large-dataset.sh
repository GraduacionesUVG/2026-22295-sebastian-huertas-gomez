#!/usr/bin/env bash
# Seeds the "volume" latency scenario: adds 2000 rows to `posts` (10 existing
# + 2000 generated = 2010 total) via db/seed-large.sql, executed against the
# already-running `db` service. Idempotent is NOT guaranteed - running this
# twice against the same db container appends another 2000 rows each time
# (there's no ON CONFLICT guard, generated titles aren't unique). Callers
# (run_latency_suite.sh, the CI workflow) must call this exactly once per
# fresh db container.
#
# Usage:
#   attack-sim/seed-large-dataset.sh [compose-project-args...]
#
# Any extra arguments are forwarded to `docker compose` verbatim, so this
# can be pointed at whatever compose invocation started the stack, e.g.:
#   attack-sim/seed-large-dataset.sh -f docker-compose.yml -f docker-compose.direct.yml
#
# With no arguments, defaults to the same compose files the CI workflow uses.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SEED_SQL="$REPO_ROOT/db/seed-large.sql"

if [ "$#" -eq 0 ]; then
  set -- -f "$REPO_ROOT/docker-compose.yml" -f "$REPO_ROOT/docker-compose.direct.yml"
fi

cd "$REPO_ROOT"

echo "[seed-large-dataset] applying db/seed-large.sql (2000 rows) to the running db service..."
docker compose "$@" exec -T db \
  psql -U notesuser -d notesdb -v ON_ERROR_STOP=1 < "$SEED_SQL"

COUNT="$(docker compose "$@" exec -T db \
  psql -U notesuser -d notesdb -tA -c 'SELECT COUNT(*) FROM posts;' | tr -d '[:space:]')"

echo "[seed-large-dataset] posts table now has ${COUNT} rows (expected 2010)."
if [ "$COUNT" != "2010" ]; then
  echo "[seed-large-dataset] WARNING: row count is not exactly 2010 - either this script ran more than once against the same db, or db/init.sql's seed changed. Not treated as fatal, but the 'volume' scenario's numbers should be reported with the actual row count, not assumed to be 2010." >&2
fi
