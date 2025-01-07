# Data assets

Data assets are tables and views from the underlying data source (mostly a warehouse). Data assets can be [related](../entities/related-data-assets.md) to entities and they are being used for creating entity features.

{% hint style="info" %}
It is recommended to use a transformation tool like dbt to transform raw data into dimensional model with DIM and FACT tables, and expose that dimensional model to Lynk Semantic Layer.
{% endhint %}

***

## Data assets YAML file

Data assets can be modified either via code or via Lynk Studio UI.\
The below example shows a YAML file for the data asset db\_prod.core.orders

See the following example:

```yaml
# db_prod.core.orders.yml

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

{% hint style="info" %}
Data assets are stored on the Lynk [Graph DB](broken-reference) during the [discovery](broken-reference) process. If changes are made to a data asset within Lynk (e.g adding fields / measures), a YAML file will be created as shown on the example above.

Once a YAML file gets created for a data asset, the asset is now stored in Git as well as on the Graph DB. Lynk will take care for syncing the Graph DB and your Git repository. See more on Lynk [Graph](broken-reference)[ DB](broken-reference) here.
{% endhint %}

### `asset`

Data Asset name and location as it appears in your underlying Data Warehouse (`db.schema.name`)

### `key`

The asset key field (primary key). \
It is important to state the correct data asset key in order to avoid duplications and errors. Lynk will automatically find and suggest data asset keys after the [discovery](broken-reference) process is completed.

### `business_key` \[optional]

Sometimes the key is just "`id`". \
In such cases, some combination of other fields might represent the level of granularity of that data asset, and make more sense business wise. We call this combination of fields the `business_key` of that asset.

{% hint style="info" %}
Business keys help us be clear on what this data asset is about, and what each row represents.  &#x20;
{% endhint %}

### `defaults`

Holds the defaults for the data asset.  See [default time field](./#default-time-field) for example.

### `time_field` \[optional]

It is recommended to choose a default time field for each data asset. Lynk will use the default time field to aggregate and filter time-related queries on features.

For example, if we have a data asset for orders db\_prod.core.orders and we set the `default_time_field` to be order\_date, Lynk will use this field for time-based aggregations by default.

{% hint style="info" %}
In case a data asset has no default `time_field` , and no other time field will be chosen on the feature definition, Lynk will not skip aggregating that feature on any time level (the aggregation will be on "all" time)
{% endhint %}

### `Measures`

Measures are reusable components that define how the data asset fields should be aggregated. Lynk applies the measure logic once a feature of type [metric](../features/metric.md) feature is created and consumed.

In practice, measures are definitions of how aggregate functions should be applied to fields;

```yaml
# db_prod.core.orders.yml

measures:

- name: total_order_amount
  description: sum of order amount
  sql: sum(total_amount)
```

### `Name`

Give the measure a name. \
This will be used when creating [metric](../features/metric.md) features and also will be shown on the Studio UI. It is recommended to give measures informative names that indicate their purpose.

### `Description` \[optional]

Describe the measure.\
It is recommended to give measures informative names that indicate their purpose - for other team members to be able to reuse the measure and for AI apps as well.&#x20;

### `SQL`

The measure definition. It should be composed of an aggregate function and a field.  \
It is possible to chain multiple aggregate functions and / or multiple fields, just like you would do on plain SQL when needed.&#x20;

{% hint style="info" %}
Lynk is SQL-first, meaning anything that would work on plain SQL will work with Lynk as well. You can type any SQL aggregate function compatible with your query engine, and Lynk will apply that as the measure definition and chain it to the query engine.

Examples: `SUM` , `COUNT` , `MIN` , `MAX` , `COUNT DISTINCT` , `APPROX_PERCENTILE` etc&#x20;
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
  sql: sum(total_amount)

- name: successful_order_amount
  description: sum of successful orders amount
  sql: sum(IFF(order_status = 'success', total_amount, 0))
```

***

## Virtual data assets

Virtual data asset are data assets that live "virtually" within Lynk. Meaning, there is no materialized asset on the underlying data source. A virtual data assets is created for each entity within Lynk, where the entity is the "asset" and it's features are the "fields".&#x20;

{% hint style="info" %}
Measures can be added to virtual data assets, just like in regular data assets.
{% endhint %}

#### Usage of virtual data assets

virtual data assets are mainly used for [chaining features](../chaining-features.md) - creating entity features based on features of other related entities.
