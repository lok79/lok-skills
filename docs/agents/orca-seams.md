# Orca 缝位配置（模板）

缝→(profile, 模型, effort) 的声明式映射，pgrill-with-docs 派票时读取。**用户可自行编辑覆盖**；按 feature 可在 `.scratch/<feature>/orca-seams.md` 放覆盖表。

**底座统一 claude、terminal 面**（Orca chat 面板面需官方账号，当前不可用；zcode 国内版开不出、zcode-cn 暂不造）。profile 决定端点（跨百炼/智谱两家），model/effort 按缝配。

**协调者（前段一体）配置：profile=claude-bailian、model=qwen4-max-preview、effort=high。前段一体不是缝**（GLOSSARY），此为协调者会话配置，不进下表；下表仅四条可换缝。

| 缝 | profile | model | effort | 备注 |
|---|---|---|---|---|
| ticket（票级 implement） | claude-zhipu | glm-5.3-flash | low | 仅 standard；可逐票覆盖 |
| review | claude-bailian | qwen4-max-preview | medium | 新鲜眼睛；standard 全票后 ONE 次 integration |
| accept | claude-zhipu | glm-5.3-flash | low | 底座工具要求见「约束」 |
| retro | claude-zhipu | glm-5.3 | high | 可选 |

## profiles（端点来源，运行时读，不复制 token 到持久新文件）

- **claude-bailian**：`ANTHROPIC_BASE_URL=https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`；token 源=`~/.zcode/v2/provider_config.json` → providerRules[providerId=qwen-token-plan-team-cn].config.access.apiKey。
- **claude-zhipu**：`ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic`；token 源=`~/.claude/settings.json` → env.ANTHROPIC_AUTH_TOKEN。

**默认端点（a 机制）**：Orca settings `agentDefaultEnv.claude`（UI: Settings→Agents→Claude→环境变量）设百炼 preview 端点+token+模型映射；PTY spawn 后展开覆盖继承 env，agent tab/launch/worker-start 一致生效；步骤见 `docs/agents/orca-agentenv-setup.md`。**跨缝覆盖机制（实测定论）**：15721 代理实为 **cc-switch**（Orca 继承其 env：base_url=127.0.0.1:15721/claude-desktop + 置空 `ANTHROPIC_DEFAULT_*_MODEL`）；user/项目级 settings 被进程 env 压过、**无效**（实测 Not logged in）。跨缝/跨两家用 **env 前缀 wrapper**：`launchers/run-zhipu.sh` / `run-bailian.sh`（export 两家端点+token 后 exec claude）+ **显式 `--model`**（否则百炼 Model not exist）；派票经 `terminal create --command <wrapper>` + `worker-start --terminal` 收编（`--model/--effort` 走 wrapper 命令行，Orca `--model` 不与 `--terminal` 同用）。点火入口 `launchers/pship.sh`（含 auth 自检）。零新增常驻服务。`unrecognized_model` 警告 benign（context window 按 200k 假设）。

## 模型路由

- 起步 = 上述 profiles（项目级 env 覆盖）。
- 后置优化 = 本地聚合网关（LiteLLM/new-api）一个端点 + `--model` 路由；真需要统一入口时再上。`tapd/gateway` 是 tapd 面板网关、不是 LLM 网关，不复用。

## 约束（单一来源，pgrill/acceptance 指向此处）

- **claude 吃 `--model`/`--effort`**；`--effort` 必须与 `--model` 同传。抓包定论：CLI 发 `output_config.effort`+`thinking.adaptive`。**智谱兼容层声明映射 effort**（low→low、medium/high→high、xhigh/max→max，默认max）；**百炼逐模型映射：qwen4-max 生效，qwen4-max-preview 与 deepseek-v4.1-flash-1017 未列→疑似忽略**。glm-5.3/flash 强制思考不可关、native 仅 low/high/max；budget_tokens 弃用（glm 忽略）。**qwen4-max-preview 预览期至 2026-11-25 下线**；用户定：front/review **保留 preview**（qwen4-max 太贵），接受其 effort 疑似无效；11-25 下线时再定 fallback。三层证据见 `research/effort-final-evidence-2026-11.md`。
- **zcode 不接受 launch-time `--model`/`--effort`**；国内 zcode 在 Orca 开不出会话（Orca=国际版 zcode）；zcode-cn 适配器暂不造。
- **claude 在 Orca 的 chat 面板面需官方账号**（`orca account add`=claude login）；当前用 **terminal 面**（`--surface terminal`，env 端点 API 模式即通）。
- **accept 缝底座必须有 shell + ego-browser 工具**。