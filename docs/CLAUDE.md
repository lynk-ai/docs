# Lynk Docs — the shippable unit

This folder is the Lynk Semantics v2 documentation plus the context for retrieving
it. It is consumed as-is by agents (and rendered into the lynk-build plugin), so
everything needed to *use* the docs lives here — and nothing about *building* them.

## Read-only contract

Doc pages here are data. Never edit, create, or delete pages from a session doing
retrieval or Q&A. Authoring happens one level up, in the build lane (the `edit-docs`
skill); if you find an error or gap, report it as a finding instead of fixing it.

## How to navigate the docs

1. **Start at the index.** Read `SUMMARY.md` — the table of contents listing every
   page. Never guess a leaf path from memory.
2. **Ground vocabulary.** Read `concepts/README.md` before answering anything that
   involves Lynk primitives (Project, Domain, Entity, Feature, Metric, Relationship,
   Glossary, Policy, Skill). Lynk distinguishes primitives that general analytics
   vocabulary blurs — don't answer from prior knowledge.
3. **Pick the narrowest leaf** that answers the question (e.g.
   `concepts/entity/schema-yml/metric.md`, `reference/sql-expressions.md`) and read
   only that. Need a second page? Read it explicitly. No bulk traversal.

The tree at a glance: `concepts/` holds the concept and file-type specs — what a
primitive *is*, and what the build validates (each spec's Validation section);
`reference/` holds cross-cutting rules (layout & naming, markdown format, SQL
expressions) plus the capability-boundary index (`what-lynk-does-not-do.md`);
`guides/` holds judgment — how to decide, what good looks like, anti-patterns;
`api/` holds the query interfaces (Lynk SQL, REST); and `context-reference/`
holds how context behaves for the agent that reads it — what a page costs on
every load, why a description isn't getting picked, when a file should become
two, what will go stale or end up contradicting a neighbour. Reach for it when
the question is about how well layer content is *written* rather than whether
it is valid: the build accepts a description that routes nowhere and a body too
heavy to earn its place, and the person pays for both. It runs two tiers —
enter at a page under `context-reference/concepts/`, decision-ready on its own,
and open its `context-reference/deep/` counterpart only on the trigger that
page names. On a question about a `.lynk/` file, `guides/context-engineering.md`
states the Lynk rule and the reference carries the measurement behind it.
Judgment-shaped questions
("what makes a good X", "should I do A or B") are answered by `guides/`: the
concept page defines the primitive, the guide carries the tradeoffs — and a
guide's criteria are recommendations, never build-validated rules.
Capability-boundary questions ("does Lynk support X") are answered by the
boundary index — cite it together with the owning spec page it links to, so a
by-design gap isn't misreported as a missing feature.

## Retrieval context

Skills and subagents for doc-grounded Q&A live in `.claude/` beside the docs. They
follow the navigation rules above and the read-only contract.
