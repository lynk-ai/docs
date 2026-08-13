---
description: Deciding what an agent may write down and when. Append-only memory reliably rots, so the write gate is the design.
layer: concept
deep: ../deep/memory-shapes.md
---

# Memory shapes

**The principle** — memory doesn't stay true by being appended to. Every durable memory system earns its keep by **deciding, at write time, what a write is allowed to do** — the write-gate is the design, everything else is storage. Even the field's founders concede the failure mode: Letta on MemGPT — "incremental memory formation… may become messy and disorganized over time." Memory rot is real and append-only guarantees it.

**Four write-time decisions, one steal each** (from the systems that pioneered them) —

| Decision at write time | Pioneered by | The steal |
|---|---|---|
| *Did this session earn a write?* — diff working state vs. archive; persist deliberately | MemGPT/Letta (paging: working vs. archival tiers) | The **archive-diff ritual** at session end: updates become decisions, not side effects |
| *Has this spot outgrown itself?* — each write may re-link, merge, rewrite neighbors | A-MEM (living note graph) | **Restructure-on-write**: hierarchy deepens exactly where writes concentrate |
| *How much is this worth?* — score at write; reflection promotes observations → insights | Generative Agents ("Smallville") | **Judge at write time**: a flat log never becomes knowledge on its own |
| *Can it prove itself?* — store runnable methods that verify on every use | Voyager (skill library) | **The write-gate is the runtime**: when memory can be a method, store the verified method |

**Status check (the shape shipped)** — this stopped being research: WRITE/COMPRESS are platform primitives (Anthropic's memory tool + context editing); Letta's MemFS runs memory as markdown-in-git with a background sleep-time agent merging session commits — the "PR shape" for memory, deployed; verified-write systems (MemGuard, TRUSTMEM, VerificAgent) now measure what ungated writes cost.

**Rules** —
- Choose write-time policy before storage tech; a vector DB with no write-gate is a poisoning queue.
- Consolidation is a separate, idle-time job (sleep-time compute) — never mid-task, always review-shaped.
- Prefer methods over facts where possible (checkable > assertable).
- Score/provenance every entry at write; retrieval-time trust repair is the expensive fallback.

**Go deeper** (`../deep/memory-shapes.md`) when: designing an agent's memory architecture, evaluating memory frameworks, or fixing a memory store that's drifting.

## Related

- [Deep: the evidence behind this page](../deep/memory-shapes.md) — open it on the trigger named above.
