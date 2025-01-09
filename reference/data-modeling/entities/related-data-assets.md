# Related data assets

Each entity has related [data assets](../data-assets/), which are tables or views that we can join with our entity. The relation between an entity and a data asset is defined on the entity YAML file, under `related_assets` or via the Studio UI.

{% hint style="info" %}
Joining related assets will allow us to enrich our entity with features
{% endhint %}

***

## Simple entity-to-asset relation

In this example, we define the relations between the entity `customer` to the data assets `db_prod.core.orders` and `db_prod.core.device`:

```yaml
# customer.yml

related_assets:

  db_prod.core.orders:
    relationship: one_to_many
    joins:
    - name: all_orders
      default: true
      type: sql
      sql:  {source}.customer_id = {destination}.customer_id

  db_prod.core.device:
    relationship: one_to_one
    joins:
    - name: customer_device
      default: true
      type: fields
      fields: 
      - source: device_id
        destination: id
        operator: equal
```

### `Related assets`

The `related_assets` property holds all the assets that relate to the entity.

Each data asset element has to include the full path to the data asset as it in the origin data warehouse - db name, schema name and asset name (`db.schema.name`)

### `Relationship`

Sets the `Relationship` between the entity and the data asset.\
The options for the Relationship property are:

* `one_to_one`
* `one_to_many`
* `many_to_many`
* `many_to_one`

The direction of the relationship is entity-to-asset. Meaning, in our example, the entity is `customer` and the first data asset is `order`. So in this case a customer has many orders.

{% hint style="info" %}
Lynk will use the relationship property to suggest the correct data assets when creating features. For example, when creating metrics, Lynk will only suggest one-to-many related assets.
{% endhint %}

### `Joins`

Define how the entity and the data asset should be joined, by connecting entity _features_ to data asset fields.

### **`name` \[optional]**

Give the join path a name.&#x20;

If you choose not to name a join path, lynk will automatically name as the join path as "default" followd by a number. For example, the first unnamed join path will be named by Lynk to `default_1`, the second to `default_2` etc..

Note that Join path `name` has to be unique on a related asset level.

{% hint style="info" %}
The `name` property will be used when creating features.\
In case there is more than one join path between an entity and a data asset, you will be able to tell Lynk how connect the entity to the related asset by using the join path `name`.
{% endhint %}

### **`default` \[optional]**

The `default` property takes boolean values (`true` / `false`).\
There can be only one default join path between an entity and a specific data asset. Lynk will use the default join path when creating features for this entity, unless a name of another join path will be stated.

In case there is more than one join path between an entity and a data asset, setting the `default` property becomes mandatory.

### `type`

The `type` property tells Lynk which method to use for defining the join path.\
The options for `type` are:

* `sql`
* `fields`
* `lookup`

### `sql` (type)

Use sql code to define how an entity is related to a data asset.\
When setting `type: sql`, you will need to add the `sql` property with the SQL definition of the relation.

See the following example;

```yaml
# customer.yml

related_assets:

  db_prod.core.orders:
    relationship: one_to_many
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
# customer.yml

related_assets:

  db_prod.core.device:
    relationship: one_to_one
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

`operator` defines the operator of the relation between the two fields.\
The options for the operator property are:

* equal
* gt
* gte
* lt
* lte

In the above example, the entity customer has a feature `device_id` which connects to the field `id` in the device data asset, using the operator `equal`.\
This translates to `customer.device_id = db_prod.core.device.id`

{% hint style="info" %}
Lynk supports multiple related fields from the source to the destination, enabling joins on more than one field when needed.
{% endhint %}

### `lookup` (type)

Sometimes the relation between an entity and a data asset is not direct. Meaning, in order to connect an entity and a data asset we have to join them via one or more lookup tables ("hops"). Lynk supports this scenario using the `lookup` join type.

See the below example:

```yaml
# customer.yml

related_assets:

  db_prod.core.payment:
    relationship: one_to_many
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

In the above example, we connect the table `db_prod.core.payment` to our `customer` entity. Note that there is no direct connection between those two, and we have to join customer to orders first and then join orders to payment.

On the first step, the source is the data asset...

Using the `lookup` type;

As seen on the above code, lookups are a n ordered list of steps;

* On the first step, `source` is always the entity and destination is the first data asset we connect to it.
* On the next steps, the source is the previous destination.
* On the last step, the destination is the final destination we would like to reach. in this case it's `db_prod.core.payment`

Inside each lookup step, we can define the connection between the source and destination, and choose how - using the `type` parameter as usual - `SQL` or `fields`

***

## Example - data asset with multiple join paths

Sometimes there is a need to define more than one way to join an entity to a data asset.

For example, imagine we are a b2b company with a sales department\
It's common that the sales agent that closed the deal (sale) is not the same agent that renewed the contract with the customer a few years later. What if we want to know for each customer, who was the agent on each occasion?\
A simple way to do that is to join customers to agents twice - one on sale\_agent and another join on renew\_agent (see below)

Lynk supports multiple join paths between an entity and a data asset as follows:

```yaml
# customer.yml

related_assets:
  db_prod.core.agents:
    relationship: many_to_many
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
