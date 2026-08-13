---
description: How much an agent can actually hold before answers get worse, which is far below the window limit. The starting point for any argument about what a file costs.
layer: concept
deep: ../deep/context-rot.md
---

# Context rot

**Claim** — answer quality degrades as input tokens grow, *even when every added token is relevant-looking*, and the degradation starts long before the window is full. This is the axiom the rest of this reference defends against.

**Go deeper** — [`deep/context-rot.md`](../deep/context-rot.md) has the study numbers behind the degradation claim, model by model. Read it when sizing a context budget for a specific model/task, arguing volume vs. accuracy trade-offs with numbers, or you need the study citations.

**Why it matters** — Chroma's 2025 study tested 18 frontier models (GPT-4.1, Claude Opus 4, Gemini 2.5, …): **every one degraded at every input-length increment tested**, non-uniformly. When the task can't be solved by literal string-matching, measured *effective* lengths collapse to a fraction of claims (NoLiMa, ≥85%-of-baseline bar): GPT-4.1 **1M → 16K**, GPT-4o **128K → 8K**, Claude 3.5 Sonnet **200K → 4K**, Gemini 1.5 Pro **2M → 2K**; at 32K most tested models fall below **half** their own baseline.

**The mechanism (three compounding effects)** —
1. **Attention dilution** — softmax attention is a fixed budget spread over more pairwise relationships as tokens grow; per-token attention mass shrinks.
2. **Position bias** — U-shaped attention: strong at the edges, weak in the middle ("lost in the middle").
3. **Distractor interference** — semantically similar-but-wrong content doesn't just dilute, it *actively misleads*; distractors hurt more than random filler.

**The resolution of the paradox** — "more context = better" and "more context = worse" are both true. Curated, task-scoped context **compounds**; raw volume **piles**. The discriminator is marginal signal per token, not size. Ask "does this token raise the probability of the right answer," never "is there room."

**Rules** —
- Treat the window as an attention budget, not a storage budget.
- Your effective context is what benchmarks measure at your accuracy bar — not the marketed window. Assume 25–50% of the advertised number for reasoning-heavy work.
- Distractors are worse than noise: filtering *near-miss* content pays more than filtering junk.
- Rot is continuous — there is no safe threshold below which tokens are free.
