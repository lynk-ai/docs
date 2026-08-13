---
description: Which context rule matters most depends on the workload — a chatbot, a long-running agent, a batch pipeline all fail on different axes. Read it before applying advice written for a different shape.
icon: diagram-project
layer: concept
deep: ../deep/implementation-profiles.md
---

# Implementation profiles

**Claim** — "best context" is implementation-relative. The principles are constant (rot, selection, one-home, gates…), but *which lever dominates* flips with the workload's shape: how long it runs, who writes to context, how results merge, and how latency-bound it is. Applying a chatbot's context strategy to a long-horizon agent (or vice versa) fails on the axis that profile stresses most.

**Go deeper** — [`deep/implementation-profiles.md`](../deep/implementation-profiles.md) has the five profiles with their dominant failure and first-order levers. Read it when starting a new system, auditing an existing one against its profile, or arbitrating which context investment comes first.

**The five profiles and their dominant axis** —

| Profile | Dominant failure | First-order levers |
|---|---|---|
| **RAG / KB chatbot** | Confusion + clash from the corpus (near-miss retrieval, stale/duplicate docs) | Selection quality (hybrid→rerank→prune); corpus hygiene (one-home, retirement) |
| **Coding agent** | Distraction from tool-output pileup; standing-context bloat | Offload + re-SELECT (agentic search, no standing dumps); non-inferable-only context files; append-only cache discipline |
| **Long-horizon autonomous agent** | Compounding distraction + poisoning over days | Compaction policy (decision-based), structured eviction, memory write-gates, sleep-time consolidation |
| **Multi-agent system** | Clash from independent decisions; cost blowup (~15× tokens) | Isolation for *read* work only; strict briefs; gates at every trust boundary; serialize the writers |
| **Text-to-SQL / semantic layer** | Silent wrong-pick (indistinguishable metrics; schema-dump confusion) | Distinguishability of names/descriptions; route-then-load schema; human-gated definitions |

**How to use a profile** — it's a *priority order*, not a menu: every profile eventually needs every principle, but budget your engineering where the profile bleeds. A KB chatbot with a perfect compaction policy and near-miss retrieval is polished in the wrong place.

**The two discriminating questions when your system doesn't match a row** —
1. *Who writes to context over time?* (nobody → selection problem; the agent → governance/memory problem; many agents → trust-boundary problem)
2. *Do parallel results merge as facts or as decisions?* (facts → isolate freely; decisions → serialize or expect clash)
