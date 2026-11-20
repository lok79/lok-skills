---
name: verify
description: "Universal-stack acceptance: drive the real runtime and verify behavior in the real environment through the seams the project profile registers. Last link of the /fhip workflow; also runs standalone to backfill verification of historical tails. Mid-chain step — invoke only within that chain or on explicit user request; never on your own initiative."
---

# Skill: verify

The universal-stack counterpart of `accept`, last link of the fhip chain; also runs standalone to backfill verification of historical tails. One job: **drive the real runtime and verify behavior in the real environment, through the seams the project profile registers** — no unit tests, no code review (already spent upstream); never fabricate a seam the stack cannot offer.

Entry: fhip passes the spec path; never guess it. Standalone, do not guess by file times: scan `.scratch/*/spec.md`, list candidates, let the user name one; a single pending spec is used directly.

## Preconditions

1. Read the spec (`.scratch/<slug>/spec.md`); confirm it has acceptance clauses or derivable assertions — if not, stop and ask the user.
2. Read the profile `docs/agents/acceptance.md` (run conventions, credentials, seam registry, side-effect surface, performance scale). Missing or missing key facts → call the Skill tool with `survey` first. Profile contradicting reality → fix the profile first (empirical probing wins), then continue.

## Split ledger（分账表）

Sort every acceptance clause into:

- **Already verified**: covered by runtime verification (unit / integration tests) — do not rerun; list names only. A ticket only statically reviewed by code-review (no runtime test) is NOT already verified: route it to the wire seam if reachable, else Unreachable.
- **Needs the real environment**: drive the registered seams below.
- **Unreachable**: no registered seam reaches it (hardware, physical devices, foreground-only surfaces not enabled in the profile, or business logic the wire seam cannot reach) → record as「无可自动化验收项」, an honest boundary record; never ask the user to verify manually. Never force-fit.

## Seams

The profile's 缝登记 is the single source of what gets driven. The catalog of seam kinds:

- **Wire seam** (service): replay real historical requests (from the request logs the profile registers) or construct per contract; assert the response body / observable state.
- **CLI seam**: run the real command; assert stdout/stderr, exit code, artifact files.
- **Surface seam** (pages/UI): a smoke-level screenshot pass via the headless screenshot tooling the profile registers (web: built-in browser, or ego-browser if the profile probed it; mobile: an emulator without opening its window where probing showed it available; desktop: the target window). **One landing-state shot per surface** (web route / emulator screen / desktop window); do not screenshot every user story. Obtain the login state per the profile's credential convention and inject it the way this stack persists sessions, then navigate directly to the target; never click through login forms or menus. Presentational interactions (modal/panel/tab/drawer) are not clicked by default; only when the interaction itself is the change's core acceptance target is one representative opened-state shot allowed. **Business-behavior correctness (what a click does to data/state, as opposed to pure presentation) is never evidenced by screenshots** — wire seam only, or「无可自动化验收项」. Comparison: with a prototype, coarse-grained match of big-block layout / key elements present / obvious misalignment; detail differences (minor color/radius deltas) recorded as findings, not iterated to pixel-match and not burning the fix budget; only a whole missing block/feature is a failure walking the budget. Without a prototype, judge against an explicit-bug checklist (obvious overlap/occlusion, text overflowing and breaking other elements beyond intended ellipsis, broken image/icon showing alt text, whole block missing/blank, font fallback to default serif, obvious misalignment) — "is it broken", not "is it pretty"; no subjective aesthetic judgment. Coverage: i18n defaults to the main language only (other languages' copy correctness is Already-verified via a unit / key-consistency-check script, not code-review alone); multi-entry defaults to one representative entry (others text-declared as present); full coverage only when the spec explicitly demands it.
- **API seam** (library): consume the built artifact in a scratch consumer project; assert public-API behavior.
- **State observation**: read-only queries on the stores/paths the profile registers.

A seam is first-class only if its whole chain — start runtime → drive → capture → clean up — runs in the background without touching the user's screen. Foreground seams default to unreachable; if the profile explicitly enabled one, it may run and the evidence notes that it occupied the screen.

## Driving the real runtime

1. The running code must include the fix: build and (re)start the runtime under test per the profile's run conventions — fresh start, fresh clean (record the PID at start; before killing, verify the process name). Old artifacts backed up for rollback. Restarting is invasive: announce a one-line checklist before doing it.
2. Credentials per the profile's degradation order; any temporary write is marked, and deleted-with-verified-zero after the run.
3. Prefer paths that write nothing: assert against pre-existing state where possible.
4. Side-effect accounting: before/after comparison of the touched state the profile's 副作用面 names; unchanged counts as zero business writes.

## Performance (default on, two tiers)

Every driven seam carries timing — request timing, command wall time, whatever the seam affords. Read-only paths repeat 10×, report p95; necessarily-writing paths single-shot, noted「单次样本，非统计口径」. Thresholds come from the profile's 性能口径 (or spec assertions) — never baked in here: no assertion written → over-threshold is a「性能发现项」(recorded, not a failure, no budget); assertion written → over-threshold is a hard-gate failure walking the fix budget.

## Evidence

All text, appended to the spec's `## Comments` under `### 验收记录（<日期时间>）`:

- Environment (which runtime, which profile, credential method)
- Per case: input + output + comparison against expectation / historical behavior
- Side-effect accounting numbers; boundary declarations (deviation + why + recovery)
- Visual cases reference screenshot paths under `.scratch/<slug>/screenshots/` (gitignored local convention), filename `<case#>-<surface>-<scene>-<HHMM>.png`
- One-line verdict: 通过 / 失败 / 卡点

A failure is a real finding from the real environment: record the evidence honestly, route back through the fix budget (max 2 fix-and-reverify rounds), stop and report if still failing.

## Red lines

- Business data read-only; the only allowed writes are the profile's declared temporary-credential convention and the runtime's own operational logs
- No fabricated business data; runtimes outside the acceptance chain are never restarted
- No push; never touch the user's uncommitted files; nothing occupies the user's screen unless the profile enabled that seam
- Business-behavior correctness (as opposed to pure presentation/style) is never evidenced by screenshots — wire-seam assertions only, or「无可自动化验收项」
