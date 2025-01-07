# Consume & APIs

Entities and features can be consumed via [SQL API](sql-api.md).

{% hint style="info" %}
REST API is on our roadmap for Q1 2025. Please [contact us](https://www.getlynk.ai/book-a-demo) if you are interested in this topic.
{% endhint %}

## Consuming entities

### joined entities - left join

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

## BI tools

You can connect your BI tool to lynk via SQL API.\
