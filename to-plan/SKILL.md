---
name: to-plan
description: "Transcribe the current spec (and tickets, if any) into a superpowers-format implementation plan plus a handoff prompt, both for a cheap executor agent. Mid-chain step of the /zhip workflow — invoke only within that chain or on explicit user request; never on your own initiative."
---

# To Plan

Translates what upstream skills settled (spec, and tickets on the standard route) into the two artifacts a cheap executor agent needs: a **plan** it executes step by step, and a **handoff prompt** that boots it with the right rules. The strong session's judgment ends here; everything downstream of this skill runs on discipline, not taste.

## Process

### 1. Load the format source

Read `/Users/lok/.agents/superpowers-dist/skills/writing-plans/SKILL.md` and treat it as the authoritative plan format — its bite-sized step granularity, task structure, file-structure-first section, code snippets, verification commands, scope check. Read it now, every run; do not write the plan from memory of what it says.

### 2. Gather source material

- Read the spec (`.scratch/<slug>/spec.md`). On the standard route, also read every ticket under `.scratch/<slug>/issues/`.
- Explore the codebase to pin the **exact file paths and line anchors** the plan format requires. The spec deliberately contains none — closing that abstraction-to-concrete gap is this skill's core job. Explore by subagent or direct reads, whichever the scale warrants.

### 3. Write the plan

Write the plan in the source format, with these overrides (each rides the source's own override conventions — e.g. it explicitly allows user-preferred plan locations):

- **Language**: English.
- **Location**: `.scratch/<slug>/plan.md` inside the current worktree — not the source's default path.
- **Header**: the "For agentic workers" line names `executing-plans` only; drop the subagent-driven-development recommendation.
- **Task order = ticket dependency order** (standard route): flatten the frontier into one linear sequence; each task notes the ticket it comes from, and carries that ticket's acceptance assertions into its verification steps. Light route (no tickets): derive tasks directly from the spec, mapping spec acceptance clauses into verification steps the same way.
- **The executor never reads the spec**: distill the spec's Problem/Solution into the plan header's Goal section (2–3 lines) instead. The spec is the orchestrator's and reviewer's document — for the executor it is a second source of truth, and second sources get arbitrated exactly when the executor is blocked.
- Keep the source's TDD step rhythm and task granularity exactly as written.

### 4. Clear the scene (standard route)

The executor reads and writes around `.scratch/<slug>/` all run long; anything task-like sitting there is a second source of truth it can be led astray by — the executor reads tickets at its peril exactly when it is blocked and looking for permission to improvise. So before the handoff prompt exists: move `issues/` out of the worktree's `.scratch/<slug>/` entirely (the main checkout holds the originals; zhip's take-back and Deliver read them there, nothing is lost). The executor's scene must physically contain only what `handoff.md` names.

### 5. Write the handoff prompt

Write `.scratch/<slug>/handoff.md` in the worktree. This file is the **single owner** of the whitelist and the report format — zhip's take-back step and everything else reference this file; nobody restates its terms.

````markdown
# Handoff: <slug>

- Worktree: /abs/path/to/.ship-worktrees/<slug>/<repo> (branch ship/<slug>; commit directly to this branch)
- Plan: /abs/path/to/.ship-worktrees/<slug>/<repo>/.scratch/<slug>/plan.md
- Execute the entire plan with the `executing-plans` skill. If anything suggests subagents, ignore it: execute in this session, no subagents.
- Overrides: do not create branches, do not merge, do not run finishing-a-development-branch. When all tasks complete, stop — the orchestrator handles review, acceptance, and merge.
- `plan.md` is the sole source of task truth. Ignore any other task-like files under this directory (e.g. `issues/`). Where anything else seems to conflict with the plan, the plan wins; when the plan blocks, STOP per the whitelist rules — never switch sources.
- Mechanical self-fix whitelist (fix yourself, record in the report; anything outside it = STOP):
  1. Plan paths/filenames that don't match reality — locate the real file, continue
  2. Environment troubles: dependency installs, port conflicts, test runner and its browsers/kernels (e.g. Playwright)
  3. Syntax-level minimal fixes to code snippets in the plan
- Mid-run rulings (where the plan is silent): you may decide only what does NOT change behavior the plan locks in — assertion values, UI copy, API responses. A ruling that would touch any of those = BLOCKED, not a ruling. Every ruling, allowed or not, goes into `workspace/ledger.md` under this directory, one line each (question → ruling → why); the report's self-fix list summarizes the ledger.
- Forbidden: weakening or skipping assertions to make tests pass; skipping any verification step; claiming completion without running the verification
- When done or blocked, write /abs/path/to/.ship-worktrees/<slug>/<repo>/.scratch/<slug>/report.md:
  - Tasks completed x/N; commits (`git log --oneline`); test results
  - Self-fix list: one line each (plan said → actually did)
  - Leftovers / concerns
  - If BLOCKED: which step, what the plan says, what was tried, why it cannot proceed
- Then reply with ONE line only: "✅ done, see report.md" or "⛔ BLOCKED at Task N"
````

### 6. Report back

One narration line: plan path (N tasks) + handoff path. No questions — granularity and slicing choices in the plan are yours to decide, per ship's Prime directive (Read `/Users/lok/.agents/skills/ship/SKILL.md`'s **Prime directive** section), with the why recorded in the plan's task notes.
