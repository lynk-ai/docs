---
description: The evidence behind context governance — the instrument-policy-owner-intervention loop in full, including compaction policy.
layer: deep
concept: ../concepts/context-governance.md
when: Standing up maintenance; choosing compaction policy
---

# Context governance — evidence & practice

Governance is where the other principles get an *actor*. Rot (`context-rot.md`) says tokens decay answers; living-sources says nothing forces the refactor; hook-vs-router says checks must be placed deliberately. Governance is the discipline that assigns each of those a signal, a policy, and an owner — the difference between knowing the failure modes and not shipping them.

## Instruments (what production systems actually watch)

| Instrument | Detects | Source of practice |
|---|---|---|
| Context-length distribution per session/task | Distraction risk; sessions drifting toward the degraded regime | Agent-framework telemetry norms |
| **KV-cache hit rate** | Prefix churn — someone is mutating what should be stable | Manus: "the single most important production agent metric" ([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)); see `caching-economics.md` |
| Retrieval precision/recall on a fixed canary query set | Selection decay as corpus grows/drifts | RAG ops practice (`selection-quality.md`) |
| Staleness age (last-verified date per page/chunk) | Living-source debt accumulating | KB staleness scoring ([Atlan](https://atlan.com/know/llm-knowledge-base-staleness/)) |
| Contradiction count (pairwise claim checks on hot topics) | Clash inventory | KB conflict detection ([Fini Labs](https://www.usefini.com/guides/ai-knowledge-base-conflicting-answers)) |
| Effective-length eval (85%-of-base-score method) | Your model×task rot curve shifting | NoLiMa method, `measuring-context.md` |
| Intervention count per governor | A dead loop (zero interventions ≠ clean corpus) | Control-loop hygiene |

## Policies (written triggers → actions, with the evidence for each)

**Compaction policy.** The dominant framework default — summarize at 70–90% of window ([Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/agents/conversations/compaction), [Google ADK](https://google.github.io/adk-docs/context/compaction/)) — is the floor, not the target. Evidence for better: **decision-based compaction** (compact when a sub-task resolves or the trajectory converges, judged by rubric) beats token-threshold triggers on cost and quality ("Self-Compacting Language Model Agents", 2026; [LangChain autonomous context compression](https://www.langchain.com/blog/autonomous-context-compression)). Write the reversibility hierarchy into the policy: **raw > compaction (drop the re-fetchable) > lossy summarization** ([Redis](https://redis.io/blog/context-compaction/)); structured *eviction* — typed rules for what leaves and what must never (["Beyond Compaction", arXiv 2606.11213](https://arxiv.org/pdf/2606.11213)) — beats uniform summarization for long-horizon agents. Align compaction moments with cache writes (both rewrite the prefix — pay once, `caching-economics.md`).

**Corpus policies.** Split/merge on the signals in `living-sources.md`, executed by the write that notices (restructure-on-write). Retirement at merge time: the superseding change marks the superseded page, same commit. Re-index after every refactor. Page budgets enforced by linter/gate, not convention.

**Write-admission policy.** The gradient from `self-compiled-vs-curated.md`: session-scratch free; shared memory through a validation gate; KB through gate + human merge; standards human-only. Poisoning enters at write time — this is the policy to make strictest first.

**Session policy (the third exit).** Compaction assumes the session is *on track*. Add the case it doesn't cover: a session that took a wrong turn early doesn't recover by compacting — the wrong turn survives the summary. Write down all three exits and their triggers: **continue** (on track), **compact** (on track, window heavy), **reset** (off track — carry forward the established facts, discard the trajectory). Trigger for the third: repeated user rephrasings, rising turns-per-resolution, or the model defending a superseded interpretation. Also decide error retention by phase: keep failures while the sub-task is live (steering signal — Manus), drop them at the compaction boundary once it resolves (history).

**Escalation policy.** Clash goes to a human with both sources attached (`four-failure-modes.md`); the agent's job ends at detection. Name the human.

## Owners (the part every failed system skipped)

The ownership finding from the docs world transfers directly: a knowledge base goes stale because "ownership, update triggers, and validation are missing" — content maintenance has to be *someone's job wired into daily work*, not a background hope ([Sainso](https://sainso-tech.com/en/blog/keeping-a-knowledge-base-from-going-stale/); staleness's third layer is literally "ownership lapse", [Atlan](https://atlan.com/know/llm-knowledge-base-staleness/)).

The ongoing owner is now a deployable component, not aspiration: **Letta's sleep-time compute** runs a background agent during idle periods that reviews sessions, reflects, and updates shared memory blocks; MemFS ships memory-as-git with a sleep-time agent merging session commits via worktrees ([Letta](https://www.letta.com/blog/sleep-time-compute/)). That is an *ongoing governor with write access and a review shape* — the pattern to copy: idle-time reflection, changes as reviewable commits, never mid-task.

| Owner | Shape | Watches | Intervenes |
|---|---|---|---|
| Maintenance / sleep-time agent | Ongoing (hook-shaped) | Staleness, page budgets, dead links, contradiction sweeps | Proposes splits/merges/retirements as reviewable changes |
| Gate at each trust boundary | Static (router-shaped) | The artifact in front of it | Blocks or passes; fail-closed |
| Telemetry + alerts | Ongoing | Length, cache-hit, canary precision | Pages a human when a trend breaks |
| Named human | Escalation terminus | Clash queue, constitution changes | Decides; owns the liability |

Assignment test: read each instrument aloud and ask *who sees this number weekly, and what are they empowered to do about it?* No name → unwatched. A name without an intervention right → decoration.

## Static + ongoing compose (worked example)

A self-maintaining corpus: hooks stamp provenance on every write (floor) → sleep-time maintenance sweeps staleness and drafts refactors (ongoing governor, proposals only) → a fail-closed gate rules on every entry to the shared layer (static governor) → clash and constitution changes route to a named human (terminus). Four owners, no gaps: nothing enters unchecked, nothing rots unwatched, nothing gets silently resolved that needed authority. Remove any one layer and a named failure mode re-opens — which is the audit method: for each of the four failure modes, point at the owner who catches it.

## By implementation type

| Implementation | Minimum viable governance |
|---|---|
| RAG KB | Canary retrieval evals + staleness dashboard + retirement-at-merge + human review of agent-drafted articles |
| Coding agent | Context-file admission test (non-inferable only) + compaction at sub-task boundaries + memory-write diff ritual at session end |
| Long-horizon agent | Decision-based compaction + structured eviction rules + sleep-time consolidation with commit-shaped writes |
| Multi-agent fleet | Per-boundary gates + shared-registry versioning + one clash-escalation queue |
| Text-to-SQL / semantic layer | CI schema-drift diff (this corpus has a compiler — wire it) + human merge on metric definitions |
