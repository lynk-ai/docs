---
description: identity roots an entity in a physical table or another entity; keys identify its rows; imports cherry-pick definitions from a parent entity.
icon: fingerprint
---

# Identity and Imports

`identity` is an [entity](../README.md)'s foundation — it declares *what this entity is*. Combined with `keys` and `imports`, it covers both standalone entities and entities that extend another.

## Contents

1. [What it is](#what-it-is)
2. [Where it lives](#where-it-lives)
3. [Format](#format)
4. [Examples](#examples)
5. [Validation](#validation)
6. [Related](#related)

## What it is

Every entity points its `identity` at one of two things, and the parser tells them apart by segment count:

- **A physical table** (3 segments — `database.schema.table`). The entity is rooted in this table's rows; one row of the table is one entity instance. This is the **standalone** case.
- **Another entity** (2 segments — `domain.entity`, in a **different** domain). The entity is the same conceptual thing as the named entity, sharing its grain and able to import its definitions. This is the **extending** case — extension is cross-domain only (typically a leaf domain extending the shared domain), so it requires a configured [`shared_domain`](../../lynk-yml.md#topology); under the default topology an entity can only root in a physical table. There is no same-domain `import`: two entities in one domain are always independent objects, even on the same physical table.

When marketing's `customer` is the same underlying thing as core's `customer`, marketing declares `identity: core.customer` and imports the specific definitions it wants. This is the explicit version of saying "these two are the same object." Without identity, two entities that happen to share columns are independent objects.

## Where it lives

The top of an entity's [`schema.yml`](README.md):

```
.lynk/domains/<domain>/entities/<entity>/schema.yml
```

## Format

### `identity` and `keys`

```yaml
identity: maindb.public.customers   # a physical table (3 segments)
keys:
  - id
```

| Field | Required | Notes |
|---|---|---|
| `identity` | ✓ | A physical table (3-segment `database.schema.table`) or another entity (2-segment `domain.entity`). |
| `keys` | conditional | The primary keys identifying rows uniquely. **Required** when `identity` is a physical table; **inherited** (and not re-authored) when `identity` is another entity. |

### `imports` — extending another entity

When `identity` points at another entity, the entity becomes an *extension* of it. It shares the parent's grain, inherits its keys, and imports specific definitions:

```yaml
identity: core.customer

imports:
  features:
    - core.customer.company_name
    - core.customer.first_paid_at
  metrics:
    - core.customer.total_arr
  entity_relationships:
    - core.customer.customer_to_subscription
```

The rules:

- **Imports are explicit cherry-picks.** You list exactly which features, metrics, and entity relationships to bring in. Anything not imported is not present — there is no auto-inheritance.
- **Imports are by reference, not by copy.** If the parent later changes an imported definition, this entity follows automatically. The schema never duplicates definitions.
- **Imports cannot be renamed.** An imported feature keeps its name. To expose it under a different name, define a new local feature whose `sql` references the imported one.
- **Imports come only from the `identity` parent.** To pull values from other entities, declare a [relationship](relationships.md) and define a feature whose SQL references it — the standard cross-entity pattern.
- **Local additions are unconstrained.** On top of imports, an extending entity adds its own [features](feature.md), [metrics](metric.md), and [relationships](relationships.md) exactly like a standalone entity. Local names cannot collide with imported names — the single namespace spans both.

Import paths use the 3-segment `domain.entity.name` form; the kind (feature, metric, relationship) is implied by the section header. Imports respect the project [topology](../../lynk-yml.md#topology) — under medallion, an entity can import from `core` but not from a peer domain.

## Examples

**A standalone entity.**

```yaml
identity: maindb.public.customers
keys:
  - id
```

**Marketing extends `core.customer`.** It reuses core's definitions and adds a marketing-specific feature.

```yaml
# .lynk/domains/marketing/entities/customer/schema.yml
identity: core.customer

imports:
  features:
    - core.customer.company_name
    - core.customer.first_paid_at
  metrics:
    - core.customer.total_arr

features:
  - name: signup_year
    description: Calendar year the customer first paid, for cohort analysis
    sql: EXTRACT(YEAR FROM customer.first_paid_at)
    data_type: number
```

The local `signup_year` derives from the imported `customer.first_paid_at` — a marketing-specific addition on top of what `core` already defines.

## Validation

- When `identity` is a physical table, `keys` is authored. When `identity` is another entity, `keys` is **not** re-authored — it's inherited.
- When `identity` is another entity, the build validates that the target is in a **different** domain (extension is cross-domain — extending an entity in your own domain fails), exists, is reachable under [topology](../../lynk-yml.md#topology), and that every item in `imports` is actually defined on the target.
- No circular identity chains — entity A extending B which extends A fails.
- Local names don't collide with imported names (the single namespace spans imports and local definitions).

## Related

- [schema.yml](README.md) — the top-level fields
- [Feature](feature.md) · [Metric](metric.md) · [Relationships](relationships.md) — what gets imported or added locally
- [lynk.yml → topology](../../lynk-yml.md#topology) — which domains an entity may import from
