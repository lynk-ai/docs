---
description: A metric is an aggregation defined on the entity it aggregates — sum, count, average, conditional aggregates — invoked with metric().
icon: sigma
---

# Metric

An aggregation defined on an [entity](../README.md) — sum, count, average, conditional aggregate — anything that produces a single value across many rows.

## Contents

1. [What it is](#what-it-is)
2. [Where it lives](#where-it-lives)
3. [Format](#format)
4. [Examples](#examples)
5. [Validation](#validation)
6. [Related](#related)

## What it is

Where a [feature](feature.md) answers *"what is this attribute?"* at row grain, a metric answers *"across many rows of this entity, what's the aggregate?"*

A metric is **entity-local**. It is defined exactly once, on the entity whose rows it aggregates — `sum_net_revenue` lives on `order` because `order` is the entity whose rows it sums. Its `sql` references that entity's own features (entity-qualified) and **cannot** reference other entities; there is no `join_name` on a metric.

To use an aggregate across an entity boundary — `customer` wanting total revenue across all its orders — you don't define a metric on `customer`. You define a [feature](feature.md) on `customer` whose `sql` references the cross-entity metric path through a [relationship](relationships.md), and the engine handles the join and grain alignment. This keeps the agent's mental model simple: **metrics aggregate the current entity; everything else is a feature**, however it's computed underneath.

## Where it lives

`.lynk/domains/<domain>/entities/<entity>/schema.yml`, under `metrics:`.

## Format

| Field | Required | Type | Notes |
|---|---|---|---|
| `name` | ✓ | string | Unique within the entity across features, metrics, and relationships. |
| `description` | ✓ | string | What the metric represents. |
| `sql` | ✓ | aggregation expression | References this entity's features, entity-qualified. No cross-entity references. [SQL expressions](../../../reference/sql-expressions.md) grammar. |
| `data_type` | ✓ | `number` \| `string` \| `datetime` \| `boolean` | The type of the aggregated value. |
| `filter` | – | SQL predicate | A WHERE clause that narrows rows before the aggregation runs. |

### Invoking a metric

A metric is invoked with `metric(<entity>.<metric_name>)`:

- **Inside `schema.yml`** — a feature's `sql` can call `metric()` to compose with an aggregate (see [SQL expressions](../../../reference/sql-expressions.md#functions)).
- **At query time** — the agent writes `metric(<entity>.<metric_name>)` in Lynk SQL; when the entity is aliased, it uses the alias. Full rules in [Lynk SQL](../../../api/lynk-sql.md#metricentitymetric_name).

## Examples

**A count.**

```yaml
- name: count_customers
  description: Count of customers
  sql: COUNT(*)
  data_type: number
```

**A conditional aggregate.** Counts churned customers without filtering the rest out.

```yaml
- name: churned_customers
  description: Count of customers who have churned
  sql: SUM(CASE WHEN customer.status = 'churned' THEN 1 ELSE 0 END)
  data_type: number
```

**An aggregate with a filter.** On Bly's `order`, revenue from completed orders only.

```yaml
- name: completed_revenue
  description: Net revenue from completed orders
  sql: SUM(order.net_amount)
  data_type: number
  filter: order.status = 'completed'
```

## Validation

- `name` is unique within the entity (features, metrics, and relationships share one namespace).
- `sql` references only this entity's own features (entity-qualified); cross-entity references and `join_name` are not allowed on a metric.
- `data_type` is one of `number`, `string`, `datetime`, `boolean`.
- Grammar errors are detailed in [SQL expressions → validation](../../../reference/sql-expressions.md#validation).

## Related

- Parent: [schema.yml](README.md) · [Entity](../README.md)
- Siblings: [Feature](feature.md) — how cross-entity aggregates are exposed · [Relationships](relationships.md)
- [SQL expressions](../../../reference/sql-expressions.md) — `metric()` and the `sql` grammar
- [Lynk SQL](../../../api/lynk-sql.md) — invoking `metric()` at query time
