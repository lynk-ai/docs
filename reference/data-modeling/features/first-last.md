# First-Last

First-Last features are great for enrichments of fields from **one-to-many** relations.\
It is commonly used to enrich an entity with fields of the first or last appearance of a one-to-many related assets or entities.

***

## Simple first-last feature

In this example, we define simple `first-last` features for the entity `customer`:

```yaml
# customer.yml

features:
- type: first_last
  name: last_call_agent_id
  asset: db_prod.core.phone_call_dim
  options:
    method: last
    sort_by: created_at
    field: agent_id
  filters: null
```

### `type`

The feature type. \
In case of first-last features, it should be set to `first_last`.

### `name`

Give the feature a name.

### `asset`

The data asset with the field to be added as feature to our entity.\
`asset` should be the full path: "db.schema.name".

{% hint style="info" %}
`asset` has to be related to our entity (see [related data asset](../entities/related-data-assets.md)).
{% endhint %}

### `join_name` \[optional]

In case of multiple join patterns were defined between an entity and a data asset, `join_name` is used to determine which join path to use for this feature.&#x20;

For more information about using multiple join paths between an entity to a data asset, visit [related data assets](../entities/related-data-assets.md#name-optional) page.

### `options`

The options for the first-last definitions on which field we would like to get and how to sort the related data asset

### `method`

Determines which instance of the data asset to retrieve - the `first` or the `last`, based on the `sort_by` option.

### `sort_by`

The data asset field to sort by.

### `field`

The name of the data asset field to retrieve as the entity feature.

### `filters`

Custom filters to be applied on the data asset. See [filters](../data-assets/filters.md) page for in depth information on how to apply filters.

