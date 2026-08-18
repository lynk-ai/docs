---
description: The same fact is stated in two places and you need to know why that is a defect rather than helpful redundancy. Two copies eventually disagree, and the agent picks one without telling anyone.
icon: house
---

# One concept, one home

**Claim** — every definition, rule, or fact an agent may rely on lives in exactly **one** authoritative place; everything else points at it. Duplication is not a style issue: two copies of one fact are two sources of truth waiting to disagree, and when they do, the model silently picks one (clash — the failure mode with no mechanical fix).

**Why it matters** — ~70% of enterprise knowledge bases contain at least one pair of directly contradictory articles (Gartner estimate); teams add ~40 docs/month and retire almost none. On real contradictions, models usually answer fluently from one source *without flagging* that a competing claim existed (WikiContradict, NeurIPS 2024). A duplicated fact fails invisibly: no diff, no error, just a confidently wrong answer for whoever retrieved the stale copy.

**The placement test** — *would two readers legitimately disagree about this?*
- **No** (ground truth: a definition, a decided rule) → one shared home, everything else points.
- **Yes** (working opinion, unreviewed draft) → stays private until it earns promotion through review.

**Rules** —
- Pointers, not copies. A copy forks; a pointer survives the original's edits. Collections (shelves, reading lists, indexes) are lists of pointers, never bodies.
- When a mirror must exist (cache, export, sync), **name the winner explicitly** — a mirror is a pointer with a refresh problem.
- The rule governs **homes, not mentions**: restating a one-line *derived* summary near the point of use (with the home linked) is legal and often position-optimal. The test: could the restatement drift into disagreeing with the home? A summary-plus-link can't survive alone; a full copy can — that's the line.
- **Findability redundancy is not truth redundancy.** Duplicate the *surfaces* (keywords, aliases, index entries — many paths in) freely; never duplicate the *fact* (one body at the end of every path). This resolves the apparent conflict with retrieval practice, which rewards redundancy: redundancy of routes helps recall; redundancy of homes creates clash.

## Evidence & practice

### Why clash is the failure this rule targets

