---
description: How much an agent can actually hold before answers get worse, which is far below the window limit. The starting point for any argument about what a file costs.
icon: hourglass-half
---

# Context rot

**Claim** — answer quality degrades as input tokens grow, *even when every added token is relevant-looking*, and the degradation starts long before the window is full. This is the axiom the rest of this reference defends against.

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

## Evidence & practice

### What the research actually measured

**Chroma, "Context Rot" (2025)** — the reference study. 18 models — Claude Opus 4/Sonnet 4/Sonnet 3.7/Sonnet 3.5/Haiku 3.5; o3, GPT-4.1 (+mini/nano), GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo; Gemini 2.5 Pro/Flash, 2.0 Flash; Qwen3 235B/32B/8B — on controlled tasks where *only input length varies* and the needed information is held constant. Verified findings:

- Every model degraded at **every** length increment tested — there is no rot-free model. Degradation is **non-uniform**: models hold, then drop, at model-specific points; you cannot extrapolate a safe budget from small-scale tests.
- **The harder the association, the faster the rot**: lower needle–question semantic similarity → steeper degradation with length. Length hurts most exactly when the task requires inference rather than string-matching — your agent workload, not the demo.
- **Distractors compound**: a single semantically-similar-but-wrong item measurably degrades performance; four compound it further; individual distractors have non-uniform potency. Claude models showed the lowest hallucination rates under distractors (tending to abstain); GPT models the highest.
- **Structure beats coherence (the counterintuitive one)**: *shuffled* haystacks outperformed logically coherent ones across all 18 models — locally coherent-but-irrelevant prose interferes more than disordered filler. "It reads well" is not "it's harmless."
- **LongMemEval**: the same questions answered from a focused ~300-token prompt vs. the full ~113K-token history — focused wins significantly across models, *with reasoning/thinking modes enabled too*. The retrieval step you're tempted to skip is worth real accuracy.
- Even trivially simple tasks (repeat a list of words) degrade with length — ruling out "the task got harder" as the explanation.

**NoLiMa (Adobe Research, 2025)** — removes the literal-match crutch from needle-in-a-haystack: minimal lexical overlap between needle and question forces latent-association inference. **Effective length** = longest context keeping ≥85% of the model's short-context base score. Verified results (claimed → effective): GPT-4.1 **1M → 16K** · GPT-4o **128K → 8K** · Claude 3.5 Sonnet **200K → 4K** · Gemini 1.5 Pro **2M → 2K** · Llama 3.3 70B **128K → 2K** · Gemini 1.5 Flash **1M → <1K**. At 32K, **10 of the models drop below 50% of their own baseline** (e.g., Llama 3.1 405B: 94.7 base → 48.4). Use this metric, not the spec sheet — the gap is not marginal, it's an order of magnitude.

**RULER (NVIDIA, 2024)** — configurable synthetic benchmark (retrieval, multi-hop tracing, aggregation, QA). Same headline: claimed vs. effective context sizes diverge sharply, and *aggregation/multi-hop degrade fastest* — the tasks agent work most resembles.

**Mechanistic grounding** — "Lost in the Middle" (Liu et al., TACL 2024) established the U-shaped position curve; "Found in the Middle" (2024) showed the cause is **intrinsic positional attention bias** — edge tokens get outsized attention regardless of semantic relevance — and that calibrating it away recovers middle-position accuracy (exact numbers in `position-and-ordering.md`). Anthropic's engineering guidance (verified) grounds the *attention budget* framing in three architectural facts: n tokens ⇒ n² pairwise relationships to spread fixed attention over; models have **less training experience and fewer specialized parameters for context-wide dependencies** (long-sequence data is rare in training mixes); and the position-encoding interpolation used to extend windows itself degrades positional understanding. Rot is not a bug to be patched out — it falls out of how transformers are built and trained.

### Numbers to plan with

