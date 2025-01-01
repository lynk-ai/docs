# Field

Field features are great for entity enrichments from **one-to-one** or **many-to-one** relations. It is commonly used to enrich an entity with simple, non aggregate fields from related assets or entities.

**Main use cases**

1. Add a field feature from a data asset with the same level of granularity as the entity (one-to-one relationship)
2. Add a field feature from a related entity with one-to-one relationship
3. Add a feature from a parent entity (many-to-one relationship)

***

## Simple field feature

In this example, we define two simple `field` features for the entity `customer`:

```yaml
# customer.yml
features: 

- type: field
  name: organization_size
  asset: db_prod.core.organizations
  field: size
  filters: null
  
- type: field
  name: is_US_customer
  asset: db_prod.core.geos
  field: iff(name = 'US', true, false)
  filters: null
```

### `type`

The feature type. \
In case of field features, it should be set to `field`.

### `name`

Give the field feature a name.&#x20;

### `asset`

The data asset with the field to be added as feature to our entity.\
`asset` should be the full path: "db.schema.name".

{% hint style="info" %}
`asset` has to be related to our entity (see [related data asset](../entities/#related-assets)).
{% endhint %}

### `field`

The name of the field we would like to get from the related asset, in order to enrich our entity.&#x20;

{% hint style="info" %}
`field` can be any SQL expression which does not include aggregate functions.&#x20;
{% endhint %}

### `filters`

Custom filters to be applied on the data asset. See [filters](../data-assets/filters.md) page for in depth information on how to apply filters.&#x20;

***

## Create field features from related entities

Lynk supports creating features based on related entities features.\
In this case, the `asset` property should be the entity name. The rest of the feature properties remain the same as in creating field features from regular data assets.

{% hint style="info" %}
This is a powerful feature that allows creating robust ETLs with Lynk's well structured data modeling framework. See [chaining features](chaining-features.md) for in depth information about this.
{% endhint %}



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
The entity we refer to as `asset` has to be related to our entity (see [related entities](../entities/related-entities.md)).
{% endhint %}

***

