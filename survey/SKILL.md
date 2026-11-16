---
name: survey
description: "Single owner of the project profile (docs/agents/acceptance.md): probe the repo's stack empirically and write the archive directly — after-the-fact review, no confirmation gate; also repair profile-vs-reality drift. Called by /fhip's Preflight and /verify; mid-chain step — invoke only within that chain or on explicit user request; never on your own initiative."
---

# Skill: survey

Single owner of the project profile: probe this repo's stack empirically and write `docs/agents/acceptance.md` directly. Called by fhip's Preflight and by verify (missing facts, or drift repair); also runs standalone on explicit request. This skill only establishes facts and writes them — the user reviews after the fact, per fhip's Prime directive. Nothing here asks the user anything: a confirmation the user would only rubber-stamp carries no information, and a stop fired from verify mid-run would deadlock an unattended fhip.

## Probe (minutes-level, empirical — never guess)

1. **Shape**: read the repo (build files, README, entry points, docs). What kind of software is this — service, CLI, app, library, several? How is it built, run, tested, typechecked? Try each command for real.
2. **Run**: how each runtime starts (dev server, binary, app bundle); what ports/resources it occupies; how to stop it cleanly.
3. **Credentials**: how a usable login state / token is obtained, and the degradation order (existing credentials → temporary marked rows → …), including any write a credential method requires.
4. **Seams**: for each surface, what is observable — wire protocol (which; where real request logs live), stdio/exit codes/artifacts, pages (which tool can screenshot them headlessly), public API, data stores (read-only query paths). For each, decide first-class vs foreground by probing: can start → drive → capture → clean up run entirely in the background? Probe the environment's tooling as fact (headless emulator flag, built-in browser, computer-use present or not).
5. **Side-effect surface**: what a verification run would write (files, tables, services, logs) — the accounting basis for verify's red lines.
6. **Performance scale**: how to time each seam; which thresholds the project asserts. None established → record「性能口径：未定（verify 只测不判）」.

## Write and report

Write the profile directly — no confirmation gate. Make the after-the-fact review land well instead:

- Every fact that could not be established is marked 未知 in place, never papered over; a seam whose driving method is 未知 is unreachable until repaired
- Foreground seams are recorded as foreground, off by default; the 缝登记 line notes how to enable one
- Every credential method that writes anything is recorded with what it writes and its cleanup
- One narration line: profile written (path); N seams — M first-class / K foreground(off) / U 未知

Write it to `docs/agents/acceptance.md`:

```
## 运行方式 — how to start/build/stop each runtime; ports/resources
## 认证与凭证 — how to obtain a usable state; degradation order; what writes what
## 缝登记 — each seam: kind, how driven, what asserted, first-class or foreground(off; edit to foreground-enabled to turn one on)
## 副作用面 — what verification may write; what is read-only
## 性能口径 — timing method per seam; thresholds; or 未定
## 够不着清单 — what no seam reaches; the user verifies manually
```

## Drift repair

Called by verify on profile-vs-reality mismatch: probe the mismatched fact, fix the profile, report the diff. Empirical wins over the archive, every time.
