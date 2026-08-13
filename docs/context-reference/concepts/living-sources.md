---
description: A file grew until it blurs, or two files drifted until they disagree, and nothing in the build will ever tell you. The signals that say split, and the ones that say merge back.
layer: concept
deep: ../deep/living-sources.md
group: The rules of truth
---

# Living sources

**Claim** — a source of truth doesn't stay put: it grows until it blurs (needs a **split**) or converges with a neighbor until they disagree (needs a **merge**) — and *nothing forces the refactor*. Code that outgrows its structure fails review or fails to compile; context that outgrows its structure just quietly degrades every answer that reads it. That asymmetry is why context debt is worse than code debt: it has no compiler.

**Why it matters** — staleness is the top decay path of deployed corpora: RAG systems drift as chunks go stale and retrieval keeps surfacing plausible-but-outdated fragments; documentation issues cost an estimated **$200K+/year for a 50-person engineering team**; support teams add ~40 docs/month and retire almost none. Every stale fragment is a future clash or poisoning event.

**Split signals (any one suffices)** —
- The page answers two different questions depending on who asks ("customers" covering two business meanings).
- Corrections accumulate as caveats instead of rewrites — a wall of "however/except/as-of".
- Readers quote different parts of it as "the answer" to the same question.
- It exceeds what one retrieval hit can usefully carry (the chunk boundary cuts mid-concept).

**Merge signals** —
- Two sources answer the same question with slightly different words (today) — a clash scheduled for later.
- Readers get whichever version their query phrasing happened to match.

**Rules** —
- Split/merge is triggered by the *write that notices*, not by a schedule — the noticing moment is the cheapest time to act (restructure-on-write, per A-MEM's model).
- Pointers absorb the refactor: readers of the old location follow a forward pointer; nothing breaks loudly — which is exactly why you must budget for it deliberately.
- Retire as deliberately as you author: a superseded page left retrievable competes with its successor in every search.
- After any split/merge, **re-index mirrors** (embedding indexes are mirrors) — or retrieval serves the pre-refactor corpus.

**Go deeper** (`../deep/living-sources.md`) when: a page/doc feels overgrown, two docs overlap, planning corpus maintenance, or estimating staleness risk.

## Related

- [Deep: the evidence behind this page](../deep/living-sources.md) — open it on the trigger named above.
