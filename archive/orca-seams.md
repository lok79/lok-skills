# Orca 缝位配置（模板）

缝→(profile, 模型, effort) 的声明式映射，pgrill-with-docs 派票时读取。**用户可自行编辑覆盖**；按 feature 可在 `.scratch/<feature>/orca-seams.md` 放覆盖表。

**底座统一 claude、terminal 面**（Orca chat 面板面需官方账号，当前不可用；zcode 国内版开不出、zcode-cn 暂不造）。profile 决定端点（跨百炼/智谱两家），model/effort 按缝配。

**全百炼（2026-11-23 起：智谱 Coding Plan 额度耗尽，全链改百炼 Token Plan）**。协调者（前段一体）配置：profile=claude-bailian、model=qwen4-max-preview、effort=high。前段一体不是缝（GLOSSARY），此为协调者会话配置，不进下表；下表仅四条可换缝。

| 缝 | profile | model | effort | 备注 |
|---|---|---|---|---|
| ticket（票级 implement） | claude-bailian | qwen4-max-preview | high | 仅 standard；可逐票覆盖；effort 疑似无效接受（靠 preview 默认 xhigh 深度） |
| review | claude-bailian | qwen4-max-preview | medium | 新鲜眼睛；standard 全票后 ONE 次 integration |
| accept | claude-bailian | deepseek-v4.1-flash-1017 | low | 省额度；effort 疑似忽略接受；底座工具要求见「约束」 |
| retro | claude-bailian | deepseek-v4.1-flash-1017 | low | 省额度 |

**11-25 下线共担**：front/review/ticket 三缝同用 preview，2026-11-25 预览期结束一起换 fallback（qwen4-max 或 flash，届时定）；run 若拖过该日需中途切换。

## profiles（端点来源，运行时读，不复制 token 到持久新文件）

- **claude-bailian**：`ANTHROPIC_BASE_URL=https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`；token 源=`~/.zcode/v2/provider_config.json` → providerRules[providerId=qwen-token-plan-team-cn].config.access.apiKey。
- **claude-zhipu**：`ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic`；token 源=`~/.claude/settings.json` → env.ANTHROPIC_AUTH_TOKEN。

**载体（orca-ship，11-24 定稿）**：协调者=**bot chat**（自带编排身份，**无 mailbox**）；工人=**预建可复用工人 bot**（owner 直接给正在跑的工人发消息=wake/插话）；读完整输出=orca-computer-use tree；**通信规范见 orca-ship §9**（指针 brief/摘要回传，禁贴全文）。**全局配置零写入**。旧 A/B 档（plain chat+mailbox / terminal+cc-switch 匹配）归档为探索资产，非日常依赖。

## 载体 bot roster 与独立性约束（配置层；orca-ship SKILL.md 不动）

| 角色 | bot | 模型/effort | 职责 |
|---|---|---|---|
| 协调者 | probe-bot | qwen4-max-preview / high | 委托原链澄清/派票/串联验收/Deliver；§9 收发；gate 仅真决策 |
| 票工人 | worker-bot-1 / worker-bot-2（复用跨票） | 缝位 ticket 值 | 按 brief 跑 pimplement（tdd-only），commit 本 worktree 分支，§9 回传 |
| 审查 | review-bot（复用跨单） | qwen4-max-preview / medium | 独立跑原 code-review（两轴）审 integration diff，回传 findings+verdict |
| 验收 | accept-bot（复用跨单） | deepseek-v4.1-flash-1017 / low | 独立跑原 accept（红线/证据/分账/性能两档），回传验收记录路径+结论一行 |
| retro | 复用 review-bot 或协调者事后 | — | 可选 |

**独立性硬约束**：review/accept **必须在独立预建 bot 会话跑**（review-bot/accept-bot），**禁复用工人会话或协调者会话自审自验**（新鲜眼睛+独立上下文+外置缝立场）。此约束在配置层生效，orca-ship SKILL.md 保持已审版本不动。**跨缝覆盖机制（实测定论）**：15721 代理实为 **cc-switch**（Orca 继承其 env：base_url=127.0.0.1:15721/claude-desktop + 置空 `ANTHROPIC_DEFAULT_*_MODEL`）；user/项目级 settings 被进程 env 压过、**无效**（实测 Not logged in）。跨缝/跨两家用 **env 前缀 wrapper**：`launchers/run-zhipu.sh` / `run-bailian.sh`（export 两家端点+token 后 exec claude）+ **显式 `--model`**（否则百炼 Model not exist）；派票经 `terminal create --command <wrapper>` + `worker-start --terminal` 收编（`--model/--effort` 走 wrapper 命令行，Orca `--model` 不与 `--terminal` 同用）。点火入口 `launchers/pship.sh`（含 auth 自检）。零新增常驻服务。`unrecognized_model` 警告 benign（context window 按 200k 假设）。

## 模型路由

- 起步 = 上述 profiles（项目级 env 覆盖）。
- 后置优化 = 本地聚合网关（LiteLLM/new-api）一个端点 + `--model` 路由；真需要统一入口时再上。`tapd/gateway` 是 tapd 面板网关、不是 LLM 网关，不复用。

## 约束（单一来源，pgrill/acceptance 指向此处）

- **claude 吃 `--model`/`--effort`**；`--effort` 必须与 `--model` 同传。抓包定论：CLI 发 `output_config.effort`+`thinking.adaptive`。**智谱兼容层声明映射 effort**（low→low、medium/high→high、xhigh/max→max，默认max）；**百炼逐模型映射：qwen4-max 生效，qwen4-max-preview 与 deepseek-v4.1-flash-1017 未列→疑似忽略**。glm-5.3/flash 强制思考不可关、native 仅 low/high/max；budget_tokens 弃用（glm 忽略）。**qwen4-max-preview 预览期至 2026-11-25 下线**；用户定：front/review **保留 preview**（qwen4-max 太贵），接受其 effort 疑似无效；11-25 下线时再定 fallback。三层证据见 `research/effort-final-evidence-2026-11.md`。
- **zcode 不接受 launch-time `--model`/`--effort`**；国内 zcode 在 Orca 开不出会话（Orca=国际版 zcode）；zcode-cn 适配器暂不造。
- **claude 在 Orca 的 chat 面板面需官方账号**（`orca account add`=claude login）；当前用 **terminal 面**（`--surface terminal`，env 端点 API 模式即通）。
- **accept 缝底座必须有 shell + ego-browser 工具**。