# Metric

Metric features are great for aggregations from **one-to-many** relations.\
It is commonly used to enrich an entity with aggregated fields from one-to-many related assets or entities.

{% hint style="info" %}
When we create a metric feature, we apply a [measure](../data-assets/#measures) aggregation to the level of an entity.
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
  filters: null

- type: metric
  name: successful_orders_count
  asset: db_prod.core.orders
  measure: orders_count
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
`asset` has to be related to our entity (see [related data asset](../entities/related-data-assets.md)).
{% endhint %}

### `join_name` \[optional]

In case of multiple join patterns were defined between an entity and a data asset, `join_name` is used to determine which join path to use for this feature.&#x20;

For more information about using multiple join paths between an entity to a data asset, visit [related data assets](../entities/related-data-assets.md#name-optional) page.

### `measure`

The name of the measure we would like to aggregate from the related asset to the level of our entity.

{% hint style="info" %}
Measures are defined on a data asset level. See [measures](../data-assets/#measures) for in depth information on this.
{% endhint %}

### `filters`

Custom filters to be applied on the data asset. See [filters](../data-assets/filters.md) page for in depth information on how to apply filters.
