---
name: ship
description: "Run everything after requirements clarification, autonomously: route the clarified work (light implement vs to-spec/to-tickets/implement-spec), decide what those skills would normally ask the user, and stop only at a budget limit. Ignition of the post-clarification build — invoke only on the user's explicit request; never on your own initiative."
argument-hint: "Nothing (ship the current conversation), or a reference to an existing spec"
---

# Ship

The clarification is over: the user has confirmed a shared understanding in this conversation (typically via `/grill-with-docs`). Ship runs **everything downstream** autonomously — implementation through delivery — and stops only at a budget limit or a scope surprise. The user expects to walk away now.

## Prime directive

Every confirmation the downstream skills would normally ask for is **yours to decide**: the seams `/to-spec` asks about, the granularity `/to-tickets` asks about — and anything the clarification never touched is decided by analysis, not reflex: judge what degree of handling this context makes proportionate, and record the why where the user will review it (spec decisions, ticket notes, final report), so the after-the-fact review finds every default carrying a why it can follow. The artifacts still get published, so the user reviews **after the fact** — not at a gate. Only the three interruptions in **Stopping** ever summon the user.

## Isolation: one worktree per run

Ship runs happen in parallel — several `/ship` on the same repo at once, plus the user's own uncommitted work sitting in the main checkout. A git working tree can only sit on one branch, so any branch switch in the shared checkout drags every other run's files with it. Therefore:

- **Every run works in its own worktree, on its own branch**: `git worktree add ../.ship-worktrees/<slug>/<repo> -b ship/<slug> <base-branch>`, then `cd` into it — specs, tickets, commits, dev servers, acceptance all happen there. All routes are equal here: trivial, light, and standard alike work on the ship branch; the base branch is only ever touched by the final merge in Deliver.
- The slug comes from the feature slug. Worktrees never litter the workspace root: everything lives under one wrapper directory `../.ship-worktrees/`, grouped one directory per ship (`<slug>/`), one worktree per repo inside (`<repo>/`) — `git worktree add` creates the intermediate directories itself. If the worktree path or the branch already exists (leftover of an earlier attempt at this same feature), remove them first (`git worktree remove --force` + `git branch -D ship/<slug>`): this namespace belongs to this run.
- A worktree inherits nothing gitignored: copy `.env`-style local files and the feature's `.scratch/<feature-slug>/` (spec, tickets, prior evidence — for runs that reference an existing spec) into it, then install dependencies per the repo convention.
- Record the main checkout's absolute path — Deliver merges back there.
- Never touch branches or worktrees this run did not create.

## Process

### 1. Preflight

- No `docs/agents/issue-tracker.md` → stop: tell the user to run `/setup-matt-pocock-skills`.
- Open questions still hanging (a design question needing a prototype, an unmade decision) → **refuse**: clarification isn't done. List what's missing and hand back.
- Key assumptions behind the clarified requirement (external channels, undocumented data/behaviour, third-party integrations) → **scout before building**: verify each empirically (minutes-level probes), append a `关键假设与实测` section to the spec with the results, and take any failed assumption back to the user to adjust the requirement before proceeding. Scouting happens here — never mid-implementation.
- An argument referencing an existing spec → the standard path starts at `/to-tickets`, skipping `/to-spec`.
- All checks pass → create the ship worktree per **Isolation** above and `cd` into it. One narration line: worktree path + branch.

### 2. Route

Analyze the clarified requirement against the codebase and announce the route in one line — verdict, path, reason — then **proceed without waiting**:

