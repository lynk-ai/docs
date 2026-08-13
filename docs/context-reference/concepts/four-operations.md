---
description: The vocabulary for what you can actually do about a crowded window — write, select, compress, isolate — and the two things that vocabulary leaves out.
layer: concept
deep: ../deep/four-operations.md
---

# The four operations (and the two the taxonomy misses)

**Claim** — WRITE / SELECT / COMPRESS / ISOLATE (Lance Martin's taxonomy, building on Karpathy's "LLM-as-OS" framing) are the four levers on *what is inside the context window right now*. They're a complete vocabulary for volume management — and an **incomplete** one for context quality, because they treat context as an unordered set.

**Go deeper** — [`deep/four-operations.md`](../deep/four-operations.md) has each operation in depth plus the two the taxonomy misses. Read it when designing an agent's context flow end-to-end, mapping your architecture to the levers, or choosing which lever to pull for a given failure mode.

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
