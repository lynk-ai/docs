---
description: A file grew until it blurs, or two files drifted until they disagree, and nothing in the build will ever tell you. The signals that say split, and the ones that say merge back.
icon: seedling
---

# Living sources

**Claim** — a source of truth doesn't stay put: it grows until it blurs (needs a **split**) or converges with a neighbor until they disagree (needs a **merge**) — and *nothing forces the refactor*. Code that outgrows its structure fails review or fails to compile; context that outgrows its structure just quietly degrades every answer that reads it. That asymmetry is why context debt is worse than code debt: it has no compiler.

**Why it matters** — staleness is the top decay path of deployed corpora: RAG systems drift as chunks go stale and retrieval keeps surfacing plausible-but-outdated fragments; documentation issues cost an estimated **$200K+/year for a 50-person engineering team**; support teams add ~40 docs/month and retire almost none. Every stale fragment is a future clash or poisoning event.

**Split signals (any one suffices)** —
- The page answers two different questions depending on who asks ("customers" covering two business meanings).
- Corrections accumulate as caveats instead of rewrites — a wall of "however/except/as-of".
- Readers quote different parts of it as "the answer" to the same question.
- It exceeds what one retrieval hit can usefully carry (the chunk boundary cuts mid-concept).

**Merge signals** —
- Two sources answer the same question with slightly different words (today) — a clash scheduled for later.
- Readers get whichever version their query phrasing happened to match.

**Rules** —
- Split/merge is triggered by the *write that notices*, not by a schedule — the noticing moment is the cheapest time to act (restructure-on-write, per A-MEM's model).
- Pointers absorb the refactor: readers of the old location follow a forward pointer; nothing breaks loudly — which is exactly why you must budget for it deliberately.
- Retire as deliberately as you author: a superseded page left retrievable competes with its successor in every search.
- After any split/merge, **re-index mirrors** (embedding indexes are mirrors) — or retrieval serves the pre-refactor corpus.

## Evidence & practice

### Why nothing forces the refactor (the core asymmetry)

Code has enforcement machinery: compilers, type checkers, tests, reviews — structure debt eventually *blocks progress*. Context has none of it: an overgrown or duplicated source keeps "working" — retrieval still returns it, models still read it, answers still come out — they're just increasingly wrong, and each reader bears a small cost invisible to the author. Documentation-drift studies describe exactly this profile: drift starts small (a renamed variable not propagated, a deprecated flag still referenced) and compounds silently ([Ferndesk, documentation drift](https://ferndesk.com/blog/documentation-drift); [Document360](https://document360.com/blog/documentation-drift/)).

The measured shape of the decay:
- Staleness accumulates across **three layers**: source documents, schema drift, ownership lapse ([Atlan, LLM KB staleness](https://atlan.com/know/llm-knowledge-base-staleness/)). A corpus can be stale even when every file is "current" — because the schema or the owner moved.
- RAG-specific decay: chunks go stale independently of documents; weak metadata lets retrieval keep finding *plausible but outdated* fragments — the retriever optimizes similarity, and old text is often more similar to old-style queries ([Glukhov, LLM wiki maintenance](https://www.glukhov.org/knowledge-management/knowledge-systems-architectures/compiled-knowledge/llm-wiki-maintenance-knowledge-drift/)).
- Cost anchor: documentation issues estimated at **>$200K/year for a 50-person engineering team**; 40–60% of support tickets deflectable by docs — stale docs deflect nothing ([Devonair, doc rot](https://devonair.ai/blog/pain-points/doc-rot-silent-killer-developer-productivity)).

### Split — signals and procedure

Signals (from the summary above): two-questions-one-page, caveat walls, readers quoting different parts, chunk boundaries cutting concepts. Procedure:

1. **Name the concepts** the page actually contains (usually 2–3, discovered by listing the distinct questions it answers).
2. **Write the current-truth core** of each as its own focused page — short, no history.
3. **Convert the old page to a forward pointer** (or a stub carrying a dated supersede note pointing to the children). Never silently delete: inbound links and retrieval memory both outlive the file, and history is diagnostic evidence for poisoning hunts.
4. **Move the caveats into history**, not into the children — a dated changelog entry preserves the "why", the child pages carry only what's true now.
5. **Re-index** (below).

The wiki-note pattern motivates step 4: a note corrected and refined for weeks becomes a wall of caveats where the reader wades through the pile to find what's true *now* — the split costs one edit and repays every future read.

### Merge — signals and procedure

Two sources answering the same question slightly differently is a clash on a timer (see `one-concept-one-home.md` for the conflict evidence — ~70% of enterprise KBs already contain contradictory pairs). Procedure: pick the winner (better home, better neighbors), fold in what the loser had that the winner lacked, convert the loser to a dated forward pointer, re-index. The dangerous shortcut is "harmonize both in place" — that leaves two homes agreeing *today*.

### Restructure-on-write — who does it, and when

The trigger discipline comes from memory-systems research: **A-MEM** ([arXiv 2502.12110](https://arxiv.org/abs/2502.12110)) treats every write as a restructuring opportunity — each new note can re-link, merge, or rewrite old notes, so the structure deepens exactly where writes concentrate. Translated to corpora: *the write that notices the overgrowth executes the split*, because (a) the noticing agent has the context loaded already, and (b) scheduled audits arrive after the damage compounded. Schedule-based maintenance is the fallback, not the primary — its real jobs are the checks writes can't see: link integrity, staleness sweeps, orphan detection (see `context-governance.md` for the ownership model, and `memory-shapes.md` for the write-gate framing).

Enforcement options, weakest to strongest:
- **Convention** ("split when it feels big") — fails exactly like all convention.
- **Thresholds with teeth**: a gate/linter that flags pages past a size or caveat-count budget at write time — turns the invisible debt into a visible diff comment.
- **Docs-as-tests**: scripted procedures executed from the doc's content — procedural docs that drift start *failing*, restoring the compiler the medium lacks ([Falconer, living documentation](https://falconer.com/guides/living-documentation)).
- **Drift monitors**: CI that cross-checks docs against code/schema on change (renamed flag → doc flagged same PR).

### The re-index rule

Every split/merge/retire changes what retrieval *should* return; the embedding index is a mirror and mirrors don't refresh themselves. Post-refactor checklist: re-embed affected pages, retire the loser's vectors (stale vectors keep winning similarity contests), and if chunking changed, re-chunk — a split's whole point is often to align chunk boundaries with concept boundaries.

### By implementation type

| Implementation | Living-source pressure point |
|---|---|
| RAG KB | Chunk staleness + retirement policy; re-index on every refactor |
| Coding agent corpus (CLAUDE.md/AGENTS.md etc.) | Caveat-pile is the dominant failure — context files accrete "also note…" lines until they hinder (see `self-compiled-vs-curated.md` for the evidence) |
| Long-horizon agent memory | Memory entries age like docs; restructure-on-write (A-MEM) or a consolidation pass (sleep-time) — never append-only forever |
| Multi-agent | Shared briefs/registries drift as agents evolve; the registry is a source too — version it |
| Text-to-SQL / semantic layer | Schema drift is measurable — CI can diff layer definitions against warehouse schema; this corpus *does* have a compiler: use it |
