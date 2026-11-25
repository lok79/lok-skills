# Ship（中文对照版）

> **本文件仅为中文对照，供阅读；技能执行以英文原版 [SKILL.md](SKILL.md) 为准。**
> 要改规则请改英文原版——改这里不生效。英文原版更新后本文件不会自动跟上。
> 对照基准：2026-11-20 的英文原版。

**技能元信息（frontmatter 翻译）**

- **name**: `ship`
- **description**: 需求澄清之后的一切，自主跑完：给澄清后的工作选路（轻量 implement 还是 to-spec/to-tickets/implement-spec），替用户决定那些技能原本要问的确认，只在预算上限处停下。这是澄清后构建的点火器——只在用户明确要求时调用，绝不自行启动。
- **argument-hint**: 不传参（直接 ship 当前对话），或传一份已有 spec 的引用

---

澄清已经结束：用户在本对话中确认了共同理解（通常经由 `/grill-with-docs`）。Ship 自主运行**下游的一切**——从实现到交付——只在预算耗尽或范围意外时停下。用户此刻的预期是：可以走开了。

## 最高指令（Prime directive）

下游技能原本会向用户要的每一个确认，都**由你来定**：`/to-spec` 会问的接缝（seam）、`/to-tickets` 会问的拆票粒度——凡是澄清没碰过的，靠分析拍板，不靠惯性：判断在当前上下文里多大程度的处理才算相称，并把理由记在用户事后会看的地方（spec 的决策记录、票的备注、最终报告），让事后审查能看到每个默认决策都带着一条可循的理由。产物照常发布，用户是**事后审查**——不是在关口上把关。只有「停下的时机」一节列的三种中断才会召唤用户。

## 隔离：每次运行一个 worktree（Isolation）

多个 ship 会并行跑——同一个仓库上可能同时有几个 `/ship`，主 checkout 里还放着用户自己未提交的工作。一个 git 工作树同一时刻只能停在一个分支上，所以在共享 checkout 里切分支，会把其他所有运行的文件一起拖走。因此：

- **每次运行都在自己的 worktree、自己的分支上干活**：`git worktree add ../.ship-worktrees/<slug>/<repo> -b ship/<slug> <base-branch>`，然后 `cd` 进去——spec、票、提交、dev server、验收全在里面发生。所有路线一视同仁：trivial、轻量、标准全都用 ship 分支；base 分支只会被 Deliver 里的最终 merge 碰到。
- slug 取自功能 slug。worktree 绝不乱丢在工作区根目录：一切收在一个包装目录 `../.ship-worktrees/` 下，每个 ship 一个目录（`<slug>/`），里面每个仓库一个 worktree（`<repo>/`）——中间目录由 `git worktree add` 自己创建。如果 worktree 路径或分支已存在（同一功能早前尝试的残留），先清掉（`git worktree remove --force` + `git branch -D ship/<slug>`）：这个命名空间归本次运行所有。
- worktree 不继承任何被 gitignore 的东西：把 `.env` 这类本地文件、以及该功能的 `.scratch/<feature-slug>/`（spec、票、既有证据——供引用已有 spec 的运行使用）拷进去，再按仓库惯例安装依赖。
- 记下主 checkout 的绝对路径——Deliver 要 merge 回那里。
- 绝不碰不是本次运行创建的分支或 worktree。

## 流程（Process）

### 1. 起飞前检查（Preflight）

- 没有 `docs/agents/issue-tracker.md` → 停下：让用户先跑 `/setup-matt-pocock-skills`。
- 还有悬而未决的问题（需要原型验证的设计问题、没拍板的决策）→ **拒绝**：澄清没做完。列出缺什么，交还给用户。
- 澄清后需求背后的关键假设（外部渠道、没写进文档的数据/行为、第三方集成）→ **先侦察再动工**：逐条实测验证（分钟级探针），把结果追加成 spec 的「关键假设与实测」一节；任何验证失败的假设，拿回给用户调整需求后再继续。侦察只在这里做——绝不在实现中途做。
- 参数引用了已有 spec → 标准路径从 `/to-tickets` 开始，跳过 `/to-spec`。
- 全部检查通过 → 按上面「隔离」一节建 ship worktree 并 `cd` 进去。播报一行：worktree 路径 + 分支。

### 2. 选路（Route）

