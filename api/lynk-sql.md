# Lynk SQL

Lynk exposes a SQL interface for querying your semantic layer. The dialect is your warehouse's SQL with two engine-specific abstractions: `METRIC('name')` for applying a pre-defined aggregation, and `USING('relationship_name')` for joining along a relationship defined in `entities_relationships.yml`. Everything else — `SELECT`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, CTEs, subqueries, window functions, every scalar and aggregate function your warehouse exposes — is standard SQL.

The agent uses this syntax internally when generating queries. As an engineer, you write it when authoring evaluation test cases — the `expected_output` field in an evaluation is a Lynk SQL query.

---

## Entity references

Entities appear as bare identifiers in `FROM` and `JOIN`. The engine resolves the entity to its underlying source table.

```sql
SELECT
  id,
  status,
  total_amount
FROM order
WHERE status = 'completed'
ORDER BY created_at DESC
```

One row is returned per entity instance — one row per order in the example above. Field names in `SELECT` and `WHERE` are feature names as defined in the entity YAML, not raw warehouse column names. Use aliases as you would for any SQL table (`FROM order o`).

---

## `METRIC()`

`METRIC('name')` applies a pre-defined metric from the entity's `metrics:` section. Use it anywhere a standard aggregate (`SUM`, `COUNT`, `AVG`) is legal — `SELECT`, `HAVING`, arithmetic expressions, CTEs, subqueries, window aggregates.

```sql
SELECT
  status,
  METRIC('count_orders')      AS count_orders,
  METRIC('sum_total_amount')  AS sum_total_amount
FROM order
WHERE created_at >= '2026-01-01'
GROUP BY status
ORDER BY sum_total_amount DESC
```

**Rules:**

