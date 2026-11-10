# CUSTOM.md — 自写与改造 skill 清单

> 用途：每次 refresh Matt 上游后，照此清单核对 `git status` / `git diff`。
> 任何本清单内的 skill 被上游内容覆盖 = 事故，用 `git checkout -- <skill>/` 一秒恢复。
> 基线：2026-11-10 与上游 mattpocock/skills@main 的全量 diff。

## 自写（上游没有，refresh 绝不可覆盖）

- accept
- computer-use
- ego-browser
- gen-image
- orca-cli
- orchestration
- probe
- ship
- show-me

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
