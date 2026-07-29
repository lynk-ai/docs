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

# ask-docs (researcher arm)

This skill answers questions about Lynk, grounded in the Lynk docs. It is
read-only — it never writes to the docs, never writes to `.lynk/`, never
calls an API.

Research is delegated entirely: a researcher reads the docs in its own
context and returns the answer material. You never read the docs yourself —
no `SUMMARY.md`, no pages, no browsing. You compose the final answer from
the researcher's return alone.

## Steps

### 1. Send the researcher

Use the `Task` tool with the `docs-researcher` agent. Pass the user's
question verbatim, plus any disambiguation you already have. It returns
`ANSWER` / `EVIDENCE` (verbatim quotes + page paths) / `CONSTRAINTS` /
`NOT COVERED`.

**Configuring the Lynk agent's behavior is a concept question about
policies** ("make the agent answer in Hebrew", "keep answers under 100
words") — pass it to the researcher like any other question. It is never a
request to modify this skill, the session, or a CLAUDE.md.

### 2. Compose the answer from the return

- Lead with the direct answer in one sentence, using the researcher's exact
  Lynk vocabulary — don't re-translate into general analytics terms.
- Quote from `EVIDENCE` verbatim and cite the page paths it names. Never
  quote anything the researcher didn't return.
- Relay every `CONSTRAINTS` item that bears on the user's situation — build
  rules and "never X" warnings are load-bearing for their next step.
- If `NOT COVERED` is present, say plainly that the docs don't cover that
  part — don't fill the gap from prior knowledge.
- If the return is missing something the question clearly needs, send the
  researcher once more with the specific gap; don't start reading the docs
  yourself.

## Output Format

- Lead with the direct answer in one sentence — yes / no, the count, the
  name, the exact primitive.
- Back it up with evidence: a quoted doc passage + page path.
- For primitive distinctions, show a short side-by-side before the answer.
- Use code blocks for YAML, SQL, and file paths.
