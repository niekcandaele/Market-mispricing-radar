#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

SERVER_PORT="${MMR_SERVER_PORT:-8768}"
SERVER_ADDRESS="${MMR_SERVER_ADDRESS:-127.0.0.1}"
APP_URL="http://${SERVER_ADDRESS}:${SERVER_PORT}"
LAUNCH_LOG="${MMR_LAUNCH_LOG:-/tmp/mmr-safe-local-demo.log}"
EVIDENCE_DIR="${MMR_SAFE_LOCAL_EVIDENCE_DIR:-${ROOT_DIR}/artifacts/safe-local-demo}"
ARCHIVE_ROOT="${MMR_SAFE_LOCAL_ARCHIVE_ROOT:-${ROOT_DIR}/artifacts/archive}"
ARCHIVE_DAY="$(date +%F)"
ARCHIVE_DIR="${ARCHIVE_ROOT}/${ARCHIVE_DAY}/market-mispricing-radar"
UTC_STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
FINAL_EVIDENCE_PATH="${EVIDENCE_DIR}/safe-local-demo-${UTC_STAMP}.json"
TMP_RESULT="$(mktemp)"
LAUNCH_PID=""

cleanup() {
  if [[ -n "$LAUNCH_PID" ]] && kill -0 "$LAUNCH_PID" 2>/dev/null; then
    kill "$LAUNCH_PID" 2>/dev/null || true
    wait "$LAUNCH_PID" 2>/dev/null || true
  fi
  rm -f "$TMP_RESULT"
  fuser -k -n tcp "$SERVER_PORT" >/dev/null 2>&1 || true
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

MMR_VERIFY_URL="$APP_URL" node scripts/verify_safe_local_recording_flow.js >"$TMP_RESULT"
mkdir -p "$EVIDENCE_DIR" "$ARCHIVE_DIR"
shopt -s nullglob
for old_path in "$EVIDENCE_DIR"/safe-local-demo-*.json; do
  mv "$old_path" "$ARCHIVE_DIR"/
done
shopt -u nullglob
mv "$TMP_RESULT" "$FINAL_EVIDENCE_PATH"
chmod 664 "$FINAL_EVIDENCE_PATH"
cat "$FINAL_EVIDENCE_PATH"
printf '\nEvidence path: %s\n' "$FINAL_EVIDENCE_PATH" >&2