| Fact | Number | Source (primary, verified) |
|---|---|---|
| Models tested that showed rot | 18 / 18 | Chroma |
| Effective length vs. claimed | GPT-4.1: 16K vs 1M · GPT-4o: 8K vs 128K · Claude 3.5 Sonnet: 4K vs 200K · Gemini 1.5 Pro: 2K vs 2M | NoLiMa |
| Models below 50% of own baseline at 32K | 10 (of 12 tested) | NoLiMa |
| Middle-position penalty (multi-doc QA, 20 docs) | GPT-3.5-Turbo: 75.8% → 53.8% (−22pp) — *below its 56.1% closed-book baseline* | Lost in the Middle |
| Focused vs. full-history prompt, same questions | ~300 tokens beats ~113K significantly, all models | Chroma / LongMemEval |
| Distraction onset in production reports | Gemini 2.5: >100K tokens (repeats past actions); Llama 3.1 405B: decline from ~32K | Gemini 2.5 tech report; Databricks (both via Breunig) |
| Controlled ablation: less history beats more | SWE-agent: last-5-observations 18.0 vs full history 15.0 (SWE-bench Lite) | [arXiv 2405.15793](https://arxiv.org/abs/2405.15793), secondary source — not re-verified |
| Multi-agent fan-out cost (for comparison) | ~15× chat token spend | Anthropic multi-agent research |

### The compounding-vs-piling resolution, precisely

Both of these are experimentally true:
- Adding the *right* document to a small context raises accuracy (all of RAG rests on this).
- Adding *any* tokens lowers per-token attention and pushes content toward the degraded middle.

So the marginal token has **two opposing effects**: its information gain vs. its dilution cost — and the dilution cost is paid by *every other token already in the window*, which is why rot accelerates. Curation is the act of only admitting tokens whose expected gain exceeds their system-wide dilution cost. "Compound, don't pile" is that inequality in slogan form.

**One necessary caveat (caching)**: cost and rot are different axes. A large *stable* prefix is cheap in dollars (90% cached-read discount) but still pays full attention cost. Caching changes the economics of *keeping* tokens, never the accuracy of *attending* to them — see `caching-economics.md`. Do not let a high cache-hit rate justify a bloated prefix.

### How to apply, by implementation type

| Implementation | Where rot bites first | First move |
|---|---|---|
| RAG / KB chatbot | Retriever near-misses (distractor interference) | Rerank + prune before generation (see `selection-quality.md`) |
| Coding agent | Accumulated tool output & file dumps | Offload to files; read excerpts, not files (WRITE/SELECT) |
| Long-horizon autonomous agent | Conversation history distraction | Compaction policy + structured notes (see `context-governance.md`) |
| Multi-agent system | Sub-agent transcripts leaking upward | Return condensed, cited results only (ISOLATE) |
| Text-to-SQL / semantic layer | Schema dump width | Route to relevant entities; never ship the whole catalog |

### How to detect it in *your* system

Rot is measurable, not vibes — instrument before you optimize: fix a task set, vary only context length/composition, plot accuracy. The 85%-of-base-score effective-length method (NoLiMa) works on private evals too. Full procedure: `measuring-context.md`.

### Sources

- [Chroma Research — Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://research.trychroma.com/context-rot)
- [NoLiMa: Long-Context Evaluation Beyond Literal Matching](https://github.com/adobe-research/NoLiMa) (arXiv 2502.05167)
- [RULER: What's the Real Context Size of Your Long-Context LM?](https://arxiv.org/abs/2404.06654)
- [Lost in the Middle (Liu et al., TACL 2024)](https://arxiv.org/abs/2307.03172) · [Found in the Middle (2024)](https://arxiv.org/html/2406.16008v1)
- [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Breunig — How Long Contexts Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html) — carries the Gemini 2.5 tech-report and Databricks distraction onsets
- [A Survey of Context Engineering for LLMs (arXiv 2507.13334)](https://arxiv.org/abs/2507.13334) — 1400-paper taxonomy; rot appears across retrieval, processing, and management components
