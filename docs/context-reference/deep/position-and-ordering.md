---
description: The evidence behind position and ordering — the U-curve evidence and placement rules with numbers.
layer: deep
concept: ../concepts/position-and-ordering.md
when: Laying out a prompt; "it was in context and it missed it"
---

# Position and ordering — evidence & practice

## What the research established

**The U-curve is real and large** ([Liu et al., "Lost in the Middle", TACL 2024](https://arxiv.org/abs/2307.03172), primary numbers verified): 20-document QA, gold document moved through positions — GPT-3.5-Turbo: **75.8%** at position 1, **53.8%** at position 10, **63.2%** at position 20. Two findings sharper than the slogan:
- The −22pp middle dip takes the model **below its own closed-book baseline (56.1%)** — mid-buried evidence is worse than no evidence, because the model would otherwise have answered from weights.
- **Extended-context variants don't fix it**: GPT-3.5-Turbo vs. its 16K version produced "nearly superimposed" curves on identical inputs — window size and window *use* are different capabilities (the NoLiMa table says the same thing at scale).

**It's attention bias, not content.** ["Found in the Middle" (2024)](https://arxiv.org/html/2406.16008v1), verified: attention decomposes into relevance + positional bias; a document's attention tracks its *position* even after random shuffling, irrespective of relevance — and models generate from what they attend to (74% of responses drew on highest-attention documents). Calibrating the bias away (attention minus a dummy-document baseline per position) lifts document-ranking Recall@3 from **20.5% → 68.3%** and end-to-end QA by **6–15pp** when gold documents sit mid-sequence — near-conclusive proof position, not content, causes the loss. Structural analyses (e.g., ["A Structural Theory of Position Bias in Transformers"](https://arxiv.org/pdf/2602.16837)) trace primacy to attention-sink behavior on early tokens plus causal-mask asymmetry; recency falls out of rotary/relative encodings favoring nearby tokens.

**Order affects reasoning, not just lookup.** ["Premise Order Matters" (Chen et al., 2024)](https://arxiv.org/pdf/2402.08939): with *all* premises present, shuffling their order away from the deduction sequence drops reasoning accuracy substantially (30%+ on some models/tasks). Ordering is part of the reasoning scaffold, not just retrieval hygiene.

**Degradation compounds with length.** Chroma's context-rot results interact: longer context deepens the U — the middle "dead zone" widens as input grows. Position discipline matters *more* at scale, exactly when you have the least room to fix it by shortening.

## The layout that follows

Read top-to-bottom as the physical prompt order:

| Zone | Content | Why here |
|---|---|---|
| 1. Stable prefix | System prompt, role, standing rules, tool definitions (fixed order) | Primacy attention + cache hits (see `caching-economics.md`) |
| 2. Reference material | Loaded docs/skills, ordered least→most relevant | The middle is the cheapest real estate — spend it on supporting, not deciding, material |
| 3. Working state | Conversation/task history (compacted) | Chronology reads naturally; old turns age into the middle, which is fine — they matter least |
| 4. Critical evidence | The 1–3 items the answer hinges on | Pre-question recency slot — the strongest position you control |
| 5. The task | Current question/instruction, output format | Recency peak; and it's the per-request variable part, so placing it last keeps zones 1–3 cacheable |

Notes:
- **Most-relevant-last within retrieved sets.** If you rank chunks, put the best immediately before the question, weakest in the middle. (Some production stacks interleave best-first *and* best-last — "bookending" — when two items are near-equal.)
- **Repeat, don't move.** If a standing rule from zone 1 is decisive for this request, *restate a one-line version* in zone 4 rather than relocating it — preserves the cache and hits both attention peaks. This is the one legitimate use of duplication (cf. `one-concept-one-home.md`: derived restatement, not a second home).
- **Recitation (the production version of repeat-don't-move)**: Manus has its agent *rewrite a todo.md at the tail of context* throughout ~50-tool-call tasks — deliberately pushing the global objective into the recency window each step, "biasing attention toward the plan without architectural changes" ([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)). The decay it fights is measured: instruction compliance drops ~5.6% in odds *per generated function* within a session (McMillan, [arXiv 2605.10039](https://arxiv.org/pdf/2605.10039)) — standing rules fade with generation distance, so re-anchor them near the work.
- **Within a config file, position doesn't matter** (same study, null verified): the target instruction at line 2 vs. 63 vs. 128 vs. 187 vs. 250 of a CLAUDE.md — no detectable compliance difference; file size 25–500 lines — none either. The U-curve governs *where content sits in the assembled window*, not where a line sits inside one small early-loaded file. Don't spend effort ordering your config file; spend it on admission and on re-anchoring at use time.
- **Long tool lists have a dead middle.** Tool selection failures concentrate in mid-list tools; below ~30 tools this is manageable, above it no ordering saves you — cut the loadout (see `selection-quality.md`).

## Debugging with position

Symptom: "the answer was in context and the model missed it." Before adding more context (the reflexive, wrong fix):
1. Find the token offset of the critical span; compute its relative position.
2. If it sits in the 20–80% band of a long context — suspect position before model quality.
3. Cheap A/B: move the span adjacent to the question and rerun. Recovery confirms a placement bug, which no retriever tuning will fix.
4. Systematic check: run a position sweep on your own eval set (same content, gold span at 0/25/50/75/100%) — this is the NIAH-style instrument adapted to your corpus; see `measuring-context.md`.

## By implementation type

| Implementation | Position discipline that pays |
|---|---|
| RAG chatbot | Rerank order → placement order; best chunk goes last, directly before the question |
| Coding agent | Fresh file reads near the task; stale reads compacted or dropped, not left mid-window |
| Long-horizon agent | Compaction summaries go *early* (they're stable); live task state stays late |
| Multi-agent | Sub-agent briefs: put the objective + constraints at both ends of the brief; middle carries reference detail |
| Text-to-SQL | Schema of the *routed* entities immediately before the NL question; catalog overview (if any) early |
