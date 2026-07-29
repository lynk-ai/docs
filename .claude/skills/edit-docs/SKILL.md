---
name: edit-docs
description: Edit, update, or make changes to Lynk's documentation. Use this skill whenever the user asks to update docs, edit documentation, add content to docs, rewrite a doc page, fix something in the docs, or make any changes to documentation files.
---

# Edit Docs Skill

You're helping maintain Lynk's technical documentation — a standalone docs repository of Markdown files that explain how to use Lynk. The docs describe the **Semantics v2** model: a `.lynk/` repository organized **by concept**, where domains are agents, entities own everything true about themselves, and a small set of primitives share one uniform shape.

## The mental model — why the docs are built this way

Every rule in this skill derives from five principles. When a case isn't covered, derive the answer from these:

1. **Context, not content.** The reader is an AI agent mid-task, loading a few pages into a bounded window. Every token on a page taxes every answer that loads it. Pages are lean, self-contained, token-bounded; depth is lazy. The GitBook site is a projection, never the design target.
2. **The delta over the model's priors.** The consumer already knows analytics, dbt, SQL. Document only what it cannot infer: where Lynk differs, what the build enforces, the judgment seniors carry. Restating general knowledge is negative value. **Negative space is content** — what doesn't exist must be said, or the prior fills the gap with invented syntax.
3. **A navigable typed graph.** Titles + frontmatter descriptions are the routing layer (the generated router in `concepts/README.md` surfaces them); fixed page anatomy gives predictable anchors; the mesh keeps every fact one hop from any mention; four genres hold four kinds of knowledge; every sentence has exactly one home.
4. **The docs obey the physics they teach.** Concept pages ≈ entities (lazy, one home), descriptions ≈ the lazy-load index, guides ≈ skills (verb-shaped, JIT), this contract ≈ a policy, lint + evals ≈ the build. When unsure how to structure something, ask: *how would Lynk model this?*
5. **Correct is behavioral.** A doc is right when a fresh agent session, given the docs alone, answers or acts correctly. Docs quality is measured by the eval suite (`evals/ask-docs/`), not judged editorially; a doc change without a guarding eval case is unverified.

## References

Load when relevant to the task — not by default.

| Reference | File | When to load |
|---|---|---|
| GitBook custom blocks | `references/gitbook_blocks.md` | Adding/editing hints, tabs, steppers, cards, or any `{% %}` block |
| GitBook frontmatter | `references/gitbook_frontmatter.md` | Page-level settings: description, icon, hidden, layout |
| GitBook variables & expressions | `references/gitbook_variables.md` | Dynamic content |
| GitBook structure & navigation | `references/gitbook_structure.md` | Modifying SUMMARY.md, .gitbook.yaml, redirects, Git Sync |
| Canonical example companies | `references/canonical-companies.md` | Writing/editing any `## Examples` section, any guide's Patterns/Anti-patterns, or the complete-example page |

## Your mission

When the user asks you to edit or update documentation, follow these steps:

---

## Step 1: Load structure and style

Read **`docs/README.md`** (the mental model) and **`docs/SUMMARY.md`** — the authoritative list of every page. Do not rely on any inlined tree; SUMMARY.md is the single page registry, and the generated router in `docs/concepts/README.md` carries each page's one-line description.

The four content folders under `docs/`:

- `docs/concepts/` — one spec page per primitive, mirroring the `.lynk/` tree.
- `docs/reference/` — cross-cutting mechanics, documented once.
- `docs/guides/` — verb-shaped judgment and methodology pages; lazy-loaded, linked from the concepts they advise.
- `docs/api/` — query interfaces.

Writing style: an engineer talking to engineers — direct, precise, honest, no hype.

## Step 2: Understand the request

If anything is ambiguous — which page, what exactly changes, existing page vs new — ask one clarifying question before touching files.

## Step 3: Place the content (the cascade)

Classify what you're about to write, in this order:

1. **A new primitive or file type in the product?** → new `concepts/` page at the position mirroring the `.lynk/` tree.
2. **A fact about one existing primitive** (field, behavior, build rule)? → the narrowest *slice* of that primitive's page: a Format row, a Validation bullet, an Example. Never a new page.
3. **A mechanic shared by ≥2 concepts?** → the owning `reference/` page; a new one only for a genuinely new mechanic.
4. **A query-interface capability?** → `api/`.
5. **Judgment** — how to choose, size, name, write well; a pattern, anti-pattern, quality bar? → the existing `guides/` page whose job matches. A *new* guide only for a new decision class (test: verb-shaped title + at least two patterns or anti-patterns to say). One stray observation is a bullet in an existing guide.
6. **One-sentence judgment bound to a specific field?** → that field's Format Notes cell, linking to the guide.

If you're writing "it depends" or "prefer X when…", you're writing a guide. Then list all files the change touches (the home, the pages that should link instead of restate, the indexes) and why.

