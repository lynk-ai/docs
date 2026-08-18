---
description: Two entities, metrics, or pages look alike and the agent keeps choosing the wrong one. How to make the difference visible in the name and the one-line description, which is all a chooser reads.
icon: clone
---

# Distinguishability

**Claim** — when a chooser (human, agent, router, text-to-SQL model) must pick between two legitimately-distinct items, the difference must be visible in **both the name and the one-line description** — because name + description is *all a chooser reads before committing*. Two items that share a name or carry near-identical descriptions force a coin-flip, and everything built on the wrong pick is silently wrong.

**Why it matters** — this is the dominant failure of tool/metric/page selection at scale: LLM tool-selection accuracy reported as low as **13% on large tool sets**; ambiguous names measurably increase wrong-tool invocation; identical tool names across MCP servers cause cross-server misrouting. The failure is silent — the wrong metric still returns numbers, the wrong tool still runs.

**The complement of one-concept-one-home** — one-home kills *illegitimate* pairs (duplicates: merge them); distinguishability separates *legitimate* pairs (genuinely distinct things: make the difference visible). First ask "are these actually one concept?" — if yes, merge (one-home). Only if no, disambiguate (this rule).

**Rules — the difference goes in BOTH surfaces** —
- **Name**: qualify with the discriminating dimension — `player_total_points` / `team_total_points`, `search_issues` / `search_docs`. A shared name can't even be *addressed* unambiguously.
- **Description**: state the discriminating fact explicitly — "…scored by the player…" vs "…by the team…". A chooser that reads name-then-description stops at the first surface that resolves; ambiguity in either surface can strand it.
- Fixing only one surface fails: name-only leaves description-trusting choosers guessing; description-only leaves a name collision tools may not even be able to reference.
- Write descriptions *contrastively* when siblings exist: say what this one does **and is not** ("returns per-player totals; for team totals use `team_total_points`").
- Test: show a fresh model only the names + descriptions and ten realistic asks — if it can't route 10/10, the surfaces are the bug.

## Evidence & practice

### The choosing model

Every selection surface in an LLM system — tool pickers, routers, retrieval over metadata, text-to-SQL metric resolution, skill triggers — runs the same protocol: the chooser reads **name**, then **one-line description**, then commits. Bodies are read *after* the choice, if ever. Two consequences:

1. The name+description pair is the complete interface. Information that lives only in the body does not exist at choice time.
2. A chooser stops at the first surface that appears to resolve the question. If the name looks decisive but is ambiguous, the description never gets consulted — which is why the difference must live in **both** surfaces.

### Evidence

- **Tool-set scale collapse, and overlap named as the cause**: RAG-MCP (Gan & Sun, via Breunig, primary-verified chain): DeepSeek-v3 tool selection degrades sharply past **30 tools** — *"overlapping descriptions"* cited as the mechanism — and past **100 tools** failure is "virtually guaranteed"; a quantized Llama 3.1 8B failed at 46 tools and succeeded at 19 (GeoEngine, both within a 16K window — breadth, not length). Secondary reports put selection accuracy as low as **13%** on large sets ([over-tooled agent problem](https://tianpan.co/blog/2026-04-19-over-tooled-agent-problem)). Indistinguishability compounds volume: the failure isn't "too many tools", it's too many *insufficiently different* tools.
- **Descriptions beat model choice**: practitioner guidance from MCP tooling teams: optimizing tool names/descriptions moves selection quality more than upgrading the underlying model ([Speakeasy, MCP tool design](https://www.speakeasy.com/mcp/tool-design/); [Arcade, tool definitions guide](https://www.arcade.dev/blog/mcp-tool-definitions-guide/)).
- **Name collisions misroute**: multiple MCP servers can expose identically-named tools; hosts may invoke the unintended server's tool ([MCP ecosystem security analysis, arXiv 2510.16558](https://arxiv.org/pdf/2510.16558)).
- **Descriptions drift from behavior**: description–code inconsistency is common enough in real MCP servers to have its own measurement literature ([arXiv 2606.04769](https://arxiv.org/pdf/2606.04769)) — a description that no longer matches behavior is indistinguishability's evil twin: distinct surfaces, wrong contents.

### A worked failure (real, semantic-layer)

Two entities, `player_game` and `team_game`, each defined a metric named `total_points` with the **identical** description "Total points scored across all games." A text-to-SQL model selecting by name+description had literally zero discriminating bits: queries grabbed player totals where team totals were meant, returned plausible numbers, and nothing flagged the error. The fix touched both surfaces: names → `player_total_points` / `team_total_points`; descriptions → "…scored by the player…" / "…by the team…". Either fix alone leaves one class of chooser guessing.

This generalizes to every pair the model must choose between: two skills with overlapping trigger descriptions, two KB pages titled "Setup guide", two API endpoints `get_user` (by id) and `get_user` (by email).

### Authoring procedure

1. **Merge test first** (one-home): are the two items actually one concept? If users would never need both, merge — don't disambiguate a duplicate.
2. **Find the discriminating dimension** — the single fact that decides between them (actor: player/team; corpus: issues/docs; direction: read/write).
3. **Put the dimension in the name** as a qualifier. Verb+object for tools (`create_meeting`, not `schedule`); entity-qualified for metrics.
4. **Put the dimension in the description, contrastively.** State what it is *and* which sibling it is not: "Per-player totals. For team-level totals use `team_total_points`." Cross-referencing siblings turns the coin-flip into a routed decision.
5. **Adversarial route-test**: give a fresh model only the surfaces + 10 realistic asks spanning both items; require 10/10. This is cheap, automatable, and catches what authors can't see (they know the difference; the surface must carry it).
6. **Re-test on every new sibling.** Distinguishability is pairwise: each addition can retroactively ambiguate items that were fine alone — per-item review never catches it.

### Boundary cases

- **More than two siblings**: the discriminating dimension must be *consistent* across the family (all metrics qualified by entity, not one by entity and one by time-grain) or the chooser must learn per-pair rules.
- **Hierarchies**: prefer fewer, parameterized items over sibling explosions — `search(corpus=issues|docs)` beats `search_issues`/`search_docs`/`search_wiki`/… once the family passes ~3–4; this also fights tool-count collapse.
- **When surfaces can't be fixed** (third-party tools): wrap or alias — a thin proxy with your own name/description is cheaper than a standing misroute rate.

### By implementation type

| Implementation | Chooser | Surface to fix |
|---|---|---|
| Tool-using agent / MCP | Model picking a tool | Tool name + description; keep loadout <30 (`selection-quality.md`) |
| RAG / library | Router picking pages from metadata | Title + one-line description; route-test per new page |
| Multi-agent | Orchestrator picking a sub-agent | Agent descriptions must partition the task space, contrastively |
| Text-to-SQL | Model resolving NL → metric/entity | Qualified metric names + discriminating descriptions in the layer |
| Skills/plugins | Trigger matching | Trigger phrases must not overlap a sibling's; adversarial-test the set |
