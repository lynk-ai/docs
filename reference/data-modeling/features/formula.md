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
  sql: IFF(({last_login_date} > date_add('day', -30, current_date())) and {total_orders} > 100, true, false)
```

On this example, we already have two features on the `customer` level: `last_login_date` and `total_orders`. We use these two features to define which customers are active customers.

{% hint style="info" %}
`formula` is a special type of feature, which is not reliant on related data assets or related entities like other feature types, as it creates features based on features of the same entity.
{% endhint %}

### `type`

The feature type.\
In case of formula features, it should be set to `formula`.

### `name`

Give the feature a name.

### `data_type` \[optional]

Specify the feature data type.\
If no data\_type specified, Lynk will assume the data type is `string`.

The options for data types are:

`string`

For any type of string data type

`number`

For any type of number data type. For example: integer, float, decimal etc..

`bool`

For boolean data type.

`datetime`

For any type of time-based data type. For example: date, timestamp, datetime etc..

### `sql`

The formula definition.

Any SQL code applies here as long as:

1. It is based on features already defined on the entity
2. it does not have aggregate functions

Referencing a feature in the SQL is done by using `{FEATURE_NAME}`

{% hint style="warning" %}
In case you have an aggregate function in a formula, you probably need to create another metric feature and then create the formula feature on top of it
{% endhint %}

***

## Understanding Formula Features

In case we need to create a new feature which is composed by other features of an Entity, we can use the **Formula** feature type.&#x20;

{% hint style="info" %}
Unlike field, metric and first-last features, which are built by enriching an entity from other data assets or other entities, formula features are meant for enriching an entity from features of that same entity.
{% endhint %}

To better understand how Formula features work, look the following diagram;

<figure><img src="../../../.gitbook/assets/image (9).png" alt=""><figcaption><p>Formula Feature Diagram</p></figcaption></figure>

The above diagram shows an example when a `customer` (entity) already has two existing features `last_order_date` and `total_orders`. We can create a new **Formula** feature `is_active_customer` as a composition of the existing features `last_order_date` and `total_orders`.
