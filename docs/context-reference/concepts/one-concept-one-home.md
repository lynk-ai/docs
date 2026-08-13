---
description: The same fact is stated in two places and you need to know why that is a defect rather than helpful redundancy. Two copies eventually disagree, and the agent picks one without telling anyone.
layer: concept
deep: ../deep/one-concept-one-home.md
---

# One concept, one home

**Claim** — every definition, rule, or fact an agent may rely on lives in exactly **one** authoritative place; everything else points at it. Duplication is not a style issue: two copies of one fact are two sources of truth waiting to disagree, and when they do, the model silently picks one (clash — the failure mode with no mechanical fix).

**Why it matters** — ~70% of enterprise knowledge bases contain at least one pair of directly contradictory articles (Gartner estimate); teams add ~40 docs/month and retire almost none. On real contradictions, models usually answer fluently from one source *without flagging* that a competing claim existed (WikiContradict, NeurIPS 2024). A duplicated fact fails invisibly: no diff, no error, just a confidently wrong answer for whoever retrieved the stale copy.

**The placement test** — *would two readers legitimately disagree about this?*
- **No** (ground truth: a definition, a decided rule) → one shared home, everything else points.
- **Yes** (working opinion, unreviewed draft) → stays private until it earns promotion through review.

**Rules** —
- Pointers, not copies. A copy forks; a pointer survives the original's edits. Collections (shelves, reading lists, indexes) are lists of pointers, never bodies.
- When a mirror must exist (cache, export, sync), **name the winner explicitly** — a mirror is a pointer with a refresh problem.
- The rule governs **homes, not mentions**: restating a one-line *derived* summary near the point of use (with the home linked) is legal and often position-optimal. The test: could the restatement drift into disagreeing with the home? A summary-plus-link can't survive alone; a full copy can — that's the line.
- **Findability redundancy is not truth redundancy.** Duplicate the *surfaces* (keywords, aliases, index entries — many paths in) freely; never duplicate the *fact* (one body at the end of every path). This resolves the apparent conflict with retrieval practice, which rewards redundancy: redundancy of routes helps recall; redundancy of homes creates clash.

**Go deeper** (`../deep/one-concept-one-home.md`) when: structuring a corpus/KB, deciding where a fact lives, handling mirrors and exports, or a contradiction just surfaced.

## Related

- [Deep: the evidence behind this page](../deep/one-concept-one-home.md) — open it on the trigger named above.
