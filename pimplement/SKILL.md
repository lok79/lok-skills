---
name: pimplement
description: "tdd-only implement variant for the Orca coordinator chain (pgrill-with-docs): builds a ticket/spec via tdd but does NOT run code-review internally — review is an external seam the coordinator dispatches. Mid-chain step; invoke only within pgrill-with-docs or on explicit user request; never on your own initiative."
---

# pimplement（tdd-only 变体）

原 `implement` 的平行变体：**只经 tdd 构建，不内置 code-review**。review 被外置成缝，由协调者（pgrill-with-docs）在本工人报告后派独立 review 面板工人。原 implement 一字不改、日常照用。

Implement the work described in the spec or ticket. Machinery they don't ask for — validation, defensive checks, error paths, retries, abstraction — is yours to decide by analysis, not reflex: where do inputs come from, what does failure cost, what would it guard, what does it cost to carry? Build what the analysis says is proportionate — which may be nothing — and give the why in your report.

If passed a ticket reference, fetch it from the issue tracker and state its title before starting. If ambiguous, ask.

Call the Skill tool with "tdd" at pre-agreed seams, by default. Skip only when the change carries no observable behavior (pure copy, comments, configuration values) — and if you skip, state that reason in the final report. "No test infrastructure" is not a skip reason: test at the highest seam the runtime allows.

If a Skill call fails with a name error (`ambiguous for subagent`, `not allowed for subagent`), don't retry another spelling — Read `/Users/lok/.agents/skills/tdd/SKILL.md` and follow it directly.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

**不要 call code-review。** review 是外置缝：协调者在本工人报告后派独立 review 面板（standard=全票落地后 ONE 次 integration review；light=本 implement 后一次）。本技能内审会破坏缝的可换底座/模型性。

Commit your work to the current branch.

Report: what was built, tdd seams used, any skip reason, machinery whys, commit ref; note that review is pending as an external seam (not done here).