---
description: Whether an ENTITY.md or any other file should become two. The test is which tasks need which parts, not how long the file got.
layer: concept
deep: ../deep/when-to-split.md
group: The levers
---

# When to split (and when to merge back)

**Claim** — the split decision is not about **size**, it is about **trigger heterogeneity**: a file should be split when its parts are needed by *different tasks*, and kept whole when its parts are needed by *the same task*. Size is a symptom that makes you look; it is not the criterion. Splitting on size alone manufactures the opposite failure — a corpus of shallow fragments nobody can reassemble.

**The test — five questions, in order**

1. **How many distinct triggers open this file?** More than one, with different needs → split along the trigger boundary. One trigger → leave it whole no matter how long.
2. **What fraction of loads uses each section?** Any section used by <~20% of the tasks that open the file is paying full price on every load — link it instead.
3. **Are the parts ever needed together?** If every reader of A also needs B, they are one unit. Splitting them just adds a hop (the always-co-loaded rule).
4. **Sideways or deeper?** Still one concept, just long → sibling files. Several *independently-cited* concepts → it earns its own index (a new disclosure level). The tell: you catch yourself wanting an index for the sub-part.
5. **What breaks?** List every file that references this one or anything defined in it. Splitting without fixing referrers is how you manufacture a clash.

**The opposite failure has a name.** Ousterhout's *shallow module* / "classitis": a unit whose **interface is large relative to its content**. A 40-line file with a name, a description, a load trigger, an index entry, and inbound links has more interface than substance — and many of them accumulate into more complexity than the one file they replaced. Its distributed-systems twin is the **nanoservice**: a component whose overhead outweighs its utility. Both apply verbatim to context files.

**Merge signals (split too far)** —
- Two files are **always read together** → one file.
- A file is **never read** → delete or re-trigger; unreachable content is worse than absent (it costs index space and pollutes routing).
- Answering one common question needs **3+ hops** → the boundary is in the wrong place.
- The **index is growing faster than the content** it indexes.
- A file exists only to **point elsewhere** (a stub that isn't a graduation marker).
- Siblings **cross-reference each other constantly** → high coupling, low cohesion: they were one concept.

**Don't split at all when** the whole corpus fits comfortably in the window with room for the task — under roughly **200K tokens** Anthropic's own guidance is to skip retrieval and load the lot (attention cost still applies; see `context-rot.md`).

**If you must split content that has cross-part dependencies**, don't leave the fragments bare — carry the context with them (parent-child retrieval, or prepend a situating line per fragment). Fragmentation without re-contextualisation is the single most measured failure of the pattern.

**Go deeper** (`../deep/when-to-split.md`) when: judging a specific file, deriving a size bar for a file type nobody has a constant for, or auditing a corpus you suspect is over-fragmented.

## Related

- [Deep: the evidence behind this page](../deep/when-to-split.md) — open it on the trigger named above.
