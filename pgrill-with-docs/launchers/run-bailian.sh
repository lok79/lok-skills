#!/bin/sh
# claude-bailian launcher: override Orca's desktop-proxy base_url with Token Plan endpoint
export ANTHROPIC_BASE_URL="https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic"
export ANTHROPIC_AUTH_TOKEN="$(python3 -I -c "import json;print([r for r in json.load(open('/Users/lok/.zcode/v2/provider_config.json'))['config']['providerConfigRules']['providerRules'] if r.get('providerId')=='qwen-token-plan-team-cn'][0]['config']['access']['apiKey'])")"
exec claude "$@"