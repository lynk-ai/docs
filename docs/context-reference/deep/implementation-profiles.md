---
description: The evidence behind implementation profiles — the five profiles with their dominant failure and first-order levers.
layer: deep
concept: ../concepts/implementation-profiles.md
when: Starting or auditing a system; deciding what to fix first
---

# Implementation profiles — the five workloads, in full

Each profile: what shapes it, where it bleeds, the priority order, and the specific evidence. The principles referenced live in their own pages; this page is the *dispatch table*.

## 1. RAG / knowledge-base chatbot

**Shape**: short sessions, latency-bound, context written by *authors* (not the agent), answers must ground in the corpus.
**Bleeds at**: selection (near-miss retrieval is the top quality ceiling — distractors actively mislead) and corpus hygiene (staleness + contradiction: ~70% of enterprise KBs hold contradictory pairs; retrieval keeps finding plausible-but-outdated fragments).
**Priority order**: (1) two-stage retrieval + pruning — hybrid recall, rerank, Provence-style prune (`selection-quality.md`); (2) corpus governance — one home per fact, retirement at merge, re-index on refactor (`one-concept-one-home.md`, `living-sources.md`); (3) grounding gate before answers ship (`hook-vs-router.md`); (4) placement — best chunk directly before the question (`position-and-ordering.md`).
**Deprioritize**: compaction and memory machinery — sessions are short; the corpus, not the transcript, is the living object.
**Instrument**: retrieval canary set + staleness dashboard (`measuring-context.md`).

## 2. Coding agent

**Shape**: medium sessions, tool-loop heavy (100:1 input:output typical), the *environment is the corpus* — most knowledge is re-fetchable from the repo at will.
**Bleeds at**: distraction (file dumps and tool output piling up) and standing-context bloat — the measured trap: the ETH Zurich AGENTS.md evaluation found context files tend to reduce task success while inflating inference cost >20%; survivors are non-inferable project facts only. And structure won't save a bloated file: McMillan's 1,650-session factorial (arXiv 2605.10039) found size/position/architecture nulls — admission is the lever, and compliance decays in-session (~5.6% odds per generated function) regardless.
**Priority order**: (1) agentic SELECT over standing dumps — grep/read excerpts on demand; no pre-built embedding index needed (the environment supports live search — the production consensus for code); (2) offload + compaction at sub-task boundaries, *compaction not summarization* — file contents are re-fetchable, so drop them reversibly (`four-operations.md`); (3) context-file admission test: would the agent get this wrong without it? (`self-compiled-vs-curated.md`); (4) append-only transcript for cache (highest-hit-rate workload there is — `caching-economics.md`); (5) memory as verified methods where possible — checkable conventions beat prose notes (Voyager steal, `memory-shapes.md`).
**Deprioritize**: retrieval infrastructure (the repo *is* the index); heavy memory graphs.
**Instrument**: ablation test on every standing block; cache-hit rate.

## 3. Long-horizon autonomous agent (days/weeks, unattended)

**Shape**: one context lineage surviving many compactions; the agent is the *primary author* of its own future context — every write is self-administered medicine.
**Bleeds at**: compounding failures — early wrong assumptions poison later reasoning ("when LLMs take a wrong turn, they get lost and do not recover" — the −39% multi-turn result); rule-following decays with generation itself (~5.6% lower compliance odds per function, McMillan); distraction accumulates monotonically; nothing external re-anchors the run — which is why Manus recites the plan into the recency window every step.
**Priority order**: (1) compaction policy — decision-based triggers (sub-task resolved?) over token thresholds; reversibility hierarchy raw > compact > summarize; typed eviction rules for what must never leave (`context-governance.md`); (2) memory write-gates — the full four-decision stack: earn, judge, restructure, verify (`memory-shapes.md`); (3) sleep-time consolidation off the critical path, commit-shaped (Letta pattern); (4) periodic self-audit against instruments, not vibes — drift detection is a governance job (`measuring-context.md`); (5) position: compaction summaries early, live state late (`position-and-ordering.md`).
**Deprioritize**: nothing — this profile is the only one that eventually needs every page; it's the stress test of the whole reference.
**Instrument**: context-length distribution over run time; intervention counts; distractor stress tests on its own accumulated notes.

