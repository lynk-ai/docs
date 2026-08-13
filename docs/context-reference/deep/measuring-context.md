---
description: The evidence behind measuring context — the instrument kit — effective length, ablation, attribution.
icon: magnifying-glass-chart
layer: deep
concept: ../concepts/measuring-context.md
---

# Measuring context — the instruments, in full

## What the public benchmarks established (and their limits)

- **NIAH (needle-in-a-haystack)** — the original probe: plant a fact, ask for it back. Now nearly saturated: frontier models ace literal retrieval at length, which is why vendors quote it. Its saturation is the *reason* better instruments exist — passing NIAH says almost nothing about reasoning at length.
- **RULER** ([arXiv 2404.06654](https://arxiv.org/abs/2404.06654)) — NIAH extended with multi-hop tracing, aggregation, and QA at configurable lengths. Key finding: claimed vs. effective sizes diverge sharply, and **aggregation/multi-hop degrade fastest** — the task shapes agent work resembles. If you adapt one public suite, adapt this one.
- **NoLiMa** ([Adobe Research](https://github.com/adobe-research/NoLiMa), arXiv 2502.05167) — removes lexical overlap between needle and question, forcing associative inference. Verified results: GPT-4.1 claimed 1M / effective **16K**; GPT-4o 128K / **8K**; Claude 3.5 Sonnet 200K / **4K**; Gemini 1.5 Pro 2M / **2K**; at 32K, 10 models sit below 50% of their own baseline. Its lasting contribution is the **metric**: *base score* at short context (250–1K tokens), *effective length* = longest context retaining ≥85% of base.
- **Chroma's context-rot protocol** ([Chroma](https://research.trychroma.com/context-rot)) — the methodological model: hold task difficulty constant, vary *only* input length and distractor composition. Their design isolates three variables worth copying: length alone, distractor presence, and needle-question similarity.

Limit to respect: all are synthetic. They bound what's possible, not what your workload gets — which is why the kit below runs on *your* corpus and tasks.

## Building the harness (one eval set, five instruments)

**Step 0 — the eval set.** 30–100 tasks from your real workload with verifiable answers (exact match, contains-check, or LLM-judge with rubric). This is the only expensive step; everything below reuses it.

**1. Effective-length sweep.** Embed each task's needed evidence in realistic context (your actual docs/history/schema, not lorem) at a length ladder — e.g. 1K / 4K / 16K / 64K / 128K. Plot accuracy vs. length; read off the ≥85%-of-base point. That's your budget for this model×task. Expect non-uniform curves (plateau, then cliff) — report the cliff, not a fitted slope.

**2. Position sweep.** Same tasks, fixed total length, gold evidence at 0/25/50/75/100% depth. A mid-context dip confirms the U-curve is biting *you*; its magnitude prices every placement decision in `position-and-ordering.md`. (This is the Chroma/NIAH depth-sweep, pointed at your own layout.)

**3. Context ablation — the highest-value cheap test.** For each standing context block (system-prompt section, tool group, always-loaded doc, memory injection): rerun the eval *without it*.
- Accuracy unchanged → the block is confusion inventory; it's paying attention cost for nothing (per the ETH Zurich AGENTS.md evaluation, "helpful" context files tend to reduce success while inflating cost >20% — measure, don't assume).
- Accuracy *improves* → you found distractors; remove or gate them.
- Accuracy drops → the block earns its tokens; record by how much, so future budget fights have numbers.
Run it quarterly and on every prefix addition — standing context only ever accretes otherwise (see `context-governance.md`).

**4. Retrieval canary set.** Fixed queries with labeled relevant docs; rerun on every corpus/index change. Track recall@k and precision@k *separately* (they fail independently — `selection-quality.md`); alert on trend, not single runs. This catches selection decay that end-to-end evals launder into vague quality drift.

**5. Distractor stress test.** Synthesize near-misses from your own corpus (the neighbor page, last quarter's version of the doc, the sibling metric) and inject alongside gold evidence. Fragility here predicts production failures better than clean-context accuracy — distractor interference, not volume, is Chroma's sharpest finding. Your worst distractors are your own stale/sibling content: this test doubles as a corpus-hygiene audit (`living-sources.md`, `distinguishability.md`).

**6. Baseline delta — does this context artifact earn its cost at all?** The with-vs-without test for any doc/skill/reference: two arms, identical except the artifact (same model, tools, task; blind to each other); a blind judge scoring against an **external rubric** — never the artifact's own phrasing, or the artifact literally grades itself and cannot lose. Three rules that make the number real:
- **Pick a task where the artifact *should* matter** — the delta is near-zero on tasks the model already aces (the *in-distribution ceiling*: a null on easy tasks is expected, not exoneration). A live two-round case: a conventional-commits skill measured a null delta (model already knew it); a niche-CLI skill measured a clear win (8/8 claims verified vs 6/8 with one false) — same method, the sign flipped with task inferability. Run both task classes before concluding.
- **Ground the judge in execution** where checkable — have it *run* the claims, not read them; the static judge in that same case could only reach "marginal" where the executing judge was decisive (the general principle: verify at the surface where the artifact is actually consumed — a green check on a proxy surface over a red authoritative one is *false green*, confidence manufactured by pointing the tool at the wrong place).
- **n=1 proves nothing** — see reliability, below.

## Two disciplines the numbers need

**Reliability: measure pass^k, not pass^1.** Agents are unstable across identical trials: τ-bench ([arXiv 2406.12045](https://arxiv.org/abs/2406.12045), verified) reports SOTA agents succeeding on **<50% of tasks**, with **pass^8 <25%** in retail — the best agent's pass^k decays ~0.69 → 0.46 from k=1 to k=4 (secondary source, not re-verified against the paper). A single-run pass overstates reliability by roughly a third. For context work this cuts twice: a context change that "fixed it" in one run may have fixed nothing; run k trials and compare *distributions*. And grade **checkpoints/final state, not a canonical path** — agents take different valid routes; a route-matcher fails correct work.

**Validity: benchmarks are living sources — they decay.** SWE-Bench+ ([arXiv 2410.06992](https://arxiv.org/abs/2410.06992)) found 32.67% of "successful" patches had solution leakage and 31.08% passed on weak tests — filtering both dropped SWE-Agent+GPT-4 from 12.47% to **3.97%, ~3× inflation**; GSM1k measured contamination-driven overfitting on GSM8k. Consequence: any absolute number quoted from an aging public benchmark inherits its validity risk — including numbers in this reference. Ablation *deltas* survive better than absolutes (both arms share the inflation, so it approximately cancels), which is one more reason the ablation instruments above are the ones to trust.

**The ablation evidence pack** (why instrument #3 is the one to run first — component ablations from the agent literature, secondary sources not re-verified against the papers; absolutes carry the validity caveat above, deltas are the point):
- SWE-agent ([arXiv 2405.15793](https://arxiv.org/abs/2405.15793)): the agent-computer interface vs. a bare shell = 18.0 vs 11.0 on SWE-bench Lite — the *interface* was worth a 64% relative gain, before touching model or prompt.
- Same table, the context-rot smoking gun: **full history 15.0 vs. last-5-observations 18.0** — keeping less context outperformed keeping all of it, in a controlled ablation.
- Same table, the tool-quality warning: a badly designed iterative search tool scored 12.0 — **worse than having no search tool at all (15.7)**. A bad tool is negative context. When an agent keeps failing, suspect its tool interface before its model or its prompt.
- ChatDev ([arXiv 2307.07924](https://arxiv.org/abs/2307.07924)): removing role descriptions from prompts dropped quality 0.395 → 0.221 — its largest single ablation.

## Ops-layer instruments (continuous, no eval set needed)

| Signal | Reading it |
|---|---|
| Context-length distribution per session | The right tail is where distraction lives; watch its growth rate, not just the mean |
| KV-cache hit rate | Churn detector — a drop means someone mutated the stable prefix ([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)); doubles as a context-discipline metric |
| Compaction/intervention counts | Zero = the governor is dead, not the corpus clean |
| Staleness age percentiles | Living-source debt, trending |
| Wrong-tool / wrong-page selection rate (sampled traces) | Distinguishability and loadout health |

## Decision table — symptom → instrument → fix page

| Symptom | Run | Then see |
|---|---|---|
| "Quality degrades in long sessions" | Effective-length sweep; length distribution | `context-rot.md`, compaction policy in `context-governance.md` |
| "It missed something that was in context" | Position sweep; ablation | `position-and-ordering.md` |
| "Answers cite wrong/irrelevant docs" | Canary set; distractor test | `selection-quality.md` |
| "Inconsistent answers to the same question" | Contradiction sweep on hot topics | `one-concept-one-home.md`, clash handling in `four-failure-modes.md` |
| "Wrong tool/metric picked" | Surface route-test (names+descriptions only) | `distinguishability.md` |
| "Costs/latency creeping" | Cache-hit rate; length distribution | `caching-economics.md` |

## Discipline

- **Re-baseline on model swap** — rot curves are model-specific; budgets don't transfer.
- **One variable per experiment** — length, position, and composition confound each other; the public protocols' whole value is isolation.
- **Keep the eval set versioned with the corpus** — an eval set that drifts from the corpus measures nothing.
- **Report effective length, not marketed windows, in design docs** — it's the number every other page in this reference budgets against.
