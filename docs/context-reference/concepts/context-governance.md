---
description: Nothing forces a cleanup on its own. How to assign a signal, a policy, and an owner so a layer stays clean instead of drifting until someone notices.
layer: concept
deep: ../deep/context-governance.md
group: The guards
---

# Context governance

**Claim** — clean context is a *control loop*, not a virtue: **instrument → policy → owner → intervention**, running continuously. The failure modes don't prevent themselves, and "everyone curates as they go" is how every corpus rots — governance means specific signals watched by a named owner empowered to intervene. What distinguishes this from vibes is that each piece is concrete: real metrics, written policies, assigned actors.

**The loop** —

| Stage | What it is | Examples |
|---|---|---|
| **Instruments** | Signals watched continuously | Context-length distribution per session; KV-cache hit rate (churn detector); retrieval precision on a canary set; staleness age per page; contradiction count; effective-length evals |
| **Policies** | Written triggers → actions | "Compact at sub-task boundaries" (beats fixed 70–90%-of-window thresholds); "split pages past budget"; "retire superseded docs at merge"; reversibility hierarchy: raw > compaction > summarization |
| **Owners** | Named actors, ongoing + static | Ongoing: a maintenance/sleep-time agent (Letta ships this: background agent reviews sessions, merges memory as commits). Static: a fail-closed gate at each trust boundary |
| **Interventions** | The actions themselves | Compact, split, merge, retire, re-index, escalate a clash to a human |

**The two governor shapes** (same axis as hook-vs-router) —
- **Ongoing**: runs continuously, catches early, pays constantly — hook-shaped (drift monitors, sleep-time consolidation, telemetry).
- **Static**: sits at a checkpoint, catches late but decisively, pays per-invocation — router-shaped (gates at publish/merge/execute).
Production systems need both: ongoing governors keep the *rate* of rot down; static governors bound the *worst case* that ships.

**Rules** —
- If you can't name who owns a signal, nobody does — and it's currently unwatched.
- Policy beats threshold: *decision-based* compaction (sub-task resolved? trajectory converged?) outperforms token-count triggers on cost and quality.
- Govern writes hardest: admission is cheaper than cleanup (poisoning enters at write time).
- The governance loop needs its own instrument: track intervention counts — zero interventions means the loop is dead, not that the corpus is clean.

**Go deeper** (`../deep/context-governance.md`) when: standing up maintenance for a corpus/agent fleet, choosing compaction policy, or assigning ownership of context health.

## Related

- [Deep: the evidence behind this page](../deep/context-governance.md) — open it on the trigger named above.
