---
description: The evidence behind selection quality — two-stage retrieval, reranking, and pruning with measured deltas. Open when tuning retrieval rather than writing a page.
layer: deep
concept: ../concepts/selection-quality.md
---

# Selection quality — evidence & practice

The missing chapter in most context writing: everyone says "curate," almost no one says how curation *breaks*. Selection fails on four independent axes — recall (didn't find it), precision (found it plus near-misses), granularity (found the right doc, shipped the wrong 90% of it), and surface (the corpus was unfindable as labeled). Each has its own fix; conflating them wastes tuning cycles.

## The evidence base

**Hybrid beats pure.** Sparse (BM25/TF-IDF) wins on exact identifiers, rare terms, and jargon; dense embeddings win on paraphrase and cross-vocabulary matching. Tuned hybrid on the WANDS benchmark: 0.7497 NDCG vs 0.6983 (BM25) and 0.6953 (dense) — **+7.4%** over the best single method ([InfoQ hybrid retrieval](https://www.infoq.com/articles/vector-search-hybrid-retrieval-rag/), [Denser hybrid guide](https://denser.ai/blog/hybrid-search-for-rag/)).

**Two stages beat one.** On text-and-table document benchmarks, hybrid recall + neural rerank achieves Recall@5 **0.816** vs 0.695 for hybrid-RRF alone (+17%), 0.644 BM25 (+27%), 0.587 dense (+39%); reranking lifts MRR@3 from 0.433 to 0.605 (+40% relative) ([From BM25 to Corrective RAG, 2026](https://arxiv.org/html/2604.01733v1)). The cross-encoder sees query and document *together* — precision no bi-encoder embedding distance can express.

**Pruning near-misses preserves (and can improve) answers.** [Provence (ICLR 2025)](https://arxiv.org/abs/2501.16214), primary details verified: a DeBERTa-v3 cross-encoder with two heads — one reranks, one emits a per-sentence binary keep mask — so pruning rides the reranker's query-aware representations at zero extra inference cost. It detects the number of relevant sentences dynamically (zero to all; threshold 0.1 conservative / 0.5 aggressive), and the paper's Pareto plots show it as **the only pruner with little-to-no performance drop across domains** at high compression (up to ~80–95% removal in favorable settings, per the paper and Breunig's summary). Perplexity ships query-aware compression in production for snippets. This is the operational confirmation of Chroma's distractor finding: retrieved-but-irrelevant sentences are net-negative tokens, not free padding — and Chroma's needle-similarity result sharpens it: degradation is steepest exactly when question-evidence similarity is low, i.e., when near-misses are hardest to tell from the answer.

**Order the stages by failure independence.** Tuning advice from production RAG playbooks: get recall@50 above ~90% *before* adding a reranker — a reranker cannot recover documents that never arrived; a better retriever can't fix a reranker that buries them.

## Agentic search vs. one-shot retrieval

One-shot (embed → top-k → generate) is a bet that the first query formulation suffices. Agentic search (the model reformulates, reads, follows references, requeries) trades latency and tokens for precision, and changes the *unit* of selection from chunks to *trajectories*. When to use which:

| Situation | Use |
|---|---|
| Latency-bound chat, homogeneous corpus | One-shot hybrid + rerank |
| Heterogeneous corpus, cross-doc questions | Agentic, few iterations, capped |
| High-stakes/audit answers | Agentic with citation verification |
| Agent already in a loop (coding, research) | Native agentic — grep/read/follow beats pre-built embeddings on code (the coding-agent consensus: Claude Code ships no embedding index; the model searches) |

Structured corollary: **metadata-first routing** (read names/descriptions, choose, then fetch bodies) is agentic search over a curated surface — the cheapest form, and the reason label quality (below) is a retrieval concern.

## The surface axis: your corpus is part of the retriever

Selection reads names, descriptions, and keywords before bodies. Failures here are unfixable downstream:
- Two items with near-identical descriptions → the chooser coin-flips regardless of retriever quality (`distinguishability.md`).
- Vocabulary mismatch between askers and authors → add synonym surface (keywords) rather than hoping embeddings bridge it.
- Tool selection is the same problem, now with primary-sourced numbers: RAG-MCP (via Breunig) — DeepSeek-v3 degrades sharply past **30 tools** (overlapping descriptions blamed directly), failure "virtually guaranteed" past **100**; the "Less is More" study — dynamic tool selection **+44%** accuracy on a 46-tool setup a quantized Llama 3.1 8B couldn't handle statically (it succeeded with 19). RAG over the tool loadout is SELECT applied to capabilities.
- **A bad tool is worse than no tool** — measured: SWE-agent's ablations scored a poorly-designed iterative search tool at 12.0 vs **15.7 with no search tools at all** ([arXiv 2405.15793](https://arxiv.org/abs/2405.15793), secondary source — not re-verified). Tools are context too: a confusing interface doesn't just fail to help, it actively costs solved tasks. When an agent keeps failing, audit the tool interface before blaming the model or the retriever.

## Anti-patterns

- **"Include it just in case"** — the direct cause of confusion-mode failure; every speculative inclusion is a distractor candidate.
- **Tuning k instead of quality** — raising top-k to fix recall imports near-misses; fix the retriever, not the quota.
- **One embedding space for everything** — code, prose, and tables have different similarity structures; route by type before embedding.
- **Trusting similarity as relevance** — similarity is a *candidate generator*; relevance is a judgment (reranker or model) — the gap between them is exactly where distractors live.

## By implementation type

| Implementation | Selection shape | Watch for |
|---|---|---|
| KB chatbot | Hybrid + rerank + prune | Stale chunks outranking fresh ones |
| Coding agent | Agentic grep/read, no index | Whole-file reads where excerpts suffice |
| Long-horizon agent | Re-SELECT from own notes | Notes unlabeled → agent can't find its own state |
| Multi-agent | Router picks from metadata | Router quality is capped by label quality |
| Text-to-SQL | Entity/metric routing before schema | Schema-dump-everything (confusion by width) |
