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

**跨两家机制**：协调者派票前按缝位 profile 往 worker worktree 写**项目级 `.claude/settings.json` env**（claude CLI 项目级覆盖 user 级），实现一个 claude 底座跨百炼/智谱；零新增常驻服务（聚合网关仍为后置可选）。

## 模型路由

- 起步 = 上述 profiles（项目级 env 覆盖）。
- 后置优化 = 本地聚合网关（LiteLLM/new-api）一个端点 + `--model` 路由；真需要统一入口时再上。`tapd/gateway` 是 tapd 面板网关、不是 LLM 网关，不复用。

## 约束（单一来源，pgrill/acceptance 指向此处）

- **claude 吃 `--model`/`--effort`**；`--effort` 必须与 `--model` 同传。各端点是否真 honor effort 见 `research/effort-honor-matrix-2026-11.md`（实测矩阵），不假设。
- **zcode 不接受 launch-time `--model`/`--effort`**；国内 zcode 在 Orca 开不出会话（Orca=国际版 zcode）；zcode-cn 适配器暂不造。
- **claude 在 Orca 的 chat 面板面需官方账号**（`orca account add`=claude login）；当前用 **terminal 面**（`--surface terminal`，env 端点 API 模式即通）。
- **accept 缝底座必须有 shell + ego-browser 工具**。