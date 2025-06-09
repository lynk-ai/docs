# Measures

Measures are reusable and governed components that define how an **entity** or a **data asset** should be aggregated.&#x20;

Lynk applies the measure logic in two scenarios:

1. Once a feature of type [metric](features/metric.md) is created or consumed
2. Once aggregating (rolling-up) an entity by some of it's features and using the MEASURE() function

### Defining Measures

Measures are definitions of how aggregate functions should be applied to features and fields&#x20;

```yaml
# db_prod.core.orders.yml

measures:
- name: total_order_amount
  description: sum of order amount
  sql: sum({total_amount})
```

### `Name`

Give the measure a name.\
This will be used when creating [metric](features/metric.md) features and also will be shown on the Studio UI. It is recommended to give measures informative names that indicate their purpose.

### `Description` \[optional]

Describe the measure.\
It is recommended to give measures informative names that indicate their purpose - for other team members to be able to reuse the measure and for AI apps as well.

### `SQL`

The measure definition. It should be composed of an aggregate function and a field.\
It is possible to chain multiple aggregate functions and / or multiple fields, just like you would do on plain SQL when needed.

{% hint style="info" %}
Lynk is SQL-first, meaning anything that would work on plain SQL will work with Lynk as well. You can type any SQL aggregate function compatible with your query engine, and Lynk will apply that as the measure definition and chain it to the query engine.

Examples: `SUM` , `COUNT` , `MIN` , `MAX` , `COUNT DISTINCT` , `APPROX_PERCENTILE` etc
{% endhint %}

#### Some more examples:

```yaml
# db_prod.core.orders.yml

measures:

- name: count_orders
  description: count of orders
  sql: count(1)

- name: total_order_amount
  description: sum of order amount
  sql: sum({total_amount})

- name: successful_order_amount
  description: sum of successful orders amount
  sql: sum(IFF({order_status} = 'success', {total_amount}, 0))
```
