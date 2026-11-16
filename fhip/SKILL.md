---
name: fhip
description: "Universal-stack variant of /ship: after requirements clarification, run the whole build autonomously on any software stack — spec, tickets, implementation, real-environment verification, delivery — with every stack fact supplied by the project profile (docs/agents/acceptance.md) instead of baked-in assumptions. Ignition of the post-clarification build — invoke only on the user's explicit request; never on your own initiative."
argument-hint: "Nothing (fhip the current conversation), or a reference to an existing spec"
---

# Fhip

The clarification is over: the user has confirmed a shared understanding in this conversation (typically via `/grill-with-docs`). Fhip runs the same post-clarification build as `/ship` — implementation through delivery, stopping only at budget limits or scope surprises — with one structural difference: **no stack is assumed**. How this repo runs, authenticates, and gets verified lives in the project profile `docs/agents/acceptance.md`, built by `/survey`; nothing here guesses it. The user expects to walk away now.

Read `/Users/lok/.agents/skills/ship/SKILL.md` first. Fhip follows its **Prime directive** (every confirmation the downstream skills would ask is yours to decide, the why recorded where the user will review it), its **Failure budgets**, its **Stopping**, and its **Deliver** — with the substitutions below. Wherever ship's text says ship branch / ship worktree, read this run's fhip branch / fhip worktree.

## Process

### 1. Preflight

Ship's **Preflight** as written — tracker check, open-questions refusal, assumption scouting, existing-spec entry — plus one check before the worktree: `docs/agents/acceptance.md` missing or missing key facts → call the Skill tool with `survey`; it writes the profile and narrates — no interruption. Then create the fhip worktree per **Isolation** below.

### 2. Isolation

Ship's **Isolation: one worktree per run**, in fhip's own namespace: worktrees under `../.fhip-worktrees/<slug>/<repo>`, branch `fhip/<slug>` — parallel fhips and ships never collide. Everything else (salvage of gitignored locals, dependency install, never touching runs you did not create) exactly as ship prescribes.

### 3. Route and Run

Ship's **Route** criteria exactly, read stack-neutrally: "crosses layers" = crosses this stack's layers (data model, interfaces, user surface — whatever shapes this repo has); "schema ripple" = ripple through the stack's data model; "content-only" = no production code of any kind. Torn between routes → `ask-matt`, as ship prescribes. Trivial and wayfinder behave exactly as ship's Route section prescribes; light calls `implement`, standard calls `to-spec` → `to-tickets` → `implement-spec` — all shared with /ship, none stack-specific. Then execute per ship's **Run**: mid-chain checkpoints become your decisions per the Prime directive; `/compact` at the nearest phase boundary if the session nears the smart zone before ticketing is done.

### 4. Accept

Call the Skill tool with `verify`, passing the spec path (`.scratch/<feature-slug>/spec.md`) — the final verification before landing. Run it **inside the fhip worktree**: the runtime under test is built and started from the worktree's code on a port/resource no other live run occupies, recorded in the evidence. A verification failure is a real finding: route it back through the fix budget (max 2 fix-and-reverify rounds), then stop and report if still failing. The final report carries verify's verdict (通过 / 失败 / 卡点) and any boundary deviations.

### 5. Deliver

Ship's **Deliver** section verbatim: salvage `.scratch/<feature-slug>/` into the main checkout first, merge in the main checkout, zero push, cleanup, close tickets — with fhip's branch/worktree names.

## Narration

Ship's **Narration**: one line per phase boundary, in the user's language, never a question; the acceptance line carries verify's verdict. The user should be able to ignore every line and read only the final report.
