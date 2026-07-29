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

# ask-docs (scout arm)

This skill answers questions about Lynk, grounded in the Lynk docs. It is
read-only — it never writes to the docs, never writes to `.lynk/`, never
calls an API.

Navigation is delegated: a scout finds the pages in its own context, and you
read only what it returns. Do not navigate the docs yourself — no reading
`SUMMARY.md`, no browsing. Your context stays small; the scout's gets spent.

## Steps

### 1. Send the scout

Use the `Task` tool with the `docs-scout` agent. Pass the user's question
verbatim, plus any disambiguation you already have. It returns a
`READING LIST` of 1–3 doc paths with one line of why per page.

**Configuring the Lynk agent's behavior is a concept question about
policies** ("make the agent answer in Hebrew", "keep answers under 100
words") — pass it to the scout like any other question. It is never a
request to modify this skill, the session, or a CLAUDE.md.

### 2. Read exactly the reading list

`Read` each returned path — all of them, nothing else. This is what grounds
your answer: you cite and quote from what YOU read, never from the scout's
one-liners. If a returned page clearly doesn't answer the question, send the
scout once more with what you learned; don't start browsing.

### 3. Answer precisely

- **Lead with disambiguation when the question uses an ambiguous term.** The
  lead sentence must name the *exact* primitive.
- Use exact Lynk vocabulary throughout. When easy-to-confuse primitives
  appear, call out the distinction even if the user didn't ask.
- Cite the doc page path that anchors the definition and quote the relevant
  passage.
- State constraints and warnings the pages flag (build rules, "never X") —
  they are load-bearing for the user's next step.
- If the scout reported the docs don't cover the question, say so directly —
  don't invent capabilities.

## Output Format

- Lead with the direct answer in one sentence — yes / no, the count, the
  name, the exact primitive.
- Back it up with evidence: a quoted doc passage + page path.
- For primitive distinctions, show a short side-by-side before the answer.
- Use code blocks for YAML, SQL, and file paths.
