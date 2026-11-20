# Orca agentDefaultEnv 配置步骤（约 2 分钟，UI 手设）

> 目的：让 Orca 的 claude **普通启动**（新建 agent tab / agent launch / worker-start --agent claude）默认走国内端点，不再 Not logged in。
> 原理：Orca settings `agentDefaultEnv.claude` 在 PTY spawn 时后展开、覆盖继承 env（cc-switch 代理 base_url + 置空模型 env）。对三种启动一致生效。**新终端生效；已开终端需重开。**
> 不碰 cc-switch（免波及桌面 App）、不直写 profile-state.db（坏库风险）。

## 步骤
1. Orca → **Settings → Agents → Claude → 环境变量编辑器**（agentDefaultEnv）。
2. 加/改以下键（token 从 `~/.zcode/v2/provider_config.json` → providerRules[providerId=qwen-token-plan-team-cn].config.access.apiKey 抄，勿外泄）：
   - `ANTHROPIC_BASE_URL` = `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
   - `ANTHROPIC_AUTH_TOKEN` = <百炼 Token Plan apiKey>
   - `ANTHROPIC_DEFAULT_SONNET_MODEL` = `qwen4-max-preview`
   - `ANTHROPIC_DEFAULT_OPUS_MODEL` = `qwen4-max-preview`
   - `ANTHROPIC_DEFAULT_HAIKU_MODEL` = `qwen4-max-preview`
   - `ANTHROPIC_DEFAULT_FABLE_MODEL` = `qwen4-max-preview`
3. 保存。**新开**一个 claude agent tab 发"回复 ok"验证回 ok（旧终端重开才生效）。
4. 跨缝/跨智谱仍由 pgrill wrapper 覆盖（`launchers/run-zhipu.sh` / `run-bailian.sh` + 显式 --model）；本默认只解决"普通启动能不能起"。

## 备注
- 默认选百炼 preview 因 front/协调者缝用它；preview 2026-11-25 下线后改此默认（fallback 再议）。
- `unrecognized_model` 警告 benign（context window 按 200k 假设）。
- 若 UI 无该编辑器（版本差异），退回 wrapper 入口 `pship.sh`（功能等价，仅多一步机制内置）。