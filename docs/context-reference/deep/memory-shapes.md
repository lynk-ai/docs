---
description: The evidence behind memory shapes — the four write-time decisions and what to steal from the systems that pioneered them. Open when designing a memory, not using one.
layer: deep
concept: ../concepts/memory-shapes.md
---

# Memory shapes — the systems, the evidence, the survey

Two layers on purpose: the **principle** (a write is a decision — write-time policy is the whole game) is stable; the **survey** of systems below is dated and will age. Steal the decisions, not the architectures.

## The principle, argued

Append-only memory converts every hallucination into a future retrieval. The mechanism is measured: incorrect knowledge written to memory "persists and reinforces over time" — retrieved, restated, re-embedded, cited by its own echoes ([Mem0, grounded memory](https://mem0.ai/blog/reducing-hallucinations-llms-with-grounded-memory)); write-gate validation is the shared blind spot across memory systems examined by the security literature ([arXiv 2604.16548](https://arxiv.org/html/2604.16548)). Meanwhile every durable system in the survey below — independently, across five years — converged on putting its intelligence at the **write**: paging decisions, restructuring decisions, scoring decisions, verification decisions. Storage and retrieval tech varies freely; write-time policy is the invariant. That convergence is the strongest design signal in the field.

## The survey (dated 2026-07 — expect drift)

| System | Shape | Write-time decision | Caveat |
|---|---|---|---|
| **MemGPT → Letta** ([arXiv 2310.08560](https://arxiv.org/abs/2310.08560)) | OS-style paging: in-context core memory (RAM) vs. archival storage; flush/summarize on pressure | What pages in/out, and what a session's diff earns | Authors' own admission of long-run disorganization; rigid tiers underperform dynamic curation on multi-hop ([A-MEM paper's comparison](https://arxiv.org/abs/2502.12110)) |
| **A-MEM** ([arXiv 2502.12110](https://arxiv.org/abs/2502.12110)) | Zettelkasten-style living graph: notes get structured attributes (context, keywords, tags) at write; link generation finds connections; new memories trigger retrospective updates of old ones | Restructure-on-write | Reports superior results over SOTA baselines across six foundation models (secondary coverage cites ~2× MemGPT on multi-hop — not verified against the paper's tables); restructuring cost paid on every write |
| **Generative Agents** ([arXiv 2304.03442](https://arxiv.org/abs/2304.03442)) | Score at write (recency × importance × relevance); reflection passes promote observations → insights | Judge at write time | Single-LLM judge — score with multiple independent lenses to de-bias |
| **Voyager** ([arXiv 2305.16291](https://arxiv.org/abs/2305.16291)) | Skill library: memory units are runnable code, verified on each use | Store only what executes | Only works where memory *can* be a method; facts still need the other gates |
| **Letta MemFS + sleep-time compute** ([Letta](https://www.letta.com/blog/sleep-time-compute/), verified) | Two-agent split: the **primary agent converses but cannot edit memory**; a separate sleep-time agent, running on idle time, holds the edit rights to shared memory blocks (and can use a stronger model at its own pace). MemFS: memory as markdown-in-git, changes as commits merged via worktrees | Consolidation as reviewed commits, off the critical path — write rights *architecturally* separated from generation | Production proof of the PR shape for memory; reported Pareto improvement (AIME/GSM8K gains with compute shifted to idle time); young |
| **Mem0** | KV extraction from conversations, dense retrieval | Extraction filter at write | Production-targeted; write-gate thinner than the research systems |
| **Verified-write line: MemGuard / TRUSTMEM / VerificAgent** ([2605.28009](https://arxiv.org/pdf/2605.28009) / [2606.25161](https://arxiv.org/pdf/2606.25161) / [2506.02539](https://arxiv.org/pdf/2506.02539)) | Admission control; learned trustworthy consolidation; human-vetted domain memory | Explicit verification of the write itself | The principle, weaponized: VerificAgent shows vetting *raises task success*, not just safety |

**Platform absorption**: WRITE and COMPRESS are now API primitives — Anthropic ships a file-based memory tool and automatic context editing/compaction as platform features. The levers stopped being framework hacks; the *policies* driving them remain yours to design.

**Compaction timing** (the paging steal, upgraded): decision-based compaction — rubric-triggered (sub-task resolved? trajectory converging?) — beats token-threshold triggers on cost and quality ("Self-Compacting LM Agents", 2026; see `context-governance.md` for the policy treatment).

## Composing the four decisions (they stack, not compete)

A production-shaped write path uses all four in sequence:

1. **Earn** (MemGPT steal): at session end, diff working state against the archive — most sessions earn *no* write. This single ritual kills write-as-side-effect, the poisoning front door.
2. **Judge** (Smallville steal): candidate writes get scored — importance, novelty vs. existing homes (`one-concept-one-home.md`), epistemic class (`self-compiled-vs-curated.md`). Multiple lenses, not one self-grade.
3. **Restructure** (A-MEM steal): the write that lands asks whether its spot outgrew itself — split/merge/re-link now, while the context is loaded (`living-sources.md`).
4. **Verify** (Voyager steal): whatever *can* be a method becomes one — a checkable rule, a runnable snippet, a schema assertion — so future use re-verifies it for free.

Consolidation (reflection, dedup, promotion of episodic → semantic) runs **off the critical path** as sleep-time work, and its output is commits for review, not silent mutations — the MemFS pattern.

## Choosing for your system

| Your situation | Lead with |
|---|---|
| Chat assistant, per-user personalization | Extraction + judge-at-write (Smallville/Mem0 shape); aggressive earn-test — most turns deserve nothing |
| Coding agent | Voyager shape wherever possible (verified snippets, checkable conventions); archive-diff for the rest |
| Long-horizon autonomous agent | Full four-decision stack + sleep-time consolidation; structured eviction rules |
| Multi-agent fleet | Private-by-default worker memory; promotion gate to shared (blast-radius gradient) |
| Shared team KB fed by agents | The PR shape literally: drafts → gate → human merge (`self-compiled-vs-curated.md`) |
