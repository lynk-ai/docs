# Consume & APIs

All semantic definitions such as entities and features can be consumed via dedicated APIs.

Visit our [SQL API](sql-api.md) and [SQL REST API](sql-rest-api.md) pages to learn more.

***

## Understanding the process

Once an SQL API or REST SQL API is sent to Lynk, the following steps get processed:

### Step 1: Parsing the query

Parsing the API query to the SQL code that will be then sent to the query engine

#### Step 1.1: Parsing Entities and Features

Parsing the relevant Entities, Relationships and Features, according to:

* Reading the query configuration from the [`USE`](./#use) statement
* Scanning for errors
* Parsing the query, according to:
  * The `git branch` as stated in the `USE` config
  * The [`context`](../data-modeling/context.md) as stated in the `USE` config
  * The [`time_agg`](../data-modeling/time-aggregation.md) as stated in the `USE` config
  * The business logic as defined in Lynk (taken from the relevant YAML files)

#### Step 1.2: Parsing Lynk Functions

Lynk functions are added post-processing Entities and Features. Once the Query has all the features are in place, Lynk applies the Functions logic - and now the query is ready to be sent to the query engine.

### Step 2: Sending the parsed SQL query to the query engine

Sending the parsed SQL query to the underlying query engine

### Step 3: Receiving the results

Receiving the results (data) from the query engine.

### Step 4: Streaming the results to the requesting client

Streaming the results back to the requesting client.\
In case of SQL error occurs on the query engine, the original error will return.\
