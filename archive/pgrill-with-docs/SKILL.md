---
name: pgrill-with-docs
description: "Orca orchestration entry + coordinator, parallel to grill-with-docs+ship (originals untouched): runs clarification (grilling+domain-modeling) then coordinates the build as Orca chat-panel workers — front monolith, per-seam base/model dispatch, externalized review/accept/retro seams, coordinator-layer human-in-loop, Deliver zero-push. A-mode default: all-chat fire-and-forget workers; B-mode fallback: terminal workers with full send/gate/wake when cc-switch current provider matches. Ignition on the user's explicit request only."
---

# pgrill-with-docs（Orca 协调者 / 平行入口）

matt 链的 Orca 编排平行入口：**一个技能承担澄清 + 协调 + 派票 + Deliver**。原 `grill-with-docs` / `ship` / `implement` / `implement-spec` / `accept` 一字不改、日常照用；本技能只读组合它们。新族源仅 `~/.agents/skills`；**claude 侧相对软链**（`~/.claude/skills`，使 claude/Orca 可 invoke）；**zcode 侧不软链**。

遵循 ship 的 **Prime directive**（下游确认都由你决、why 记录到用户事后会审处）、**Failure budgets**、**Stopping**、**Deliver**。术语见 `GLOSSARY.md`；架构权衡见 `docs/adr/0001-orca-orchestration-parallel-family.md`。

## 0. 载入 Orca 指南 + 编排 mailbox

按 orca-cli skill 选 executable（`/Applications/Orca.app/Contents/Resources/bin/orca`，不在 PATH）；`orca skills get orca-cli` / `orca skills get orchestration` 载版本匹配指南；prefer `--json`。

**A 档（默认）**：协调者 = **structured chat 会话**（`agent launch --surface chat`，吃 UI 端点配置=百炼，实证通）。chat 会话**无编排身份**（stable_pane_required），故先建一个**专用 shell 终端当编排 mailbox**（`terminal create --command sh --title pgrill-mailbox`），所有 orchestration 动词带 `--from <mailbox handle>`。**不碰任何全局配置**（~/.claude、cc-switch 一字不动）。
**B 档（fallback）**：仅当 cc-switch 当前供应商=目标端点时，可用 terminal 协调者 + terminal 工人全编排（send/gate/wake 直达工人）。

## 1. 澄清（前段一体起点）

在本协调者会话跑 grilling + domain-modeling（同 grill-with-docs）：rounds/frontier、GLOSSARY/ADR 懒创建。收敛才进下一步。

## 2. Preflight（ship 照搬）

- 无 `docs/agents/issue-tracker.md` → stop，告诉用户跑 `/setup-matt-pocock-skills`。
- 无 `docs/agents/acceptance.md` 或缺关键事实 → call `survey` 补 profile（不打断）。
- 开放问题未决 → refuse 列缺项交还。
- 关键假设 → 分钟级实探 scouting 记 spec；失败假设交还。
- **auth 自检**：chat launch 一次 trivial prompt 验端点应答；失败 stop 提示查端点/额度，不偷绕。

## 3. Route（ship 判据，栈中立）

trivial / light / standard / wayfinder-scale → refuse 推荐 wayfinder。真 torn → ask-matt。

## 3b. 隔离（ship Isolation 照搬）

每 run 一个 worktree 一个分支；trivial/light/standard 一律；salvage gitignored 本地；不碰非本 run 的 worktree/分支；主 checkout 只由 Deliver 最终 merge 触碰。

## 4. 前段一体 + 派票

- **前段一体**：grill→to-spec→to-tickets 在**本协调者会话同一上下文**完成（light 延伸到 implement）。
- **trivial**：协调者自己改+直接看；无 review；accept 跳过；commit+短报告。
- **light**：协调者本会话跑 `pimplement`；Route 时写 acceptance-plan.md（带验收断言）；完成后派一个 review chat 工人（§5）。
- **standard（A 档）**：`run-create --from <mailbox>` → `task-create --deps` 建 DAG → `task-list --ready` → 每票：
  1. `worktree create --name <slug>-t<n> --repo <repo> --base-branch <integration>`（**不带 --agent**）；
  2. 拷 `.scratch/<feature>/` 进该 worktree（in-domain）；
  3. `agent launch --agent claude --surface chat --worktree id:<wt> --model <model> --effort <effort> --prompt '<票 brief：in-domain 路径 + 验收判据 + 只跑 pimplement + commit 到本 worktree 分支>' --json` → 记 session id 进票 Comments；
  4. **轮询 `agent read --id <session>`** 判完成（fire-and-forget：无 send/wake 到工人）；
  5. 完成后协调者 shell `git merge` 该支进 integration（冲突即停报告）。
  三元组按 `docs/agents/orca-seams.md`。
- **standard（B 档）**：`worker-start --task --terminal <handle> --timeout-ms 180000` + send/gate/wake 直达工人（仅 cc-switch 匹配时）。
- **票内容红线**：票里路径一律工人自己 worktree 的 in-domain 相对路径，禁协调者/主 checkout 绝对路径（T01 假死根因实证）。

## 5. 外置缝（review / accept / retro）

- **code-review**：standard=全票落地 integration 后 ONE 次 integration review chat 工人（call 原 `code-review`），findings 派单个 fix chat 工人；light=implement 后一次。≤2 轮。
- **accept**：chat 工人 call 原 `accept`（或按 profile 用 `verify`），spec 路径（standard）/ acceptance-plan.md（light）作为输入传入；真环境验收；≤2 轮。底座工具约束见 orca-seams。
- **retro**：可选 chat 工人 call 原 `retro`。
- 派法同 §4（worktree+拷 scratch+chat launch+agent read 轮询+merge）。

## 6. 人在环（A 档：协调者层）

`gate-create --question --options --from <mailbox>` / `gate-resolve` 在**协调者层**；用户与**协调者 chat 面板**对话拍板。**工人不可中途插话**（chat 无 send 动词）——改方向 = 不再读旧 chat + amend brief 重派新 chat（旧支不 merge）。观察 = `agent read` 轮询 + Orca 面板肉眼。B 档恢复 `send --to dispatch` 直达工人。

## 7. Budgets / Stopping（ship 照搬）

票重试 ≤2；review ≤2；accept ≤2；超预算 stop+报告。只三种召唤用户：预算尽 / 范围意外 / Preflight 拒绝。

## 8. Deliver（ship 照搬，零 push）

salvage `.scratch/<feature>/` 回主 checkout → 主 checkout merge 本 run 分支 → 清 worktree/分支 → close tickets → 报告（spec/票路径、review 状态、accept verdict、预算、"未 push"）。

## 9. 非侵入红线

永不修改原 ship/implement/implement-spec/accept/grill-with-docs；只读 call。新族仅 pgrill-with-docs + pimplement。**全局配置零写入**（~/.claude/settings.json、~/.claude.json、cc-switch 不动）；隔离只用 run worktree + 进程级/Orca 级手段。

**镜像编辑注记**：pimplement 镜像 implement 的 machinery/tdd 段；pgrill 引用 ship 节名锚点（Prime directive / Preflight / Route / Isolation / Deliver / Failure budgets / Stopping）。上游改版重排时同步检查本族（CUSTOM.md 有注记）。