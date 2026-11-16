# CUSTOM.md — 自写与改造 skill 清单

> 用途：每次 refresh Matt 上游后，照此清单核对 `git status` / `git diff`。
> 任何本清单内的 skill 被上游内容覆盖 = 事故，用 `git checkout -- <skill>/` 一秒恢复。
> 基线：2026-11-10 与上游 mattpocock/skills@main 的全量 diff。

## 自写（上游没有，refresh 绝不可覆盖）

- accept
- computer-use
- ego-browser
- fhip
- gen-image
- orca-cli
- orchestration
- probe
- ship
- show-me
- survey
- to-plan
- verify
- zhip

## 改造过（与上游不同，refresh 前先看 diff，保留本地版）

- ask-matt
- chief-of-staff
- code-review
- codebase-design
- grill-with-docs
- grilling
- implement
- implement-spec
- improve-codebase-architecture
- research
- setup-matt-pocock-skills
- tdd
- to-spec
- to-tickets
- wayfinder

## 与上游一致（可被安全覆盖）

- claude-handoff, diagnosing-bugs, domain-modeling, git-guardrails-claude-code,
  grill-me, handoff, loop-me, migrate-to-shoehorn, pr, prototype, retro,
  scaffold-exercises, setup-pre-commit, setup-ts-deep-modules, teach,
  to-questionnaire, triage, wait-what, wizard,
  writing-beats, writing-for-agents, writing-fragments, writing-shape

## superpowers-dist（obra/superpowers 本机母版，zhip/to-plan 的外部依赖）

- `~/.agents/superpowers-dist/` = obra/superpowers 的 git clone（保留 git）；升级 = `git pull` 后 `git diff HEAD@{1}` 看上游变化
- 消费面 1：`to-plan` 运行时 Read `dist/skills/writing-plans/SKILL.md` 当 plan 格式规范。升级 diff 触及 writing-plans 时，复查 to-plan 的 override 清单（语言/落点/头部/任务序）是否仍成立
- 消费面 2：执行端安装 = 复制 4 个裁剪子目录（`executing-plans`、`test-driven-development`、`verification-before-completion`、`systematic-debugging`）到执行端自己的 skills 目录。**不用任何端的 marketplace/plugin 安装**——那会装全套 + using-superpowers 强制网，违背裁剪原则
- 执行端合格判据：skills 目录机制 / 能跑 shell / 同机文件系统 / 便宜档位 / fresh 会话。满足即合格，不锁定产品
- `zhip` 引用 ship 的节名锚点（Preflight / Route / Prime directive / Accept / Deliver / Failure budgets / Stopping）；`fhip` 引用同批锚点 + Isolation / Run / Narration（其 Accept 被 verify 覆写）：ship 改版重排这些节名时，同步检查 zhip 和 fhip 的引用

## 刷新流程（替代旧的"备份→全目录覆盖"）

```bash
# 1. 拉上游到临时目录
rm -rf /tmp/mattpocock-skills-upstream
git clone --depth 1 https://github.com/mattpocock/skills /tmp/mattpocock-skills-upstream

# 2. 只同步「与上游一致」清单里的 skill（粗暴法：先覆盖，再靠 git 抢救）
rsync -a --delete /tmp/mattpocock-skills-upstream/skills/*/<name>/ ~/.agents/skills/<name>/   # 逐个一致项

# 3. 核对改造项：上游有值得吸收的改动吗？
diff -rq ~/.agents/skills/<改造项>/ /tmp/mattpocock-skills-upstream/skills/*/<改造项>/

# 4. git 定格
git -C ~/.agents/skills add -A && git -C ~/.agents/skills commit -m "refresh $(date +%F)"
# 误覆盖 → git -C ~/.agents/skills checkout -- <skill>/
```
