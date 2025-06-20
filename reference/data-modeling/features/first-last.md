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
  data_type: string
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

Specifies which asset time field to use in case of time-based aggregation is applied to the first-last feature. If not specified, Lynk will use the asset's [default `time_field`](../data-assets.md#time_field-optional).

See [time aggregation](../time-aggregation.md) for more information on how time fields are being used for time-based feature aggregations.

### `options`

The options for the first-last definitions on which field we would like to get and how to sort the related data asset

### `method`

Determines which instance of the data asset to retrieve - the `first` or the `last`, based on the `sort_by` option.

### `sort_by`

The data asset field to sort by.

### `field`

The name of the data asset field to retrieve as the entity feature.

### `offset`

Use `offset` to choose the second, third or other field values with an offset from the start or from the end of the sorted list

#### Offset - Example 1

Enriching the `customer` entity with the **`order_status`** of the **third** order, ordered by `created_at`:

```yaml
# customer.yml

features:
- type: first_last
  name: second_order_status
  data_type: string
  asset: db_prod.core.orders
  options:
    method: first
    sort_by: created_at
    field: order_status
    offset: 3
  filters: null
```

#### Offset - Example 2

Enriching the `customer` entity with the **`order status`** of the **second** order from the last (one before the last order), ordered by `created_at`:

```yaml
# customer.yml

features:
- type: first_last
  name: second_order_status
  data_type: string
  asset: db_prod.core.orders
  options:
    method: last
    sort_by: created_at
    field: order_status
    offset: 2
  filters: null
```

### `filters`

Custom filters to be applied on the data asset. See [filters](filters.md) page for in depth information on how to apply filters.

***

## Understanding First-Last Features

In case we have a **many-to-one** relationship between a Data Asset and an Entity, and we need to enrich the entity with a field from the Data Asset **without aggregating it -** we can't just take the field - we need to define which occurrence to take. This is when we should use first-last features.

To better understand how First-Last features work, look the following diagram;

<figure><img src="../../../.gitbook/assets/image (1) (1).png" alt=""><figcaption><p>First Last Feature Diagram</p></figcaption></figure>

The above diagram shows an example when a customer (entity) has many orders (data asset). That means, each `customer` may be associated with more than one row in `db.schema.orders`.

In this case, we took the field `total_price` of the **last** order, sorted by `order_date`, and added it to the customer entity as a feature.
