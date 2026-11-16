---
name: grill-with-docs
description: "A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. Clarification entry of the /ship workflow — invoke only on the user's explicit request; never on your own initiative."
---

Call the Skill tool twice, for "grilling" and "domain-modeling".

## Closing the session

When the grilling reaches confirmed shared understanding, close it there: state that clarification is final, tell the user `/ship` (or `/zhip`, the delegated variant) will now run the build end-to-end, and stop. Do not start `/to-spec`, `/to-tickets`, or any implementation on your own — `/ship` and `/zhip` are the only ignitions for post-clarification work. If the user explicitly invokes a specific skill instead, obey that.
