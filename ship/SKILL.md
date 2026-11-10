---
name: ship
description: "Run everything after requirements clarification, autonomously: route the clarified work (light implement vs to-spec/to-tickets/implement-spec), decide what those skills would normally ask the user, and stop only at a budget limit. Ignition of the post-clarification build — invoke only on the user's explicit request; never on your own initiative."
argument-hint: "Nothing (ship the current conversation), or a reference to an existing spec"
---

# Ship

The clarification is over: the user has confirmed a shared understanding in this conversation (typically via `/grill-with-docs`). Ship runs **everything downstream** autonomously — implementation through delivery — and stops only at a budget limit or a scope surprise. The user expects to walk away now.

## Prime directive

Every confirmation the downstream skills would normally ask for is **yours to decide**: the seams `/to-spec` asks about, the granularity `/to-tickets` asks about — and anything the clarification never touched is decided by analysis, not reflex: judge what degree of handling this context makes proportionate, and record the why where the user will review it (spec decisions, ticket notes, final report), so the after-the-fact review finds every default carrying a why it can follow. The artifacts still get published, so the user reviews **after the fact** — not at a gate. Only the three interruptions in **Stopping** ever summon the user.

## Process

### 1. Preflight

- No `docs/agents/issue-tracker.md` → stop: tell the user to run `/setup-matt-pocock-skills`.
- Open questions still hanging (a design question needing a prototype, an unmade decision) → **refuse**: clarification isn't done. List what's missing and hand back.
- Key assumptions behind the clarified requirement (external channels, undocumented data/behaviour, third-party integrations) → **scout before building**: verify each empirically (minutes-level probes), append a `关键假设与实测` section to the spec with the results, and take any failed assumption back to the user to adjust the requirement before proceeding. Scouting happens here — never mid-implementation.
- An argument referencing an existing spec → the standard path starts at `/to-tickets`, skipping `/to-spec`.

### 2. Route

Analyze the clarified requirement against the codebase and announce the route in one line — verdict, path, reason — then **proceed without waiting**:

- **Trivial path** — the clarified change is content-only: data, template JSON, docs, config values — no production code, no schema, no cross-layer concepts, and the result is verifiable by direct observation. Work on the base branch directly: no feature branch, no `/implement`, no `/tdd`, no review subagents. The verification is the thing itself — render or run what changed and look at it before reporting. Commit in the repo's convention and report in a few lines. If code changes start appearing or the scope surprises, stop and fall back to the light path.
- **Wayfinder scale**: requirements are clear, but the way to build them isn't (greenfield, a huge feature, several architectural directions still foggy). Refuse: recommend `/wayfinder`; when its map clears, it collapses into a spec, then `/ship` again.
- **Light path** — the work fits one session: a contained change, no schema ripple, no new concepts crossing layers. Then no feature branch: record the base branch's current HEAD SHA as the review fixed point, then call the Skill tool with `implement` on the base branch itself (it drives `/tdd` and runs `/code-review` itself, reviewing `git diff <fixed point>...HEAD`).
- **Standard path** — multi-session scale: crosses layers (schema/API/UI), introduces concepts, will slice into multiple tickets. Call the Skill tools in order: `to-spec`, then `to-tickets`, then `implement-spec` (it runs implementer subagents across the frontier and `/code-review` over the integration branch).

Genuinely torn between routes? Call the Skill tool with `ask-matt` and apply its main-flow branch: *can this be built in one session?*

### 3. Run

Execute the routed skills, converting their checkpoints into decisions:

- `/to-spec`: pick the seams yourself — prefer existing seams, the highest one possible, and the fewest.
- `/to-tickets`: decide slicing and blocking edges yourself; 确认每张票带「怎么算对」的断言条款(趁上下文新鲜随票落盘,缝测试的断言来源);publish and keep moving.
- `/implement-spec`, `/implement`: follow them as written — they already drive `/tdd`, parallel subagents, and `/code-review`.

Watch context: if the session nears the smart zone before ticketing is done, `/compact` at the nearest phase boundary and carry on.

### 4. Deliver

Finish locally on the base branch — **nothing is ever pushed**:

- **Trivial and light paths** (no feature branch): the work already sits on the base branch as commits — no merge, no branch to delete. Abandoning a failed run means resetting **only this run's own commits** back to the recorded fixed point; the user's pre-existing uncommitted changes are never touched.
- **Standard path** (integration branch):
  - Merge the feature branch back into the base branch it was cut from (usually main), locally, before the run ends: when the user returns, the base branch already contains the work.
  - **The merge must never cost the user their uncommitted changes.** If the merge is blocked by files that were already uncommitted on the base branch before this run, `git stash push` them (message noting these are the user's changes) → complete the merge → `git stash pop` immediately. Never clear the way with discard operations (`reset --hard`, `checkout --`, `clean`), and never leave the user's changes sitting in the stash.
  - After the merge, delete the feature branch created in this run locally (`git branch -d`, which refuses if anything is unmerged). Never delete branches you did not create in this run.
- **Zero push, all run**: push no branch, push no merged base branch, open no PR. If a remote (GitHub/GitLab) exists, leave it untouched; pushing or opening a PR is the user's call afterwards.
- Close the tickets per the local convention.

End with a report in the user's language: spec and tickets (paths), how the work landed (standard: merged into which base branch, which feature branch was deleted; light/trivial: committed directly on the base branch), code-review status (findings raised vs fixed), budgets consumed, one-line outcome — a note that nothing was pushed.

### 5. Accept

Call the Skill tool with `accept`, passing the spec path (`.scratch/<feature-slug>/spec.md`) — the last phase of the chain, so the user's single `/ship` runs all the way through real-environment verification. Acceptance is HTTP-replay against the real chain only (environment facts and red lines live in `docs/agents/acceptance.md`); evidence lands in the spec's Comments as text. An acceptance failure is a real finding: record the evidence honestly, route it back through the fix budget (max 2 fix-and-reverify rounds), then stop and report if still failing. HTTP-unreachable items are recorded as「无可自动化验收项」, never force-fitted. The final report must include the acceptance verdict (通过 / 失败 / 卡点) and any boundary deviations.

## Failure budgets

Self-heal within budget; over budget, stop:

- A ticket whose implementation fails: relaunch it (fresh implementer) up to **2** retries.
- `/code-review` findings: fix, then re-run the review — up to **2** rounds. Review passes when findings reach zero or only non-blocking judgement calls remain.
- Acceptance failure: fix and re-verify — up to **2** rounds.
- Over budget anywhere → stop and report: where it's stuck, what was tried, the single decision the user needs to make.

## Stopping

Only three things summon the user mid-run:

1. **Budget exhausted** (above).
2. **Scope surprise**: a discovery that changes what "done" means — the "small change" hides a cross-module refactor. Show what has already landed, lay out the options, ask.
3. **Preflight refusal** (missing tracker, unfinished clarification, wayfinder scale).

Never stop for: seam choices, ticket granularity, review findings within budget, and the merge (it's part of Deliver, not a question).

## Narration

One line per phase boundary, in the user's language, never a question: route verdict; spec published; tickets published (N total, K runnable now); ticket merged (i/N); a retry when one happens; review passed; landed (standard: branch merged → base, local only; light/trivial: committed on the base branch); delivered. The user should be able to ignore every line of this and read only the final report.
