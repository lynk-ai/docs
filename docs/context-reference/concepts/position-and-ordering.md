---
description: Where to put the load-bearing part of a file. Content buried in the middle can score worse than leaving it out entirely.
layer: concept
deep: ../deep/position-and-ordering.md
---

# Position and ordering

**Claim** — context is not a set; it's a sequence, and *where* content sits changes accuracy. Models attend in a U-curve — strong at the beginning (primacy) and end (recency), weak in the middle. Measured: GPT-3.5-Turbo on 20-doc QA drops from **75.8% (answer first) to 53.8% (answer middle)** — below its own **closed-book baseline of 56.1%**: mid-buried evidence is worse than no evidence ("Lost in the Middle", Liu et al., TACL 2024).

**The mechanism** — intrinsic positional attention bias: edge tokens receive outsized attention *regardless of semantic relevance* ("Found in the Middle", 2024 — calibrating the bias away recovers middle accuracy, proving position, not content, causes the loss). Order also affects reasoning itself: premise order changes chain-of-reasoning accuracy even when all premises are present (Chen et al., 2024).

**Placement rules** —
- **Instructions and role: first.** They also want to be the stable cached prefix — accuracy and economics agree here.
- **The question/task: last.** Recency slot, and it's the part that varies per request (cache-friendly).
- **Critical evidence: edges, never buried.** If one document decides the answer, put it just before the question.
- **Long lists (tools, docs): assume the middle is half-invisible.** Cut the list before you reorder it — fewer items beats better-sorted items.
- **Rank-order retrieved chunks by relevance toward the edges**, most relevant closest to the question.

**One tension to manage** — recency wants dynamic content late; caching wants stable content early. These are compatible (stable-early + dynamic-late is exactly the cache-optimal layout), but *mid-prefix mutation* breaks both: it invalidates the cache suffix and puts fresh content in the dead zone. Append; don't insert.

**Go deeper** (`../deep/position-and-ordering.md`) when: designing a prompt/agent-loop layout, debugging "the answer was in context and it still missed it," or ordering retrieved evidence.

## Related

- [Deep: the evidence behind this page](../deep/position-and-ordering.md) — open it on the trigger named above.
