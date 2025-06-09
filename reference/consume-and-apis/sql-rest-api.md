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

### `entity`

Name of the main entity

```json
// example - main entity block
"entity": "customer"
```

### `joins`

Entities to join to the \`main\_entity\`

```json
// example - joined entities
"joins": [
   {
     "entity": "order",
     "joinName": "customer_orders",
     "alias": "o"
   } 
 ]
```

### `timeAggregation`

The time aggregation definition

```json
// example - time aggregation
"timeAggregation": {
   "timeGrain": "day",
   "windowSize": 3,
   "direction": "backward"
},
```

`timeAggregation` has the following nested parameters:

* `timeGrain`
* `windowSize` \[optional]
* `direction` \[optional]

{% hint style="info" %}
For more information about time aggregations, visit the [Time Aggregations](../data-modeling/time-aggregation.md) page.
{% endhint %}

### `select`

The fields to select.&#x20;

There are 3 types of fields you can use in the select clause:&#x20;

* `field`
* `measure`
* `lynk_function`

```json
// example - select
"select": [
   {
     "type" : "field",
     "entity": "customer",
     "field" : "customer_id",
     "alias": "cid"
   },
   {
     "type" : "measure",
     "measure" : "average_sales",
     "alias": "total_orders"
   },
   {
     "type" : "lynk_function",
     "alias": "pop1",
     "function": "pop",
     "params" : {
       "feature": "total_orders",
       "offset": 12,
       "repeats": 1,
       "popOperator": "({a}-{b})",
       "offsetOperator": "min",
       "toDate": false
     }
   }
 ]

```

`select` - `field` &#x20;

Use this option for fetching entity **features**

`select` - `measure`

Use this option for fetching entity measures (rollup the entity)

{% hint style="info" %}
Measures are reusable aggregate definitions that can be applied on Entities.

Just like regular SQL, when using measures (aggregate functions), we need to make sure to put the rest of the entity features in the `GROUP BY` clause.
{% endhint %}

`select` - `lynk_function`

Defines the function name and parameters

***

1. “where” / “having” - support type “sql” or “fields”.
2.
   1. “type” = “sql”: defines SQL to use
   2. “type” = “fields”: defines an array of where/having filters to apply:
   3.
      1. “entity” - name of the entity to take the field from
      2. “field” - name of the entity’s field to use
      3. “operator” - The operator to use
      4. “values” - Array of values to use
3. “groupBy” - Array of fields (mentioned in the select) to GROUP BY
4. “sort” - Array of items to sort by:
5.
   1. “entity” - name of the entity to take the member from
   2. “member” - name of the entity field to sort by
   3. “direction” - “desc” / “asc” (default “asc”)
6. “limit” - number of rows to return&#x20;
7. “offset” - number of rows to skip
