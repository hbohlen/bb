#!/usr/bin/env bash
# Launch a headless Chromium with CDP open against the fork's dev server.
#
# The measurement scripts need a CDP websocket with a stable port, which
# agent-browser does not expose (it picks one per session). Chrome rejects the
# CDP socket unless it is started with a remote-allow-origins wildcard, so
# suppress_origin alone is not enough.
#
# Usage: docs/design/scripts/launch-s26.sh [port]
set -euo pipefail

PORT="${1:-40673}"
APP_URL="${APP_URL:-http://127.0.0.1:11580}"
CHROME="$(ls -d "$HOME"/.cache/ms-playwright/chromium-*/chrome-linux64/chrome | sort -V | tail -1)"

if curl -fsS -o /dev/null "http://127.0.0.1:${PORT}/json/version" 2>/dev/null; then
  echo "CDP already listening on ${PORT}"
  exit 0
fi

rm -rf /tmp/bb-s26-profile
"$CHROME" \
  --headless=new \
  --remote-debugging-port="$PORT" \
  --remote-allow-origins='*' \
  --user-data-dir=/tmp/bb-s26-profile \
  --no-first-run \
  --no-default-browser-check \
  --disable-gpu \
  --window-size=412,891 \
  "$APP_URL" >/tmp/bb-s26-chrome.log 2>&1 &

for _ in $(seq 1 40); do
  if curl -fsS -o /dev/null "http://127.0.0.1:${PORT}/json/version" 2>/dev/null; then
    echo "CDP ready on ${PORT}; browser at ${APP_URL}"
    exit 0
  fi
  sleep 0.5
done

echo "Chrome did not open CDP on ${PORT}; see /tmp/bb-s26-chrome.log" >&2
exit 1