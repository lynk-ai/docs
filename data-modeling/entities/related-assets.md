# Related assets

Each entity has related [data assets](../data-assets/), from which we can create features. \
The relation between an entity and a data asset is defined on the entity YAML file, under `related_assets`.&#x20;

ADD here a diagram showing an entity and related assets

## Simple entity-to-asset relation

In this example, we define the relation between the entity `customer` to the data asset `db_prod.core.orders` :

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

### Related asset

The `related_assets` property in the entity YAML file is an object that holds all the assets that relate to that entity.  In the above example we have two data assets that relate to the customer `entity` (orders and device).&#x20;

### db.schema.name

Each data asset has to include the full name - db name, schema name and asset name.

### Relationship

The relationship type will help Lynk suggest the correct data assets when creating new features on the entity level. For example, when creating a metric - Lynk will only suggest one-to-many related assets.&#x20;

The direction of the relationship is entity-to-asset. Meaning, in our example, the entity is `customer` and the first data asset is `order`. So in this case a customer has many orders.&#x20;

### Joins

dasdfsa

name



## A simple entity-asset relation









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



