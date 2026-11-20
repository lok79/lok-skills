#!/bin/sh
# claude-zhipu launcher: override Orca's desktop-proxy base_url with domestic endpoint
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"
export ANTHROPIC_AUTH_TOKEN="$(python3 -I -c "import json;print(json.load(open('/Users/lok/.claude/settings.json'))['env']['ANTHROPIC_AUTH_TOKEN'])")"
exec claude "$@"