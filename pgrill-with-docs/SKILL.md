---
name: pgrill-with-docs
description: "Orca orchestration entry + coordinator, parallel to grill-with-docs+ship (originals untouched): runs clarification (grilling+domain-modeling) then coordinates the build as Orca structured-chat panel workers — front monolith, per-seam base/model dispatch, externalized review/accept/retro seams, gate/send human-in-loop, Deliver zero-push. Ignition of the post-clarification Orca build; invoke only on the user's explicit request; never on your own initiative."
---

# pgrill-with-docs（Orca 协调者 / 平行入口）

matt 链的 Orca 编排平行入口：**一个技能承担澄清 + 协调 + 派票 + Deliver**。原 `grill-with-docs` / `ship` / `implement` / `implement-spec` / `accept` 一字不改、日常照用；本技能只读组合它们。新族源仅 `~/.agents/skills`、不软链。

遵循 ship 的 **Prime directive**（下游技能会问的确认都由你决、why 记录到用户事后会审的地方）、**Failure budgets**、**Stopping**、**Deliver**。术语见 GLOSSARY.md（协调者/缝/前段一体/面板工人/tdd-only 变体/integration review/派票/决策门/底座/缝位配置/平行入口）；架构权衡见 docs/adr/0001。

## 0. 载入 Orca 指南

按 orca-cli skill 选 executable（本机 `/Applications/Orca.app/Contents/Resources/bin/orca`，不在 PATH）；`orca skills get orca-cli` 与 `orca skills get orchestration` 载版本匹配指南；prefer `--json`。协调者=**Orca 内 agent 面板会话**（wake 自动推进）；外部脚本协调仅 fallback（`--from` 终端身份 + 只读 poll，不跑 `check`）。

## 1. 澄清（前段一体起点）

在本协调者会话跑 grilling + domain-modeling（同 grill-with-docs）：rounds/frontier、GLOSSARY/ADR 懒创建。澄清收敛才进下一步。

## 2. Preflight（ship 照搬）

- 无 `docs/agents/issue-tracker.md` → stop，告诉用户跑 `/setup-matt-pocock-skills`。
- 无 `docs/agents/acceptance.md` 或缺关键事实 → call `survey` 补 profile（不打断）。
- 开放问题未决 → refuse，列缺项交还。
- 关键假设 → 分钟级实探 scouting，结果记 spec；失败假设交还用户。

## 3. Route（ship 判据，栈中立）

trivial（纯内容）/ light（单会话）/ standard（多会话跨层）/ wayfinder-scale → refuse 推荐 wayfinder。真 torn → ask-matt。

## 4. 前段一体 + 实现

- **前段一体**：grill→to-spec→to-tickets 在**本会话同一底座+模型**不间断上下文完成（light 延伸到 pimplement）。
- **trivial**：协调者自己改+直接看；**无 review**；**accept 跳过**；commit+短报告。
- **light**：协调者本会话 call `pimplement`（tdd-only）；完成后派**一个独立 review 面板**（见 §5）。
- **standard**：协调者 `run-create` → `task-create --deps` 建 DAG → `task-list --ready` → 并行 `worker-start --task <id> --agent <base> --model <model>`（按缝位配置）派**票面板工人**跑 `pimplement`；wake 推进 frontier。

面板=structured chat：agent 的 Chat|CLI 设置 + env 端点配置（claude 走 `~/.claude/settings.json` env；zcode 走自身配置）。**zcode 不接受 `--model`**（硬拒）：zcode 缝换模型改 zcode 配置或该缝派 claude/codex 工人。

## 5. 外置缝（review / accept / retro）

- **code-review**：standard=**全部票落地 integration 后 ONE 次** integration review 面板（call 原 `code-review`），findings 派**单个 fix 工人**修；light=pimplement 后一次 review 面板。≤2 轮。
- **accept**：独立面板工人 call 原 `accept`（或按 acceptance profile 用 `verify`），读 spec（standard）/ Route 写的 plan.md（light）；真环境验收；≤2 轮修复。accept 缝底座须有 shell+ego-browser。
- **retro**：可选面板。

## 6. 人在环

`gate-create --question --options` / `gate-resolve` 决策门在面板弹给用户；`send --to dispatch:<id>` 运行中插话（working worker 即时读）；观察=`worker-read` / `terminal read/wait` / 面板本身。

## 7. Budgets / Stopping（ship 照搬）

票重试 ≤2；review ≤2；accept ≤2；超预算 stop+报告。只三种召唤用户：预算尽 / 范围意外 / Preflight 拒绝。

## 8. Deliver（ship 照搬，零 push）

salvage `.scratch/<feature>/` 回主 checkout → 主 checkout merge 本 run 分支 → 清 worktree/分支 → close tickets → 报告（spec/票路径、review 状态、accept verdict、预算、"未 push"）。

## 9. 非侵入红线

永不修改原 ship/implement/implement-spec/accept/grill-with-docs；只读 call。新族仅 pgrill-with-docs + pimplement，源 `~/.agents/skills`、不软链、不补 zcode 链。