#!/usr/bin/env bash
set -euo pipefail

url="${1:-http://127.0.0.1:7333/mcp}"
tool="${2:-}"
args_json="${3:-}"

if [[ -z "$tool" || -z "$args_json" ]]; then
  echo "Usage: $0 [url] <tool_name> '<json_arguments>'" >&2
  echo "Example:" >&2
  echo "  $0 http://127.0.0.1:7333/mcp run_dna '{\"params\":{\"dna\":\"ATCG\"}}'" >&2
  exit 1
fi

headers="$(curl -sS -D - -o /dev/null "$url" \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"curl","version":"0.1"},"capabilities":{}}}')"

session_id="$(printf "%s" "$headers" | awk -F': ' 'tolower($1)=="mcp-session-id"{print $2}' | tr -d '\r')"

payload=$(python - <<'PY' "$tool" "$args_json"
import json
import sys

name = sys.argv[1]
arguments = json.loads(sys.argv[2])
req = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {"name": name, "arguments": arguments},
}
print(json.dumps(req))
PY
)

curl -sS "$url" \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  -H "mcp-session-id: ${session_id}" \
  -d "$payload" \
  | awk -F'data: ' '/^data: /{print $2}'
