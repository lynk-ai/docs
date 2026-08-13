---
description: Deciding what loads every session versus what the agent fetches on demand, so a layer can keep growing without making every question heavier.
layer: concept
deep: ../deep/progressive-disclosure.md
group: The levers
---

# Progressive disclosure

**Claim** — load context lazily: a small always-present index of *pointers*, full content only when the task demands it. The point is the economics: cost scales with what's **used**, not what **exists** — so a knowledge base can grow without making every session heavier. This reference itself runs the pattern (concept cards always cheap; deep pages on demand).

**Why it matters** — the alternative is standing context, and standing context only accretes: every addition pays attention cost on *every* request forever (rot), while on-demand content pays once per actual use. The ETH Zurich AGENTS.md result is this economics enforced by measurement: standing context files tend to reduce task success while inflating inference cost >20%; only non-inferable, task-relevant content earns permanent residence.

**The three stages** —
1. **Pointer** (always loaded): name + one-line description + when-to-load trigger. Costs ~20 tokens per item; this is the layer that must be distinguishable (`distinguishability.md`).
2. **Card / summary** (loaded on match): the decision-ready compression — claims, rules, numbers. Enough to act on for routine cases.
3. **Body** (loaded on need): full evidence, procedures, edge cases.

**Rules** —
- **Pointers, not content, in the standing layer.** The index describes; it never excerpts (excerpts age into stale copies — `one-concept-one-home.md`).
- **The index has a cliff, not a slope**: over budget, the tail is silently *never read* — items past the cutoff cease to exist (hooks preview ~2KB; long listings die in the attention middle). Budget it like an SLA.
- **The trigger is part of the pointer**: "load when X" beats a topic label — routing runs on task-shaped triggers, not titles.
- **Read vs. execute inside stage 3**: read what the model must *reason over*; wrap in a script what only needs its *result* — executed code never enters the window, only its output does. The cheapest disclosure never loads at all.
- **Break-even is measurable**: content used on fraction *f* of requests belongs standing only when *f* is high (with caching, roughly *f* > ~10% on price — and attention cost always votes for on-demand; see `caching-economics.md`).
- **Grow sideways before deeper**: too-long-but-one-concept → sibling pages; a sub-part *readers cite independently* → its own index (a new disclosure level). The tell: you catch yourself wanting an index for it.
- **Depth must be reachable**: lazy loading fails if the pointer layer can't route — invest in surfaces (names, descriptions, keywords) as retrieval infrastructure (`selection-quality.md`).

**Go deeper** (`../deep/progressive-disclosure.md`) when: structuring a corpus/skill/tool surface for on-demand loading, or deciding what earns standing-context residence.

## Related

- [Deep: the evidence behind this page](../deep/progressive-disclosure.md) — open it on the trigger named above.
