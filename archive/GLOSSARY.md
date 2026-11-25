# Orca 编排协调者（Orchestration）

在 matt 技能链之上加一层 Orca 编排：把链的各阶段派给可独立指派「底座 + 模型」的面板工人，协调者持派票权并落地。本表只收本_context_ 已确认的领域语言；命名与架构已定稿（Q19–26，ADR-0001）。

## Language

**协调者（Coordinator）**:
拥有一个 Run 的单一 agent 会话；跑前段一体、持派票权、派缝工人、落 Deliver。协调者不是工人。
_Avoid_: 主控、master、orchestrator（平台义）

**缝（Seam）**:
可独立指派「底座 + 模型」的阶段边界，编排切换的单位。四条可换缝：票级 implement、code-review、accept、retro。
_Avoid_: 阶段、step、node

**前段一体（Front monolith）**:
grill→to-spec→to-tickets 在同一不间断上下文、同一底座+模型里完成；light 路线上延伸到 implement。不是缝。
_Avoid_: 澄清段、前段（歧义）

**面板工人（Panel worker）**:
以结构化聊天面板（非终端 TUI）呈现的被监督工人；一个被派的任务/缝对应一个面板。
_Avoid_: 终端工人、subagent（子代理义）

**tdd-only 变体（tdd-only variant）**:
只经 tdd 构建、不内置 code-review 的 implement 变体；review 被外置成缝。
_Avoid_: 精简 implement、lite implement

**integration review**:
standard 路线全部票落地到 integration 分支后的那一次 code-review；区别于 light 的单次 implement 后 review。
_Avoid_: 每票 review、逐票审

**非侵入平行技能族（Non-invasive parallel skill family）**:
与原技能并列新增的 Orca 技能族；原技能永不修改，新族只读组合原技能。
_Avoid_: 改版 ship、ship v2、ship 模式

**派票（Dispatch）**:
协调者把一张就绪票指派给一个面板工人，并选定其底座+模型。
_Avoid_: 分发、spawn

**决策门（Gate）**:
在面板里 surfaced 给人拍板的阻塞决策点。
_Avoid_: 审批、checkpoint

**底座（Base）**:
一个现成的 agent CLI 运行时（zcode / claude / codex …），不是平台自家 agent loop，也不是模型。
_Avoid_: 模型、provider

**缝位配置（Seam config）**:
缝→(底座, 模型) 的声明式映射，协调者派票时读取；用户可自行编辑覆盖。
_Avoid_: 硬编码路由、模型写死

**平行入口（Parallel entry）**:
Orca 链的统一入口兼协调者（技能名 pgrill-with-docs，p=parallel）；一个技能承担澄清+协调+派票+Deliver。原 grill-with-docs 与 ship 保留日常用。
_Avoid_: ship v2、Orca 模式、主控