#!/bin/sh
# claude-zhipu launcher: CLI-level --settings file (above user settings env rewritten by cc-switch).
S="/tmp/claude-zhipu-$$.json"
: > "$S"; chmod 600 "$S"
python3 -I - "$S" <<'PY'
import json, sys
key = json.load(open('/Users/lok/.claude/settings.json'))['env']['ANTHROPIC_AUTH_TOKEN']
env = {'ANTHROPIC_BASE_URL': 'https://open.bigmodel.cn/api/anthropic',
       'ANTHROPIC_AUTH_TOKEN': key,
       'ANTHROPIC_DEFAULT_SONNET_MODEL': 'glm-5.3',
       'ANTHROPIC_DEFAULT_OPUS_MODEL': 'glm-5.3',
       'ANTHROPIC_DEFAULT_HAIKU_MODEL': 'glm-5.3-flash',
       'ANTHROPIC_DEFAULT_FABLE_MODEL': 'glm-5.3-flash'}
json.dump({'env': env}, open(sys.argv[1], 'w'))
PY
exec claude --settings "$S" --dangerously-skip-permissions "$@"