---
description: How to keep a shipped semantic layer correct as the warehouse and the business change — drift, refactors, deprecation, and a definition changelog.
icon: wrench
---

# Maintaining a Layer

Building a layer is a one-time act; keeping it correct is continuous. A layer that passed the build last
month can serve wrong answers today because the warehouse moved underneath it, a definition was renamed
without updating its references, or a metric's meaning drifted. This page covers the four maintenance moves
that keep a layer trustworthy over time.

## Contents

1. [Keeping in sync with the warehouse](#keeping-in-sync-with-the-warehouse)
2. [Renaming and refactoring](#renaming-and-refactoring)
3. [Deprecation lifecycle](#deprecation-lifecycle)
4. [A definition changelog](#a-definition-changelog)

## Keeping in sync with the warehouse

Every feature and metric resolves to real warehouse columns. When a column is renamed, retyped, or dropped,
the definitions that depend on it break — but only the [build](../concepts/project.md) reveals it, and a
layer that isn't rebuilt keeps serving the last good version while the definitions silently rot.

- **Detect drift.** Rebuild on a schedule (or on warehouse-schema change), not only when editing the layer.
  The build's field-probe is what surfaces a column that no longer exists.
- **Respond.** When a definition loses its backing column, either repoint it at the new column or disable it
  with [`enabled: false`](markdown-format.md#enabled-false) until it can be repaired — do not leave a broken
  definition live.
- **Re-ground at the authoritative surface.** After any change to a value's `sql` or its underlying columns,
  re-check the value at the **compiled build**, not by re-querying raw tables — a raw query is a proxy that
  can pass while the build fails. Compare against an external anchor, in order of preference: a curated truth
  table of verified values → a sanity invariant (`0 ≤ pct ≤ 100`, parts sum to the total, counts
  non-negative) → a hand-computed value from raw rows — never the definition's own SQL. A definition that
  still *compiles* can still be *wrong* (see
  [aggregation correctness](../concepts/entity/schema-yml/metric.md#aggregation-correctness)).

## Renaming and refactoring

A feature, metric, or relationship `name` is referenced by other definitions through `metric()`,
[`@` injection](markdown-format.md#references), and relationship `join_name`s. A rename that misses a
reference leaves a dangling reference, which fails the build. Do it as one atomic change:

1. **Find every reference** to the name across the layer (`metric(<entity>.<name>)`, `@…`, `join_name`).
2. **Rename** the definition.
3. **Update every reference** found in step 1.
4. **Rebuild** to confirm nothing dangles.

The same order applies when moving a definition to a different entity to satisfy
[one home](../concepts/entity/README.md#validation) or to resolve a
[domain-wide name collision](../concepts/entity/schema-yml/metric.md#validation).

## Deprecation lifecycle

[`enabled: false`](markdown-format.md#enabled-false) removes a primitive from the build without deleting it.
For content that is genuinely being *retired* (not just paused), treat removal as a lifecycle, not a delete:

1. **Mark deprecated.** Set `enabled: false` and add a one-line pointer to the replacement in the primitive's
   `description` or body.
2. **Keep it discoverable** for one release cycle, so consumers and downstream references can migrate.
3. **Remove** only after that cycle, once nothing references it — a reference to a removed primitive fails
   the build exactly like a reference to one that never existed.

This prevents the two failure modes of ad-hoc deletion: orphaned references, and consumers surprised by a
definition that vanished without a replacement.

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

- [Project](../concepts/project.md) — the build/validate/deploy lifecycle that surfaces drift
- [Markdown Format → `enabled: false`](markdown-format.md#enabled-false) — the disabling mechanism
- [Metric → Validation](../concepts/entity/schema-yml/metric.md#validation) — the correctness rules to preserve across changes
- [Entity → Validation](../concepts/entity/README.md#validation) — one concept, one home
