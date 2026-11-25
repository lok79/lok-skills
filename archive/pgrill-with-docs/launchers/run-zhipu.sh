#!/bin/sh
# claude-zhipu launcher (11-20 proven bare form): process env only, no flags, no global writes.
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"
export ANTHROPIC_AUTH_TOKEN="$(python3 -I -c "import json;print(json.load(open('/Users/lok/.claude/settings.json'))['env']['ANTHROPIC_AUTH_TOKEN'])")"
export ANTHROPIC_DEFAULT_SONNET_MODEL="glm-5.3"
export ANTHROPIC_DEFAULT_OPUS_MODEL="glm-5.3"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="glm-5.3-flash"
export ANTHROPIC_DEFAULT_FABLE_MODEL="glm-5.3-flash"
exec claude "$@"