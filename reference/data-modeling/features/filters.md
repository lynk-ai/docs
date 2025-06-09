# Filters

When creating features on an entity, it is possible to filter the entities and data assets we create feature from using the `filters` property.

{% hint style="info" %}
This page is about adding filters to feature definitions.

Filters can be also applied on an entity using the `WHERE` clause, on the consumption level.\
For more information on this, visit [SQL API](../../consume-and-apis/sql-api.md) and [SQL REST API](../../consume-and-apis/sql-rest-api.md) and look for the `WHERE` clause.
{% endhint %}

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
    sql: "{asset}.{order_date} >= '2025-01-01' and {asset}.{order_date} <= '2025-12-31'"

- type: metric
  name: successful_orders_count
  asset: db_prod.core.orders
  measures: count_orders
  filters:
  - type: fields
    field: order_status
    operator: is
    values:
    - success
```

### `filters`

Filters are defined in the `filters` property. This is an array that can get as many filter inputs as needed, where each input can be defined as a SQL statement or a YAML statement (`type` : `sql` / `field`).

{% hint style="info" %}
When defining multiple `filters` inputs, Lynk will chain these filters with an `and` statement between them and then apply them : filter\_1 and filter\_2 and filter\_3
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
    sql: "{asset}.{order_date} >= '2025-01-01' and {asset}.{order_date} <= '2025-12-31'"
```

### `fields` (type)

Use simple YAML-style to define how a data asset should be filtered.\
When setting `type: fields`, you will need to add the `fields` property with the fields and the operator that define the relation.

#### Example (`fields`):

```yaml
# customer.yml

features: 

- type: metric
  name: successful_orders_count
  asset: db_prod.core.orders
  measures: count_orders
  filters:
  - type: fields
    field: order_status
    operator: is
    values:
    - success
```

In the above example we filter the data asset `db_prod.core.orders` to retrieve only records where the `value` of the `field` order\_status is 'success'.

Using the `filters` type `fields`, the following properties should be specified:

### `field`

The field name in the data asset, which we would like to apply a filtering logic on.

### `Operator`

The operator to be applied on the `field` , that defines the logic of which values we would like to filter in the results. The options for the operator property are:

#### `is`

Equals to.\
"A `equals` B" translates to "A `=` B".

Usage example (`is` operator):

```yaml
...
  filters:
  - type: fields
    field: order_status
    operator: is
    values:
    - success
```

Retrieves only records where the `value` of the `field` order\_status **is** 'success'.

#### `is_not`

Does not equal to.\
"A `is_not` B" translates to "A `!=` B" (or "A `<>` B").

Usage example (`is_not` operator):

```yaml
...
  filters:
  - type: fields
    field: order_status
    operator: is_not
    values:
    - success
```

Retrieves only records where the `value` of the `field` order\_status **is not** 'success'.

#### `between`

Between two values\
"A `between` B and C" translates to "A `>=` B and A `<=` C

Usage example (`between` operator):

```yaml
...
  filters:
  - type: fields
    field: order_date
    operator: between
    values:
    - 2024-01-01
    - 2025-01-01
```

Retrieves only records where the `values` of the `field` order\_date are **between** '2024-01-01' and '2025-01-01'.

Note that the order matters - the first value is the lower bound and the second value is the upper bound of the `between` operator.

#### `gt`

Greater than.\
"A `gt` B" translates to "A `>` B".

Usage example (`gt` operator):

```yaml
...
  filters:
  - type: fields
    field: order_amount
    operator: gt
    values:
    - 100
```

Retrieves only records where the `value` of the `field` order\_amount is **greater than** 100.

#### `gte`

Greater than or equals to.\
"A `gte` B" translates "to a `>=` b".

Usage example (`gte` operator):

```yaml
...
  filters:
  - type: fields
    field: order_amount
    operator: gte
    values:
    - 100
```

Retrieves only records where the `value` of the `field` order\_amount is **greater than or equals** 100.

#### `lt`

Lower than.\
"A `lt` B" translates "to a `<` b".

Usage example (`lt` operator):

```yaml
...
  filters:
  - type: fields
    field: order_amount
    operator: lt
    values:
    - 100
```

Retrieves only records where the `value` of the `field` order\_amount is **lower than** 100.

#### `lte`

Lower than or equals to.\
"A `lte` B" translates "to a `<=` b".

Usage example (`lte` operator):

```yaml
...
  filters:
  - type: fields
    field: order_amount
    operator: lte
    values:
    - 100
```

Retrieves only records where the `value` of the `field` order\_amount is **lower than or equals** 100.

#### `is_set`

The value is not NULL.\
"A `is_set`" translates to "A `is not null`".

Usage example (`is_set` operator):

```yaml
...
  filters:
  - type: fields
    field: order_amount
    operator: is_set
```

Retrieves only records where the `value` of the `field` order\_amount is **set**. Meaning, order\_amount **is not Null**.

Note that in the case of the operator `is_set` there is no need to add the `values` property.

#### `is_not_set`

The value is NULL.\
"A `is_not_set`" translates to "A `is null`".

Usage example (`is_not_set` operator):

```yaml
...
  filters:
  - type: fields
    field: order_amount
    operator: is_not_set
```

Retrieves only records where the `value` of the `field` order\_amount is **not set**. Meaning, order\_amount **is Null**.

Note that in the case of the operator `is_not_set` there is no need to add the `values` property.

### `Values`

The values to accept.\
Lynk will apply the `operator` logic to the `field` and the given `values`. The records that will return are the records where that filtering logic returns "true" (see [this example](filters.md#example-fields))\\

***
