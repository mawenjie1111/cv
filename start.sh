#!/usr/bin/env bash
# Start the FastAPI backend and Vue frontend together.
# Usage: ./start.sh        (installs deps if missing, then runs both)
#        SKIP_INSTALL=1 ./start.sh   (skip dependency install)
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

# Pick a Python launcher that exists on this machine.
if command -v python >/dev/null 2>&1; then
  PY=python
elif command -v py >/dev/null 2>&1; then
  PY=py
else
  echo "Error: Python not found on PATH." >&2
  exit 1
fi

# Install dependencies unless explicitly skipped.
if [ "${SKIP_INSTALL:-0}" != "1" ]; then
  echo "==> Installing backend dependencies"
  "$PY" -m pip install -r "$BACKEND_DIR/requirements.txt"

  echo "==> Installing frontend dependencies"
  (cd "$FRONTEND_DIR" && npm install)
fi

PIDS=()

# Kill both child processes when this script exits or is interrupted.
cleanup() {
  echo
  echo "==> Shutting down"
  for pid in "${PIDS[@]:-}"; do
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
    fi
  done
}
trap cleanup EXIT INT TERM

echo "==> Starting backend at http://localhost:8000"
(cd "$BACKEND_DIR" && exec "$PY" -m uvicorn app.main:app --reload) &
PIDS+=("$!")

echo "==> Starting frontend at http://localhost:5173"
(cd "$FRONTEND_DIR" && exec npm run dev) &
PIDS+=("$!")

echo "==> Both running. Press Ctrl+C to stop."
# Wait on all children; exit as soon as either one stops.
wait -n
