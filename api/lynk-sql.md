# Lynk SQL

Lynk exposes a SQL interface for querying your semantic layer. The dialect is your warehouse's SQL with two engine-specific abstractions: `METRIC('name')` for applying a pre-defined aggregation, and `USING('relationship_name')` for joining along a relationship defined in `entities_relationships.yml`. Everything else — `SELECT`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, CTEs, subqueries, window functions, every scalar and aggregate function your warehouse exposes — is standard SQL.

The agent uses this syntax internally when generating queries. As an engineer, you write it when authoring evaluation test cases — the `expected_output` field in an evaluation is a Lynk SQL query.

---

## How it works

Lynk SQL is compiled into your warehouse's native SQL before execution. The engine resolves `METRIC()` calls to their aggregation expressions, expands `USING('relationship_name')` into the relationship's `ON` clause from `entities_relationships.yml`, and rewrites entity references to the underlying source tables. Everything else passes through to the warehouse.

Two consequences worth knowing:

- **The dialect is your warehouse's.** `FILTER (WHERE ...)` works on Postgres; `IFF()` and `QUALIFY` work on Snowflake; `PERCENTILE_CONT(...) WITHIN GROUP (...)` works on most modern warehouses. If your warehouse doesn't expose a function, neither does Lynk SQL.
- **Some constructs depend on how the engine emits SQL.** `WITH RECURSIVE`, for example, isn't supported on every engine because of how Lynk generates CTEs. If a construct fails compilation, fall back to a form the engine can express.

**Read-only.** Lynk SQL compiles to a single `SELECT` statement. `CREATE`, `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, and other DDL/DML are not supported.

---

## Entity references

Entities appear as identifiers in `FROM` and `JOIN` — no wrapper, no quoting. The engine resolves the entity to its underlying source table.

```sql
SELECT
  o.id,
  o.status,
  o.total_amount
FROM order o
WHERE o.status = 'completed'
ORDER BY o.created_at DESC
```

One row is returned per entity instance — one row per order in the example above. Field names in `SELECT` and `WHERE` are feature names as defined in the entity YAML, not raw warehouse column names. Aliases (`FROM order o`) work as in any SQL query.

---

## `METRIC('<metric_name>')`

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

Lynk SQL supports the full set of standard SQL join types — `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN`, `CROSS JOIN`. Pick whichever the question requires. The join *condition* can be expressed in four forms:

| Form | Use when |
|---|---|
| `JOIN <entity>` (no `ON`, no `USING`) | The default relationship between the two entities in `entities_relationships.yml` is what you want. The engine uses the join marked `default: true` for that entity pair. |
| `JOIN <entity> USING('relationship_name')` | A named relationship exists in `entities_relationships.yml` and you want that specific one — typically because the entity pair has more than one defined join. |
| `JOIN <entity> USING(<common_feature_name>)` | Standard SQL: the two sides share a column/feature name and you want a join on equality of that column. The argument is an unquoted identifier, not a string literal. |
| `JOIN <entity> ON <expr>` | No relationship matches, you need extra predicates beyond the relationship's keys, or you're joining a CTE or subquery (where relationships don't apply). |

The two `USING` forms are distinguished by the argument: a **single-quoted string literal** names a relationship from `entities_relationships.yml`; an **unquoted identifier** names a common column.

### Default join — no `ON`, no `USING`

When two entities have a single join defined in `entities_relationships.yml` (or one of multiple is marked `default: true`), join them by name alone. The engine fills in the `ON` clause from the default relationship.

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

When the entity pair has more than one relationship defined, name the one you want with `USING()` and a string literal. The engine looks up the relationship and expands its `ON` clause at compile time.

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
- `USING()` in this form is only valid for joins **predefined in `entities_relationships.yml`**.
- `USING()` cannot be combined with additional predicates. `USING('rel') AND extra_predicate` is invalid — switch to a manual `ON` clause when you need extra filters baked into the join.

### `USING(<common_feature_name>)`

Standard SQL `USING` — the unquoted identifier names a column/feature that exists on both sides of the join, and the engine joins on equality of that column.

```sql
SELECT
  o.id,
  o.total_amount,
  c.email
FROM order o
LEFT JOIN customer c USING(customer_id)
WHERE o.status = 'completed'
```

Use this when the two entities (or an entity and a CTE) share a column name and you don't need or want to reference a named relationship.

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

The `ON` expression is standard SQL — any boolean expression valid in your warehouse works. `ON` (or column-based `USING`) is the only join form available when one side is a CTE or subquery, since named relationships are defined between entities, not against derived tables.

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

Joins to a CTE or subquery use a manual `ON` clause (or a column-based `USING(<column>)`) — the relationship-name `USING('rel')` and the no-clause default-join form apply only to entities defined in `entities_relationships.yml`.

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
| `JOIN <entity> USING(<common_feature_name>)` | Yes |
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

## Common pitfalls

**Wrapping entities in `entity('...')`.** Entities are identifiers in `FROM` and `JOIN` — no wrapper. `FROM entity('customer')` is not valid Lynk SQL; write `FROM customer`.

**Writing `METRIC()` without quotes, without an alias, or in lowercase.** `METRIC(count_customers)` (missing quotes), `METRIC('count_customers')` without an `AS` alias, and `metric('count_customers')` (lowercase) all fail. The canonical form is `METRIC('count_customers') AS count_customers`.

**Using raw warehouse table names.** Lynk SQL operates on entities. `FROM db_prod.core.orders` bypasses the semantic layer — write `FROM order` and let the engine resolve the table.

**Using `{feature_name}` curly braces in a query.** That syntax is reserved for *feature-definition* SQL (formula `sql:`, entity-metric `sql:`, filter `sql:`, join `sql:`). In a Lynk SQL query, reference features by name without braces: `WHERE status = 'active'`, not `WHERE {status} = 'active'`. The same rule applies to formula features (`WHERE customer_tier = 'Enterprise'`, not `WHERE {customer_tier} = 'Enterprise'`).

**Combining `USING('rel')` with extra predicates.** `USING('rel') AND extra_predicate` is invalid. Switch to a manual `ON` clause when you need extra filters baked into the join.

---

## Related reference

- [Metrics](../concepts/metrics.md) — how entity metrics are defined, what `sql:` accepts, metric-over-metric composition
- [Entities](../concepts/entities.md) — entity anatomy and feature types
- [Relationships YAML Reference](../file-types/relationships-yaml.md) — how join paths are named, defaulted, and configured
- [Evaluations](../concepts/evaluations.md) — where `expected_output` queries are used
