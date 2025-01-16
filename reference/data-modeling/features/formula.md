# Formula

Formula features are used when we need to create features on top of other features of the same entity. It is commonly used to enrich an entity with more complex calculations that require multiple aggregations or calculations to be done first.

## Simple formula feature

In this example, we define simple `metric` features for the entity `customer`:

```yaml
# customer.yml
features:
  
- type: formula
  name: is_active_customer
  data_type: boolean
  sql: IFF((last_login_date > date_add('day', -30, current_date())) and total_orders > 100, true, false)
  features: 
  - feature: last_login_date
  - feature: total_orders
  
```

On this example, we already have two features on the `customer` level: `last_login_date` and `total_orders`. We use these two features to define wbich customers are active customers.

{% hint style="info" %}
`formula` is a special type of feature, which is not reliant on related data assets or related entities like other feature types, as it creates features based on features of the same entity.
{% endhint %}

### `type`

The feature type. \
In case of formula features, it should be set to `formula`.

### `name`

Give the feature a name.

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

### `sql`&#x20;

The formula definition.&#x20;

Any SQL code applies here as long as:

1. It is based on features already defined on the entity
2. it does not have aggregate functions

{% hint style="warning" %}
In case you have an aggregate function in a formula, you probably need to create another metric feature and then create the formula feature on top of it
{% endhint %}

### `features`&#x20;

A list of the features that were included in the formula `sql` definition.

### `feature`

The feature name for each feature that was included in the formula `sql` definition.
