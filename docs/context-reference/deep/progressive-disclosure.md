---
description: The evidence behind progressive disclosure — the three stages, the economics per part, and where the pattern breaks.
layer: deep
concept: ../concepts/progressive-disclosure.md
---

# Progressive disclosure — evidence & practice

## The economics, precisely

Let a corpus have N items, average body size D tokens, pointer size p tokens (~20), and per-request usage fraction f per item.

- **Standing (everything always loaded)**: every request pays N·D — and pays it in *attention*, not just dollars, pushing the whole window toward the rot regime. Grows linearly with corpus size: the corpus's growth is the system's decay.
- **Progressive**: every request pays N·p (the index) + f·D per item actually used. The index grows with N but at pointer weight (20 tokens/item ⇒ a 500-item corpus indexes in ~10K tokens); bodies are pay-per-use.

The crossover is early and brutal: with D≈1,500 and p≈20, standing costs 75× the index weight per item. Caching softens the *dollar* gap for stable standing content (~10% price — `caching-economics.md`) but never the attention gap — a cached token still dilutes and still buries the middle (`context-rot.md`). Hence the asymmetric rule: **price can occasionally justify standing residence; attention almost never does.**

Empirical anchor for the "standing content hurts" half: the ETH Zurich AGENTS.md evaluation — always-loaded context files tend to reduce coding-agent task success while inflating inference cost >20%; the surviving content is the non-inferable minimum. (McMillan's factorial study, [arXiv 2605.10039](https://arxiv.org/pdf/2605.10039), adds the structural nulls: within 25–500 lines, size and layout of the standing file don't detectably matter — *what* is admitted does.) And the confusion failure mode generally: superfluous present content degrades output even when correct (`four-failure-modes.md`).

## Convergent evolution (the shape keeps getting reinvented)

The same three-stage architecture appears wherever context meets scale, independently:

