# Metric

Metric features are great for aggregations from **one-to-many** relations.\
It is commonly used to enrich an entity with aggregated fields from one-to-many related assets or entities.

***

## Simple Metric feature

A Metric feature is simply applying a [measure](../data-assets/#measures) aggregation to the level of an entity.

In this example, we define simple `metric` features for the entity `customer`:

```yaml
# customer.yml
features:
  
- type: metric
  name: total_logins
  asset: db_prod.core.fact_logins
  measure: logins_count
  filters: null

- type: metric
  name: orders_count
  asset: db_prod.core.orders
  measure: orders_count
  filters: null
```

### `type`

The feature type. \
In case of metric features, it should be set to `metric`.

### `name`

Give the feature a name.&#x20;

### `asset`

The data asset with the field to be added as feature to our entity.\
`asset` should be the full path: "db.schema.name".

{% hint style="info" %}
`asset` has to be related to our entity (see [related data asset](../entities/#related-assets)). \
Lynk will use the `joins` definition to join the asset to our entity when creating the feature.
{% endhint %}

### `measure`

The name of the measure we would like to aggregate from the related asset to the level of our entity.&#x20;

### `filters`

Custom filters to be applied on the data asset. See [filters](../data-assets/filters.md) page for in depth information on how to apply filters.

***

## Time aggregations

Lynk separates feature business logic from time granularity.&#x20;

There is no need to create multiple features with the same business logic and different time granolarity.&#x20;





***



## Create metric features from related entities

Just as we can add features from related data assets, it is possible to create features from entities.

In case of a creating a metric from a related entity, the entity name should be specified as the `asset`. The rest of the parameters remain the same as in creating metric features from regular data assets.

See the below example:

```yaml
# customer.yml
features: 

- type: metric
  name: total_
  asset: team
  field: name
  filters: null
```

{% hint style="info" %}
The `asset` has to be related to our entity (see [related entities](../entities/related-entities.md)). Lynk will use the `joins` definition to join the related entity to our entity when creating the feature.
{% endhint %}

***

