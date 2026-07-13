---
description: Practices for keeping a shipped semantic layer trustworthy over time — starting with a definition changelog.
icon: wrench
---

# Best Practices

Building a layer is a one-time act; keeping it correct is continuous. The build catches broken references and
unbacked columns every time it runs (see [schema.yml → Validation](../concepts/entity/schema-yml/README.md#validation)
and [SQL expressions → Validation](sql-expressions.md#validation)) — but some things the build can't catch on
its own. This page collects the practices that keep a layer trustworthy between builds.

## A definition changelog

A metric's *meaning* can change even when its name doesn't — a denominator is corrected, a filter is added,
a scale is fixed. When a number moves, the team needs to know why. Keep a short changelog of consequential
definition changes: what changed, when, and why.

- It answers "why is this number different from last month?" without a forensic dig.
- It lets you re-run the value checks that guarded the old definition, so an already-fixed correctness bug
  doesn't silently regress.

A changelog is a maintenance record, not a schema primitive — keep it wherever the team already tracks
change (a `CHANGELOG` file in the project, commit messages, or a supporting doc), close to the layer it describes.

## Related

- [Project](../concepts/project.md) — the build/validate/deploy lifecycle
- [Metric → Validation](../concepts/entity/schema-yml/metric.md#validation) — the correctness rules to preserve across changes
- [schema.yml → Validation](../concepts/entity/schema-yml/README.md#validation) — references and columns resolve at build
