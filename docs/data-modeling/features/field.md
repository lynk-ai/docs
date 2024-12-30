# Field

Field features are great for enrichments from **one-to-one** or **many-to-one** relations.\
It is commonly used to enrich an entity with simple, non aggregate fields from one-to-one related assets or entities.&#x20;

**Main use cases**

1. Add a feature from a data asset that is on the same level of granularity as the entity (one-to-one relationship)
2. Add a feature from a parent entity (many-to-one relationship)

***

## Simple field feature

In this example, we define two simple `field` features for the entity customer:

```yaml
# customer.yml
features: 

- name: team_name
  asset: team
  type: field
  field: name
  filters: null
  
- name: is_US_customer
  asset: db_prod.core.geos
  type: field
  field: iff(geo = 'US', true, false)
  filters: null
```

We added two field features to the entity customer. One from the related data asset "db\_prod.core.geos" and one from the related entity "team"**.**

### `name`

The feature name.&#x20;

### `asset`

The data asset to join in order to enrich our entity with the field feature.&#x20;

In case of a regular data asset, the full path is needed to be specified; "db.schema.name". &#x20;

In case of an enrichment from a related entity, the entity name is needed to be specified and Lynk will automatically reference to it's virtual data asset.

{% hint style="info" %}
`asset` has to be related to our entity - either as a [related data asset](../entities/#related-assets) or as a [related entity](../entities/#related-entities). Lynk will use the `joins` definition to join the asset to our entity when creating the feature.
{% endhint %}

### `type`

The feature type. In case if field features, it should be `field`.

### `field`

The field name of the field we would like to get from the related asset and enrich our entity with it.&#x20;

{% hint style="info" %}
`field` can be any SQL expression which does not include aggregate functions.&#x20;
{% endhint %}

### `filters`

filter the asset

***

## Using a custom join path

explain here how to use a join path to the asset which is not the default one







Customer has one-to-one relationship with organization (each customer has one organization and vice versa). We would like to&#x20;

&#x20;if we would like to enrich the entity "customer" with the name of the sales agent that closed the deal with that customer

Field features are great for one-to-one relations.\
It is commonly used to enrich our entity with simple, non aggregate fields from related assets or entities.

Field suite a **one-to-one**  relationship between the entity and the data asset or entity we create the feature from.

SHOW CODE EXAMPLE
