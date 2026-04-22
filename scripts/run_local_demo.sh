#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

EXPORT_LIMIT="${MMR_EXPORT_LIMIT:-200}"
BUNDLE_PATH="${MMR_APP_BUNDLE_PATH:-artifacts/streamlit/app_bundle.json}"
SERVER_ADDRESS="${MMR_SERVER_ADDRESS:-127.0.0.1}"
SERVER_PORT="${MMR_SERVER_PORT:-8768}"
STREAMLIT_HEADLESS="${MMR_SERVER_HEADLESS:-true}"

python3 scripts/export_streamlit_bundle.py --limit "$EXPORT_LIMIT"

if fuser -n tcp "$SERVER_PORT" >/dev/null 2>&1; then
  PORT_PIDS="$(fuser -n tcp "$SERVER_PORT" 2>/dev/null || true)"
  for pid in $PORT_PIDS; do
    cmd="$(ps -p "$pid" -o args= 2>/dev/null || true)"
    if [[ "$cmd" == *streamlit* ]]; then
      kill "$pid" 2>/dev/null || true
    fi
  done
  sleep 1
fi

if fuser -n tcp "$SERVER_PORT" >/dev/null 2>&1; then
  echo "Port $SERVER_PORT is still in use. Set MMR_SERVER_PORT to override it, for example: MMR_SERVER_PORT=8770 ./scripts/run_local_demo.sh" >&2
  exit 1
fi

MMR_APP_BUNDLE_PATH="$BUNDLE_PATH" \
uv run --with streamlit streamlit run zerve/app/streamlit_app.py \
  --server.headless "$STREAMLIT_HEADLESS" \
  --server.address "$SERVER_ADDRESS" \
  --server.port "$SERVER_PORT"
