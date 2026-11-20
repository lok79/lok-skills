#!/bin/sh
# pship — one-command ignition of the Orca coordinator (pgrill-with-docs).
# usage: pship "<需求>"   (host = current Orca worktree, else a new top-level worktree in cwd repo)
set -e
REQ="$*"
[ -n "$REQ" ] || { echo "usage: pship \"<需求>\""; exit 1; }
O=/Applications/Orca.app/Contents/Resources/bin/orca
DIR=$(cd "$(dirname "$0")" && pwd)
WRAP="$DIR/run-bailian.sh"
MODEL=qwen4-max-preview
EFFORT=high

# auth self-check: stop early with a clear message, no silent retry / profile swap
if ! "$WRAP" -p --model "$MODEL" "只回复 ok" >/tmp/pship-authcheck.txt 2>&1; then
  echo "auth 自检失败：请用 pship 入口 / 检查百炼端点 token / 检查网络。详情 /tmp/pship-authcheck.txt"
  exit 1
fi
grep -q ok /tmp/pship-authcheck.txt || {
  echo "auth 自检未回 ok：检查端点/token。详情 /tmp/pship-authcheck.txt"
  exit 1
}
echo "auth 自检 ok"

CMD="$WRAP --model $MODEL --effort $EFFORT"
RESP=$("$O" terminal create --worktree current --title pship-coord --command "$CMD" --json 2>&1) || RESP=""
HANDLE=$(echo "$RESP" | grep -oE '"handle": *"[^"]+"' | head -1 | cut -d'"' -f4)
if [ -z "$HANDLE" ]; then
  REPO=$(git rev-parse --show-toplevel 2>/dev/null || echo /Users/lok/.zcode/workspace/default/.scratch/orca-spike)
  WRESP=$("$O" worktree create --name "pship-coord-$(date +%s)" --no-parent --repo "path:$REPO" --json 2>&1)
  WID=$(echo "$WRESP" | grep -oE '"id": *"[^"]+::[^"]+"' | head -1 | cut -d'"' -f4)
  [ -n "$WID" ] || { echo "建协调者 worktree 失败: $WRESP"; exit 1; }
  RESP=$("$O" terminal create --worktree "id:$WID" --title pship-coord --command "$CMD" --json 2>&1)
  HANDLE=$(echo "$RESP" | grep -oE '"handle": *"[^"]+"' | head -1 | cut -d'"' -f4)
fi
[ -n "$HANDLE" ] || { echo "起协调者终端失败: $RESP"; exit 1; }
echo "协调者终端: $HANDLE"

"$O" terminal wait --terminal "$HANDLE" --for tui-idle --timeout-ms 60000 --json >/dev/null 2>&1 || true
# new worktree triggers claude trust dialog; accept it before delivering the request
if "$O" terminal read --terminal "$HANDLE" --json 2>/dev/null | grep -qiE "trust|safety check"; then
  "$O" terminal send --terminal "$HANDLE" --text "" --enter --json >/dev/null 2>&1 || true
  "$O" terminal wait --terminal "$HANDLE" --for tui-idle --timeout-ms 30000 --json >/dev/null 2>&1 || true
fi
"$O" terminal send --terminal "$HANDLE" --text "/pgrill-with-docs $REQ" --enter --json >/dev/null 2>&1 || \
  echo "投递失败：请手动在协调者终端输入 /pgrill-with-docs $REQ"
echo "需求已投递。观察: $O terminal read --terminal $HANDLE --json"