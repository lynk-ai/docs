# Entities

Entities are real-world concepts like customers, orders, payments etc. \
Lynk data modeling framework treats entities as first-class citizens, meaning everything we build and consume is around entities.

The main concept of Lynk Semantic Layer is to create a central source of truth for each of the entities in the business, in a trusted and accessible way. In other words, from a business perspective, for each business entity it should be clear what we know of it, and where we can find it. We call these pieces of information on an entity level - [features](../features/).

From a data perspectives, we can think of entities as [virtual data assets](broken-reference), and their features as the fields of these virtual assets.

***

## Defining Entities

Entities can be defined either via code or via Lynk Studio UI.\
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

{% hint style="info" %}
For quick onboarding to Lynk, use the [discovery](./#discovery) process to automatically extract business entities from your Data Warehouse and SQL files&#x20;
{% endhint %}

### Key table

Entities are defined by a key data asset. \
An entity key data asset is a table or a view in the data warehouse, that has all the entity instances and each entity instance exists only once on this asset.&#x20;

For example, if our entity is customer, it's key data asset should have all the customers, and each customer appears only once in that data asset.

{% hint style="info" %}
The entity DIM table is a good fit here, if exists in the DWH.\
However, any data asset which answers the the above requirement can fit. Once loaded as an entity in Lynk, you will be able to add as many enrichment features as needed.
{% endhint %}

### Aliases

Sometimes different people might call the same entity by different names. e.g a `customer` can also be referred to as a `user`. This is relevant especially when interacting with AI apps to ask questions. Lynk supports aliases to entity names.

### Features

Features are attributes that represent all we know about our Entities. \
It can be simple fields, aggregated metrics, first - last features, period-over-period formulas, custom formulas and more. See [Features](./#features) page for in depth information on this.

### Related assets

Define which Data Assets are related to the entity. Related assets will be shown and used when creating new features for an entity. For example, if the data asset `db_prod.core.orders` is related to the entity `customer`, we will be able to extract features from `db_prod.core.orders` to the `customer` level. See [Related assets](related-assets.md) for in depth information on this.

### Related entities

Just like in the real world, entities relate to each other in many ways. To ensure consistency and simplicity, Lynk stores all entity relationships in one place - `entities_relationships.yml` file. See [related entities](related-assets.md) for in depth information on this.

Entities relationships are used by lynk when creating features and for joining entities on the [consumption](../../consume/) layer.

***

## Consuming Entities

You can easily consume Entities and Features via [SQL API](../../consume/sql-api/), [REST API](../../consume/rest-api.md) or via Lynk [Playground](../../consume/playground.md) (see [consume](../../consume/) for in depth information on this).

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