- **Trivial path** — the clarified change is content-only: data, template JSON, docs, config values — no production code, no schema, no cross-layer concepts, and the result is verifiable by direct observation. Work on the ship branch in the ship worktree: no extra branch, no `/implement`, no `/tdd`, no review subagents. The verification is the thing itself — render or run what changed and look at it before reporting. Commit in the repo's convention and report in a few lines. If code changes start appearing or the scope surprises, stop and fall back to the light path.
- **Wayfinder scale**: requirements are clear, but the way to build them isn't (greenfield, a huge feature, several architectural directions still foggy). Refuse: recommend `/wayfinder`; when its map clears, it collapses into a spec, then `/ship` again.
- **Light path** — the work fits one session: a contained change, no schema ripple, no new concepts crossing layers. The ship branch is the feature branch: call the Skill tool with `implement` on it (it drives `/tdd` and runs `/code-review` itself, reviewing `git diff <base-branch>...HEAD` — three-dot against the merge-base, which is exactly where this branch was cut).
- **Standard path** — multi-session scale: crosses layers (schema/API/UI), introduces concepts, will slice into multiple tickets. The ship branch doubles as the integration branch — `implement-spec` reuses it, it does not create another. Call the Skill tools in order: `to-spec`, then `to-tickets`, then `implement-spec` (it runs implementer subagents across the frontier and `/code-review` over the integration branch; its per-ticket worktrees take this run's slug prefix so parallel ships never collide).

Genuinely torn between routes? Call the Skill tool with `ask-matt` and apply its main-flow branch: *can this be built in one session?*

### 3. Run

Execute the routed skills, converting their checkpoints into decisions:

- `/to-spec`: decide the seams without asking — the highest seam; and the fewest.
- `/to-tickets`: decide slicing and blocking edges yourself; 确认每张票带「怎么算对」条款(趁上下文新鲜随票落盘;后端票写行为断言,是缝测试的断言来源;前端票写视觉验收标准——对照原型或预期样式描述,供 accept 截图对比当判据);publish and keep moving.
- `/implement-spec`, `/implement`: follow them as written — they already drive `/tdd`, parallel subagents, and `/code-review`.

Watch context: if the session nears the smart zone before ticketing is done, `/compact` at the nearest phase boundary and carry on.

### 4. Accept

Call the Skill tool with `accept`, passing the spec path (`.scratch/<feature-slug>/spec.md`) — the final verification before landing, so the user's single `/ship` runs all the way through real-environment verification. Acceptance is HTTP-replay against the real chain for backend behavior plus screenshot comparison for frontend pages (rendered screenshot vs prototype; before/after when no prototype — screenshots land in `.scratch/<feature-slug>/screenshots/`, diff list as text; captured with ZCode's built-in browser, never by clicking through the UI to establish state — login form and menus untouched, environment facts and red lines live in `docs/agents/acceptance.md`); backend evidence lands in the spec's Comments as text. Run it **inside the ship worktree**: build and start the dev server / acceptance backend from the worktree's code on a port no other live ship occupies, recording the port in the evidence; the acceptance database may be shared with parallel ships — its read-mostly replay and credential-row red lines already account for that. An acceptance failure is a real finding: record the evidence honestly, route it back through the fix budget (max 2 fix-and-reverify rounds), then stop and report if still failing. Items neither seam can reach (e.g. hardware/device behavior) are recorded as「无可自动化验收项」, never force-fitted. The final report must include the acceptance verdict (通过 / 失败 / 卡点) and any boundary deviations.

### 5. Deliver

Land the run: merge the ship branch into the base branch in the **main checkout** — **nothing is ever pushed**:

- **Salvage gitignored artifacts first**: `.scratch/<feature-slug>/` (spec, tickets, acceptance evidence) is a gitignored local convention — the merge cannot carry it. Copy the whole directory from the worktree back to the main checkout before any later step can destroy it; on an abandoned run, salvage it too, then tear down.
- **Merge in the main checkout, never in the worktree**: `git -C <main-checkout> merge ship/<slug>` (the path recorded in Preflight). When the user returns, the base branch already contains the work.
- **The merge must never cost the user their uncommitted changes.** If the merge is blocked by files that were already uncommitted on the base branch before this run, `git stash push` them (message noting these are the user's changes) → complete the merge → `git stash pop` immediately. Never clear the way with discard operations (`reset --hard`, `checkout --`, `clean`), and never leave the user's changes sitting in the stash.
- **Parallel delivery**: another ship may be merging at the same moment — on `index.lock` contention, wait briefly and retry. If the merge itself conflicts (two ships touched the same files): `git merge --abort` (then `git stash pop` if you stashed), stop and report — cross-ship conflict resolution is the user's call, outside the fix budgets.
- **Cleanup**: delete the ship branch locally (`git branch -d`, which refuses if anything is unmerged) and remove the worktree (`git worktree remove`, with `--force` if it refuses over gitignored build artifacts — allowed only after the salvage step). Never delete branches or worktrees you did not create in this run.
- **Abandoning a failed run** = salvage `.scratch/<feature-slug>/`, then remove the worktree and delete the ship branch (`git branch -D` — it was never merged, that's the point). The main checkout was never touched by this run, so there is nothing to reset and the user's pre-existing uncommitted changes are never in danger.
- **Zero push, all run**: push no branch, push no merged base branch, open no PR. If a remote (GitHub/GitLab) exists, leave it untouched; pushing or opening a PR is the user's call afterwards.
- Close the tickets per the local convention.

End with a report in the user's language: spec and tickets (paths), how the work landed (which ship branch merged into which base branch; worktree and branch cleaned up), code-review status (findings raised vs fixed), the acceptance verdict carried from Accept, budgets consumed, one-line outcome — a note that nothing was pushed.

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

One line per phase boundary, in the user's language, never a question: worktree created (path + branch); route verdict; spec published; tickets published (N total, K runnable now); ticket merged (i/N); a retry when one happens; review passed; acceptance verdict (通过 / 失败 / 卡点); landed (ship branch merged → base branch in the main checkout, worktree removed); delivered. The user should be able to ignore every line of this and read only the final report.
