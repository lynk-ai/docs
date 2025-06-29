# Metric

Metric features are great for aggregations from **one-to-many** relations.\
It is commonly used to enrich an entity with aggregated fields from one-to-many related assets or entities.

{% hint style="info" %}
When we create a metric feature, we apply a [measure](../data-assets.md#measures) aggregation to the level of an entity.
{% endhint %}

***

## Simple metric feature

In this example, we define simple `metric` features for the entity `customer`:

```yaml
# customer.yml

features:
  
- type: metric
  name: orders_count
  asset: db_prod.core.orders
  measure: orders_count
  data_type: number
  filters: null

- type: metric
  name: successful_orders_count
  asset: db_prod.core.orders
  measure: orders_count
  data_type: number
  time_field: order_date
  filters:
  - type: field
    field: order_status
    operator: is
    values:
    - success
```

### `type`

The feature type.\
In case of metric features, it should be set to `metric`.

### `name`

Give the metric feature a name.

### `asset`

The data asset with the measure to be aggregated to the level of our entity.\
`asset` should be the full path: "db.schema.name".

{% hint style="info" %}
`asset` has to be related to our entity (see [related data asset](../relationships/related-data-assets.md)).
{% endhint %}

### `join_name` \[optional]

In case multiple join patterns are defined between an entity and a data asset, `join_name` is used to determine which join path to use for a specific feature.

For more information about using multiple join paths between an entity and a data asset, visit the [related data assets](../relationships/related-data-assets.md#name-optional) page.

### `data_type` \[optional]

Specify the feature data type. \
If no data\_type specified, Lynk will assume the data type is `string`.

The options for data types are:

`string`

For any type of string data type

`number`

For any type of number data type. For example: integer, float, decimal etc..

`datetime`&#x20;

For any type of time-based data type. For example: date, timestamp, datetime etc..

`bool`

For boolean data type.

### `time_field` \[optional]

Specifies which asset time field to use in case of time-based aggregation is applied to the metric. If not specified, Lynk will use the asset's [default `time_field`](../data-assets.md#time_field-optional).

See [time aggregation](../time-aggregation.md) for more information on how time fields are being used for time-based metric aggregations.

### `measure`

The name of the measure we would like to aggregate from the related asset to the level of our entity.

{% hint style="info" %}
Measures are defined on a data asset level. See [measures](../data-assets.md#measures) for in depth information on this.
{% endhint %}

### `filters`

Custom filters to be applied on the data asset. See [filters](filters.md) page for in depth information on how to apply filters.

## Understanding Metric features

In case we have a **many-to-one** relationship between a Data Asset and an Entity, and we need to enrich the entity with some aggregation from the Data Asset **-** we can define which [measure](../measures.md) to enrich the entity by.

To better understand how Field features work, look the following diagram;

<figure><img src="../../../.gitbook/assets/image (8).png" alt=""><figcaption><p>Metric Feature Diagram</p></figcaption></figure>

The above diagram shows an example when a customer (entity) has many orders (data asset). That means, each `customer` can be associated with many rows in `db.schema.orders`.

In this case, we took the measure `total_price` which translates to the aggregate definition `SUM(total_price)` and adding it to the customer entity as a metric feature.
