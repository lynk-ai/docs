---
name: edit-docs
description: Edit, update, or make changes to Lynk's documentation. Use this skill whenever the user asks to update docs, edit documentation, add content to docs, rewrite a doc page, fix something in the docs, or make any changes to documentation files.
---

# Edit Docs Skill

You're helping maintain Lynk's technical documentation — a standalone docs repository of Markdown files that explain how to use Lynk to data engineers and technical users.

The docs describe the **Semantics v2** model: a `.lynk/` repository organized **by concept**, where domains are agents, entities own everything true about themselves, and a small set of primitives share one uniform shape.

## References

These reference files are available to you, load them when relevant to the task — do not load all of them by default.

| Reference | File | When to load |
|---|---|---|
| GitBook custom blocks | `references/gitbook_blocks.md` | When adding or editing GitBook-specific components: hints, tabs, steppers, expandable sections, columns, cards, embeds, buttons, or any `{% %}` block syntax |
| GitBook frontmatter | `references/gitbook_frontmatter.md` | When configuring page-level settings: description, icon, hidden, layout width, sidebar visibility, or page-level variables |
| GitBook variables & expressions | `references/gitbook_variables.md` | When working with dynamic content — space or page variables, or `<code class="expression">` inline expressions |
| GitBook structure & navigation | `references/gitbook_structure.md` | When modifying SUMMARY.md, .gitbook.yaml, understanding file organization, or working with Git Sync |
| Canonical example companies | `references/canonical-companies.md` | When writing or editing the `## Examples` section of any page — contains exact entity names, feature names, metrics, and glossary terms for Grove (B2B SaaS), Bly (E-commerce), and Arcadia (Mobile gaming), expressed in v2 schema form |

## Your mission

When the user asks you to edit or update documentation, follow these steps:

---

## Step 1: Load structure and style

Before anything else, read these files:

1. **`README.md`** (repo root) — The landing page and mental model. It lays out the six concept drawers and the `.lynk/` tree, and links to every page.
2. **`SUMMARY.md`** (repo root) — The GitBook sidebar; the authoritative list of every page and where it sits.
3. Load additional references from the References table above only when relevant to the task.

This is a standalone docs repository. Documentation lives at the root level in three folders:

- `concepts/` — one page per primitive, organized as a concept map: `project`, `lynk-yml`, `lynk-md`, `glossary`, `domain/` (+ its scope pages), `entity/` (→ `entity-md` + `schema-yml/` → identity-and-imports / feature / metric / relationships), `policy`, `skill`, `docs-folder`.
- `reference/` — cross-cutting building blocks, written once and linked from every concept that uses them: `layout-and-naming`, `markdown-format`, `sql-expressions`.
- `api/` — query interfaces: `lynk-sql` (the query dialect) and `rest-api`.

Writing style: write like an engineer talking to engineers — direct, precise, honest, no hype. No buzzwords, no vague claims, no marketing language.

## Step 2: Understand the request

If the request is clear, proceed. If anything is ambiguous — which page is affected, what exactly should change, whether new content belongs on an existing page or a new one — ask before touching files. One clarifying question is better than making the wrong edit.

## Step 3: Identify affected files

Docs changes often ripple. Think about:

- The primary page where the change belongs — and whether that's the topic's **single home** (see the no-duplication rule below).
- Pages that reference the changed concept and should link to it rather than restate it.
- Whether the change touches `README.md` or `SUMMARY.md` (new page, renamed page, moved page).

List all the files you plan to touch and explain why each one is affected.

## Step 4: Read existing content

Read every file you plan to edit before writing anything. Don't overwrite blindly — understand the structure and how your change fits.

## Step 5: Show a plan and get confirmation

**For minor edits** (one sentence, a value, a single field): describe what you'll change in one sentence, then proceed.

**For significant changes** (rewrites, new sections, new pages, structural changes): present the proposed structure first and wait for confirmation before writing.

## Step 6: Make the edits

Write the changes. Follow the page template and the style guide below.