## Step 4: Read existing content

Read every file you plan to edit before writing anything.

## Step 5: Show a plan and get confirmation

**Minor edits** (a sentence, a value, a field): describe the change in one sentence, then proceed. **Significant changes** (rewrites, new sections, new pages, structural changes): present the proposed structure first and wait for confirmation.

## Step 6: Make the edits

Follow the templates and rules below.

## Step 7: Update the indexes

- **`SUMMARY.md`** — the sidebar matches the filesystem exactly; no orphans, no dangling entries. Guides live in the `## Guides` section. A new guide is added there **and** to the Related section of each concept it advises (every page needs in-degree ≥ 2: SUMMARY plus at least one content page).
- **`README.md`** — update the mental-model tables or navigation cards if a page was added, removed, or repurposed.
- **Run `python3 scripts/generate_router.py`** after adding, moving, retiring, or re-describing any page — the router in `concepts/README.md` is generated from frontmatter and must not go stale.
- **Retired or moved pages get a `redirects:` entry** in `.gitbook.yaml` — published URLs must not break.

## Step 8: Keep links and reference topology intact

Every cross-topic mention is a link; every link resolves; nothing restates content that has a home elsewhere. Then run the static lint: `cd evals/ask-docs && uv run pytest -m "not evaluation"`.

## Step 9: Guard the change

Per principle 5: a consequential content change should have an eval case in `evals/ask-docs/datasets/questions.yaml` that would fail without it. Add one (or flag that one is needed) for anything an agent could previously get wrong.

---

## The spec page template (`concepts/` and `reference/`)

GitBook frontmatter (`description`, `icon`) above the title. The `description` is routing-load-bearing — it appears verbatim in the router.

```
# <Topic>                ← one-line definition directly under the title
## What it is            ← three moves, ≤150 words total (see below)
## Where it lives        ← path(s) in the .lynk/ tree
## Format                ← contract only: field/grammar tables with required/optional + types
## Examples              ← two examples, labeled by what they show
## Validation            ← machine-enforced rules ONLY
## Related               ← parent · sub-concepts · reference pages · Guides: line
```

**Rules:**

