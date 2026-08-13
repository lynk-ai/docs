---
description: Deciding what an agent may write into the layer itself and what a person must approve first, set by how much damage a bad entry would do.
layer: concept
deep: ../deep/self-compiled-vs-curated.md
---

# Self-compiled vs. curated knowledge

**Claim** — agent-written (self-compiled) and human-authored (curated) knowledge are not rival systems; they are **the same artifact at two trust stages**. A self-compiled draft becomes curated truth by passing review — the PR shape: the agent proposes, the merge makes it truth. What varies by system is *who* holds merge rights, and that should be set by **blast radius**, not ideology.

**Go deeper** — [`deep/self-compiled-vs-curated.md`](../deep/self-compiled-vs-curated.md) has both failure directions with evidence, and how to set merge rights. Read it when designing memory write paths, deciding review policy for agent-generated docs, or writing/pruning context files (CLAUDE.md, AGENTS.md).

**Why it matters — both failure directions are now measured** —
- *Ungated agent writes rot the shared layer*: memory-security surveys find write-gate validation is a shared blind spot across examined memory systems; contaminated entries persist and reinforce across sessions. Verified-memory systems (VerificAgent and successors) show human-vetted memory measurably improves task success over unvetted accumulation.
- *Unreviewed human writes rot it too*: the ETH Zurich AGENTS.md evaluation found context files tend to **reduce task success while inflating inference cost >20%**; LLM-generated context files were net-negative (recommendation: omit them), human ones help only when confined to non-inferable project facts. And a 1,650-session factorial study (McMillan) found file *structure* (size, position, even cross-file contradictions) doesn't detectably matter — **what's admitted matters; instructions then decay in use** (~5.6% lower compliance odds per generated function). Curation is a *quality bar*, not an authorship label.

**The gradient (set merge rights by blast radius)** —

| Layer | Blast radius of a wrong merge | Door |
|---|---|---|
| Session notes, working memory | One session | Agent writes freely |
| Shared operational memory | Every future session of one agent | Agent writes through a validation gate |
| Team knowledge base | Every reader, human and agent | Agent proposes; automated gate checks; human merges |
| Constitution / standards / definitions | Every decision downstream | Human-only merge, always |

**Rules** —
- Never let content skip a stage: "confident draft" is not a trust level.
- The gate can be automated wherever criteria are checkable (structure, sources, consistency); the *authority* to declare truth scales with blast radius because downstream readers stop re-checking — trust is the thing being manufactured.
- Mark provenance on every entry (who wrote, who reviewed, when) — unmarked prose all reads equally true to a model.
- Gate the write, not just the read: retrieval-time filtering of a poisoned store is strictly harder than admission control.
