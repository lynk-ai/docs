# Entities

Entities are real-world concepts like customers, orders, payments etc.\
These are first-class citizens in Lynk, meaning everything we build and consume is around entities.

The main concept of Lynk Semantic Layer is to create a central source of truth for each of the entities in the business, in a trusted and accessible way. In other words, from a business perspective, for each business entity it should be clear what we know of it, how was it defined, and where we can find it. We call these pieces of information on an entity level - [features](features/).

***

## Defining Entities

Entities can be defined either via code or via Lynk Studio UI.\
The below example shows how we define a `customer` entity as a YAML file:

```yaml
# customer.yml

name: customer

description: a customer is a user who logged in at least once

key_table: db_prod.core.customer_dim

aliases:
- user

features:

- type: metric
  name: orders_count
  asset: db_prod.core.orders
  measure: orders_count
  filters: null
  
related_assets:

  db_prod.core.orders:
    relationship: one_to_many
    joins:
    - name: all_orders
      default: true
      type: sql
      sql: "{source}.{customer_id} = {destination}.{customer_id}"

```

{% hint style="info" %}
For a quick onboarding, use the [discovery](entities.md#discovery) process to automatically extract business entities from your Data Warehouse schemas and SQL code.
{% endhint %}

### `key_table`

An entities is defined by it's key data asset.\
An entity key data asset is a table or a view in the data warehouse, that has all the entity instances, and each entity instance exists only once on this asset.

For example, if our entity is customer, it's key data asset should have all the customers, and each customer appears only once in that data asset.

{% hint style="info" %}
The entity DIM table is a good fit here, if exists in the DWH.\
However, any data asset which answers the the above requirement can fit. Once loaded as an entity in Lynk, you will be able to add as many enrichment features as needed.
{% endhint %}

### `aliases`

Sometimes different people might call the same entity by different names. e.g a `customer` can also be referred to as a `user`. This is relevant especially when interacting with AI apps to ask questions. Lynk supports aliases to entity names.

### `features`

Features are attributes that represent all we know about our Entities.\
It can be simple fields, aggregated metrics, first - last features, period-over-period formulas, custom formulas and more. See [Features](entities.md#features) page for in depth information on this.

### `related_assets`

Define which Data Assets are related to the entity. Related assets will be shown and used when creating new features for an entity. For example, if the data asset `db_prod.core.orders` is related to the entity `customer`, we will be able to extract features from `db_prod.core.orders` to the `customer` level. See [Related assets](relationships/related-data-assets.md) for in depth information on this.

***

## Entity relationships

To see how to define and use relationships between entities, please see [Related entities](relationships/related-entities.md) page.

***

## Consuming Entities

Entities and Features are consumed via [SQL API](../consume-and-apis/sql-api.md), [REST API](entities/broken-reference/) or via Lynk [Playground](entities/broken-reference/). See [Consume & APIs](../consume-and-apis/) for in depth information on this.

```sql
-- Example for a simple SQL API query

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

Lynk [Governance](../governance.md) makes sure Entities are unique:

* Entities have unique names
* Entities have unique Key data asset
* Entity key asset validation (no duplications, no missing instances)
* Entities do not share the same aliases

***

## Discovery

Lynk Discovery makes it easy to bootstrap your project and define entities automatically. Read more on this on the [Discovery](entities.md#discovery) page.