## 4. Multi-agent system

**Shape**: parallel windows, results merging upward; ~15× token cost of single-chat (Anthropic; plain agents ~4×) buys breadth — and the spend *is* the mechanism: token usage alone explains 80% of performance variance on BrowseComp.
**Bleeds at**: clash — the defining risk. The field's live disagreement, resolved by work type: Anthropic's research system beat single-agent by 90.2% (Opus 4 lead + Sonnet 4 subs) on breadth-first *read* work (findings merge as facts); Cognition's "don't build multi-agents" objection — actions carry implicit decisions, and parallel decisions conflict (their Flappy Bird example: Mario background + incompatible bird, each locally fine) — is about *write* work. Anthropic's own "when not to" list (shared-context tasks, tight dependencies, most coding) concedes the same. **Isolate readers, serialize writers.**
**Priority order**: (1) the work-type split above — fan out research/review/retrieval; keep design/code/decisions in one context; (2) strict briefs — Anthropic's verified formula: each sub-agent gets *an objective, an output format, tool/source guidance, and clear task boundaries*; vague briefs measurably caused duplicated work. Scale effort explicitly in the brief: simple fact-find = 1 agent / 3–10 tool calls; comparisons = 2–4 agents / 10–15 calls each; complex research = 10+ agents with divided responsibilities. Pointers to shared truth, never pasted copies that snapshot-drift (`one-concept-one-home.md`); (3) condensed, cited returns only — ~1,000–2,000 tokens per sub-agent (Anthropic's production figure); the transcript never merges, the findings do; (4) gates at every trust boundary, not just final output (`hook-vs-router.md`); (5) roster distinguishability — the orchestrator routes on agent names+descriptions; overlapping descriptions = misrouted work (`distinguishability.md`).
**Deprioritize**: shared long-term memory between workers (share pointers, not stores).
**Instrument**: token-spend per outcome vs. single-agent baseline — the 15× only pays above a value bar; wrong-agent routing rate.

## 5. Text-to-SQL / semantic layer

**Shape**: high-stakes single-shot selection — NL question → metric/entity choice → executable SQL; errors return *plausible numbers*, the most silent failure in this reference.
**Bleeds at**: distinguishability (sibling metrics with identical descriptions force coin-flips — the `total_points` case) and confusion-by-width (whole-catalog schema dumps).
**Priority order**: (1) distinguishable surfaces — entity-qualified metric names, contrastive descriptions, route-tested per new sibling (`distinguishability.md`); (2) route-then-load — resolve to entities first, ship only their schema, placed directly before the question (`selection-quality.md`, `position-and-ordering.md`); (3) one home per definition, human-gated — a wrong metric definition is wrong in every dashboard downstream; the layer, not prompts, defines metrics (`one-concept-one-home.md`, `self-compiled-vs-curated.md`); (4) validation gate against the layer before warehouse execution (`hook-vs-router.md`); (5) schema-drift CI — this corpus has a compiler; wire it (`living-sources.md`).
**Deprioritize**: transcript memory/compaction — the corpus is the layer, sessions are short.
**Instrument**: wrong-metric selection rate on a labeled question set; ambiguity audit on every layer change.

## Cross-profile invariants (what never flips)

1. **Rot is unconditional** — every profile budgets attention, none gets marketed-window tokens for free.
2. **Write-time gates beat read-time repair** — wherever anything writes to persistent context.
3. **Surfaces are infrastructure** — names/descriptions carry every routing decision in every profile.
4. **Measure before optimizing** — the reflexive fix (add context) and the right fix are usually opposites.
5. **Clash resolution needs authority** — no profile lets the model silently pick between contradictions.

## If your system spans profiles

Most real systems are hybrids (a coding agent with a KB; a multi-agent researcher feeding a long-horizon planner). Decompose by *context lineage*: each separately-evolving window/store gets its own profile row and its own priority order. The boundaries between lineages are trust boundaries — gate them (`hook-vs-router.md`).
