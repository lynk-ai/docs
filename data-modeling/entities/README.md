# Entities

Entities are real-world concepts like customers, orders, payments etc. \
Lynk data modeling framework treats Entities as first-world citizens, meaning everything we build is around Entities and Features for our Entities.

***

## Defining Entities

You can easily define entities either via code or via Lynk Studio UI.\
The below example shows how we define a `customer` entity as a YAML file:

```yaml
// customer.yml

name: customer

description: a customer is a user who logged in at least once

key_table: db_prod.core.customer_dim

aliases:
- user

features:
- name: customer_id
  type: field
  ...

related_assets:
- db_prod.core.orders
  ...

```

### Key table

Entities in lynk are defined by a key data asset (a table or a view in the underlying DWH)\
For example, if our entity is `customer`, it's key data asset should have all the customers, and each customer appears once in that data asset.

### Aliases

Sometimes different people might call the same entity by different names. e.g a `customer` can also be referred to as a `user`. This is relevant especially when interacting with AI apps to ask questions. Lynk supports aliases to entity names

### Features

Features are attributes that represent all we know about our Entities. \
It can be simple fields, aggregated metrics, first - last features, period-over-period formulas, custom formulas and more. See [Features](./#features) page for in depth information on this

### Related assets

Define which Data Assets are related to the entity. Related assets will be shown when creating new features for an entity. See [Related assets](related-assets.md) for in depth information on this.

### Related entities

Just like in the real world, entities relate to each other in many ways. To ensure consistency and simplicity, Lynk stores all entity relationships in one place - `entities_relationships.yml` file,.

For example we can define that `customer` entity relates to `order` entity in a one-to-many relationship, where the join path is `customer.order_id = order.id.` This relation definition will be used by lynk across many places within the data modeling framework;

***

## Consuming Entities

You can easily consume Entities and Features via lynk [Playground](../../consume/playground.md), [SQL API](../../consume/sql-api.md) or [REST API](../../consume/rest-api.md).

For example, here is a simple SQL API request to get some features defined on a `customer` level:

```sql
// A simple SQL API query

SELECT  customer_id,
        total_order_amount,
        first_order_date,
        last_order_status
FROM    entity('customer')
WHERE   country = 'US'
LIMIT   100
```

***

## Governance

Lynk [Governance](../../governance.md) makes sure Entities are unique:

* Entities have unique names
* Entities have unique Key data asset
* Entities do not share the same aliases

***

## Discovery

Lynk Discovery makes it easy to bootstrap your project and define entities automatically. Read more on this on the [Discovery](./#discovery) page.

