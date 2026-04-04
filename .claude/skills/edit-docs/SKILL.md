---
name: edit-docs
description: Edit, update, or make changes to Lynk's documentation. Use this skill whenever the user asks to update docs, edit documentation, add content to docs, rewrite a doc page, fix something in the docs, or make any changes to documentation files. Also trigger when the user asks to add a new guide, update an overview page, or change how something is explained in the docs. Even if the user doesn't say "docs" explicitly — if they're describing a change to written documentation or reference material in this project, use this skill.
---

# Edit Docs Skill

You're helping maintain Lynk's technical documentation — a standalone docs repository of Markdown files that explain how to use Lynk to data engineers and technical users.

## References

These reference files are available to you, load them when relevant to the task — do not load all of them by default.

| Reference | File | When to load |
|---|---|---|
| GitBook custom blocks | `references/gitbook_blocks.md` | When adding or editing GitBook-specific components: hints, tabs, steppers, expandable sections, columns, cards, embeds, buttons, or any `{% %}` block syntax |
| GitBook frontmatter | `references/gitbook_frontmatter.md` | When configuring page-level settings: description, icon, hidden, layout width, sidebar visibility, or page-level variables |
| GitBook variables & expressions | `references/gitbook_variables.md` | When working with dynamic content — space or page variables, or `<code class="expression">` inline expressions |
| GitBook structure & navigation | `references/gitbook_structure.md` | When modifying SUMMARY.md, .gitbook.yaml, understanding file organization, or working with Git Sync |
| Canonical example companies | `references/canonical-companies.md` | When writing or editing Full Examples sections in `file-types/` docs — contains exact entity names, feature names, metrics, and glossary terms for Grove (B2B SaaS), Bly (E-commerce), and Arcadia (Mobile gaming) |

---

## Step 1: Load structure and style

Before anything else, read these files:

1. **`README.md`** (repo root) — The index of all documentation files. This tells you what sections exist, what each file covers, and how the docs are organized.
2. Load additional references from the References table above only when relevant to the task.

This is a standalone docs repository. All documentation lives at the root level in topic folders:
- `concepts/` — deep-dive references: domains, entities, context, agent, evaluations, Lynk SQL
- `file-types/` — field-by-field reference for every file type (YAML and Markdown)
- `guides/` — task-focused how-to guides
- `project/` — step-by-step walkthrough using a real example

Writing style: write like an engineer talking to engineers — direct, precise, honest, no hype. No buzzwords, no vague claims, no marketing language.

## Step 2: Understand the request

If the request is clear, proceed. If anything is ambiguous — which section is affected, what exactly should change, whether new content should live in an existing file or a new one — ask before touching files. One clarifying question is better than making the wrong edit.

## Step 3: Identify affected files

Docs changes often ripple. Think about:
- The primary file where the change belongs
- Any files that reference the changed concept (e.g., `readme.md` table of contents, overview pages that summarize detail pages)
- Whether the change introduces new content that should be reflected in the index

List all the files you plan to touch and explain why each one is affected.

## Step 4: Read existing content

Read every file you plan to edit before writing anything. Don't overwrite blindly — understand what's already there, what the structure is, and how your change fits.

## Step 5: Show a plan and get confirmation

**For minor edits** (fixing a single sentence, correcting a value, updating one field): describe what you'll change in one sentence, then proceed.

**For significant changes** (rewrites, new sections, new pages, structural changes): present the proposed structure first and wait for confirmation before writing. If the user wants adjustments, update the plan first.

## Step 6: Make the edits

Write the changes. Follow the style guide:
- Short sentences, active voice, specific over vague
- One idea per paragraph, whitespace between sections
- Technical but not academic — explain how things work, not just that they work
- No buzzwords, no hype, no vague claims
- Tables and bullet lists for reference content; prose for explanations
- Apply the Terminology Rules at the end of this skill.

## Step 7: Update the readme

After every change, update `README.md` (repo root) to reflect:
- New files added (add a row to the relevant table)
- Changed file purposes (update the description)
- New sections or structural changes

The readme is the index — keep it accurate.

## Step 8: Update summary.md

After updating `README.md`, edit `summary.md` to reflect the same structural changes:
- New files added (add the appropriate entry in the correct section)
- Renamed or moved files (update the path)
- Removed files (remove the entry)
- New sections or folders (add a section header and entries)

`summary.md` drives the GitBook sidebar — keep it in sync with `README.md`.

## Step 9: Suggest skill updates if folder structure changed

