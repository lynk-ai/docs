# Data assets

Data assets are tables and views in your data warehouse. It can be from any layer - from raw data to aggregated tables.&#x20;

It is recommended that you would use a transformation tool like dbt to transform your raw data into a clean and clear dimensional model with DIM and FACT tables - and expose that dimensional model to lynk Semantic Layer.&#x20;

Within Lynk, you can create the logical business layer that connects all the different DIM tables, connects between DIM and FACT tables to create aggregations and First-Last features and more complex features - resulting in one connected, clear and governed source of truth.

```yaml
// Some code

asset: db_prod.core.orders

key: order_id

business_key: []

defaults:
  time_field: order_date

measures:
- name: count_orders
  description: count of orders
  sql: count(1)
- name: total_order_amount
  description: sum of order amount
  sql: sum(total_amount)

```

### Asset

Data Asset name and location (`db.schema.name`)

### Key

The asset key field (primary key). \
It is important to state the correct data asset key in order to avoid duplications and errors. Lynk will automatically find and suggest data asset keys after the [discovery](../../discovery.md) process is completed

### Business key

Sometimes the key is just "`id`", and there is some combination of fields that represent the true level of granularity of that table (what is the meaning of each row). In such cases, we can use the `business_key` and pass it these fields, so it will be clear what this data asset is about, and what each row represents.  &#x20;

### Default time field

It is highly recommended to choose a default time field for each data asset. Lynk will use the default time field to aggregate and filter time-related queries.&#x20;

For example, if we have a data asset for orders db\_prod.core.orders and we set the default\_time\_field to be "order date" - from now on, unless stated otherwise - this will be the field we aggregate by for date calculations&#x20;

### Measures

Measures are reusable components that define how one or more fields should be aggregated. Lynk applies the measure logic once a [metric](../features/metric.md) feature is created for a specific entity.

Lynk is SQL-first, meaning anything that would work on plain SQL will work with Lynk as well. You can type any SQL aggregate function (from your query engine) and Lynk will apply that as the measure definition. Examples: `SUM` , `COUNT` , `MIN` , `MAX` , `COUNT DISTINCT` , `APPROX_PERCENTILE` etc&#x20;

Required Define measures via YAML files

**name**

measure name

Description

measure descriptiom

SQL

measure descriptiom
