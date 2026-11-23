---
name: pgrill-with-docs
description: "Orca orchestration entry + coordinator, parallel to grill-with-docs+ship (originals untouched): runs clarification (grilling+domain-modeling) then coordinates the build as Orca structured-chat panel workers — front monolith, per-seam base/model dispatch, externalized review/accept/retro seams, gate/send human-in-loop, Deliver zero-push. Ignition of the post-clarification Orca build; invoke only on the user's explicit request; never on your own initiative."
---

# pgrill-with-docs（Orca 协调者 / 平行入口）

matt 链的 Orca 编排平行入口：**一个技能承担澄清 + 协调 + 派票 + Deliver**。原 `grill-with-docs` / `ship` / `implement` / `implement-spec` / `accept` 一字不改、日常照用；本技能只读组合它们。新族源仅 `~/.agents/skills`、不软链。

遵循 ship 的 **Prime directive**（下游技能会问的确认都由你决、why 记录到用户事后会审的地方）、**Failure budgets**、**Stopping**、**Deliver**。术语见 `GLOSSARY.md`（协调者/缝/前段一体/面板工人/tdd-only 变体/integration review/派票/决策门/底座/缝位配置/平行入口）；架构权衡见 `docs/adr/0001-orca-orchestration-parallel-family.md`。

## 0. 载入 Orca 指南

按 orca-cli skill 选 executable（本机 `/Applications/Orca.app/Contents/Resources/bin/orca`，不在 PATH）；`orca skills get orca-cli` 与 `orca skills get orchestration` 载版本匹配指南；prefer `--json`。协调者=**Orca 内 agent 面板会话**（wake 自动推进）；外部脚本协调仅 fallback（`--from` 终端身份 + 只读 poll，不跑 `check`）。

## 1. 澄清（前段一体起点）

在本协调者会话跑 grilling + domain-modeling（同 grill-with-docs）：rounds/frontier、GLOSSARY/ADR 懒创建。澄清收敛才进下一步。

## 2. Preflight（ship 照搬）

- 无 `docs/agents/issue-tracker.md` → stop，告诉用户跑 `/setup-matt-pocock-skills`。
- 无 `docs/agents/acceptance.md` 或缺关键事实 → call `survey` 补 profile（不打断）。
- **auth 自检**：按缝位默认 profile 的 wrapper 跑一次 `-p "只回复 ok"`；失败/未回 ok → stop，提示"用 pship 入口 / 检查端点 token / 检查网络"，不自动重试、不偷换 profile。
- 开放问题未决 → refuse，列缺项交还。
- 关键假设 → 分钟级实探 scouting，结果记 spec；失败假设交还用户。

## 3. Route（ship 判据，栈中立）

trivial（纯内容）/ light（单会话）/ standard（多会话跨层）/ wayfinder-scale → refuse 推荐 wayfinder。真 torn → ask-matt。

## 3b. 隔离（ship Isolation 照搬）

每 run 一个 worktree、一个分支（本 run 命名空间）；**trivial/light/standard 一律**在 run worktree 干活；salvage gitignored 本地（`.scratch/` 等）进 worktree；不碰非本 run 创建的 worktree/分支；主 checkout 只由 Deliver 的最终 merge 触碰。

## 4. 前段一体 + 实现

- **前段一体**：grill→to-spec→to-tickets 在**本会话同一底座+模型**不间断上下文完成（light 延伸到 pimplement）。
- **trivial**：协调者自己改+直接看；**无 review**；**accept 跳过**；commit+短报告。
- **light**：协调者本会话 call `pimplement`（tdd-only）；**Route 时趁澄清新鲜写 acceptance plan.md（`.scratch/<feature>/acceptance-plan.md`，须带验收断言）**供 accept 读；完成后派**一个独立 review 面板**（§5）。
- **standard**：协调者 `run-create` → `task-create --deps` 建 DAG → `task-list --ready` → 并行 `worktree create --name <slug>-t<n> --repo <repo> --base-branch <integration> --agent claude --model <model> --effort <effort> --prompt '<票 brief，in-domain 路径>' --json`（**Orca 原生路径：预置 trust + 用 UI 默认端点/命令；UI 默认须为百炼**，见 `docs/agents/orca-agentenv-setup.md`）→ `worker-start --task <id> --terminal <handle> --timeout-ms 180000` 收编（readiness 默认窗口太短已实证）；wake 推进 frontier。**raw `terminal create --command` 不预置 trust 会卡对话框，勿用**；三元组按 `docs/agents/orca-seams.md`。
- **票内容红线**：票里引用路径一律**工人自己 worktree 的 in-domain 相对路径**，禁写协调者/主 checkout 绝对路径（T01 假死根因实证：越域读被权限门挡）。

面板与模型路由约束（structured chat=Chat|CLI 设置+env 端点、zcode `--model` 硬拒及绕法、accept 底座工具要求）**单一来源见 `docs/agents/orca-seams.md`「模型路由/约束」**，不在此复述。当前底座统一 **claude、terminal 面**（chat 面需官方账号）。**默认端点**经 Orca `agentDefaultEnv.claude`（UI 设百炼 preview，三种启动一致生效，步骤见 `docs/agents/orca-agentenv-setup.md`）；**跨缝/跨两家**靠 env 前缀 wrapper（`launchers/run-zhipu.sh`/`run-bailian.sh`，覆盖 cc-switch 代理继承 env）+ 显式 --model；项目级 settings 无效（被进程 env 压过），勿用。点火入口 `launchers/pship.sh`。

## 5. 外置缝（review / accept / retro）

- **code-review**：standard=**全部票落地 integration 后 ONE 次** integration review 面板（call 原 `code-review`），findings 派**单个 fix 工人**修；light=pimplement 后一次 review 面板。≤2 轮。
- **accept**：独立面板工人 call 原 `accept`（或按 acceptance profile 用 `verify`），**把 spec 路径（standard）/ Route 写的 acceptance-plan.md 路径（light）作为 accept 的 spec 输入传入**（plan 须带验收断言）；真环境验收；≤2 轮修复。底座工具约束见 `docs/agents/orca-seams.md`。
- **retro**：可选面板，call 原 `retro`。

## 6. 人在环

`gate-create --question --options` / `gate-resolve` 决策门在面板弹给用户；`send --to dispatch:<id>` 运行中插话（working worker 即时读）；观察=`worker-read` / `terminal read/wait` / 面板本身。

## 7. Budgets / Stopping（ship 照搬）

票重试 ≤2；review ≤2；accept ≤2；超预算 stop+报告。只三种召唤用户：预算尽 / 范围意外 / Preflight 拒绝。

## 8. Deliver（ship 照搬，零 push）

salvage `.scratch/<feature>/` 回主 checkout → 主 checkout merge 本 run 分支 → 清 worktree/分支 → close tickets → 报告（spec/票路径、review 状态、accept verdict、预算、"未 push"）。

## 9. 非侵入红线

永不修改原 ship/implement/implement-spec/accept/grill-with-docs；只读 call。新族仅 pgrill-with-docs + pimplement，源 `~/.agents/skills`；**claude 侧相对软链**（`~/.claude/skills`，既有拓扑，使 claude/Orca 可 invoke）；**zcode 侧不软链**、不补 zcode 缺失链。

**镜像编辑注记**：pimplement 镜像 implement 的 machinery/tdd 段；pgrill 引用 ship 节名锚点（Prime directive / Preflight / Route / Isolation / Deliver / Failure budgets / Stopping）。上游 ship/implement 改版重排这些节名时，同步检查本族（CUSTOM.md 有锚点注记）。