# Orca 缝位配置（模板）

缝→(底座, 模型) 的声明式映射，pgrill-with-docs 派票时读取。**用户可自行编辑覆盖**；按 feature 可在 `.scratch/<feature>/orca-seams.md` 放覆盖表。

**协调者（前段一体）配置：base=claude、model=qwen4-max、effort=high。前段一体不是缝**（GLOSSARY），此为协调者会话配置，不进下表；下表仅四条可换缝。

| 缝 | base | model | effort | 备注 |
|---|---|---|---|---|
| ticket（票级 implement） | claude | glm-4.6 | high | 仅 standard；可逐票覆盖 |
| review | claude | deepseek-v4 | medium | 新鲜眼睛；standard 全票后 ONE 次 integration |
| accept | claude | glm-4.6 | medium | 底座工具要求见「约束」 |
| retro | claude | glm-4.6 | low | 可选 |

## 模型路由

- **起步 = Orca agent profiles**：claude-qwen / claude-glm / claude-deepseek 各带 env 端点（`ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`），派票选 profile。零新增服务。
- **后置优化 = 本地聚合网关**（LiteLLM/new-api）：一个端点 + `--model` 路由各家模型；真需要"一个 base 跨多家模型"时再上。`tapd/gateway` 是 tapd 面板网关、**不是** LLM 网关，不复用。

## 约束（单一来源，pgrill/acceptance 指向此处）

- **zcode 不接受 launch-time `--model`/`--effort`**（Orca 硬拒/忽略）：zcode 缝的模型与思考强度在 **zcode app 自身配置**里改，或该缝派 claude/codex 工人。
- **`--effort` 必须与 `--model` 同传**（Orca：--effort requires --model）；取值 low/medium/high 等 reasoning effort 档。端点是否 honor effort 未知→记发现项，不假设。
- **claude 在 Orca 的 chat 面板面需官方账号**（`orca account add` = 跑 `claude login`）；无官方登录时 claude 用 **terminal 面**（`--surface terminal`，读 `~/.claude/settings.json` env 端点即通）或改 **zcode 面板**（chat 免官方墙）。
- codex 端点走 `~/.codex` 配置（智谱接入）；面板=structured chat 需 agent Chat|CLI 设置 + 端点。
- **accept 缝底座必须有 shell + ego-browser 工具**。