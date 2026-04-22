#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

SERVER_PORT="${MMR_SERVER_PORT:-8768}"
SERVER_ADDRESS="${MMR_SERVER_ADDRESS:-127.0.0.1}"
APP_URL="http://${SERVER_ADDRESS}:${SERVER_PORT}"
LAUNCH_LOG="${MMR_LAUNCH_LOG:-/tmp/mmr-safe-local-demo.log}"
LAUNCH_PID=""

cleanup() {
  if [[ -n "$LAUNCH_PID" ]] && kill -0 "$LAUNCH_PID" 2>/dev/null; then
    kill "$LAUNCH_PID" 2>/dev/null || true
    wait "$LAUNCH_PID" 2>/dev/null || true
  fi
  fuser -k -n tcp "$SERVER_PORT" 2>/dev/null || true
}
trap cleanup EXIT

./scripts/run_local_demo.sh >"$LAUNCH_LOG" 2>&1 &
LAUNCH_PID=$!

for _ in $(seq 1 60); do
  if curl -fsS "$APP_URL" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

if ! curl -fsS "$APP_URL" >/dev/null 2>&1; then
  echo "Safe local demo did not become reachable at $APP_URL" >&2
  echo "Launcher log:" >&2
  cat "$LAUNCH_LOG" >&2 || true
  exit 1
fi

MMR_VERIFY_URL="$APP_URL" node scripts/verify_safe_local_recording_flow.js
