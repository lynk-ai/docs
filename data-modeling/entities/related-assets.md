# Related assets

Each entity has related [data assets](../data-assets/), from which we can create features. \
The relation between an entity and a data asset is defined on the entity YAML file, under `related_assets`.&#x20;

\[ADD here a diagram showing an entity and related assets]

## Simple entity-to-asset relation

In this example, we define the relations between the entity `customer` to the data assets `db_prod.core.orders` and `db_prod.core.device` :

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
        destination: id
        operator: equal
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
Lynk supports multiple join paths between an entity and a data asset, hens the `joins` property is an array.&#x20;

### **name \[optional]**

The join path a name. \
If you choose not to name a join path, lynk will consider the name as "default".\
Note that in case another join path will be added, naming it will be mandatory as there can be only one "default" join path name.

The name property will be used when creating a feature. \
In case there is more than one join path between an entity and a data asset, you will be able to tell Lynk how connect the entity to the related asset by using the join path name.

### **default \[optional]**

The `default` property takes boolean values (`true` / `false`).\
There can be only one default join path between an entity and a specific data asset. Lynk will use the default join path when creating features for this entity, unless a name of another join path will be stated.

In case there is more than one join path between an entity and a data asset, setting the `default` property becomes mandatory.

### type

The type property will be used to tell Lynk using which method you define the join path. The options for `type` are:

* `sql`
* `fields`
* `lookup`

### `sql` (type)

Use sql code to define how an entity is related to a data asset.\
When setting `type: sql`, you will need to add the `sql` property with the SQL definition of the relation as follows:

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
When setting `type: fields`, you will need to add the `fields` property with the fields and the operator that define the relation:

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

In the above example, the entity customer has a feature `device_id` which connects to the field `id` in the device data asset, using the operator `equal,` which translates to `customer.device_id = db_prod.core.device.id`

{% hint style="info" %}
Multiple related fields from the source and the destination are supported, enabling joins on more than one field when needed.
{% endhint %}

### `lookup` (type)

Sometimes the relation between an entity and a data asset is not direct, but goes via one or more lookup tables (or "hops"). Lynk supports this scenario using the join type `lookup` as follows:

```yaml
// customer.yml

related_assets:

  lynk.core.payment:
    relationship: one-to-many
    joins:
    - name: all_payments
      default: true
      type: lookup
      lookup:
      - destination: db_prod.core.orders
        type: sql
        sql: {source}.id = {destination}.customer_id
      - destination: db_prod.core.payment
        type: sql
        sql: {source}.order_id = {destination}.order_id
```

As seen on the above code, lookups kave multiple steps. This is an ordered list of steps to get from the source (the entity) to the destination \*asset".&#x20;

On the first step, the source is the data asset...

Using the `lookup` type;

`destination` refers to the entity

`destination` refers to the data asset

`operator` defines the&#x20;

## Multiple join paths

Often there is a need to define more than one way to join an entity to a data asset.&#x20;

For example, imagine we are a b2b company with a sales department\
It's common that the sales agent that closed the deal (sale) is not the same agent that renewed the contract with the customer a few years later. What if we want to know for each customer, who was the agent on each occasion? \
A simple way to do that is to join customers to agents twice - one on sale\_agent and another join on renew\_agent (see below)

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
Note that in the case of multiple join paths, each join path needs to have a `name` and only one can be set to `default`
{% endhint %}



### Structure



