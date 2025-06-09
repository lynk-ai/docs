# SQL REST API

Querying the SQL REST API is as simple as sending a json format with the parameters you would use in a regular SQL query.&#x20;

{% hint style="info" %}
For AI agents, it is recommended to use the SQL REST API - as it is easier for agents to understand and generate.
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

## Request body examples

### Simple example

In the example below you can find a simple Request Body for SQL REST API

```json
// Request body
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
     "field": "nation_id",
     "operator" : "equal",
     "values": [
       "40", "42"
     ]
   }]
 },
 "oredrBy": [
   {"entity": "customer", "member": "customer_id", "direction": "desc"}
 ],
 "limit": 100
}
```

## Time aggregation example - Request body

```json
// Request body
{
 "entity": "customer",
 "joins": [
   {
     "entity": "order",
     "joinName": "customer_orders",
     "alias": "o"
   } 
 ],
 "timeAggregation": {
   "timeGrain": "day",
   "windowSize": 7,
   "direction": "backward"
 },
 "startTime": "2025-01-01",
 "stopTime": "2025-06-01",
 "select": [
   {
     "type" : "field",
     "entity": "customer",
     "field" : "nation_name",
     "alias": "nation_name"
   },
   {
     "type" : "measure",
     "measure" : "total_sales",
     "alias": "total_sales"
   },
   {
     "type" : "lynk_function",
     "alias": "pop1",
     "function": "pop",
     "params" : {
       "feature": "total_sales",
       "offset": 12,
       "repeats": 1,
       "popOperator": "({a}-{b})",
       "offsetOperator": "min",
       "toDate": false
     }
   }
 ],
 "where": {
   "type": "fields",
   "fields": [{
     "entity": "customer",
     "field": "customer_id",
     "operator" : "equal",
     "values": [
       "C1", "C2"
     ]
   }]
 },
 "having": {
   "type": "fields",
   "fields": [{
     "entity": "customer",
     "field": "customer_id",
     "operator" : "equal",
     "values": [
       "C1", "C2"
     ]
   }]
 },
 "groupBy": ["m1", "f1"],
 "oredrBy": [
   {"entity": "customer", "member": "f1", "direction": "desc"}
 ],
 "limit": 100,
 "offset": 100
}
```

\
