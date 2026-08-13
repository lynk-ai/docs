---
description: The evidence behind caching economics — prefix discipline, breakeven maths, and where cache hits actually land.
layer: deep
concept: ../concepts/caching-economics.md
when: Designing the message layout; cost/latency spikes
---

# Caching economics — evidence & practice

## The pricing physics

Prefill (processing input tokens) is where agent workloads spend most compute — agent loops routinely run 100:1 input:output ratios. KV-caching lets the server skip prefill for any prefix it has seen byte-identically before.

| Fact | Number | Source |
|---|---|---|
| Cached-read price (Anthropic) | ~10% of base input rate | [Digital Applied, caching economics](https://www.digitalapplied.com/blog/prompt-caching-economics-cache-first-agent-architecture-2026) |
| Cache-write premium | +25% over base, one-time | same |
| Breakeven | ≈ 1.4 reads per write | same |
| TTFT at high hit rate | seconds → <200ms | [Spheron, KV-cache economics](https://www.spheron.network/blog/context-engineering-production-ai-agents-kv-cache-long-context/) |
| Effective compute saved at 90% hit rate | 80–90% per request | same |
| Reported production hit rates, stable-prefix designs | 75–95%; one case 85.2% reusing 46,059 tokens/request | [F5 KV-cache-aware prompt engineering](https://ankitbko.github.io/blog/2025/08/prompt-engineering-kv-cache/) |

Manus (production agent company), primary source verified: KV-cache hit rate is "the single most important metric for a production-stage AI agent" — their agent averages **~50 tool calls per task** at a **100:1 input:output token ratio**, and on Claude Sonnet the cached-vs-uncached spread was **$0.30 vs $3.00 per MTok — 10×** — so the hit rate multiplies into essentially the whole bill ([Manus, context engineering lessons](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).

## The invalidation model (what actually breaks caches)

A cache hit requires a **byte-identical prefix**. Everything after the first differing byte re-prefills. The recurring production bugs:

1. **Timestamps/UUIDs in the system prompt** — a `Current time: 14:32:07` line at the top invalidates the entire session's cache every request. Put volatile facts late, or quantize them (date, not second).
2. **Non-deterministic serialization** — tool schemas emitted from a hash map: identical schemas, shifting key order, zero hits. Sort keys; pin tool order.
3. **Mid-history mutation** — re-summarizing turn 3, deleting a failed tool call, "cleaning up" old messages: every token after the edit re-prefills. Manus's rule: **append-only context**; even *errors stay in the transcript* (with the bonus that the model learns from seeing its own failure).
4. **Dynamic tool loadouts** — adding/removing tools mid-session rewrites the (early-positioned) tool block. Manus's rule, verified: **mask, don't remove** — constrain choice via logits masking / response prefilling while keeping definitions byte-stable; removal both invalidates the cache *and* confuses the model when history references tools that no longer exist. If the loadout must genuinely vary, route to differently-scoped agents instead.
5. **Conversation forking** — parallel branches each pay a cache write; fine if each branch reads ≥1.4 times, wasteful for single-shot speculative branches.

## Design patterns

- **Cache-aligned layout** = accuracy-aligned layout (happy coincidence, see `position-and-ordering.md`): stable system/rules/tools first (primacy + cacheable), volatile task last (recency + per-request anyway). The layouts agree; there is no real trade-off in zone order — only in *churn discipline*.
- **Compaction at boundaries, not thresholds**: compaction is a deliberate cache-purchase — you rewrite history, pay one write premium, then read the smaller prefix many times. Do it at sub-task boundaries where the old context is finished appreciating. Compacting mid-task pays the premium *and* loses in-flight recency.
- **Cache-aware skill/reference design**: standing references (like this one) belong in the stable prefix tier only if used most turns; occasionally-used depth belongs behind progressive disclosure (load-on-demand appends), which costs fresh tokens *once* rather than cached tokens *always*. The break-even: a D-token deep page consulted on fraction f of requests costs f·D fresh vs. D·0.1 cached-every-turn — on pure price, on-demand wins when f < ~10% (plus the attention saving, which always favors on-demand; see below).
- **Session note / sticky pointers**: a small always-loaded pointer layer (≤2KB) that keys into on-demand bodies is the cache-optimal shape of progressive disclosure: the pointer layer is stable (cacheable), the bodies are pay-per-use.

## The tension with context-rot, resolved precisely

Caching makes tokens cheap in **dollars and latency**; it does nothing for **attention**. A cached 100K prefix still dilutes attention over 100K tokens and still buries mid-prefix content in the dead zone. So:

- Dollar-optimal ≠ accuracy-optimal. The 10% price makes it *tempting* to keep everything; rot makes that a quality bug you've merely made affordable.
- Correct objective: **minimize tokens for accuracy first** (rot bounds the budget), **then maximize stability within that budget** (caching prices it). In that order — a cheap wrong answer is still wrong.
- The only place caching legitimately *changes* a context decision: content on the keep/drop margin that is perfectly stable and frequently used (e.g., core tool definitions) — the discount can tip it to "keep." Content that is volatile or rarely used gets no help from caching and should fight for admission on accuracy grounds alone.

## By implementation type

| Implementation | Cache posture |
|---|---|
| RAG chatbot | System+tools cached; retrieved chunks are per-request (never cached) — keep them lean instead |
| Coding agent | Long-lived session, append-only transcript: the highest-hit-rate workload there is; protect it (no mid-history edits) |
| Long-horizon agent | Compaction cadence = cache-write cadence; align both to sub-task boundaries |
| Multi-agent | Each sub-agent pays its own cache writes — another reason briefs should be small and workers should batch reads |
| Text-to-SQL | Semantic-layer definitions of *hot* entities cacheable; full catalog stays out (rot), cold entities load on route |