## Step 7: Update README.md and SUMMARY.md

After every change, keep the two indexes accurate:

- **`README.md`** — update the mental-model tables, the `.lynk/` tree, or the navigation cards if a page was added, removed, or repurposed.
- **`SUMMARY.md`** — add, move, or remove the page entry so the GitBook sidebar matches the filesystem exactly. No orphans, no dangling entries.

## Step 8: Keep links and the topology of references intact

After editing, confirm:

- Every cross-topic mention is a link, and every link resolves (path and anchor).
- The change didn't duplicate content that already has a home elsewhere (see the no-duplication rule).

## Step 9: Suggest skill updates if the folder structure changed

If this edit added or removed a top-level documentation folder (beyond `concepts/`, `reference/`, `api/`), suggest — but do not make — an update to this skill so future edits to the new folder stay consistent. Do not edit the skill file yourself; only flag the need.

---

## The page template

Every page in `concepts/` and `reference/` follows the same seven-section template. GitBook page frontmatter (`description`, `icon`) sits above the title.

```
# <Topic>                ← one-line definition directly under the title
## Contents              ← numbered table of contents
## What it is            ← role in the mental model; when to use it (and when not)
## Where it lives        ← path(s) in the .lynk/ tree
## Format                ← fields / frontmatter / grammar — tables with required/optional + types
## Examples              ← one minimal example, then one realistic; label each with its own name
## Validation            ← what the build enforces (the rules a failed build cites)
## Related               ← parent · sub-concepts · reference pages used
```

**Rules:**

- **All seven sections, in this order.** Omit one only when it is genuinely N/A — e.g. a page describing a container rather than a file may have no single `## Format` (the `domain/` page is the standing example; it uses concept-specific sections instead).
- **One-line definition** directly under the H1, before `## Contents`.
- **`## Examples`** carries two examples — a minimal one and a realistic one. Label each with a short bold name describing *what it shows* (e.g. **A single term.**, **Marketing extends `core.customer`.**), not with the words "Minimal"/"Realistic". Use realistic data from the canonical companies — no `{placeholder}` values.
- **`## Validation`** doubles as the user-facing index of build errors for that topic.

### Linking rules

- The **first mention** of another concept or reference page on a page links to it.
- A concept page links **down** to each sub-concept; a sub-concept links **up** to its parent in its opening line.
- A **domain-scope page** (`domain/lynk-md.md`, `domain/glossary.md`) references its root concept (`concepts/lynk-md.md`, `concepts/glossary.md`) for the shared definition, and states only the scope behavior (appended / merged, domain wins).
- Concept pages link to every reference page they rely on (e.g. `feature.md` → `sql-expressions.md`; `entity-md.md` → `markdown-format.md`).

### No duplication — one concept, one home

This is the load-bearing rule, mirroring the product's "one concept, one home." A topic is documented **in one place**; every other page links to it instead of restating it. When you're about to explain something, ask whether it already has a home:

| Topic | Home |
|---|---|
| The `.lynk/` tree, folder & naming rules | `reference/layout-and-naming.md` |
| Frontmatter contract (`name`/`description`/`enabled`) and `@` injection | `reference/markdown-format.md` |
| The `sql:` grammar (segment counts, `metric()`/`first()`/`last()`, filter, join binding) | `reference/sql-expressions.md` |
| `lynk.yml` settings, incl. the `topology` setting | `concepts/lynk-yml.md` |
| Cross-domain reference *rules* (the behavior) | `concepts/lynk-yml.md#topology`, referenced from `domain/README.md` |
| Build lifecycle, the project minimum | `concepts/project.md` |
| The query dialect | `api/lynk-sql.md` |

If a page is starting to explain an off-topic concept at length, trim it to a sentence and link to the home.

---

## Sections of the docs

### Concepts (`concepts/`)

**Purpose:** One page per primitive, each able to stand on its own. Pages follow the seven-section template. The folder mirrors the `.lynk/` root: root concepts at the top level, sub-concepts nested (`domain/`, `entity/`, `entity/schema-yml/`).

