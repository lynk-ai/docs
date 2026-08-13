---
description: Proving a change helped instead of asserting it — how to measure what your agent can actually hold and whether a page earns the tokens it costs.
icon: ruler
layer: concept
deep: ../deep/measuring-context.md
---

# Measuring context

**Claim** — every claim in this reference (rot, position penalties, selection failures) is *measurable in your own system*, and none of the fixes should be applied blind. A degradation claim without an instrument is a vibe; the instrument turns context engineering from folklore into tuning.

**Go deeper** — [`deep/measuring-context.md`](../deep/measuring-context.md) has the instrument kit — effective length, ablation, attribution. Read it when building the eval harness, choosing benchmarks, or arguing a context change with numbers.

**The core metric — effective length** (NoLiMa's method, portable to private evals): fix a task set; measure accuracy at short context (the *base score*); then increase context realistically. Your **effective length** = the longest context at which the model keeps ≥85% of its base score. That number — not the marketed window — is your budget. Most 128K-claiming models fall far short on non-literal tasks.

**The instrument kit** —

| Instrument | Answers | Cost |
|---|---|---|
| **Effective-length sweep** | What's my real context budget for *this* model × *this* task? | One eval set + a length ladder |
| **Position sweep** (same content, gold span at 0/25/50/75/100%) | Is my U-curve costing accuracy? Is placement the bug? | Trivial once the eval set exists |
| **Context ablation** (run with less) | Is any given block earning its tokens? *Removal that doesn't hurt = confusion inventory; removal that helps = distractors found* | The single highest-value cheap test |
| **Retrieval canary set** (fixed queries, judged results) | Is selection decaying as the corpus grows? Recall and precision separately | Small labeled set, rerun on corpus change |
| **Distractor stress test** (inject near-miss content) | How fragile is my task to plausible-wrong context? | Synthesize from your own corpus's neighbors |
| **Ops dashboards** (context-length distribution, cache-hit rate, intervention counts) | Is the system drifting toward the degraded regime? | Telemetry you likely half-have |

**Rules** —
- Never benchmark with literal-match needles only (classic NIAH is nearly saturated and overstates ability); use tasks needing inference — the gap between literal and non-literal is exactly the gap between marketing and your workload.
- Measure before optimizing: the reflexive fix (add more context) and the correct fix (move/prune/split) are *opposites* — only an instrument tells you which.
- **An artifact's value is its with-vs-without delta**, judged blind against an *external* rubric on a task where it *should* matter — expect null deltas on tasks the model already aces (run a non-inferable task class too).
- **One run proves nothing**: agents decay ~⅓ from pass^1 to pass^4 (τ-bench: SOTA <50% single-run, pass^8 <25%). Run k trials before believing a context change "worked."
- Trust *deltas* over absolutes: public-benchmark absolutes inflate as they age into training data (SWE-Bench+ measured ~3×); ablation deltas mostly cancel the inflation.
- Re-run on every model swap: rot curves are model-specific and non-uniform; a budget tuned for one model silently misfits the next.
