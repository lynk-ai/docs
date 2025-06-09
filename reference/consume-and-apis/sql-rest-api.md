# SQL REST API

Querying the SQL REST API is as simple as sending a json format with the parameters you would use in a regular SQL query.&#x20;

{% hint style="info" %}
For AI agents, it is recommended to use the SQL REST API.\
SQL REST API is easier for agents to understand and generate.
{% endhint %}

## Connecting to Lynk SQL REST API

Connecting to Lynk SQL REST API is done via a regular HTTP POST request to the following endpoint:

`/api/sql/query?branch=&context=`

For example:

```json
// SQL REST API example
/api/sql/query?branch=dev&context=marketing
```

### `branch` \[optional]

Indicate which git branch to use.\
Allows exploring semantic definitions while in development.

If not specified, Lynk will take the definitions of the branch which is defined as the main branch.

### `context` \[optional]&#x20;

Indicate which context to use.\
Allows consuming semantic definitions from different [contexts](../data-modeling/context.md).

If not specified, Lynk will take the `default` context

***

## Authentication

To authenticate with the SQL REST API, you need to create and use an [API token](authentication.md).\
The API token should be sent in the `x-api-key` header of the request.

***

## Request body - simple example

In the example below you can find a simple Request Body for SQL REST API.

In this example, we request for top 100 the customers (customer\_id) and their total\_sales, for customers from BRAZIL, ordered by total\_sales.

```json
// Request body - simple SQL REST API
{
 "entity": "customer",
 "select": [
   {
     "type" : "field",
     "entity": "customer",
     "field" : "customer_id",
     "alias": "customer_id"
   },
   {
     "type" : "field",
     "measure" : "total_sales",
     "alias": "total_sales"
   },
 ],
 "where": {
   "type": "fields",
   "fields": [{
     "entity": "customer",
     "field": "nation_name",
     "operator" : "equal",
     "values": [
       "BRAZIL"
     ]
   }]
 },
 "oredrBy": [
   {"entity": "customer", "member": "total_sales", "direction": "desc"}
 ],
 "limit": 100
}
```

The above simple SQL REST API request simple example is equivalent to the following SQL API request:

```sql
// Simple example - equivalent SQL API
USE {
    "branch" : "<branch>",    -- Use from endpoint's query param
    "context" : "<context>",  -- Use from endpoint's query param
    }
}
SELECT 
    customer_id,
    total_sales
FROM entity("customer")
WHERE nation_name in ('BRAZIL')
ORDER BY total_sales DESC
limit 100
```

***

## Request body parameters

### `Entity`

The main entity to retrieve.&#x20;