**Editing:** Keep each page to its own concept; push shared mechanics to a `reference/` page and link. When adding a page, place it to match the concept map and add it to `README.md` and `SUMMARY.md`.

### Reference (`reference/`)

**Purpose:** Cross-cutting capabilities used by many concepts, documented once. Pages follow the seven-section template, though `## Where it lives` may be N/A for a pure-grammar page.

**Editing:** A reference page is the single home for its mechanic. If you find the same rule on a concept page, move it here and leave a link behind.

### API Reference (`api/`)

**Purpose:** The interfaces for querying Lynk. `lynk-sql.md` is the query dialect; `rest-api.md` covers HTTP endpoints.

**Page structure (not the seven-section template):**
- `# H1` title — the interface name
- 2–3 sentence intro: what it is, who uses it, when
- Named `##` sections per capability or syntax element, each with a short explanation, a realistic code example, and a reference table where useful
- A `## Related reference` section linking to the concept and reference pages with deeper context

**Tone:** Reference-first. Assume the reader knows what they want and needs the exact syntax.

---

## Constraints

- Only edit documentation files in the topic folders (`concepts/`, `reference/`, `api/`), `README.md`, and `SUMMARY.md`. Do not edit `.claude/` or tooling files unless the user explicitly asks.
- Always read before writing.
- Always keep `README.md` and `SUMMARY.md` in sync with the filesystem.
- If you find yourself writing "leverage", "revolutionary", or "game-changing", stop and rewrite.
- **Never use customer names in examples.** Database, schema, table, column, entity, and field names in code or prose must be generic. Use `maindb`, `public`, `orders`, `customers` and the canonical example companies (Grove / Bly / Arcadia) — never a real Lynk customer's tenant, schema, or product terminology. Before saving, scan your additions for proper-noun strings that look like a real organization and replace them with generic equivalents.

---

## Writing style

- Short sentences, active voice, specific over vague.
- One idea per paragraph, whitespace between sections.
- Technical but not academic — explain how things work, not just that they work.
- Tables and bullet lists for reference content; prose for explanations.
- Apply the Terminology Rules below.

## Terminology Rules

Apply these to every edit.

**The model.** A Lynk project is a `.lynk/` git repository, consumed as versioned, validated **builds**. Agents reason against a deployed build of a branch, scoped to one domain. Never describe live-edit querying.

**Domains are agents.** Each domain is one team's analytical agent. A user talks to one agent (one domain) at a time. The domain is derived **from the path** under `domains/` — there is no `domain:` frontmatter field, and no `domain: "*"` / `domain: "default"`. Cross-domain references are governed by `topology` (medallion only for now), declared in `lynk.yml`.

**Entities own what's true about them.** Everything true about a thing lives in its entity folder (`ENTITY.md` prose + `schema.yml` structure). An entity's `identity` roots it in a physical table or another entity; an extending entity `imports` specific definitions. Facts go on entities; *ways of reasoning* go in skills; *vocabulary* goes in the glossary; *behavior* goes in policies.

**Features and metrics are uniform.** A feature has the six fields `name`, `description`, `sql`, `data_type`, optional `join_name`, optional `filter`. A metric is the same minus `join_name`, and is entity-local. There are no `field` / `formula` / `first_last` / `metric` feature *types* — every feature is a `sql` expression. Cross-entity aggregates are exposed as features whose `sql` references a `metric(entity.metric_name)`.

**Lazy vs. eager loading.** Orientation (`LYNK.md`), vocabulary (`GLOSSARY.yml`), and policies are always loaded. Entities and skills are lazy — the agent indexes them by their `description` and loads only what a question needs. Describe *when* content loads, not *who* reads it.

**Query syntax.** At query time the agent writes Lynk SQL: entities as tables, features as columns, `metric(entity.metric_name)` (using the alias when the entity is aliased), and `USING('join_name')` for relationship joins. Queries are single-domain. Do not use the old `METRIC('name')` form except as an explicit anti-example.
