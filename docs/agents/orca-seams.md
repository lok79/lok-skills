# Orca 缝位配置（模板）

缝→(底座, 模型) 的声明式映射，pgrill-with-docs 派票时读取。**用户可自行编辑覆盖**；按 feature 可在 `.scratch/<feature>/orca-seams.md` 放覆盖表。

| 缝 | base | model | 备注 |
|---|---|---|---|
| front（前段一体） | claude | qwen4-max | 协调者会话；grill→spec→票同上下文 |
| ticket（票级 implement） | claude | glm-4.6 | 仅 standard；可逐票覆盖 |
| review | claude | deepseek-v4 | 新鲜眼睛；standard 全票后 ONE 次 integration |
| accept | claude | glm-4.6 | 底座须有 shell+ego-browser |
| retro | claude | glm-4.6 | 可选 |

## 模型路由

- **起步 = Orca agent profiles**：claude-qwen / claude-glm / claude-deepseek 各带 env 端点（`ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`），派票选 profile。零新增服务。
- **后置优化 = 本地聚合网关**（LiteLLM/new-api）：一个端点 + `--model` 路由各家模型；真需要"一个 base 跨多家模型"时再上。`tapd/gateway` 是 tapd 面板网关、**不是** LLM 网关，不复用。

## 约束

- **zcode 不接受 launch-time `--model`**（Orca 硬拒）：zcode 缝换模型改 zcode 自身配置，或该缝派 claude/codex 工人。
- 面板=structured chat：agent Chat|CLI 设置 + env 端点；无官方登录墙（env 端点已通）。
- accept 缝底座必须有 shell + ego-browser 工具。