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
-- Simple example - equivalent SQL API
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

Define the main entity of the query

```json
// example - main entity caluse
"entity": "customer"
```

### `joins`

Entities to be joined to the main entity&#x20;

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
For more information about time aggregations, visit  [Time Aggregations](../data-modeling/time-aggregation.md).
{% endhint %}

### `select`

The fields to select

There are three types of fields you can select in the `select` clause:&#x20;

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

```json
// example - select - field
"select": [
   {
     "type" : "field",
     "entity": "customer",
     "field" : "customer_id",
     "alias": "cid"
   }
]
```

`select` - `measure`

Use this option for fetching entity **measures**

```json
// example - select - measure
"select": [
   {
     "type" : "measure",
     "measure" : "average_sales",
     "alias": "total_orders"
   }
]
```

{% hint style="info" %}
Measures are reusable aggregate definitions that can be applied on entity rollup.

Just like regular SQL, when using measures (aggregate functions), make sure to put the rest of the entity features in the `GROUP BY` clause.
{% endhint %}

`select` - `lynk_function`

Use this option to apply a Lynk Function and fetching it's result.\
For more information about this, visit [Lynk Functions](../data-modeling/lynk-functions/).

```json
// example - select - lynk function (POP)
"select": [
  {
     "type" : "lynk_function",
     "alias": "total_orders_over_last_4_months_average",
     "function": "pop",
     "params" : {
       "feature": "total_orders",
       "offset": 1,
       "repeats": 4,
       "offsetOperator": "average",
       "popOperator": "({a}/{b})"
     }
   }
 ]
```

### `where`

Apply filters to the query

There are two types of filters you can apply in the `where` clause:&#x20;

* `fields`
* `sql`

{% hint style="warning" %}
Note that you can apply either `fields` or `sql` filters, but not both at the same `where` clause. \
(The effect will be the same whichever way you choose to apply as filter)
{% endhint %}

### `where` - `fields`

In case of applying `where` filters as `fields`, you will need to add the following parameters:

* `entity` - the entity which the field to filter on belongs to
* `field` -  the entity feature to filter on
* `operator` - the filter operator (see all options for [filter operators](../data-modeling/filters.md#operator))
* `values` - an array of field values to filter by

```json
// example - where - fields
"where": {
  "type": "fields",
  "fields": [{
    "entity": "customer",
    "field": "nation_id",
    "operator" : "equal",
    "values": [
      "40", "42"
    ]
  }]
}
```

The above example translates to the following SQL `WHERE` clause:

```sql
-- example - where - fields
WHERE customer.nation_id in ("40", "42")
```

### `where` - `sql`

Apply a simple sql expression to use for filtering

```json
// example - where - sql
"where": {
  "type": "sql",
  "sql": "{customer}.{nation_id} in ('40', '42')"
}
```

### `groupBy`

Array of fields to use in the `group by` clause

```json
// example - groupBy
"groupBy": ["1", "2"]
```

### `having`

Apply filters to the query using aggregated fields

There are two types of filters you can apply in the `having` clause:&#x20;

* `fields`
* `sql`

{% hint style="warning" %}
Note that you can apply either `fields` or `sql` filters, but not both at the same `where` clause. \
(The effect will be the same whichever way you choose to apply as filter)
{% endhint %}

### `having` - `fields`

In case of applying `having` filters as `fields`, you will need to add the following parameters:

* `entity` - the entity which the field to filter on belongs to
* `measure` -  the entity measure to filter on
* `operator` - the filter operator (see all options for [filter operators](../data-modeling/filters.md#operator))
* `values` - an array of field values to filter by

```json
// example - having - fields
"having": {
  "type": "fields",
  "fields": [{
    "entity": "customer",
    "measure": "measure(total_sales)",
    "operator" : "gt",
    "values": [
      "100"
    ]
  }]
}
```

The above example translates to the following SQL `HAVING` clause:

```sql
-- example - having - fields
HAVING customer.total_sales > ("100")
```

### `having` - `sql`

Apply a simple sql expression to use for filtering

```json
// example - having - sql
"where": {
  "type": "sql",
  "sql": "{customer}.{total_sales} > ('100')"
}
```

### `sort`&#x20;

Array of items to sort by (order by):

In case of applying `sort` option, you will need to add the following parameters:

* `entity` - the entity to take the field to sort by from
* `field` -  the entity field to sort by
* `direction` - “desc” or “asc”. (default “asc”)

```json
// example - sort
"sort": [
   {"entity": "customer", "field": "total_sales", "direction": "desc"}
 ]
```

### `limit`&#x20;

The number of rows to return&#x20;

```json
// example - groupBy
"limit": 3
```

### `offset`&#x20;

The  number of rows to skip

```json
// example - offset
"offset": 100
```
