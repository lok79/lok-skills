---
name: orca-ship
description: "Orca bot-carrier thin adaptation of the matt chain: delegates clarification/spec/tickets/implement/review/accept/retro/budgets/Stopping/Deliver to the original skills (single authority, never paraphrased); self-contained only for carrier/identity, per-stage model seams, visibility/interruption, and the inter-session communication protocol. Ignition of the post-clarification build on Orca bots; invoke only on the user's explicit request; never on your own initiative."
---

# orca-ship (thin adaptation layer)

The original skills are the **single authority**. This skill never paraphrases their rules — it points at them and reads them at run time. Self-contained sections: 0, 4 (brief/seams), 5 (return template), 6, 9, 10. Everything else delegates.

Prime directive, Failure budgets, Stopping, Deliver: follow `ship/SKILL.md` anchors verbatim (read that skill at run time; do not restate).

## 0. Carrier & identity (self-contained)

- Coordinator = **a bot chat**. Bot chats carry orchestration sender identity (proven: `run-create` ok without `--from`); **no mailbox terminal needed**.
- Workers = **pre-created reusable worker bots** (owner accepts once per bot); dispatch via the §9 brief; the owner can message a running worker bot directly (that message wakes it).
- Reading outputs: `bot chats` lastSaid is a truncated preview and `agent read` is weak for chats → read full replies via **orca-computer-use accessibility tree** (`get-app-state --element-index <reply container>`).
- Wake = owner UI message. **No external cron polling.**
- **Zero writes to global config** (`~/.claude`, cc-switch untouched). Endpoint/model = bot/UI config (bailian internal seams).
- Resolve the Orca executable per orca-cli skill; load version-matched guides (`orca skills get orca-cli` / `orchestration`); prefer `--json`.

## 1. Clarification — delegate

Call `grill-with-docs` (it drives `grilling` + `domain-modeling`). Do not restate rounds/frontier/GLOSSARY rules.

## 2. Preflight — delegate + self-check

Follow ship §Preflight (tracker / open questions / assumption scouting / existing-spec entry).
Self-contained addition: endpoint/auth self-check via one trivial bot prompt; on failure **stop with a clear message**, no workaround.

## 3. Route — delegate

Follow ship §Route (trivial / light / standard / wayfinder-refuse; genuinely torn → `ask-matt`).

## 4. Front monolith + dispatch — delegate + brief/seams

Follow ship §Run and §Isolation; call `to-spec` / `to-tickets` / `implement-spec` (or `implement` for light) exactly as ship prescribes; the front monolith stays one unbroken context.
Self-contained: dispatch each ready ticket to a worker bot using the **§9 brief template**; inject seam model/effort from `docs/agents/orca-seams.md` (bailian-internal); the worker runs `pimplement` (tdd-only) and commits to its own worktree branch. Merge per ship/implement-spec prescription.

## 5. review / accept / retro — delegate + return template

Call `code-review` / `accept` / `retro` as the originals prescribe (accept input = spec or acceptance-plan **path pointer**).
Self-contained: require the **§9 return template** from every worker; reject free-form dumps.

## 6. Human-in-loop — delegate + carrier

Follow ship §Stopping (three summons: budget / scope surprise / preflight refusal).
Self-contained: the owner may message any running bot at any time (wake/interrupt); **gates only for real decisions**; no procedural confirmations.

## 7. Budgets — delegate

ship §Failure budgets (ticket ≤2 / review ≤2 / accept ≤2).

## 8. Deliver — delegate

ship §Deliver (salvage `.scratch`, main-checkout merge, **zero push**, cleanup, close tickets, final report).

## 9. Communication protocol (self-contained, hard)

**Down brief (coordinator → worker bot; pointers, never content):**
```
ticket: <.scratch/<feature>/issues/NN-*.md path>
spec: <.scratch/<feature>/spec.md path>
acceptance-criteria-at: <ticket "怎么算对" section / spec acceptance section>
base-branch: <integration branch>
worktree: <this worker's worktree path>
model/effort: <seam values>
task: call pimplement (tdd-only); commit to this worktree branch.
return: per return template; no process logs.
```
**Up return (worker → coordinator; fixed format):**
```
commit: <hash>
tests: <total/failed/skipped> (command + exit)
boundary: <unreachable/deviation declarations, or none>
evidence: <screenshot/log paths>
```
**Pointer discipline:** between sessions transfer only deltas/summaries + pointers; full spec/diff/logs stay in domain files, read on demand; **never paste full text** into briefs or returns.

## 10. Non-invasive & archive

Originals never modified (ADR-0001). Old `pgrill-with-docs` is archived as an exploration asset, not a daily dependency. Resume-triage slot reserved (user deferred).