If this edit added or removed a top-level documentation folder (beyond `concepts/`, `guides/`, `project/`, `file-types/`), suggest — but do not make — an update to the `edit-docs` skill itself.

Specifically: each top-level folder needs its own `###` section in the **Docs Sections** part of the skill explaining the folder's purpose, page structure, tone, and conventions for editing and adding pages. Without that, future edits to the new folder will lack the guidance needed to stay consistent.

Tell the user: "You may want to add a section to the edit-docs skill for the new `<folder>/` folder covering its purpose, page structure, and editing conventions."

Do not edit the skill file — only flag the need.

---

## Docs Sections

The docs have four distinct sections. Each has its own purpose, structure, and conventions. Match the section before writing anything.

---

### Project Walkthrough (`project/`)

**Purpose:** A top-down narrative guide for building a complete semantic layer from scratch. Pages follow a prescribed build sequence and tell a story using Grove (a B2B SaaS company) as the running example.

**Page structure:**
- `# Step N: [Step Name]` title
- 1–2 sentence framing of what this step produces and why it precedes the next step
- `## Why [This Step]?` — explain the reasoning using contrast: what goes wrong if skipped vs. what you gain
- `## [Substep Name]` for each file or action in this step:
  - **Location:** exact file path
  - A "This file answers: *...*" line stating what question the file is written to resolve
  - A fenced code block with a complete, realistic Grove example (not a skeleton with `{placeholders}`)
  - A `**What to include:**` bullet list and a `**What to leave out:**` bullet list
- A `## Key Point` section tying the step back to the build sequence rationale

**Tone:** Narrative and instructional together. Always explain *why* alongside *what*. "Write the glossary first, because without it the agent has to guess what 'churned customer' filters on."

**Editing an existing page:** Update examples, file paths, or guidance bullets. If the build sequence changes, update `project/index.md` step list and `README.md`.

**Adding a new step:** Only if the build sequence genuinely changes. Add the step file, add it to `project/index.md`'s numbered list, and add a row to the Project Walkthrough table in `README.md`.

---

### Concepts (`concepts/`)

**Purpose:** Deep-dive reference for how specific systems behave across the platform. These pages explain cross-cutting behavior that affects multiple file types or the agent as a whole — not tied to any single file type or build step.

**Existing pages:** `concepts/domains.md`, `concepts/entities.md`, `concepts/context.md`, `concepts/agent.md`, `concepts/evaluations.md`, `concepts/lynk-sql-api.md`

**Page structure:**
- `# H1` title — the concept name, short
- 2–3 sentence intro explaining what the concept is and why it matters
- Named `##` sections for each distinct aspect of the behavior, each with:
  - Prose explanation of how the system works
  - Code examples showing real behavior (not `{placeholders}`)
  - Field reference tables where relevant
- No "When to Use" or "When NOT to Use" sections — concepts pages explain behavior, not when to create a file

**Tone:** Precise and explanatory. Describe what the system does, not what the user must do. "Named domains inherit from `domain: '*'`" not "you must configure inheritance."

**Editing an existing page:** Update prose, examples, or tables to reflect current system behavior. Do not add file-type-specific detail that belongs in `file-types/`.

**Adding a new page:** Propose the title, intro, and `##` section outline — get confirmation before writing. Then add a row to the Concepts table in `README.md`.

---

### File-Types Reference (`file-types/`)

**Purpose:** Deep-dive reference for every file type. Used when someone needs exact structure, allowed fields, or to understand what content belongs where. Two sub-types: Markdown context files (Template A) and YAML reference files (Template B).

#### Template A — Markdown Context Files

1. **Title + description** — `# H1` title followed by 2–4 sentences: what this file type is, what it controls, and why it matters.

2. **Frontmatter** — The YAML frontmatter block with a field reference table showing exact keys and allowed values.

3. **File Body** — What goes into this file. Use a named `##` subsection for each distinct content area (e.g., "Domain-Wide Knowledge", "Entity Knowledge"). Within each subsection: one sentence explaining what belongs there, followed by a fenced code block with realistic field names and actual values (not `{placeholders}`). Add a callout note after the code block if there's a constraint or common mistake specific to that content area.

4. **Best Practices** — 4–6 rules. Each is a bolded lead sentence + one sentence of explanation.

5. **Common Pitfalls** — 3–5 anti-patterns. Each is bolded with an explanation of why it fails.

