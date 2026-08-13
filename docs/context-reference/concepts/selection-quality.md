---
description: The agent retrieved something plausible but wrong. Why near-misses do more damage than obvious junk, and the retrieval shape that fixes it.
layer: concept
deep: ../deep/selection-quality.md
---

# Selection quality

**Claim** — SELECT is the lever everything else depends on, and it fails in a specific, measurable way: retrievers return *plausible near-misses*, and near-misses hurt more than junk (distractor interference actively misleads; it doesn't just dilute). Curation advice is empty without a theory of how selection breaks.

**Go deeper** — [`deep/selection-quality.md`](../deep/selection-quality.md) has two-stage retrieval, reranking, and pruning with measured deltas. Read it when building or tuning any retrieval pipeline, choosing hybrid vs. dense vs. agentic search, or diagnosing why the right page never arrives.

**Why it matters** — two-stage retrieval (broad recall → precise rerank) beats every single-stage method: Recall@5 **0.816 vs 0.695** for hybrid fusion alone, 0.644 for BM25, 0.587 for dense-only. Query-aware pruning (Provence, ICLR 2025) then cuts retrieved content at high compression with little-to-no quality loss — the only pruner that's Pareto-dominant across domains — because the near-misses it deletes were *hurting*: Chroma measured distractors actively degrading answers, compounding with each one added.

**The architecture that wins** —
1. **Recall stage** — hybrid sparse+dense (BM25 catches exact/rare terms; embeddings catch paraphrase). Fix recall first: don't tune precision until recall@50 > 90%.
2. **Precision stage** — cross-encoder reranker (MRR@3 +40% relative in benchmark runs).
3. **Pruning stage** — sentence-level, query-aware (Provence-style), because the unit of rot is the token, not the chunk.
4. **Agentic escalation** — when one-shot retrieval can't answer, let the model *search iteratively* (query → read → requery). Trades latency for precision; right for high-stakes, wrong for chat latency.

**Rules** —
- Measure recall and precision separately; they fail independently and have different fixes.
- The most dangerous retrieval result is rank-2-but-wrong, not rank-50.
- Selection surfaces (names, descriptions, keywords) are part of retrieval quality — badly labeled corpus = unfixable retriever (see `distinguishability.md`).
- Every SELECT should justify its tokens: "might be relevant" is how confusion enters.