- **All six sections, in this order.** No `## Contents` section — GitBook renders its own ToC, and the block is dead tokens for the agent. For **container concepts** (project, domain, entity), `## Format` is the folder-contract table — containers follow the same template; there are no exempt pages.
- **`## What it is` makes exactly three moves:** (a) role + the delta from the nearest confusable primitive; (b) *why the model shapes it this way* — 1–3 sentences of rationale; (c) use-when / don't-when one-liners, linking to the governing guide for the long form. A What-it-is that only categorizes fails review.
- **`## Format`** carries contracts. A Notes cell may hold ONE sentence of field-bound judgment ("state the scale"); anything needing a paragraph goes to a guide.
- **`## Validation` litmus: every bullet corresponds to a possible build failure.** Quality bars ("descriptions should be distinguishable") live in guides. **A rule that contradicts the reader's prior carries its why inline** — one sentence of mechanism, so the agent can generalize it.
- **Constraint prominence.** A constraint the reader must act on *while applying* the page — a precondition ("X must already exist"), a prohibition ("never X"), an irreversible behavior — opens its section or paragraph as a **bolded standalone sentence**. Never mid-paragraph, never only in a code comment or parenthetical: agents synthesizing a page compress out non-prominent preconditions (measured: a mid-paragraph "identity is never a query" was dropped from 75% of answers; the same rule bolded at the pattern's start survived).
- **`## Related`** ends with a `Guides:` line when a guide governs this concept.

## The guide template (`guides/`)

```
# <Verb-shaped title>    ← one line: the decision this guide produces
## When you need this    ← 3–5 trigger situations (mirror them in the frontmatter description)
## The principle         ← the one rule that generates the patterns; ≤100 words
## Patterns              ← ### per named pattern: situation → ONE recommended move (+ named deviation conditions; never a menu) → canonical-company example
## Anti-patterns         ← ### per named anti-pattern, as a TRIPLE: wrong form (real syntax, labeled) → why it fails (the observable mechanism) → the fix
## The bar               ← checklist of testable statements defining a good X
## Related               ← the concept pages this guide governs (bidirectional)
```

**Rules:** verb-shaped title and description ("Choosing…", "How to decide…"); a guide quotes at most **one line** of spec — anything more is a link; guides never restate field tables or mechanics; each guide is bounded by a nameable decision question and capped at ~1,200 words — split by task, never grow past it; the **constraint-prominence rule** (spec Rules above) applies to every Pattern — a precondition the reader must satisfy before the pattern works opens the pattern as a bolded sentence, never mid-paragraph or in a code comment.

## The example policy

- Spec pages are **correct-only**: two examples, one minimal + one realistic, each labeled in bold by *what it shows* (never "Minimal"/"Realistic"), structurally different from each other, using canonical-company data — no placeholders.
- **Wrong examples exist only in guides' Anti-patterns**, always inline-labeled ("wrong — double-counts"). Deprecated/legacy forms (e.g. `METRIC('name')`) appear only as explicit, labeled anti-examples.
- Every schema example obeys the build rules: keys declared as features where joined or queried, no templating, metrics take no arguments, cross-entity aggregates as features wrapping `metric()`.

### No duplication — one concept, one home

A topic is documented in one place; every other page links to it. When about to explain something, check whether it already has a home:

| Topic | Home |
|---|---|
| The `.lynk/` tree, folder & naming rules | `reference/layout-and-naming.md` |
| Frontmatter contract and `@` injection | `reference/markdown-format.md` |
| The `sql:` grammar (segment counts, functions, filter, join binding) | `reference/sql-expressions.md` |
| `lynk.yml` settings incl. `topology` | `concepts/lynk-yml.md` |
| Cross-domain reference rules | `concepts/lynk-yml.md#topology` |
| Build lifecycle, the project minimum | `concepts/project.md` |
| Capability boundaries ("Lynk doesn't do X" — by-design / planned / upstream) | `reference/what-lynk-does-not-do.md` — one line + link per boundary; the full rule stays on the owning spec page |
| The query dialect | `api/lynk-sql.md` |
| Placement judgment (what goes where) | `guides/where-knowledge-goes.md` |
| Metrics/time/state judgment | `guides/metrics-time-and-state.md` |
| Entity design judgment | `guides/designing-entities.md` |
| Domain design judgment | `guides/designing-domains.md` |
| Context budgeting (@ vs link, splitting files) | `guides/context-engineering.md` |
| Change management (renames, deprecation, changelog) | `guides/evolving-the-layer.md` |
| The complete worked example | `guides/complete-example.md` |

For anything not in this table, the router (`docs/concepts/README.md`) lists every page with its one-line description.

### Linking rules

- First mention of another concept links to it; parents link down, sub-concepts link up in their opening line.
- Domain-scope pages (`domain/lynk-md.md`, `domain/glossary.md`) defer the shared definition to the root concept page and state only scope behavior.
- Concept pages link to every reference page they rely on; guides link to every concept page they govern.

---

## Constraints

- Only edit documentation files in `docs/concepts/`, `docs/reference/`, `docs/guides/`, `docs/api/`, `docs/README.md`, and `docs/SUMMARY.md`. Do not edit `.claude/`, `docs/.claude/`, `docs/CLAUDE.md`, or tooling files unless the user explicitly asks.
- Always read before writing.
- Keep `README.md`, `SUMMARY.md`, and the generated router in sync with the filesystem.
- If you find yourself writing "leverage", "revolutionary", or "game-changing", stop and rewrite.
- **Never use customer names in examples.** Use `maindb`, `public`, generic table names, and the canonical companies (Grove / Bly / Arcadia). Before saving, scan additions for proper nouns that look like a real organization.

## Writing style

- Short sentences, active voice, specific over vague. One idea per paragraph.
- Tables and bullet lists for reference content; prose for explanations.
- Apply the Terminology Rules below.

## Terminology Rules

Apply these to every edit.

**The model.** A Lynk project is a `.lynk/` git repository, consumed as versioned, validated **builds**. Agents reason against a deployed build of a branch, scoped to one domain. Never describe live-edit querying.

**Domains are agents.** Each domain is one team's analytical agent; a user talks to one at a time. The domain is derived **from the path** — no `domain:` field exists. Cross-domain references are governed by `topology` (medallion only), declared in `lynk.yml`.

**Entities own what's true about them.** Facts go on entities (`ENTITY.md` prose + `schema.yml` structure); *ways of reasoning* in skills; *vocabulary* in the glossary; *behavior* in policies. An entity's `identity` roots it in a physical table or another entity; extension imports explicit definitions.

**Features and metrics are uniform.** A feature has `name`, `description`, `sql`, `data_type`, optional `join_name`, optional `filter`. A metric is the same minus `join_name`, entity-local, and takes no arguments. There are no feature *types*. Cross-entity aggregates are features whose `sql` wraps `metric(entity.metric_name)`. **Keys are not features** — declare a feature for any joined or queried key column.

**Lazy vs. eager loading.** Orientation, vocabulary, and policies always load. Entities and skills are lazy, indexed by `description`. Describe *when* content loads, not *who* reads it.

**Query syntax.** Lynk SQL: entities as tables, features as columns, `metric(entity.metric_name)` (alias-aware), `USING('join_name')`. Queries are single-domain. `first()`/`last()` are authoring-only. The old `METRIC('name')` form appears only as a labeled anti-example.