- **Agent skills** (Anthropic skills / MCP prompts): name+description always visible; instruction body loads on invocation. Anthropic's context-engineering guidance names the general strategy "just-in-time" context — lightweight identifiers standing, runtime fetches for bodies, hybrid (pre-load the hot core, explore for the rest) when latency demands.
- **Tool surfaces**: schema summaries in the loadout, full docs fetched on demand; deferred-tool patterns load schemas via search only when needed — SELECT applied to capabilities.
- **RAG itself** is the pattern at corpus scale: the index (embeddings/metadata) is the standing layer; chunks load per query.
- **Memory paging** (MemGPT lineage): core memory standing, archival storage behind retrieval ([arXiv 2310.08560](https://arxiv.org/abs/2310.08560)).
- **Documentation systems**: llms.txt, API TOCs, man-page synopses — pointer layers for machine readers.
- **The file shape itself converged too**: OKF (Google Cloud/BigQuery — markdown + YAML frontmatter, one concept per file, `index.md` as the disclosure layer), Anthropic's SKILL.md, Cursor's `.mdc` rules, CLAUDE.md/AGENTS.md, Letta's MemFS (markdown in git) — five owners, one container: *small markdown files + frontmatter + progressive disclosure*. Convergence under independent selection is evidence the shape is load-bearing, not fashion.

When this many independent lineages converge on index-always/body-on-demand, treat it as the shape the problem imposes, not a style preference. The layering stack that emerges (which surface carries which knowledge): **llms.txt** (web discovery) → **AGENTS.md/.mdc** (behavioral instructions) → **SKILL.md** (procedures) → **OKF-style knowledge files** (domain knowledge) → **MCP** (actions). Putting content on the wrong layer — procedures in a config file, domain knowledge in a system prompt — is a placement bug this stack makes visible (see `authoring-standing-surfaces.md`).

## The three stages, precisely (and why there is no fourth)

Community shorthand labels the stages L1/L2/L3 (Anthropic's Agent Skills codified them: metadata / instructions / resources). The clean derivation: a stage is defined by *when* content enters context, and there are only three such moments — **always** (discovery), **on match** (activation), **on touch** (execution). What looks like an L4 is execution *recursing* — a reference pointing at another reference is the third ring applied again, not a new ring. Corollary: any corpus with an index, bodies, and linked detail runs these same three stages, whatever the substrate.

**Inside stage 3 there are two cost shapes, not one** — the split most treatments miss:

| | **Read** | **Execute** |
|---|---|---|
| What enters context | The full text of the reference | Nothing — code runs in a shell |
| What's paid | Every token of the document | Only the printed output |
| Prefer when | The model must **reason over** the material (semantics, policy, a schema it interprets) | The work is **deterministic** and only the result matters (fetch, transform, validate) |

A 400-line script costs ~zero tokens to run and a handful to report; the same 400 lines *read* cost their full length whether or not all of it was needed. **The cheapest disclosure is content that never enters the window at all** — this is why the skills layout splits `references/` (read) from `scripts/` (execute), and why "wrap it in a script" is a context decision, not just an engineering one.

## Design of each stage

**Stage 1 — the pointer.** Three fields: *name* (addressable, qualified — `distinguishability.md`), *one-line description* (the routing promise: exactly what the body delivers, contrastive with siblings), *load-when trigger* (task-shaped: "when debugging wrong-item selection", not "about naming"). The trigger is the innovation most systems skip — choosers route on situations, and a topic label makes them infer the situation mapping themselves.

The discovery layer has a **hard budget with a cliff, not a slope**. Delivery channels truncate — a session-start hook's output may surface only ~2KB of preview; long tool/skill listings age into the attention dead-zone — and an over-budget index doesn't degrade gracefully: **its tail is silently never read**, so every item past the cutoff ceases to exist for the agent, with no error anywhere. Production instance: CandleKeep's session "sticky note" caps at ≤2KB of IDs and counts (never contents) precisely because the host inlines only that much. Budget the pointer layer like an SLA: a truncated index is an index whose tail was deleted for every reader.

**Stage 2 — the card.** The decision-ready middle: claims, rules, key numbers, and *when to go deeper*. Bar: a competent reader should act correctly on routine cases from the card alone. This stage is what makes disclosure "progressive" rather than binary — without it, every non-trivial route pays full body cost.

**Stage 3 — the body.** Evidence, procedures, numbers with sources, edge cases. Free to be long: it's paid for only when consulted. Discipline it with living-source rules (split when it blurs — `living-sources.md`), not length anxiety.

**Contract between stages**: each layer must honestly summarize the one below (a card that oversells its body mis-routes exactly like a bad description); and deeper layers never contradict shallower ones — the card is a *derived restatement* of the body, tethered, per `one-concept-one-home.md`.

> **Deciding whether a specific file should be split at all** — including how to detect that you've split *too far* — is `when-to-split.md`. This page argues the pattern; that one runs the test.

## Growing the structure: sideways or deeper

When a body outgrows itself, there are two moves, and a clean tell for choosing:

| Move | When | What it looks like |
|---|---|---|
| **Split sideways** | Still *one concept* — just too long, or buried under caveats | Sibling pages at the same level; the short current page keeps the name, specifics move to siblings |
| **Deepen a level** | A sub-part has become *several concepts readers cite independently* | The sub-part earns its own index — a new discovery layer; the old page shrinks to a forward pointer |

**The tell for deepening: you find yourself wanting an index for the sub-part.** An index is a discovery layer, and you only need one when there are several things to disclose. The two error modes are symmetric: deepening a single concept creates an index over one page (pure overhead); flattening a genuine cluster creates a pile of siblings with no index (an un-navigable shelf). Size alone never justifies deepening — only *independently-cited plurality* does.

## Failure modes of the pattern itself

- **Index bloat**: pointers accrete descriptions-turned-paragraphs until the "small" layer is a standing document. Budget the pointer (≤2 lines) as strictly as bodies — and remember the cliff above: past the budget, the tail isn't "less read", it's *never* read.
- **Unroutable depth**: bodies exist but triggers/keywords don't match how askers phrase tasks — lazy loading degrades to never loading. Route-test the pointer layer (`distinguishability.md`); add synonym surfaces (`selection-quality.md`).
- **Excerpt drift**: the index quotes bodies "for convenience"; quotes go stale; the index now contradicts its own content. Pointers describe, never excerpt.
- **Hidden standing costs**: “temporarily” pinned bodies that never unpin. Run the ablation test (`measuring-context.md`) on everything standing, quarterly.
- **Habit, not contract — the deepest failure**: an agent that politely reads one page at a time is running a *habit*; nothing stops it from reading the whole folder, and the moment it does, the economics collapse. The pattern is only trustworthy when something *enforces* the stages (briefs that forbid whole-corpus reads, tools that serve excerpts not files, a check that rejects changes which touch a body but not its index entry — a stale index makes routing silently unsafe). Polite routing ≠ safe routing.

## By implementation type

| Implementation | Standing layer | On-demand layer |
|---|---|---|
| RAG KB | Index/metadata only | Chunks per query (plus rerank+prune before admission) |
| Coding agent | Non-inferable project facts (short) | Files read per task; docs fetched per need |
| Long-horizon agent | ≤2KB session note of pointers | Own notes/archive re-SELECTed by pointer |
| Multi-agent | Roster of names+descriptions | Lens/brief bodies loaded when a worker is seated |
| Text-to-SQL | Entity/metric catalog (names + one-liners) | Full definitions + schema for routed entities only |
