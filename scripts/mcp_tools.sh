#!/usr/bin/env bash
set -euo pipefail

url="${1:-http://127.0.0.1:7333/mcp}"
mode="${2:-}"

headers="$(curl -sS -D - -o /dev/null "$url" \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"curl","version":"0.1"},"capabilities":{}}}')"

session_id="$(printf "%s" "$headers" | awk -F': ' 'tolower($1)=="mcp-session-id"{print $2}' | tr -d '\r')"

response="$(curl -sS "$url" \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  -H "mcp-session-id: ${session_id}" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{"cursor":null}}' \
  | awk -F'data: ' '/^data: /{print $2}')"

if [[ "$mode" == "--raw" ]]; then
  printf '%s\n' "$response"
  exit 0
fi

python - <<'PY' "$response"
import json
import sys

data = json.loads(sys.argv[1])
tools = data.get("result", {}).get("tools", [])
for tool in tools:
    name = tool.get("name", "")
    desc = (tool.get("description") or "").strip()
    line = f"{name}: {desc}" if desc else name
    print(line)
PY
