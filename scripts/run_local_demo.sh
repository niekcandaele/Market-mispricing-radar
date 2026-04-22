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

MMR_APP_BUNDLE_PATH="$BUNDLE_PATH" \
uv run --with streamlit streamlit run zerve/app/streamlit_app.py \
  --server.headless "$STREAMLIT_HEADLESS" \
  --server.address "$SERVER_ADDRESS" \
  --server.port "$SERVER_PORT"
