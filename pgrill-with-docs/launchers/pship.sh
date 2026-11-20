#!/bin/sh
# pship — one-command ignition of the Orca coordinator (pgrill-with-docs).
# usage: pship "<需求>"   (host worktree = current Orca worktree, else new top-level in cwd repo)
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

# coordinator terminal: current Orca worktree, fallback new top-level in cwd repo
CMD="$WRAP --model $MODEL --effort $EFFORT"
RESP=$("$O" terminal create --worktree current --title pship-coord --command "$CMD" --json 2>&1) || \
RESP=$("$O" terminal create --worktree new-top-level --repo "path:$(git rev-parse --show-toplevel 2>/dev/null || echo /Users/lok/.zcode/workspace/default/.scratch/orca-spike)" --name pship-coord --title pship-coord --command "$CMD" --json 2>&1)
HANDLE=$(echo "$RESP" | grep -oE '"handle":"[^"]+"' | head -1 | cut -d'"' -f4)
[ -n "$HANDLE" ] || { echo "起协调者终端失败: $RESP"; exit 1; }

"$O" terminal wait --terminal "$HANDLE" --for tui-idle --timeout-ms 60000 --json >/dev/null 2>&1 || true
"$O" terminal send --terminal "$HANDLE" --text "/pgrill-with-docs $REQ" --enter --json >/dev/null 2>&1
echo "协调者已起: $HANDLE ；需求已投递。观察: $O terminal read --terminal $HANDLE --json"