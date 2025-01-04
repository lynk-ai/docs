# Filters

Filtering data assets is simple and can be done on a feature definition level.

See the following example:

```yaml
# customer.yml
features: 

- type: metric
  name: orders_count_2025
  asset: db_prod.core.orders
  measures: count_orders
  filters:
  - type: sql
    sql: order_date >= '2025-01-01' and order_date <= 2025-12-31'

- type: metric
  name: successful_orders_count
  asset: db_prod.core.orders
  measures: count_orders
  filters:
  - type: fields
    field: order_status
    operator: equal
    values:
    - success
```

### `filters`

Filters are defined in the `filters` property. This is an array that can get as many filter inputs as needed, where each input can be defined as a SQL statement or a YAML statement (`type` : `sql` / `field`).&#x20;

{% hint style="info" %}
When defining multiple `filters` inputs, Lynk will chain these filters with an `and` statement between them and then apply them : filter\_1 and filter\_2 and filter\_3&#x20;
{% endhint %}

### `type`

Use the filters `type` property to determine which method to use for the filter.\
The options for `type` are:

* `sql`
* `field`

### `sql` (type)

Use sql code to define how a data asset should be filtered.\
When setting `type: sql`, you will need to add the `sql` property with the SQL definition of the relation.

In this example, we use SQL to filter the `orders` data asset to retrieve only records where the `order_date` field is in 2025 for the feature `orders_count_2025`.

```yaml
# customer.yml
features: 

- type: metric
  name: orders_count_2025
  asset: db_prod.core.orders
  measures: count_orders
  filters:
  - type: sql
    sql: order_date >= '2025-01-01' and order_date <= 2025-12-31'
```

### `fields` (type)

Use simple YAML-style to define how a data asset should be filtered.\
When setting `type: fields`, you will need to add the `fields` property with the fields and the operator that define the relation.

See the following example:

```yaml
// customer.yml

featurs: 

- type: metric
  name: successful_orders_count
  asset: db_prod.core.orders
  measures: count_orders
  filters:
  - type: fields
    field: order_status
    operator: equal
    values:
    - success
```

In the above example we filter the data asset `db_prod.core.orders` to retrieve only records where the `value` of the `field` order\_status equals to 'success'.

Using the `filters` type `fields`, the following properties should be specified:

### `field`

The field name in the data asset, which we would like to apply a filtering logic on.

### `Operator`

The operator to be applied on the `field` , that defines the logic of which values we would like to filter in the results. The options for the operator property are:

#### `equals`

Equals to.\
"A `equals` B" translates to "A `=` B".

#### `is not`

Does not Equals to.\
"A `is not` B" translates to "A `!=` B" (or "A `<>` B").

#### `gt`

Greater than.\
"A `gt` B" translates to "A `>` B".

#### `gte`

Greater than or equals to.\
"A `gte` B" translates "to a `>=` b".

#### `lt`

Lower than.\
"A `lt` B" translates "to a `<` b".

#### `lte`

Lower than or equals to.\
"A `lte` B" translates "to a `<=` b".

#### `is_set`

The value is not NULL.\
"A `is_set`" translates to "A `is not null`".

#### `is_not_set`

The value is NULL.\
"A `is_not_set`" translates to "A `is null`".

***