对照代码库分析澄清后的需求，一行播报选路结论——判定、路径、理由——然后**不等确认，直接推进**：

- **Trivial 路径**——澄清后的改动纯属内容：数据、模板 JSON、文档、配置值——不碰生产代码、不碰 schema、没有跨层概念，且结果能直接观察验证。在 ship worktree 的 ship 分支上干：不开额外分支、不调 `/implement`、不调 `/tdd`、不开 review 子代理。验证就是事物本身——把改的东西渲染或跑起来，亲眼看过了再报告。按仓库惯例提交，几行报告收尾。一旦开始出现代码改动、或范围出意外，停下，回退到轻量路径。
- **Wayfinder 量级**：需求清楚，但怎么建不清楚（全新项目、超大功能、几个架构方向还雾着）。拒绝：推荐 `/wayfinder`；等它的地图清晰了，收敛成一份 spec，再重新 `/ship`。
- **轻量路径（Light）**——活儿一个会话装得下：改动收敛、没有 schema 涟漪、没有跨层新概念。ship 分支就是功能分支：在它上面用 Skill 工具调 `implement`（它自己驱动 `/tdd`、自己跑 `/code-review`，review 的是 `git diff <base-branch>...HEAD`——三点写法，对 merge-base 比较，而那正是本分支切出来的位置）。
- **标准路径（Standard）**——多会话量级：跨层（schema/API/UI）、引入新概念、要拆成多张票。ship 分支兼任集成分支——`implement-spec` 复用它，不另建。按顺序用 Skill 工具调：`to-spec` → `to-tickets` → `implement-spec`（它沿可开工前沿派实现者子代理，并对集成分支跑 `/code-review`；它的每票 worktree 带本次运行的 slug 前缀，并行的 ship 永不撞车）。

真的在两条路之间拿不定？用 Skill 工具调 `ask-matt`，套用它主流程的那个分支判断：*这活儿一个会话能建完吗？*

### 3. 执行（Run）

执行选中的技能，把它们原本要问的确认点转化为你的决策：

- `/to-spec`：不问，自己定接缝——取最高的缝；取最少的缝。
- `/to-tickets`：拆法和阻塞边自己定；确认每张票带「怎么算对」条款（趁上下文新鲜随票落盘；后端票写行为断言，是缝测试的断言来源；前端票写视觉验收标准——对照原型（有原型时）或显性样式破损判据（无原型时），供 accept 截图冒烟当判据）；发布，继续推进。
- `/implement-spec`、`/implement`：照它们写的执行——它们已经自带 `/tdd`、并行子代理和 `/code-review`。

盯住上下文：如果拆票还没做完、会话已逼近 smart zone，就在最近的阶段边界 `/compact`，然后继续。

### 4. 验收（Accept）

用 Skill 工具调 `accept`，传入 spec 路径（`.scratch/<feature-slug>/spec.md`）——这是落地前的最终验证，让用户一条 `/ship` 直通真实环境验证。验收 = 后端行为对真实链路做 HTTP 回放 + 前端页面做冒烟级截图过一遍（每个路由/页面一张落地态截图——有原型时对照原型做粗粒度比较，没原型时按显性 bug 清单核对，不是前后 diff；截图落在 `.scratch/<feature-slug>/screenshots/`，发现以文字记录；用 ego-browser 截——ego 不可用时退回 ZCode 内置浏览器，并记为载体偏差；登录态和路由到达靠 API 登录注入 + 直接 goto，绝不靠点登录表单或菜单；纯展示性交互默认不点，除非该交互本身就是本次改动的核心验收对象；业务行为正确性绝不用截图作证——只认 HTTP 回放，否则标「无可自动化验收项」；环境事实与红线在 `docs/agents/acceptance.md`）；后端证据以文字落进 spec 的 Comments。**在 ship worktree 里跑**：用 worktree 的代码构建并启动 dev server / 验收后端，端口选一个没有其他存活 ship 占用的，并把端口记进证据；验收数据库可以与并行 ship 共用——它以读为主的回放和凭据行红线已经考虑了这一点。并行 ship 同时验收：在 worktree/端口隔离之上，浏览器隔离遵循 accept 的页面归属约定——每次运行只碰自己的页面和 TaskSpace（命名 `accept-<slug>`），绝不碰用户的标签页或别的运行的。验收失败是真实发现：如实记录证据，走修复预算回炉（最多 2 轮修复-复验），仍失败就停下报告。两条缝都够不着的项（如硬件/设备行为）记为「无可自动化验收项」，绝不硬凑。最终报告必须带上验收判定（通过 / 失败 / 卡点）和一切边界偏差。

