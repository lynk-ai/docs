# Related assets

Each entity has related [data assets](../data-assets/), from which we can create features. \
The relation between an entity and a data asset is defined on the entity YAML file, under `related_assets`.&#x20;

\[ADD here a diagram showing an entity and related assets]

## Simple entity-to-asset relation

In this example, we define the relations between the entity `customer` to the data assets `db_prod.core.orders` and `db_prod.core.device`&#x20;

```yaml
// customer.yml

related_assets:

  db_prod.core.orders:
    relationship: one-to-many
    joins:
    - name: all_orders
      default: true
      type: sql
      sql:  {source}.customer_id = {destination}.customer_id

  db_prod.core.device:
    relationship: one-to-one
    joins:
    - name: customer_device
      default: true
      type: fields
      fields: 
      - source: device_id
      - destination: id
      - operator: equal
```

### Related assets

The `related_assets` property holds all the assets that relate to the entity.&#x20;

Each data asset element has to include the full path to the data asset as it in the origin data warehouse - db name, schema name and asset name (`db.schema.name`)

### Relationship

Sets the `Relationship` between the entity and the data asset.\
The options for the Relationship property are:

* `one-to-one`
* `one-to-many`
* `many-to-many`
* `many-to-one`

The direction of the relationship is entity-to-asset. Meaning, in our example, the entity is `customer` and the first data asset is `order`. So in this case a customer has many orders.&#x20;

Lynk will use the relationship property to suggest the correct data assets when creating new features on the entity level. For example, when creating a metric - Lynk will only suggest one-to-many related assets (as metrics are aggregations of measures to the level of an entity).

### Joins

Define how the entity and the data asset should be joined. \
The `joins` property is an array. Lynk supports multiple join paths between an entity and a data asset

### **name \[optional]**

Give the join path a name.&#x20;

This property is optional. \
If you choose not to name a join path, lynk will consider the name as "default".\
Note that in case another join path will be added, naming it will be mandatory as there can be only one "default" join path name.

The name property will be used when creating a feature. \
In case there is more than one join path between an entity and a data asset, you will be able to tell Lynk how connect the entity to the related asset by using the join path name.

### **default \[optional]**

The `default` property takes boolean values (`true` / `false`).

There can be only one default join path between an entity and a specific data asset. Lynk will use the default join path when creating features for this entity, unless a name of another join path will be stated.

In case there is more than one join path between an entity and a data asset, you will be able to tell Lynk how connect the entity to the related asset by using the join path name.

### type

The type property will be used to tell Lynk using which method you define the join path. \
The options for `type` are

* `sql`
* `fields`
* `lookup`

### `sql` (type)

Use plain sql to define how an entity is related to a data asset.\
When setting `type: sql`, you will need to add the `sql` property with the SQL definition of the relation.

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

Use a simple YAML-style way to define how an entity is related to a data asset.\
When setting `type: fields`, you will need to add the `fields` property with the fields and the operator that define of the relation.

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
      - destination: id
      - operator: equal
```

Using the `fields` type;

`source` refers to the entity

`destination` refers to the data asset

`operator` defines the operator of the relation between the two fields. the options for the operator property are:

* equal
* gt
* gte
* lt
* lte

In the above example, the entity customer has a feature `id` which connects to the orders data asset field `customer_id`

{% hint style="info" %}
When adding related data assets to an entity using the Studio UI, lynk will add these relations to the relevant YAML file automatically, using join type `fields`.
{% endhint %}

### `lookup` (type)

## Multiple join paths between entity-to-asset

It's often common that there is more than one way to join two tables.&#x20;

{% hint style="info" %}
For example, imagine we are a b2b company with a sales department\
It's common that the sales agent that closed the deal (sale) is not the same agent that renewed the contract with the customer a few years later. What if we want to know for each customer, who was the agent on each occasion? \
A simple way to do that is to join customers to agents twice - one on sale\_agent and another join on renew\_agent (see below)
{% endhint %}

Lynk supports multiple join paths between an entity and a data asset as follows:&#x20;

```yaml
// customer.yml

related_assets:
  db_prod.core.agents:
    relationship: many-to-many
    joins:
    - name: sale_agent
      default: true
      type: fields
      fields:
      - source: sale_agent_id
        destination: id
        operator: equal
    - name: deactivate_agent
      default: false
      type: fields
      fields:
      - source: renew_agent_id
        destination: id
        operator: equal
```

{% hint style="info" %}
note that each join path has a `name` and only one of them can be set to `default`
{% endhint %}



```yaml
// customer.yml

name: customer

description:

key_table: demo_dev.tpch_sf1.customer

aliases: []

features: []

related_assets:
  demo_dev.tpch_sf1.customer:
    relationship: one-to-one
    joins:
    - name: all_customers
      default: true
      type: fields
      fields:
      - entity_field: customer_id
        asset_field: customer_id
        operator: equal

  demo_dev.tpch_sf1.orders:
    relationship: one-to-one
    joins:
    - name: all_orders
      default: true
      type: sql
      sql:  {source}.customer_id = {destination}.customer_id

  lynk.core.payment:
    relationship: one-to-one
    joins:
    - name: all_payments
      default: true
      type: lookup
      lookup:
      - type: sql
        destination: lynk.core.order
        sql: {source}.cust_id = {destination}.customer_id
      - type: fields
        destination: lynk.core.payment
        fields:
        - source_field: order_id
          destination_field: order_id
          operator: equal
    - name: successful_payments
      default: false
      type: lookup
      lookup:
      - type: sql
        destination: lynk.core.order
        sql: {source}.cust_id = {destination}.customer_id and {destination}.order_status = 'O'
      - type: fields
        destination: lynk.core.payment
        fields:
        - source_field: order_id
          destination_field: order_id
          operator: equal
```

### Structure



