---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.  
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask *now* without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question, continuing the count from previous rounds (round two starts after round one's last question, e.g. Q1–Q3 then Q4…), and give your recommended answer — a judged position, not a reflex: where the clarification is silent (validation, error handling, edge cases, configurability), analyse this context (where inputs come from, what failure costs, what the machinery would guard) and recommend the degree the analysis says is proportionate, with the why stated in the ➡️ line; "none" is a legitimate recommendation. Then wait for the user's answers before the next round.

Format a round like so:

````
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

👀 <only when the question is about what the built thing looks or feels like: the concrete end state — a scenario walkthrough with real values on screen, an example table, a before/after pair, or a sketch/annotated screenshot — so the answer is seen, not imagined. Omit otherwise>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

👀 <same rule as Q1: include whenever this question or its recommended answer shows the concrete end state; omit otherwise>

➡️ <your recommended answer>

---

📋 复制下面这块回答，默认全部按推荐，要改哪题就改哪行：

```
1. 按推荐
2. 按推荐
```
````

Word each question so "yes" accepts your recommended answer.

The numbered lines at the end are the **answer block**: a plain fenced code block, one line per question in the round, each numbered with its question's own number — the line for QN reads `N. 按推荐`. Question numbers keep counting across rounds, and the block follows them: the template above depicts the first round (Q1, Q2), but a round asking Q4–Q6 must render the block as `4. 按推荐` / `5. 按推荐` / `6. 按推荐`, never restarting at 1 — a bare `2.` in a later round would collide with the already-settled Q2. Every line is pre-filled with `按推荐` ("take the recommended answer"). The user copies the whole block, pastes it into their input, and either sends it untouched to accept every recommendation or edits only the lines they disagree with. Parse their reply by number: `按推荐` on line N adopts your recommended answer for QN; anything else on that line is their answer verbatim. Never add question titles or anything else to the block — the lines must stay copy-paste ready.

**Render the effect, don't offer abstractions.** When a question — or its recommended answer — is about what the built thing will look or feel like, carry the concrete end state inline as the 👀 block: by default a scenario walkthrough (one person, one day, one task, real values on screen), an example table for state and data questions, a before/after pair for edge and failure behaviour, a sketch or annotated screenshot for UI. The 👀 block is a per-question slot: it appears under any question in the round that meets the condition, never only under the first. This adds no reply mechanism — the user still answers through the answer block; the rendering turns imagining the recommendation into looking at it, so accepting the recommendation becomes safe at a glance. Escalate to a prototype only when a question needs runnable code. Confirmed renderings are primary material: they flow into the spec's user stories and the acceptance criteria.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a *later* round, not this one.

Finding *facts* is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The *decisions* are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
