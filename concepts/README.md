---
description: One page per primitive of the Lynk model — what each building block is, where it lives, and the rules the build enforces.
icon: shapes
---

# Concepts

The building blocks of a `.lynk` project — one page per primitive.

Each page documents a single concept: what it is, where it lives in the [`.lynk/` tree](../reference/layout-and-naming.md), its format, and the rules the build enforces. For how these fit together — the mental model — start with the [Overview](../README.md). For the shared mechanics every concept relies on, see [Reference](../reference/layout-and-naming.md).

## The primitives

| Concept | What it is |
|---|---|
| [Project](project.md) | The `.lynk` repository and its build lifecycle. |
| [lynk.yml](lynk-yml.md) | Project settings, including cross-domain [topology](lynk-yml.md#topology). |
| [LYNK.md](lynk-md.md) | Orientation — who the business and each team is. |
| [GLOSSARY.yml](glossary.md) | Vocabulary — the terms a team uses and what they refer to. |
| [Domain](domain/README.md) | One team's analytical agent. |
| [Entity](entity/README.md) | What exists — [`ENTITY.md`](entity/entity-md.md) prose + [`schema.yml`](entity/schema-yml/README.md) structure. |
| [Policy](policy.md) | How the agent operates and presents. |
| [Skill](skill.md) | A reusable procedure for a recurring kind of analysis. |
| [Reference Files](reference-files.md) | Shared files referenced across a project. |

## Related

- [Overview](../README.md) — the mental model: how the concepts fit together
- [Reference](../reference/layout-and-naming.md) — layout, markdown format, and the `sql:` grammar
- [Lynk SQL](../api/lynk-sql.md) — the query dialect
