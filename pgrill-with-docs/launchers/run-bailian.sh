#!/bin/sh
# claude-bailian launcher: CLI-level --settings file (precedence above user settings env,
# which cc-switch rewrites). Project-level env is ignored by claude (security), so use --settings.
S="/tmp/claude-bailian-$$.json"
: > "$S"; chmod 600 "$S"
python3 -I - "$S" <<'PY'
import json, sys
key = [r for r in json.load(open('/Users/lok/.zcode/v2/provider_config.json'))['config']['providerConfigRules']['providerRules'] if r.get('providerId') == 'qwen-token-plan-team-cn'][0]['config']['access']['apiKey']
env = {'ANTHROPIC_BASE_URL': 'https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic',
       'ANTHROPIC_AUTH_TOKEN': key}
for k in ('SONNET', 'OPUS', 'HAIKU', 'FABLE'):
    env['ANTHROPIC_DEFAULT_' + k + '_MODEL'] = 'qwen4-max-preview'
json.dump({'env': env}, open(sys.argv[1], 'w'))
PY
exec claude --settings "$S" --dangerously-skip-permissions "$@"