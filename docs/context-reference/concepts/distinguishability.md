---
description: Two entities, metrics, or pages look alike and the agent keeps choosing the wrong one. How to make the difference visible in the name and the one-line description, which is all a chooser reads.
layer: concept
deep: ../deep/distinguishability.md
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

**Go deeper** (`../deep/distinguishability.md`) when: naming tools/metrics/pages, designing MCP servers or routers, or debugging wrong-item selection.

## Related

- [Deep: the evidence behind this page](../deep/distinguishability.md) — open it on the trigger named above.
