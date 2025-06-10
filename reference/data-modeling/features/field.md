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
  data_type: number
  filters: null
  
- type: field
  name: is_us_customer
  asset: db_prod.core.geos
  join_name: login_geo
  data_type: boolean
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
`asset` has to be related to our entity (see [related data asset](../relationships/related-data-assets.md)).
{% endhint %}

### `join_name` \[optional]

In case multiple join patterns are defined between an entity and a data asset, `join_name` is used to determine which join path to use for a specific feature.

In the example above, we are joining the entity `customer` to the `geos` asset using the `login_geo` join path name. For more information about using multiple join paths between an entity and a data asset, visit the [related data assets](../relationships/related-data-assets.md#name-optional) page.

### `data_type` \[optional]

Specify the feature data type. \
If no data\_type specified, Lynk will assume the data type is `string`.

The options for data types are:

`string`

For any type of string data type

`number`

For any type of number data type. For example: integer, float, decimal etc..

`bool`

For boolean data type.

`datetime`&#x20;

For any type of time-based data type. For example: date, timestamp, datetime etc..

### `field`

The name of the field we would like to get from the related asset, in order to enrich our entity.&#x20;

{% hint style="info" %}
`field` can be any SQL expression which does not include aggregate functions.&#x20;
{% endhint %}

### `filters`

Custom filters to be applied on the data asset. See [filters](filters.md) page for in depth information on how to apply filters.&#x20;

## Understanding Field Features

In case we have a **one-to-one** relationship between a Data Asset and an Entity, and we need to enrich the entity with a field from the Data Asset **-** we can simply define which field to enrich the entity by.

To better understand how Field features work, look the following diagram;

<figure><img src="../../../.gitbook/assets/image (6).png" alt=""><figcaption><p>Field Feature Diagram</p></figcaption></figure>

The above diagram shows an example when a customer (entity) has one nation (data asset). That means, each `customer` can be associated with only one row in `db.schema.nations`.

In this case, we took the field `nation_name` , and added it to the customer entity as a feature.
