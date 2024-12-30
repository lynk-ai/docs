# Features

Features are entity-level attributes, representing all the things we know of entities.\
Lynk makes it simple to create features, based on related data assets or related entities.

ADD A DIAGRAM OF OPTIONAL FEATURES FOR THE CUSTOMER ENTITY

{% hint style="info" %}
Features represent the business logic of enriching entities with information based on other related assets or entities.
{% endhint %}

***

## Types of features

### Field&#x20;

Field features are great for enrichments from **one-to-one** relations.\
It is commonly used to enrich an entity with simple, non aggregate fields from one-to-one related assets or entities. See more in depth information on [Field](field.md)[ features](field.md).

### Metric

Metric features are great for aggregations from **one-to-many** relations.\
It is commonly used to enrich an entity with aggregated fields from one-to-many related assets or entities. See more in depth information on [Metric features](metric.md).

### First-Last

First-Last features are great for enrichments of fields from **one-to-many** relations.\
It is commonly used to enrich an entity with fields of the first or last appearance of a one-to-many related assets or entities. See more in depth information on [First-Last features](first-last.md).

### Formula

Formula features are used when we need to create calculated features on top of other features.\
It is commonly used to enrich an entity with more complex calculations that require multiple aggregations or calculations to be done first. See more in depth information on [Formula features](formula.md).

***

## Consuming features

Features are consumed via [SQL API](../../consume/sql-api/), [REST API](../../consume/rest-api.md) or via Lynk [Playground](../../consume/playground.md). See [consume](../../consume/) for in depth information on this.

For example, here is a simple SQL API request to get some features defined on a customer level:

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

Lynk [Governance](../../governance.md) makes sure features are unique and trusted:

* Features have unique names
* Features have unique definitions
* Monitoring relationship type to make sure feature definitions won't break