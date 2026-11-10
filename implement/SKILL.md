---
name: implement
description: "Implement a piece of work based on a spec or set of tickets. Mid-chain step of the /ship workflow — invoke only within that chain or on explicit user request; never on your own initiative."
---

Implement the work described by the user in the spec or tickets. Machinery they don't ask for — validation, defensive checks, error paths, retries, abstraction — is still yours to decide without asking, but by analysis, not reflex: where do inputs come from, what does failure cost here, what would it guard, what does it cost to carry? Build what the analysis says is proportionate for this context — which may well be nothing — and give the why in your report. A required feature doesn't exempt its internals: build to the degree specified; extra checks, branches, or hardening packed inside count as unrequested machinery under the same rule. Machinery whose reason nobody can state is the failure mode this rule exists to kill.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Call the Skill tool with "tdd" at pre-agreed seams, by default. Skip only when the change carries no observable behavior (pure copy, comments, configuration values) — and if you skip, state that reason in the final report. "No test infrastructure" is not a skip reason: test at the highest seam the runtime allows (for backend changes, the HTTP layer asserting the response body).

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, call the Skill tool with "code-review" to review the work.

Commit your work to the current branch.
