# Filters

### `filters`

Custom filters to be applied on the data asset.

See the following example:

```yaml
# customer.yml
features: 

- type: field
  name: current_customer_city
  asset: db_prod.core.customer_details_snapshot
  field: city_name
  filters:
  - type: field
    field: end_time
    operator: is
    values:
    - 2999-01-01
```

In the above example we filter the data asset `customer_details_snapshot` to return only rows with `end_time = '2999-01-01'`, meaning current status of the snapshot. This will give us the current city\_name for each customer in that customers snapshot.

### `type` (filters)

The `type` property tells Lynk which method to use for the filter.\
The options for `type` are:

* `sql`
* `field`

A simple YAML-style to define how an entity is related to a data asset.

### `sql` (type)

Use sql code to define how an entity is related to a data asset.\
When setting `type: sql`, you will need to add the `sql` property with the SQL definition of the relation.

See the following example;

```yaml
// customer.yml

related_assets:

  db_prod.core.orders:
    relationship: one-to-many
    joins:
    - name: all_orders
      default: true
      type: sql
      sql:  {source}.id = {destination}.customer_id
```

Using the `sql` type;

`{source}` refers to the entity

`{destination}` refers to the data asset

In the above example, the entity customer has a feature `id` which connects to the orders data asset field `customer_id`

### `fields` (type)

A simple YAML-style to define how an entity is related to a data asset.\
When setting `type: fields`, you will need to add the `fields` property with the fields and the operator that define the relation.

See the following example:

```yaml
// customer.yml

related_assets:

  db_prod.core.device:
    relationship: one-to-one
    joins:
    - name: customer_device
      default: true
      type: fields
      fields: 
      - source: device_id
        destination: id
        operator: equal
```

Using the `fields` type;

`source` refers to the entity

`destination` refers to the data asset

`operator` defines the operator of the relation between the two fields. \
The options for the operator property are:

* equal
* gt
* gte
* lt
* lte

In the above example, the entity customer has a feature `device_id` which connects to the field `id` in the device data asset, using the operator `equal`. \
This translates to `customer.device_id = db_prod.core.device.id`

{% hint style="info" %}
Lynk supports multiple related fields from the source to the destination, enabling joins on more than one field when needed.
{% endhint %}

***