6. **When to Use This File** — Lead with 2–3 numbered decision criteria (the actual rule for when to add an entry), then give 4–5 example trigger scenarios below as illustrations. Format for examples: `"trigger phrase"` → what to add/update. Decision criteria first, examples second — a data engineer setting up a new file needs the rule, not just pattern-matching.

7. **When NOT to Use This File** — Redirects to the correct file for each common mistake. Format: "if X, use Y instead."

8. **Full Examples** — Exactly 3 examples, one per canonical company (see **Canonical Example Companies** below). Always in this order: B2B SaaS → E-commerce → Mobile gaming. One-sentence intro per example explaining what it demonstrates. Use the exact entity names, feature names, metric names, and glossary terms from the canonical profiles — do not invent new ones. No placeholder text.

#### Template B — YAML Reference Files

1. **Title + description** — `# H1` followed by 2–4 sentences explaining what this YAML file is, what it defines, and why it exists.

2. **Top-Level Structure** — A skeleton YAML with inline comments on all top-level keys. Followed by a field reference table.

3. **Field Reference** — Each major YAML section in its own `##` subsection, with field tables, allowed values, and inline examples.

4–8. Same as Template A (Best Practices, Common Pitfalls, When to Use, When NOT to Use, Full Examples — but Full Examples are complete YAML files).

**Rules for both templates:**
- All 8 sections must be present. Section order is fixed.
- Do not add sections outside this structure without explicit user approval.
- Full Examples must use realistic data — no `{placeholder}` values in examples.

**Adding a new file-type page:** Rare — only when a new file type is introduced to the product. Use the appropriate template in full, then add a row to the File-Types Reference table in `README.md`.

---

### Guides (`guides/`)

**Purpose:** Task-focused how-to guides for specific operations. Each guide answers "how do I do X?" with a concrete, actionable checklist a developer can follow step by step.

**Page structure:**
- `# Guide: [Task Name]` title
- `## Before You Start` — 2–4 decision questions to answer before beginning. Each is a bolded question + one sentence explaining why it matters (what goes wrong if you skip it).
- Numbered steps (`### 1. [Step Name]`), each containing:
  - **File:** exact file path with `{entity}` style placeholders for variable parts
  - A minimum-viable code block (YAML or Markdown) using `{placeholder}` values to show structure
  - A `**Checklist:**` with `- [ ]` items for that step
  - A `→ See [Reference Page]` link to the relevant file-type reference
- `## Quick Reference` table at the end: Step | File | Reference

**Tone:** Direct and imperative. "Create the entity YAML." "Add relationships." "Verify." No padding, no explanation of why unless it prevents a common mistake.

**Editing an existing guide:** Update file paths, code snippets, or checklist items. Keep step numbering stable — renaming a step number ripples into any doc that links to it.

**Adding a new guide:** Follow the structure above exactly. Before writing, propose the title, "Before You Start" questions, and numbered step list — get confirmation. Then add a row to the Guides table in `README.md`.

---

## Constraints

- Only edit documentation files in the topic folders (`concepts/`, `file-types/`, `guides/`, `project/`) and `README.md`. Do not edit `.claude/` or tooling files unless the user explicitly asks.
- Always read before writing.
- Always update `README.md` after changes.
- If you find yourself writing "leverage", "revolutionary", or "game-changing", stop and rewrite.

---

## Canonical Example Companies

All Full Examples sections across all file-type docs use three canonical companies. When writing examples, load `references/canonical-companies.md` and use the exact names, entity names, feature names, metrics, and glossary terms defined there. Never invent alternatives.

**Framing**
- Lynk is the best analyst in the world. We give you the framework to teach her about your business and your data.

**The agent**
- There is one agent. It performs tasks (like `text-to-sql`). Do not refer to "task executors" or split the agent into multiple personas. The agent is the single reasoning layer that reads context and produces output.
- Context is loaded by the agent at different points. Describe *when* it's loaded, not *who* reads it.

**Context scoping**
- Context **compounds** — the agent loads all applicable levels together. 
- Scoping is controlled by frontmatter, not file names. File names are up to the user. When explaining scoping, reference frontmatter fields, not file paths.

**Domain naming**
- The `default` domain is the **main domain**. Refer to it as "the main domain (`default`)" on first use.

**Domain sections in file-type docs**
- When a file type supports a `domain` frontmatter field, keep the domain section in that file brief — one or two sentences explaining what scoping it applies and a link to the [Domains reference](../concepts/domains.md).
- Do not document inheritance behavior, override rules, exclusion syntax, or multi-file merging in individual file-type docs. All of that belongs on the Domains reference page.
