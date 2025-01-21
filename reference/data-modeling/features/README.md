# Features

Features are entity-level attributes, representing all the things we know of entities.\
Lynk makes it simple to create features, based on related data assets or related entities.

{% hint style="info" %}
Features represent the business logic of enriching entities with information based on other related assets or entities.
{% endhint %}

***

## Types of features

### Field

Field features are great for enrichments from **one-to-one** or **many-to-one** relations.\
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

## Chaining features

Lynk supports creating features based on previously created features on related entities.

For example, let's assume we have an entity called `user` and another entity called `team`, with in a many-to-one relationship. You can create a feature called `is_active_user` on the `user` level and consume it for creating a metric feature `active_users_count` on the `team` entity level.

{% hint style="info" %}
This allows building consistent, accessible and governed business logic - See [chaining features](../chaining-features.md) for in depth information about this.
{% endhint %}

***

## Consuming features

Features are consumed via [SQL API](../../consume-and-apis/sql-api.md), [REST API](broken-reference/) or via Lynk [Playground](broken-reference/).

For example, here is a simple SQL API request to get some features defined on a customer level:

```sql
-- A simple SQL API query

SELECT  customer_id,
        total_order_amount,
        first_order_date,
        last_order_status
FROM    entity('customer') 
WHERE   country = 'US'
LIMIT   100
```

See [consume](../../consume-and-apis/) for in depth information on this.

***

## Time aggregations

Lynk separates between business logic and time aggregations like rolling\_window on the consumption layer. See [time aggregations](../../consume-and-apis/time-aggregation.md) for in depth information on this.

***

## Governance

Lynk [Governance](../../governance.md) makes sure features are unique and trusted:

* Features have unique names
* Features have unique definitions
* Monitoring relationship type to make sure feature definitions won't break
