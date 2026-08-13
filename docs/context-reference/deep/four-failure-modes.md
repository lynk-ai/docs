---
description: The evidence behind four failure modes — measured onsets for each mode and how to tell them apart from a transcript. Open when diagnosing a live failure.
layer: deep
concept: ../concepts/four-failure-modes.md
---

# The four failure modes — diagnosis & fixes

Taxonomy: Drew Breunig, ["How Long Contexts Fail"](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html) (June 2025); fixes catalog from his companion ["How to Fix Your Context"](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html), reproduced with runnable examples in LangChain's [`how_to_fix_your_context`](https://github.com/langchain-ai/how_to_fix_your_context).

## Diagnostic procedure

Work the symptoms in this order — cheapest test first. Each mode now has a *named, primary-sourced* exemplar:

1. **Same wrong fact recurring across turns?** → *Poisoning.* Canonical case (Gemini 2.5 technical report, via Breunig): the Pokémon-playing agent hallucinated game-state details **into its own goals section**, then pursued impossible goals and repeated failed strategies for turns on end — the poisoned *goal*, not a poisoned fact, is the expensive variant. Search the transcript for the fact's first appearance; everything referencing it downstream is contaminated.
2. **Quality falls as the session lengthens, content held constant?** → *Distraction.* Measured onsets: Gemini 2.5 began repeating past actions past **~100K accumulated tokens** (its own tech report); Databricks measured correctness decline from **~32K** for Llama 3.1 405B — distraction starts at a fraction of the window, and smaller models turn earlier. Related in-session decay: instruction compliance drops ~5.6% odds per generated function (McMillan) — even rules, not just history, fade with length-in-use.
3. **Quality falls as you widen the payload (more docs, more tools), length modest?** → *Confusion.* Verified numbers: Berkeley Function-Calling Leaderboard — **every** model performs worse given more than one tool; the GeoEngine benchmark run — a quantized Llama 3.1 8B **fails with 46 tools, succeeds with 19**, both fitting in a 16K window: it's count/breadth, not length, that killed it.
4. **Inconsistent answers to the same question within one session?** → *Clash.* Measured at conversation scale by ["LLMs Get Lost in Multi-Turn Conversation"](https://arxiv.org/abs/2505.06120) (Laban et al., 200,000+ simulated conversations): information arriving **sharded across turns** — each turn potentially conflicting with the model's premature assumptions — costs an average **−39% across six generation tasks** vs. the same information in one turn (o3: 98.1 → 64.1). Decomposition: minor capability loss + major *unreliability* spike; "when LLMs take a wrong turn, they get lost and do not recover." Diff the context for contradictions; check whether both entered legitimately (stale + fresh doc is the classic case).

## The fix menu, mapped

| Fix (Breunig/LangChain catalog) | Fixes | What it does |
|---|---|---|
| **Context quarantine** | Poisoning | Untrusted/unverified output runs in an isolated thread; only validated results merge back |
| **Context validation** | Poisoning | A check between generation and persistence — nothing self-written re-enters without passing a gate |
| **Context summarization / compaction** | Distraction | Boil accumulated history; reset at sub-task boundaries. Reversibility hierarchy: prefer raw > compaction (drop what's re-fetchable) > lossy summary ([Redis compaction guide](https://redis.io/blog/context-compaction/)) |
| **RAG over the loadout** | Confusion | Retrieve the *relevant* docs/tools per step instead of standing loadouts. RAG-MCP (Gan & Sun, via Breunig): DeepSeek-v3 tool selection degrades sharply past **30 tools** (overlapping descriptions); past **100 tools**, failure "virtually guaranteed"; vector-search over the tool registry restored performance |
| **Tool loadout management** | Confusion | Keep offered tools under ~30; select per-task. "Less is More" (via Breunig): dynamic LLM-driven selection improved tool accuracy **~3×/+44%** on the 46-vs-19-tool setup — with 18% power and 77% speed side-benefits; secondary reports put selection accuracy as low as **13%** on large sets ([over-tooled agent problem](https://tianpan.co/blog/2026-04-19-over-tooled-agent-problem)) |
| **Context pruning** | Confusion | Query-aware sentence-level pruning ([Provence, ICLR 2025](https://arxiv.org/abs/2501.16214)): a DeBERTa cross-encoder that reranks *and* prunes in one pass, dynamically detecting how many sentences to keep (zero to all); the paper's Pareto plots show it as the only pruner with little-to-no quality drop across domains, at high compression (up to ~80–95% removal in favorable settings, per the paper and Breunig's summary) |
| **Context offloading** | Distraction, confusion | Move working state to files/scratchpads; re-SELECT on demand. Anthropic's "think" tool (a designated scratch space) + domain prompts: up to **+54%** on specialized agent benchmarks (via Breunig) |
| **Detect → classify → escalate** | Clash | ConflictRAG-style pipelines detect and classify conflicts before generation ([ConflictRAG](https://arxiv.org/pdf/2605.17301)); resolution policy is human-owned |

## Clash deserves its own section

The knowledge-conflicts literature ([survey, arXiv 2403.08319](https://arxiv.org/abs/2403.08319)) splits conflicts into **context–memory** (retrieved facts vs. the model's weights), **inter-context** (two retrieved sources disagree — Breunig's clash), and **intra-memory**. Two findings matter for builders:

- Models don't reliably flag contradictions unprompted — on WikiContradict-style real contradictions they often answer fluently from *one* source with no signal that a competing claim existed ([WikiContradict, NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/c63819755591ea972f8570beffca6b1b-Paper-Datasets_and_Benchmarks_Track.pdf)). Silent resolution is the default failure.
- Scale of the problem: a Gartner-attributed estimate (secondary source — treat as order-of-magnitude) that ~70% of enterprise knowledge bases contain at least one directly contradictory article pair, with support teams adding ~40 docs/month and retiring almost none ([Fini Labs](https://www.usefini.com/guides/ai-knowledge-base-conflicting-answers)).
- One honest null: McMillan's factorial study planted a *directly contradicting instruction* in a second config file and measured **no detectable compliance change** on a simple marker rule (+0.33pp, affirmative-null Bayes support). Clash's measured damage concentrates on *facts and evolving assumptions* (the −39% sharded-conversation result), not necessarily on simple rule-vs-rule contradictions — diagnose accordingly.

Structural prevention beats detection: one home per fact (`one-concept-one-home.md`) makes inter-context clash impossible *within your own corpus*; detection pipelines then only have to cover external/uncontrolled sources.

## The conversation as its own failure surface

The four modes describe *what is in the window*. Multi-turn adds a dynamic they don't capture: **the wrong turn that never gets corrected.** Laban et al. ([arXiv 2505.06120](https://arxiv.org/abs/2505.06120), 200,000+ simulated conversations) decompose the −39% multi-turn penalty into *minor capability loss + a large instability spike*, and name the mechanism: models commit to an interpretation early on incomplete information, then defend it — "when LLMs take a wrong turn in a conversation, they get lost and do not recover."

What follows for managing a live conversation:

- **Early commitment is the failure, so intervene early.** A clarifying question before the first substantive answer is worth more than any amount of later correction — and it is the cheapest retrieval available (`selection-quality.md`: asking beats searching when the missing fact lives with the user).
- **Correction ≠ recovery.** Telling the model it was wrong leaves both the wrong turn and the correction in context — the failure mode is *contamination*, not stubbornness. For a genuinely wrong branch, **reset and re-state the task with the accumulated facts**, rather than appending "actually, no".
- **Distinguish the three exits**: *continue* (on track), *compact* (on track, window heavy — `context-governance.md`), *reset* (off track — carry forward the facts, drop the trajectory). Most systems implement only the first two, which is why bad sessions never recover.
- **Re-anchor the objective periodically.** The task statement ages into the dead zone as the transcript grows; recitation (`position-and-ordering.md`) is the counter.
- **Instrument it**: a spike in turns-per-resolution, or repeated near-identical user rephrasings, is the observable signature of a session that has gotten lost.

## Taxonomy limits — say them out loud

- **Poisoning ≈ delayed clash**: a poisoned fact eventually collides with the true one; the difference is whether the wrong fact had time to be built upon. Treat poisoning fixes as *earlier-in-time* clash fixes.
- **Distraction vs. confusion** both reduce signal share; they differ on axis (length vs. breadth) and therefore on fix (compact vs. curate). If you can't tell which you have, measure both axes separately (`measuring-context.md`).
- The taxonomy covers *in-window* failures only. Selection failures (retrieved the wrong thing) and position failures (right thing, wrong place) are upstream — see `selection-quality.md` and `position-and-ordering.md`.

## By implementation type

| Implementation | Dominant mode | Standing guard |
|---|---|---|
| RAG chatbot | Confusion (near-miss retrieval), clash (stale corpus) | Rerank+prune; corpus dedup & retirement policy |
| Coding agent | Distraction (tool-output pileup), poisoning (wrong early assumption) | Compaction at sub-task boundaries; validate before writing memory |
| Long-horizon agent | Distraction, poisoning compounding over days | Session-boundary compaction ritual + write-gates |
| Multi-agent | Clash (parallel workers deciding independently — Cognition's core objection to fan-out) | Strict briefs; single decision-owner per question |
| Text-to-SQL | Confusion + clash (ambiguous/duplicate metric definitions) | Distinguishability rules on names/descriptions |