- The metric name is a single-quoted string literal: `METRIC('count_orders')`, not `METRIC(count_orders)`.
- Every `METRIC()` call must carry an alias: `METRIC('count_orders') AS count_orders`.
- `METRIC()` resolves against the **`FROM` entity** — the main entity in the query. To apply a metric defined on a different entity, push that aggregation into a CTE or subquery (see [CTEs and subqueries](#ctes-and-subqueries)).
- Apply `GROUP BY` to any non-aggregated features in the `SELECT` — same rule as standard SQL aggregates.

When the question needs the metric's logic applied to a filtered subset, or combined with a non-aggregate expression that the metric definition doesn't capture, fall back to writing the aggregation manually.

---

## Joins

Lynk SQL supports the full set of standard SQL join types — `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN`, `CROSS JOIN`. Pick whichever the question requires. The join *condition* can be expressed in three forms:

| Form | Use when |
|---|---|
| `JOIN <entity>` (no `ON`, no `USING`) | The default relationship between the two entities in `entities_relationships.yml` is what you want. The engine uses the join marked `default: true` for that entity pair. |
| `JOIN <entity> USING('relationship_name')` | A named relationship exists in `entities_relationships.yml` and you want that specific one — typically because the entity pair has more than one defined join. |
| `JOIN <entity> ON <expr>` | No relationship matches, you need extra predicates beyond the relationship's keys, or you're joining a CTE or subquery (where relationships don't apply). |

### Default join — no `ON`, no `USING`

When two entities have a single join defined in `entities_relationships.yml` (or one of multiple is marked `default: true`), you can join them by name alone. The engine fills in the `ON` clause from the default relationship.

```sql
SELECT
  o.id,
  o.total_amount,
  c.email
FROM order o
LEFT JOIN customer c
WHERE o.status = 'completed'
```

### `USING('relationship_name')`

When the entity pair has more than one relationship defined, name the one you want with `USING()`. The engine looks up the relationship and expands its `ON` clause at compile time.

```sql
SELECT
  o.id,
  o.total_amount,
  c.email
FROM order o
LEFT JOIN customer c USING('order_to_billing_customer')
WHERE o.status = 'completed'
```

**Rules:**

- The relationship name is a single-quoted string literal.
- `USING()` is only valid for joins **predefined in `entities_relationships.yml`**. It is not a substitute for `ON` on arbitrary joins.
- `USING()` cannot be combined with additional predicates. `USING('rel') AND extra_predicate` is invalid — switch to a manual `ON` clause when you need extra filters baked into the join.

### `ON <expr>`

Use a manual `ON` clause when no relationship matches, when the join needs extra predicates beyond the relationship's keys, or when joining a CTE or subquery.

```sql
SELECT
  o.id,
  o.total_amount,
  c.email
FROM order o
LEFT JOIN customer c
  ON c.id = o.customer_id
 AND c.is_test_account = false
WHERE o.status = 'completed'
```

The `ON` expression is standard SQL — any boolean expression valid in your warehouse works. `ON` is the only join form available when one side is a CTE or subquery, since relationships are defined between entities, not against derived tables.

---

## CTEs and subqueries

CTEs (`WITH ... AS`) and subqueries are supported. Two situations make them useful:

1. **Applying a `METRIC()` to a filtered subset** that the metric definition itself doesn't capture (e.g., the same metric over two distinct time windows in one query).
2. **Aggregating from an entity other than the `FROM` entity** — `METRIC()` resolves against the main entity, so reach a different entity by isolating it in a CTE or subquery and exposing the aggregated value to the outer query.

```sql
WITH refunded_totals AS (
  SELECT
    customer_id,
    METRIC('sum_refund_amount') AS sum_refund_amount
  FROM refund
  WHERE created_at >= '2026-01-01'
  GROUP BY customer_id
)
SELECT
  c.id,
  c.email,
  METRIC('count_orders') AS count_orders,
  r.sum_refund_amount
FROM customer c
LEFT JOIN refunded_totals r
  ON r.customer_id = c.id
GROUP BY c.id, c.email, r.sum_refund_amount
```

Joins to a CTE or subquery use a manual `ON` clause — `USING()` and the bare default-join form apply only to entities defined in `entities_relationships.yml`.

Reach for a CTE when it earns its place — clearer expression of grain transitions, isolating a filtered metric scope, or splitting a query into named stages. A CTE that exists because you *could* write one is just noise.

---

## Window functions and `QUALIFY`

Window functions are supported, and `METRIC()` can appear inside the window — both as the aggregated expression and inside `OVER (ORDER BY ...)`. The `QUALIFY` clause filters rows by a window function result, the way `HAVING` filters by an aggregate.

```sql
SELECT
  country,
  METRIC('count_players') AS count_players,
  DENSE_RANK() OVER (ORDER BY METRIC('count_players') DESC) AS country_rank
FROM player
GROUP BY country
QUALIFY country_rank <= 5
```

All standard window forms work: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`, `PERCENT_RANK`, `LAG`, `LEAD`, `FIRST_VALUE`, `LAST_VALUE`, aggregates as windows (`SUM(x) OVER (PARTITION BY ...)`), and `ROWS BETWEEN ... PRECEDING/FOLLOWING` frames.

---

## Set operations and subqueries

`UNION`, `UNION ALL`, `INTERSECT`, and `EXCEPT` are supported between any two Lynk SQL queries. Subqueries pass through as standard SQL — scalar subqueries in `SELECT`/`WHERE`/`HAVING`, `IN (subquery)`, and `EXISTS` / `NOT EXISTS`.

---

## SQL functions

Every scalar, aggregate, and window function your warehouse supports is available. Date math, string operations, conditional expressions, casts (`CAST`, `::`, `TRY_CAST`) — write them as you would in plain SQL. The engine only intercepts `METRIC()` and `USING()`; everything else passes through to the warehouse.

---

## Supported statements

| Statement | Supported |
|---|---|
| `SELECT` (incl. `DISTINCT`) | Yes |
| `FROM <entity>` | Yes |
| `JOIN <entity>` (default relationship) | Yes |
| `JOIN <entity> USING('relationship_name')` | Yes |
| `JOIN <entity> ON <expr>` | Yes |
| `INNER` / `LEFT` / `RIGHT` / `FULL OUTER` / `CROSS JOIN` | Yes |
| `WHERE` | Yes |
| `GROUP BY` (including by position: `GROUP BY 1`) | Yes |
| `HAVING` (with `METRIC()` or raw aggregates) | Yes |
| `QUALIFY` (window-result filter) | Yes |
| `ORDER BY` (with `NULLS FIRST` / `NULLS LAST`) | Yes |
| `LIMIT` / `OFFSET` | Yes |
| CTEs (`WITH`, `WITH RECURSIVE`) | Yes |
| Subqueries (scalar, `IN`, `EXISTS`) | Yes |
| Window functions (`OVER`, `PARTITION BY`, `ROWS BETWEEN`) | Yes |
| Set operations (`UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT`) | Yes |
| Casts (`CAST`, `::`, `TRY_CAST`) | Yes |
| DDL / DML | No |

---

## Related reference

- [Entities](../concepts/entities.md) — how entity metrics are defined, including metric-over-metric composition
- [Relationships YAML Reference](../file-types/relationships-yaml.md) — how join paths are named, defaulted, and configured
- [Evaluations](../concepts/evaluations.md) — where `expected_output` queries are used
