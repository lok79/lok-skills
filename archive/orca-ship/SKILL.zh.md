# orca-ship 中文对照版（只读，执行以英文 SKILL.md 为准）

> 本文件供阅读/审查，**不被执行**。逐节对照英文 SKILL.md；如有出入以英文为准。

# orca-ship（薄适配层）

原链 skill 是**唯一权威**。本技能**不转述**它们的规矩——只指向它们、运行时读取。自含节：0、4（brief/缝位）、5（回传模板）、6、9、10。其余全部委托。

Prime directive（下游确认自决+留痕）、Failure budgets（预算）、Stopping（三召唤）、Deliver（交付）：运行时读 `ship/SKILL.md` 对应锚点照办，不复述。

## 0. 载体与身份（自含）
- 协调者 = **一个 bot chat**。bot chat 自带编排 sender 身份（实证：不带 --from 跑 run-create  ok）⇒ **不需要 mailbox 终端**。
- 工人 = **预建、可复用的工人 bot**（owner 每个接受一次）；按 §9 brief 派票；**owner 可直接给正在跑的工人 bot 发消息**（该消息即唤醒它）。
- 读输出：`bot chats` 的 lastSaid 是截断预览、`agent read` 对 chat 弱 ⇒ 完整回复用 **orca-computer-use 无障碍树**读（get-app-state --element-index <回复容器>）。
- wake = owner UI 消息。**无外部 cron 盯梢**。
- **全局配置零写入**（~/.claude、cc-switch 一字不动）。端点/模型 = bot/UI 配置（百炼内部缝位）。
- 按 orca-cli skill 选 Orca executable；载版本匹配指南（orca skills get orca-cli / orchestration）；prefer --json。

## 1. 澄清 — 委托
call `grill-with-docs`（它驱动 grilling + domain-modeling）。不复述 rounds/frontier/GLOSSARY 规矩。

## 2. Preflight — 委托 + 自检
照 ship §Preflight（tracker/开放问题/假设 scouting/existing-spec 入口）。
自含附加：用一条 trivial bot prompt 做端点/auth 自检；失败**停并报清楚**，不偷绕。

## 3. Route — 委托
照 ship §Route（trivial/light/standard/wayfinder 拒绝；真 torn → ask-matt）。

## 4. 前段一体 + 派票 — 委托 + brief/缝位
照 ship §Run 与 §Isolation；按 ship 规定 call to-spec / to-tickets / implement-spec（light 用 implement）；前段一体保持一个不间断上下文。
自含：每张就绪票按 **§9 brief 模板**派给工人 bot；从 `docs/agents/orca-seams.md` 注入缝位模型/effort（百炼内部）；工人跑 `pimplement`（tdd-only）并 commit 到自己 worktree 分支。merge 照 ship/implement-spec 规定。

## 5. review / accept / retro — 委托 + 回传模板
按原 skill 规定 call code-review / accept / retro（accept 输入 = spec 或 acceptance-plan 的**路径指针**）。
自含：要求每个工人按 **§9 回传模板**回报；拒收自由格式_dump。

## 6. 人在环 — 委托 + 载体
照 ship §Stopping（三召唤：预算/范围意外/Preflight 拒绝）。
自含：owner 可随时给任何正在跑的 bot 发消息（唤醒/插话）；**gate 只用于真决策**；无过程性确认。

## 7. 预算 — 委托
ship §Failure budgets（票≤2 / review≤2 / accept≤2）。

## 8. Deliver — 委托
ship §Deliver（salvage .scratch、主 checkout merge、**零 push**、清理、close tickets、最终报告）。

## 9. 通信规范（自含，硬节）
**下行 brief（协调者→工人 bot；指针，不传内容）**：
```
ticket: <.scratch/<feature>/issues/NN-*.md 路径>
spec: <.scratch/<feature>/spec.md 路径>
acceptance-criteria-at: <票内「怎么算对」节 / spec 验收节>
base-branch: <integration 分支>
worktree: <本工人 worktree 路径>
model/effort: <缝位值>
task: call pimplement（tdd-only）；commit 到本 worktree 分支。
return: 按回传模板；不贴过程日志。
```
**上行回传（工人→协调者；固定格式）**：
```
commit: <hash>
tests: <总数/失败/跳过>（命令+exit）
boundary: <够不着/偏离声明，无则写无>
evidence: <截图/日志路径>
```
**指针纪律**：会话间只传增量/摘要+指针；spec/diff/日志全量留域内文件按需读；**brief/回传禁贴全文**。

## 10. 非侵入与归档
原链零改动（ADR-0001）。旧 `pgrill-with-docs` 归档为探索资产、非日常依赖。续跑甄别留位（用户搁置）。