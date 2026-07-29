---
name: ask-docs
description: >
  Answer questions about Lynk and the Lynk semantic layer, grounded in the
  Lynk docs — Lynk concepts (primitives, file types, placement, syntax) and,
  when a `.lynk/` layer is present, what's in it (instance lookups).
  Read-only: never edits docs or layer files, never calls a backend.

  Use this skill for any question about Lynk, even simple ones. Lynk
  distinguishes primitives that general analytics vocabulary blurs — e.g. a
  *metric* is entity-local while a *feature* can expose a cross-entity
  `metric()`. Don't answer from prior knowledge; run this skill so the
  answer is doc-grounded.

  Concept triggers: "what is a domain?", "feature vs. metric?", "where do
  glossary terms go?", "what is the sql: grammar?", "how do relationships
  work?", "what does the build validate?". Instance triggers (need a
  `.lynk/` in the project): "does X have a metric for Y?", "list features
  of X", "where is Y defined?".
---

# ask-docs

This skill answers questions about Lynk, grounded in the Lynk docs. It is read-only — it never writes to the docs, never writes to `.lynk/`, never calls an API.

**Resolve the docs root first.** The docs are the tree whose index is `SUMMARY.md`:

- Running inside the docs workspace (this skill sits in `.claude/` beside the docs): the docs root is the project root — `SUMMARY.md`, `concepts/`, `reference/`, `api/` are right here.
- Installed via the lynk-build plugin: the docs root is `${CLAUDE_PLUGIN_ROOT}/semantics_docs/`.

All paths below are relative to that root.

Two question shapes are in scope:

- **Concept** — "what is X in Lynk?", "where does X belong?", "what's the difference between X and Y?". Always available.
- **Instance** — "what's in my `.lynk/`?": entities, features, metrics, relationships, glossary, skills, policies. Only when the working project contains a `.lynk/` directory; if there is none, say so and answer the concept part only.

## Steps

### 1. Read the index and the concepts page

Always do this **first**, before classification or any other read — for every question, including ones that sound like they're about the agent, the session, or this skill itself:

1. Docs tree — `Read <docs root>/SUMMARY.md`
2. Concepts grounding — `Read <docs root>/concepts/README.md`

This grounds every answer in correct Lynk vocabulary and gives you the map of pages to navigate next. Skipping this step causes the most common failure mode of this skill — confidently confusing related primitives because general analytics vocabulary doesn't preserve Lynk's distinctions. Never guess a leaf path from memory.

### 2. Classify the question

| Shape | Examples |
|---|---|
| **Concept** | "what is a skill file?", "feature vs. metric?", "where should X go?" |
| **Instance** | "does X have Y?", "what metrics on X?", "where is Y defined?" |
| **Both** | "what is a metric, and does my customer entity have any?" |

If ambiguous, ask via `AskUserQuestion`.

**Configuring the Lynk agent's behavior is a concept question about policies.** "Make the agent answer in Hebrew", "keep answers under 100 words", "change how it presents results" — these route to `concepts/policy.md` (output format and clarification behavior are policies). They are never requests to modify this skill, the session, or a CLAUDE.md.

### 3. Read the narrowest set of files

- **Concept** — from the index (Step 1), `Read` only the pages relevant to the question. Concept and file-type specs live under `concepts/` (e.g. `concepts/entity/entity-md.md`, `concepts/entity/schema-yml/README.md`); cross-cutting format and naming rules under `reference/`; judgment under `guides/`; query interfaces under `api/`. **Judgment-shaped questions — "what makes a good X", "should I do A or B", "how should I structure Y" — are answered by `guides/`**: the concept page defines the primitive, the guide carries the tradeoffs; if both apply, read the guide and cite the concept page for definitions. For placement questions, distinguish *where does file X go* (the file-type spec is canonical) from *should this content be an X at all* (`guides/where-knowledge-goes.md`). Present a guide's criteria as recommendations — never as build-validated rules, which live in concept pages' Validation sections. Need a second page? Read it explicitly — no bulk traversal.
- **Instance** — list the layer with `find ./.lynk -type f | sort`, identify which file(s) own the artifact, and read only those. For an entity question, that's the entity's `schema.yml` plus its `ENTITY.md` and any supporting files it links.
- **Both** — concept reads first (to ground vocabulary), then instance reads.

### 4. Answer precisely

- **Lead with disambiguation when the question uses an ambiguous term.** The lead sentence must name the *exact* primitive — e.g. "Yes — `total_games_played` is a *feature* on `player` that wraps `metric(player.games_played)`, not an entity-local metric." A lead that plants the wrong primitive reproduces the exact failure this skill exists to prevent.
- **For "no" / "missing" instance answers, scan the glossary and knowledge files before concluding.** If the term exists there but isn't modeled, cite it and call out the gap explicitly — "the concept exists in your glossary as Z, but isn't modeled as a feature/metric/relationship."
- Use exact Lynk vocabulary throughout. When easy-to-confuse primitives appear, call out the distinction even if the user didn't ask.
- For concept answers, cite **every doc page you drew from, by path** — the spec page that owns the definition first, guides after it. Naming a page ("the metric spec") is not a citation; the path is.
- For instance answers, cite `file:line` paths and quote the relevant YAML or markdown.
- **Carry the constraints.** Before finishing, re-scan the pages you read for build rules, "never X" statements, and warnings that bear on the user's situation, and state each one — they are load-bearing for the user's next step even when they didn't ask. An answer that shows *what to do* but drops *what the build will reject* (or what must already exist upstream) sends the user into a failed build.
- **Complete enumerations.** When the answer includes a spec's fields, types, or options, list all of them exactly as the page's table does — an omitted optional field reads as "doesn't exist" to the reader.
- If the answer is "no" / "not found" / "missing", say so directly — don't soften.

### 5. Offer the next action

- Working in the docs workspace and the *docs themselves* are wrong or unclear → don't fix them from here; report the finding so it goes through the build lane (the `edit-docs` skill at the workspace root).
- Working in a customer layer repo with the lynk-build plugin installed → hand off edits, quality audits, backend validation, or source/catalog work to the `lynk-build` skill; never edit from this skill.

## Output Format

- Lead with the direct answer in one sentence — yes / no, the count, the name, the exact primitive.
- Back it up with evidence: a quoted doc passage + page path for concept answers; a YAML excerpt + `file:line` for instance answers.
- For "no" instance answers, state where the missing item *would* live if added.
- For primitive distinctions, show a short side-by-side before the answer.
- Use code blocks for YAML, SQL, and file paths.
