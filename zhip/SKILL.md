---
name: zhip
description: "Delegated variant of /ship: after requirements clarification, orchestrate everything in this (strong) session — spec, tickets, and an executor-ready superpowers plan — then stop at one handoff while a cheap executor agent implements the plan in its own session, then take back, review, accept, and deliver here. Invoke only on the user's explicit request; never on your own initiative."
argument-hint: "Nothing (zhip the current conversation), or a reference to an existing spec"
---

# Zhip

The clarification is over: the user has confirmed a shared understanding in this conversation (typically via `/grill-with-docs`). Zhip runs the same post-clarification build as `/ship` with one structural difference: **implementation is delegated**. This session produces spec, tickets, and a plan; a cheap executor agent implements the plan in a separate session; this session then takes back, reviews, accepts, and delivers. The user expects to walk away — except at the handoff, which is zhip's one deliberate stop.

Calls zhip makes to `to-spec`, `to-tickets`, `code-review`, and `accept` carry the user's explicit request authority: the user ignited this chain, so the mid-chain descriptions of those skills are satisfied.

## Process

### 1. Preflight

Read `/Users/lok/.agents/skills/ship/SKILL.md` and follow its **Preflight** section verbatim — tracker check, open-questions refusal, assumption scouting, existing-spec entry — including the worktree creation under its **Isolation: one worktree per run** section. One narration line: worktree path + branch.

### 2. Route

Apply ship's routing criteria exactly: Read ship's **Route** section and decide trivial / light / standard / wayfinder by its standards, never from memory. Then map the verdict (this mapping is zhip's own):

- **Wayfinder** → refuse exactly as ship's Route section prescribes.
- **Trivial** → Read ship's Route section's trivial-path bullet and follow it verbatim. Nothing is delegated; the run stays in this session end to end.
- **Light** → call the Skill tool with `to-spec`, then step 3.
- **Standard** → call the Skill tool with `to-spec`, then `to-tickets`, then step 3.

On the light and standard routes, `to-spec` and `to-tickets` run under ship's Prime directive as well (Read ship's **Prime directive** section): their checkpoints become your decisions.

### 3. Plan and hand off

Call the Skill tool with `to-plan`. It writes `.scratch/<slug>/plan.md` and `.scratch/<slug>/handoff.md` inside the ship worktree. Then **stop**: tell the user, in one line, that the handoff prompt is at `<worktree>/.scratch/<slug>/handoff.md` — paste its contents into a fresh session of the executor agent. Wait. Do not proceed until the user reports back.

### 4. Take back

When the user reports done or blocked:

- Read `<worktree>/.scratch/<slug>/report.md` — the executor's self-report: self-fix list, leftovers, BLOCKED details if any.
- Read `workspace/ledger.md` if the executor kept one (the handoff requires it): mid-run rulings where the plan was silent. Audit each against the ruling line in `handoff.md` — a ruling that touched locked-in behavior (assertion values, UI copy, API responses) is a review finding even if the executor flagged it honestly.
- **Do not trust claims of green.** Verify in the worktree yourself: `git log`, then run the test suite (or a targeted spot-check) per repo convention.
- Whitelist self-fixes (the whitelist terms live in `handoff.md` — `to-plan` owns them; do not restate them here): accept and continue.
- BLOCKED: diagnose in this session, revise the plan (re-run `to-plan` or edit `plan.md`), then re-hand-off. Round-trips count against the retry budget of the ticket they block.
- Over budget anywhere → stop and report, per ship's **Failure budgets** section.

### 5. Review

Call the Skill tool with `code-review`, fixed point `<base-branch>` (three-dot diff of the ship branch — exactly where this run was cut). Fix findings **yourself** in the worktree: the strong session does the fixing; the executor is never summoned back for fixes. Re-run the review until findings are zero or non-blocking, within ship's review budget.

### 6. Accept

Read ship's **Accept** section and follow it verbatim: call the Skill tool with `accept`, passing the spec path (`.scratch/<slug>/spec.md`); run inside the ship worktree; fix budget, verdict wording, and red lines as written there.

### 7. Deliver

Read ship's **Deliver** section and follow it verbatim: salvage `.scratch/<slug>/` into the main checkout first, merge there (never in the worktree), cleanup, zero push, close tickets.

## Failure budgets

Read ship's **Failure budgets** section and apply it unchanged, plus one zhip-specific rule: executor BLOCKED round-trips count as the ticket-retry budget of the ticket they block.

## Stopping

Ship's three (Read its **Stopping** section) plus zhip's two by design: the handoff stop (step 3) and the take-back wait (step 4). Never stop for anything else that ship itself wouldn't stop for.

## Narration

One line per phase boundary, in the user's language, never a question: worktree created (path + branch); route verdict (+ "delegated" on light/standard); spec published; tickets published (N total); handoff ready (plan path + handoff path); taken back (report verdict); review passed; acceptance verdict (通过 / 失败 / 卡点); landed (ship branch merged → base branch in the main checkout, worktree removed); delivered. The user should be able to ignore every line of this and read only the final report.
