# Metric

Metric features are great for aggregations from **one-to-many** relations.\
It is commonly used to enrich an entity with aggregated fields from one-to-many related assets or entities.

***

## Simple Metric feature

A Metric feature is simply applying a [measure](../data-assets.md#measures) aggregation to the level of an entity.

In this example, we define two simple `metric` features for the entity `customer`:

```yaml
# customer.yml
features:

- type: metric
  name: total_orders
  asset: db_prod.core.orders
  measure: total_sales
  filters: null
  
- type: metric
  name: count_orders
  asset: db_prod.core.orders
  measure: total_successful_orders
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

### `field`

The name of the field we would like to get from the related asset, in order to enrich our entity.&#x20;

{% hint style="info" %}
`field` can be any SQL expression which does not include aggregate functions.&#x20;
{% endhint %}

### `filters`

Add a custom filter. See [filters](../filters.md) page for in depth information on this.

***

## Create field features from related entities

Just as we can add features from related data assets, it is possible to create features on top of other entities features.

In case of an enrichment from a related entity, the entity name should be specified as the `asset`, and Lynk will reference to it's virtual data asset. The rest of the parameters remain the same as in creating field features from regular data assets.

See the below example:

```yaml
# customer.yml
features: 

- type: field
  name: team_name
  asset: team
  field: name
  filters: null
```

{% hint style="info" %}
The `asset` has to be related to our entity (see [related entities](../entities/related-entities.md)). Lynk will use the `joins` definition to join the related entity to our entity when creating the feature.
{% endhint %}

***

## Using a custom join path

explain here how to use a join path to the asset which is not the default one





Customer has one-to-one relationship with organization (each customer has one organization and vice versa). We would like to&#x20;

&#x20;if we would like to enrich the entity "customer" with the name of the sales agent that closed the deal with that customer

Field features are great for one-to-one relations.\
It is commonly used to enrich our entity with simple, non aggregate fields from related assets or entities.

Field suite a **one-to-one**  relationship between the entity and the data asset or entity we create the feature from.

SHOW CODE EXAMPLE
