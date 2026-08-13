---
description: Why a lean layer can still be expensive — cached tokens cost about a tenth of fresh ones, so churn drives the bill rather than size. Read it when deciding what stays stable and what gets rewritten each turn.
layer: concept
deep: ../deep/caching-economics.md
---

# Caching economics

**Claim** — tokens don't cost the same. A cached input token costs ~10% of a fresh one (Anthropic: 90% read discount, 25% one-time write premium, breakeven ≈ 1.4 reads), and a cache hit skips prefill compute — TTFT drops from seconds to sub-200ms at high hit rates. Context design that ignores this optimizes the wrong bill.

**Go deeper** — [`deep/caching-economics.md`](../deep/caching-economics.md) has prefix discipline, breakeven maths, and where cache hits actually land. Read it when designing an agent loop's message layout, costing a system, or diagnosing latency/cost spikes.

**Why it changes the advice** — "keep context lean" is an *accuracy* rule (rot). Caching adds an orthogonal *economic* rule: the cost of context is dominated by its **churn**, not its size. A 30K stable prefix read 50 times costs less than a 5K prefix rewritten every turn. The two rules compose: minimize total tokens for accuracy; among the tokens you keep, maximize stability for cost.

**Rules (prefix discipline)** —
- **Stable-first layout**: system prompt, rules, tool definitions at the top; anything per-request at the bottom. One changed byte invalidates everything after it.
- **Character-for-character stability**: no timestamps, request IDs, or "randomized" examples in the prefix; serialize tools/JSON deterministically — same schemas in a different key order is a full cache miss.
- **Append-only sessions**: agent loops that only append to history keep the whole transcript cacheable; mid-history edits (silent truncation, re-summarizing turn 3) forfeit the suffix.
- **Compact at cache-priced moments**: compaction rewrites history — schedule it at natural boundaries (sub-task done) where you'd re-write the cache anyway, not mid-flight.

**The hit-rate numbers** — production reports: stable-prefix designs reaching ~85% hit rates reusing ~46K tokens/request; workloads with 60%+ prefix overlap sustaining 75–95%; effective compute cost per request down 80–90% at 90% hit rate. Manus calls KV-cache hit rate *the* single most important production agent metric.

**The boundary** — caching never buys accuracy: a cached token still spends attention budget and still rots. Cheap ≠ free. Never let hit rate justify a fat prefix (see `context-rot.md`).
