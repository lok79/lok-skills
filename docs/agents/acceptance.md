# Project profile — ~/.agents/skills（Orca 协调者平行技能族）

> survey 实探于 2026-11-20。stack = markdown 技能库（无传统 app runtime）；本 profile 服务于 fhip/verify 对「新增 pgrill-with-docs + pimplement + 缝位配置」的真环境验收。未立事实标 未知，不糊。

## 运行方式

- **被测 runtime = Orca**（编排层）。app 已 running（pid 见 `orca status`），runtime state=ready，v1.4.247。启动：`/Applications/Orca.app/Contents/Resources/bin/orca open --json`；无头：`orca serve --port <port>`（spike 记默认 6768）。
- **skills repo 本身无 build/test/typecheck 命令**（无 package.json/Makefile/pyproject/Cargo；纯 SKILL.md markdown）。"运行"= 被 agent harness（claude/zcode/Orca）消费；验证 = dogfood 跑协调者链。
- 停止/清理：`orca terminal close --worktree <sel> --all`、`orca worktree rm --worktree <sel> --force --delete-branch`、`orca orchestration reset --all`（仅清本次 spike/run 状态）。
- 占用资源：Orca runtime + 其 worktrees（`~/orca/workspaces/<repo>/<name>`）+ fhip worktrees（`../.fhip-worktrees/<slug>/<repo>`）+ serve 端口（若起）。

## 认证与凭证

- **无 DB / 无登录表 / 无临时凭证行机制**。"凭证"= agent 端点配置：claude 走 `~/.claude/settings.json` 的 env（`ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`，智谱兼容端点）；zcode 走自身配置。
- Orca structured chat 面板要求 agent 配置**带上 env 端点**；spike 实证：launch 未带 env（agentEnv 空）→ `notSignedIn`。降级序：现有端点配置 → 无更下层（不写任何凭证存储）。
- 本 profile 不写凭证；verify 只读端点配置存在性，不打印 token 值。

## 缝登记

- **S1 Orca orchestration CLI（first-class）**：drive = `orca orchestration run-create / task-create --deps / task-list --ready / worker-start --agent --model / send / gate-create / gate-resolve / worker-release`；assert = 回执 JSON `ok` 与字段（dispatchId/taskId/status/delivery/followUpOf）；全程 CLI 可后台 start→drive→capture→clean。
- **S2 工人输出观察（first-class）**：drive = `orca orchestration worker-read --source auto|transcript|terminal`、`orca terminal read / wait --for tui-idle`；assert = 输出含预期标记、status/liveness 字段；后台可跑。
- **S3 技能内容结构（first-class）**：drive = filesystem 读 SKILL.md；assert = frontmatter name/description 齐全、references 路径存在、Skill call 名对应已装技能、新技能只读引用原技能（不改原文件）；后台可跑。
- **S4 dogfood 端到端（first-class）**：drive = 在 Orca 以 pgrill-with-docs 协调者跑一个 scratch feature；assert = 面板工人创建（structured）、票级派票、gate 阻塞/解锁、review/accept 制品落 `.scratch/<feature>/`、Deliver merge；证据 = S1/S2 回执 JSON + `.scratch` 制品；后台可跑（CLI+文件）。
- **S5 Orca 面板视觉（foreground，off）**：原生桌面截图需 computer-use / ai-screen（GUI）；ego-browser 只适用 web、不适用原生 Orca app。默认 off；启用 = 将本缝改 foreground-enabled 并经 ai-screen 分层路由（用户屏幕零打扰）。

## 副作用面

- **可写**：`.scratch/<feature>/`（spec/票/验收证据）、Orca worktrees、Orca 协调状态（run/tasks/gates）、skills repo 的 git 分支与提交（fhip/<slug>）。
- **只读 / 红线**：用户其他 repo（个人公司/tapd 等）、**原技能文件（ship/implement/implement-spec/accept 等禁改）**、`~/.claude/settings.json`（只读存在性）、用户浏览器标签/其他 run 的 worktree。

## 性能口径

未定（verify 只测不判）。计时法：S1 回执耗时、S2 worker-read 时间戳；无项目阈值。

## 够不着清单

- Orca 面板视觉渲染细节（S5 foreground off，未启用则不验）。
- 模型输出质量 / 底座×模型可用性（用户已实测，OUT）。
- Orca 商业许可/定价（未知，未取证）。
- 真实多底座认证组合的逐一实跑（OUT；spike 已证机制）。