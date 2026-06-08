# Metrics

A metric is an aggregation expression defined on an entity. Metrics are how the agent computes quantities — revenue totals, order counts, averages, ratios. All aggregation logic in Lynk lives on metrics; the agent does not invent aggregations at query time.

There are two surfaces for metrics:

- **Entity metrics** — defined in the `metrics:` section of an entity YAML. Each metric is a SQL aggregate expression over the entity's features.
- **Metric features** — a feature of type `metric` on a dimension entity that pulls an aggregated value from a metric on a related entity. This is **feature chaining**.

The two work together: an entity metric defines *how* to aggregate; a metric feature exposes the aggregated value as an attribute of a related entity.

---

## Entity Metrics

Entity metrics are defined in the `metrics:` section of an entity YAML. Each metric is an aggregation expression — a SQL aggregate function over the entity's features.

```yaml
metrics:
  - name: count_orders
    description: Total number of orders
    sql: COUNT({order_id})

  - name: sum_net_revenue
    description: Total net revenue across orders, in USD
    sql: SUM({net_amount})

  - name: avg_order_value
    description: Average net order value, in USD
    sql: AVG({net_amount})
```

`sql` is a SQL aggregate expression. Feature names inside `{...}` reference features defined on the same entity.

Entity metrics define *how* to aggregate — not which rows to aggregate. Filtering happens at query time, not in the metric definition.

Entity metrics exist on fact entities — `order`, `session`, `purchase`. They are the aggregation primitives that metric features reference from other entities.

---

## What's allowed in `sql:`

The `sql:` field accepts any aggregation expression your warehouse SQL dialect accepts. The engine passes it through to the warehouse after substituting `{feature_name}` references and resolving any nested `METRIC()` calls.

Always available across dialects:

- Plain aggregates — `SUM`, `COUNT`, `COUNT(DISTINCT)`, `AVG`, `MIN`, `MAX`.
- Conditional aggregation — `SUM(CASE WHEN {is_completed} = 1 THEN {net_amount} ELSE 0 END)`, `COUNT(DISTINCT CASE WHEN {is_active} = 1 THEN {customer_id} END)`.
- Arithmetic between aggregates, typically with a `NULLIF` denominator — `SUM({net_amount}) / NULLIF(COUNT({order_id}), 0)`.
- Metric-over-metric composition — `METRIC('sum_net_revenue') / NULLIF(METRIC('count_orders'), 0)` (see below).
- Scalar wrappers like `CASE`, `COALESCE`, `ROUND`, `CAST` inside the aggregate.

Dialect-specific constructs pass through if your warehouse supports them:

- `FILTER (WHERE ...)` clauses — Postgres.
- `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {net_amount})` — most modern warehouses.
- `IFF(...)`, `APPROX_PERCENTILE(...)` — Snowflake.

Window functions are not supported inside a metric definition's `sql:`. They **are** supported in `formula` feature `sql:` (a window produces a per-row value, which is what a formula is) and in queries — see [Lynk SQL](../api/lynk-sql.md) and the [formula section of the entity YAML reference](../file-types/entity-yaml.md#formula--derived-value).

---

## Metric-Over-Metric Composition

A metric's `sql:` can reference other metrics on the same entity via `METRIC('name')`. Use it to compose ratios, sums, and differences once — instead of repeating the underlying aggregation in every query that needs the derived value.

```yaml
metrics:
  - name: count_orders
    sql: COUNT({order_id})

  - name: sum_net_revenue
    sql: SUM({net_amount})

  # Composed from the metrics above
  - name: avg_revenue_per_order
    sql: "METRIC('sum_net_revenue') / NULLIF(METRIC('count_orders'), 0)"
```

Nested `METRIC()` calls resolve against the same entity that defines them. There is no cross-entity composition at this layer — to combine metrics defined on different entities, use a `metric` feature on the destination entity (see below).

Wrap denominators in `NULLIF(..., 0)` to avoid division-by-zero errors.

Composed metrics are queried the same way as base metrics: `METRIC('avg_revenue_per_order') AS avg_revenue_per_order`.

---

## Metric Features

A metric feature is a feature of type `metric` on one entity that pulls an aggregated value from a metric on a related entity.

The `customer` entity below surfaces revenue from the `order` entity:

```yaml
# On the customer entity
features:
  - type: metric
    name: total_revenue
    description: Total net revenue from all completed orders placed by this customer
    data_type: number
    source: order
    metric: sum_net_revenue
```

The `source` field points to the entity whose metrics you want to use. The `metric` field names the specific metric on that entity.

This makes `total_revenue` queryable as an attribute of every customer — without duplicating the aggregation logic. The SQL for `SUM({net_amount})` lives once, on the `order` entity. Any entity that relates to `order` can surface it via a metric feature.

---

## How Feature Chaining Works

Feature chaining requires three parts:

1. **A fact entity** defines a metric. `order` defines `sum_net_revenue` as `SUM({net_amount})`.
2. **A relationship** connects the two entities. `customer-order` is defined in `entities_relationships.yml`.
3. **A metric feature** on the dimension entity references the fact entity's metric. `customer` defines `total_revenue` pointing to `order.sum_net_revenue`.

When the agent resolves `total_revenue` on `customer`, it:

1. Looks up the `customer-order` relationship
2. Uses the default join (`customer_to_order`)
3. Aggregates `SUM({net_amount})` from `order`, grouped by the customer key

All three parts are required. If the relationship does not exist, the metric feature fails to resolve.

---

## Filtered Metric Features

Metric features can include filters that narrow the rows before aggregating. This lets you define multiple scoped metrics from the same fact entity without creating separate entity metrics for each.

```yaml
- type: metric
  name: spend_last_30_days_usd
  description: Net revenue from purchases in the last 30 days, in USD
  data_type: number
  source: purchase
  filters:
    - type: sql
      sql: >
        {source}.{purchase_currency} = 'USD'
        AND {source}.{purchase_date} >= CURRENT_DATE - INTERVAL '30 days'
  metric: sum_net_revenue_usd
```

`{source}` in filter expressions refers to the source entity, and `{feature_name}` references features defined on that entity. Filters are applied before aggregation.

Filtered metric features are how you express business-specific aggregations — revenue in a fiscal quarter, active subscriptions, spend from a specific channel — without modifying the underlying entity metric.

---

## Which Join Is Used

By default, metric features use the default join on the relationship between the two entities. To use a non-default join, specify `join_name` on the metric feature. Multiple named joins on a relationship let you compute different metrics through different join paths.

For how joins are defined and named, see [Relationships YAML Reference](../file-types/relationships-yaml.md).

---

## Related Reference

- [Entities](./entities.md) — entity anatomy, the four feature types, how context compounds on entities
- [Entity YAML Reference](../file-types/entity-yaml.md) — field-by-field reference for entity YAML files, including the `metrics:` and `features:` sections
- [Relationships YAML Reference](../file-types/relationships-yaml.md) — how to connect entities and define named joins
- [Lynk SQL](../api/lynk-sql.md) — query-side syntax: how `METRIC('name')` is called from a query, joins, CTEs
