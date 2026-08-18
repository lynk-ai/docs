---
description: The vocabulary for what you can actually do about a crowded window — write, select, compress, isolate — and the two things that vocabulary leaves out.
icon: sliders
---

# The four operations (and the two the taxonomy misses)

**Claim** — WRITE / SELECT / COMPRESS / ISOLATE (Lance Martin's taxonomy, building on Karpathy's "LLM-as-OS" framing) are the four levers on *what is inside the context window right now*. They're a complete vocabulary for volume management — and an **incomplete** one for context quality, because they treat context as an unordered set.

**The four** —

| Operation | Means | Example |
|---|---|---|
| **WRITE** | Persist outside the window so it isn't lost or crammed in now | Scratchpad file, memory store, todo list on disk |
| **SELECT** | Pull in only what's relevant, exactly when relevant | Read one file, load one skill, retrieve 3 chunks |
| **COMPRESS** | Shrink in place without losing the point | Summarize a tool result; compaction |
| **ISOLATE** | Give a sub-task its own window; return only the distilled result | Research sub-agent returning cited findings |

WRITE/SELECT trade on *time* (needed later vs. now); COMPRESS/ISOLATE trade on *volume*. Anthropic's production triad — compaction, structured note-taking, sub-agents — is COMPRESS, WRITE, ISOLATE productized.

**What the set-model misses (two more decisions you always make)** —
- **ORDER** — *where* in the window content sits changes accuracy (U-curve: edges strong, middle weak) and changes cost (stable prefix = cache hits). Every SELECT implies a placement decision the taxonomy doesn't name. → `position-and-ordering.md`
- **CACHE** — token *economics* aren't uniform: a cached prefix token costs ~10% of a fresh one, which reshapes what COMPRESS is worth doing on. → `caching-economics.md`

**Also note the blur** — SELECT and COMPRESS converge at the boundary (query-aware pruning like Provence is "select at sentence granularity"). Don't argue category membership; argue token budgets.

## Evidence & practice

Attribution: WRITE/SELECT/COMPRESS/ISOLATE is Lance Martin's framing (LangChain, 2025), building on Karpathy's "LLM as OS / context as RAM" analogy. The 1400-paper [Context Engineering survey (arXiv 2507.13334)](https://arxiv.org/abs/2507.13334) uses a compatible academic cut — context *retrieval/generation*, *processing*, *management* — with RAG, memory systems, and multi-agent systems as the composed implementations. The two taxonomies map cleanly: SELECT ≈ retrieval, COMPRESS ≈ processing, WRITE ≈ management-out, ISOLATE ≈ multi-agent management.

### Choosing the lever — failure mode → operation

| You observe | Pull | Not |
|---|---|---|
| Losing state across turns/sessions | WRITE | Bigger window (rot) |
| Right answer exists but wasn't in context | SELECT | More standing context (confusion) |
| Everything needed is present, window bloating | COMPRESS | Truncation (silent loss) |
| One sub-task generates huge intermediate mess | ISOLATE | In-line processing (distraction) |
| Right content, wrong accuracy anyway | ORDER (see below) | More retrieval |
| Costs scaling linearly with session length | CACHE (see below) | Smaller model |

### Each lever's craft, with evidence

**WRITE** — the discipline is the *write-gate*: what earns persistence (see `memory-shapes.md` and `self-compiled-vs-curated.md`). Anthropic's "structured note-taking" is WRITE productized: the agent maintains notes outside the window and re-SELECTs them ([Anthropic, effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

**SELECT** — the highest-leverage and most failure-prone lever; it has its own page (`selection-quality.md`). Headline numbers: hybrid BM25+dense beats either alone (+7.4% NDCG on WANDS); two-stage retrieve-then-rerank dominates single-stage (Recall@5 0.816 vs 0.695); pruning near-misses *improves* answers (Provence).

**COMPRESS** — reversibility is the design axis ([Redis](https://redis.io/blog/context-compaction/), [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/agents/conversations/compaction)): *compaction* drops what's re-fetchable from the environment (reversible — file contents, tool results that can be re-run); *summarization* is lossy and permanent. Hierarchy: **raw > compaction > summarization**. *When* to compress is a decision, not a threshold: rubric-triggered compaction (sub-task resolved? trajectory converged?) beats fixed 70–90%-of-window triggers on both cost and quality ("Self-Compacting Language Model Agents", 2026; LangChain [autonomous context compression](https://www.langchain.com/blog/autonomous-context-compression)). Cognition's production caveat (verified): for truly long tasks they compress history with a *dedicated model* trained to keep "key details, events, and decisions" — and call even that "hard to get right", worth fine-tuning; Anthropic's compaction guidance agrees on what survives: architectural decisions and unresolved bugs stay, redundant tool outputs go.

**ISOLATE** — the highest-variance lever, both sides now primary-verified. For it: Anthropic's multi-agent research system (Opus 4 lead + Sonnet 4 sub-agents) beat single-agent Opus 4 by **90.2%** on their internal research eval; on BrowseComp, **token usage alone explains 80% of performance variance** (token usage + tool calls + model choice: 95%) — separate windows are a way to *spend more attention*, which is exactly why they cost **~15× chat tokens** (plain single agents: ~4×). Sub-agents return condensed summaries of ~1,000–2,000 tokens ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)). Against it: Cognition's "don't build multi-agents", verified — two principles: *share full agent traces, not summaries*, and *actions carry implicit decisions; conflicting decisions produce bad results*. Their Flappy Bird example: one sub-agent builds a Mario-style background, another an incompatible bird — each decision locally fine, jointly incoherent ([Cognition](https://cognition.com/blog/dont-build-multi-agents)). Reconciliation (both posts actually agree): Anthropic's own "when not to" list is Cognition's argument — shared-context tasks, heavy inter-dependencies, most coding. ISOLATE wins for **read** work (results merge as facts) and loses for **write** work (results merge as decisions). Isolate readers, serialize writers.

### The two levers the set-model misses

The four operations decide **what** is in the window. Two further decisions always exist and are invisible in the taxonomy:

1. **ORDER** — position changes accuracy (U-curve, up to ~30% penalty for middle placement) and cost (prefix stability determines cache hits). A SELECT that drops the key document mid-window can underperform a smaller context with edge placement. Full treatment: `position-and-ordering.md`.
2. **CACHE** — cached input tokens cost ~10% of fresh ones (Anthropic pricing; 25% write premium, breakeven ≈1.4 reads). This inverts some COMPRESS decisions: aggressively summarizing a *stable* prefix can cost more than leaving it cached. Full treatment: `caching-economics.md`.

Treat the complete toolkit as **six decisions**: what to write out, what to pull in, what to shrink, what to split off, where to put it, what to keep stable.

### Worked composition (one pass of a library/RAG pipeline)

1. Corpus pages = WRITE (knowledge persisted outside every window)
2. Router picks 3 pages from metadata = SELECT (cheap surface: names + descriptions only)
3. Scout reads candidates in its own window = ISOLATE
4. Scout returns pointers + 2-line justifications = COMPRESS (the return is the compressed artifact)
5. Main agent loads pointed pages *after* the stable system prefix = ORDER + CACHE

Each stage exists because skipping it reintroduces a named failure: skip 2 → confusion; skip 3 → distraction; skip 4 → the isolation was pointless; skip 5 → pay full price for the middle of the window.
