---
description: Use lynk semantic definitions in your BI, AI and embedded analytics tools
---

# Consume APIs

Lynk offers several ways to consume semantic definitions from various tools.&#x20;

<figure><img src="../../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

## Consuming entities

Main entity

joined entities - left join

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

You can connect your BI tool to lynk via [SQL API](sql-api/).\