### 5. 交付（Deliver）

落地本次运行：在**主 checkout** 里把 ship 分支 merge 进 base 分支——**任何东西都不 push**：

- **先抢救被 gitignore 的产物**：`.scratch/<feature-slug>/`（spec、票、验收证据）是被 gitignore 的本地约定——merge 带不走它。在任何后续步骤可能毁掉它之前，把整个目录从 worktree 拷回主 checkout；放弃的运行也要先抢救，再拆。
- **在主 checkout 里 merge，绝不在 worktree 里**：`git -C <main-checkout> merge ship/<slug>`（路径是 Preflight 记下的那个）。用户回来时，base 分支已经包含这次的工作。
- **merge 绝不让用户赔上未提交的改动。**如果 merge 被本次运行之前就已在 base 分支上未提交的文件挡住：`git stash push` 它们（message 注明这是用户的改动）→ 完成 merge → 立刻 `git stash pop`。绝不用丢弃类操作清路（`reset --hard`、`checkout --`、`clean`），也绝不把用户的改动留在 stash 里不管。
- **并行交付**：另一个 ship 可能同一瞬间也在 merge——遇到 `index.lock` 争用，稍等重试。如果 merge 本身冲突（两个 ship 改了同一批文件）：`git merge --abort`（若 stash 过则接着 `git stash pop`），停下报告——跨 ship 的冲突怎么解是用户的决定，在修复预算之外。
- **清理**：本地删掉 ship 分支（`git branch -d`，有未合并内容它会拒绝）并移除 worktree（`git worktree remove`，若因 gitignore 的构建产物拒绝则加 `--force`——只允许在抢救步骤之后用）。绝不删不是本次运行创建的分支或 worktree。
- **放弃失败的运行** = 抢救 `.scratch/<feature-slug>/`，然后移除 worktree、删掉 ship 分支（`git branch -D`——它从没被合并，这正是重点）。主 checkout 从未被本次运行碰过，所以没什么可 reset，用户既有的未提交改动永远没有危险。
- **全程零 push**：不 push 任何分支、不 push 合并后的 base 分支、不开 PR。有远端（GitHub/GitLab）也原样不动；push 或开 PR 是用户之后的决定。
- 按本地约定关票。

收尾用用户的语言写报告：spec 和票（路径）、工作怎么落的地（哪个 ship 分支 merge 进了哪个 base 分支；worktree 和分支已清理）、code-review 状态（提了多少发现、修了多少）、从 Accept 带过来的验收判定、消耗的预算、一句话结果——外加一句「什么都没 push」。

## 失败预算（Failure budgets）

预算内自愈；超预算，停：

- 实现失败的票：重新发起（换新实现者），最多 **2** 次重试。
- `/code-review` 的发现：修，然后重跑 review——最多 **2** 轮。发现清零、或只剩不阻塞的判断题时，review 算过。
- 验收失败：修复并复验——最多 **2** 轮。
- 任何一处超预算 → 停下报告：卡在哪、试过什么、用户需要拍的那一个决策。

## 停下的时机（Stopping）

运行中途只有三件事能召唤用户：

1. **预算耗尽**（见上）。
2. **范围意外**：某个发现改变了「做完」的定义——「小改动」里藏着跨模块重构。展示已落地的部分，摆出选项，问用户。
3. **Preflight 拒绝**（缺 tracker、澄清未完成、wayfinder 量级）。

绝不为这些停下：接缝选择、拆票粒度、预算内的 review 发现、以及 merge（它是 Deliver 的一部分，不是问题）。

## 播报（Narration）

每个阶段边界一行，用用户的语言，绝不提问：worktree 已建（路径 + 分支）；选路判定；spec 已发布；票已发布（共 N 张，K 张现在可开工）；票已合并（i/N）；发生重试时报一行；review 通过；验收判定（通过 / 失败 / 卡点）；已落地（ship 分支 merge → 主 checkout 的 base 分支，worktree 已移除）；已交付。用户应该可以无视这里的每一行，只读最终报告。