The knowledge-conflicts literature gives the rule its teeth. The [survey (arXiv 2403.08319, EMNLP 2024)](https://arxiv.org/abs/2403.08319) distinguishes **inter-context conflict** — two retrieved sources disagree — as the class caused directly by duplicated homes. Findings that matter:

- **Silent resolution is the default.** On [WikiContradict (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/c63819755591ea972f8570beffca6b1b-Paper-Datasets_and_Benchmarks_Track.pdf) — real Wikipedia contradictions — models typically answer from one source with no acknowledgment a competing claim was present. You don't get an error; you get confidence.
- **Which copy wins is arbitrary from the caller's view**: recency in context, position, phrasing similarity to the query — none of which track truth.
- **Scale**: ~70% of enterprise KBs hold at least one directly contradictory article pair; ~40 docs/month added, old ones rarely retired (Gartner-attributed estimate, secondary source — order-of-magnitude, not audited: [Fini Labs](https://www.usefini.com/guides/ai-knowledge-base-conflicting-answers)). Duplication is the *normal state* of an ungoverned corpus, not an edge case.
- Detection pipelines exist — [ConflictRAG](https://arxiv.org/pdf/2605.17301) (detect → classify → resolve → generate), reasoning-model claim comparison across articles — but they are the expensive, lossy fallback. Structural prevention inside your own corpus is strictly cheaper: a fact that exists once *cannot* inter-context-clash with itself.

### The placement test, operationalized

*Would two readers legitimately disagree about this?*

| Signal | Shared home | Stays private |
|---|---|---|
| Nature | Ground truth: definition, decided rule, measured fact | Working opinion, hypothesis, draft reasoning |
| Review state | Promoted (reviewed/merged) | Not yet reviewed |
| Downstream trust | Others may rely on it blindly | Only its author should act on it |
| On conflict | A bug — escalate | Expected — it's an opinion |

Promotion is the only door between the columns (see `self-compiled-vs-curated.md`). An unreviewed claim placed in the shared layer is poisoning-in-waiting regardless of how confident it sounds.

### The home you don't control: the model's own weights

The conflicts survey names three types; everything above is **inter-context** (two retrieved sources disagree). The one builders forget is **context–memory conflict**: your supplied fact contradicts what the model absorbed in training. That makes the weights *a competing home for every fact you provide* — one you cannot edit, cannot date-stamp, and cannot delete.

Consequences that change authoring:

- **Stating a fact is not the same as installing it.** When your context contradicts a strongly-held parametric belief, the model may follow either. Contested facts need *explicit override framing* — "as of 2026-07 this API returns X; older documentation saying Y is superseded" — not a bare assertion.
- **The riskiest facts are the plausibly-outdated ones**: renamed APIs, changed defaults, reversed policies, anything the model saw a hundred times in an older form. A quiet correction loses to a loud memory.
- **Novel facts are safe; corrections are not.** Content with no parametric competitor (your internal conventions, your schema) lands cleanly. That's a second argument for admitting only non-inferable content (`authoring-standing-surfaces.md`, rule 2) — non-inferable content is precisely the content with no rival home in the weights.
- **Symptom to watch**: the model answers correctly when the fact is quoted directly in the question, but reverts to the older version in longer sessions — the supplied fact ages into the attention dead zone (`position-and-ordering.md`) and the weights take over. Re-anchor rather than restate once.

### Freshness: time as a source of forked homes

`living-sources.md` covers structural drift (split/merge). The temporal case belongs here because it is a one-home failure: **the same fact at two times is two homes unless one is marked superseded.** Practices that keep it single:

- **Date-stamp anything volatile** ("verified 2026-07-08"), and prefer relative-free absolutes — "as of <date>", never "recently" or "currently".
- **Supersede visibly rather than delete**: the old statement stays with a dated note pointing forward, so a reader who retrieved the old version can tell. Deleting it leaves stale copies in caches, indexes, and screenshots with nothing to contradict them.
- **Keep volatile facts out of always-loaded surfaces** — a timestamp in a standing file guarantees rot *and* breaks caching (`caching-economics.md`).
- **Give freshness an owner**: staleness age percentiles are a governance instrument (`context-governance.md`), not a hope.

### The redundancy tension, resolved honestly

Retrieval practice *rewards* redundancy — a fact stated in two places gets found by two query phrasings. Naive one-home dogma would hurt recall. The resolution is to split what gets duplicated:

- **Routes: duplicate freely.** Keywords, aliases, synonyms, index rows, cross-references, redirects — many paths, all terminating at the same body. Pure findability; can't drift into contradiction because routes carry no claims.
- **Derived restatements: allowed with a tether.** A one-line summary at point-of-use, linked to the home ("per <home>: X"). Position-optimal (edge placement near the question — see `position-and-ordering.md`) and safe *because* it's visibly subordinate: when it drifts, the link exposes the drift.
- **Homes: never duplicate.** A second full statement of the fact, able to stand alone, is a fork. It will be edited independently eventually — the clash is built in the day the copy is made, it just hasn't fired yet.

Rule of thumb: **duplicate surfaces, tether summaries, never fork bodies.**

### Mirrors, caches, and exports

Real systems need copies: a wiki export, a Notion sync of a repo doc, a vector index over the corpus, a downstream cache. Each is legal under one condition: **the winner is named**. Declare which artifact is authoritative, treat all others as regenerable views, and version the regeneration (a stamped "mirrored from X at T" beats an unstamped copy). A mirror without a named winner is just a slow fork. Corollary for RAG: your **embedding index is a mirror** — re-index on write or stamp staleness, or the retriever keeps serving the corpus's past (see `living-sources.md` on chunk staleness).

### Failure patterns seen in practice

- **The three-doc definition**: "customer" defined in three places; a pricing change updates two. Every reader of the third is now confidently wrong, and no diff will flag it — diffs compare versions of one file, not agreement across files.
- **Copy-paste onboarding docs**: team A copies team B's setup guide; six months later the guides prescribe incompatible steps and retrieval serves them interleaved.
- **Agent memory duplicating the KB**: an agent stores a summary of a policy in its own memory; the policy changes; the memory doesn't. Memory entries that restate governed facts should store *pointers* (fetch-on-recall), reserving stored prose for what has no home elsewhere.
- **The un-retired predecessor**: the new doc ships, the old one stays retrievable. Supersede visibly (dated note on the old, pointing forward) or the retriever will keep choosing by similarity, which the old doc often wins.

### By implementation type

| Implementation | One-home discipline |
|---|---|
| RAG KB | Dedup at ingest; retirement policy as strong as authoring policy; conflict detection only for uncontrolled/external sources |
| Coding agent | Constants/config: one source file; docs point at code (or are generated from it), never restate values |
| Long-horizon agent | Working memory = private column; promotion to shared notes is an explicit, reviewed step |
| Multi-agent | One decision-owner per question; workers receive pointers to shared truth, not pasted copies that snapshot-drift mid-run |
| Text-to-SQL / semantic layer | Each metric/entity defined once in the layer; dashboards and prompts reference by name — a metric redefined in a prompt is a fork with SQL consequences |
