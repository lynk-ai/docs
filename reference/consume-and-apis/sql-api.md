# SQL API

Querying the SQL API is as simple as writing a simple SQL SELECT statement.

## Query structure

The SQL API supports standard `SELECT` statements.\
The query format is similar to a vanilla (regular) SQL query, using the SQL flavor of your query engine (Snowflake, BigQuery etc).

#### Example:

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

## Entities and features

When querying Lynk via the SQL API, we are actually querying **entities** and their **features**. As shown in the above example, the `FROM` statement expects an entity using the `entity()` function, and the fields in the `SELECT` statement are actually **features**.

### Main entity

The **main entity** is the first entity passed to the `FROM` statement, using the `entity()` function.&#x20;

#### For example:

```sql
// A simple SQL API query

SELECT  customer_id,
        count_orders
FROM    entity('customer')
```

The above example will return a record per `customer`. Meaning, all customers will return, and for each customer Lynk will return exactly one row. The metric `count_orders` will be calculated across all available time range

#### Another example, with `time_agg`:&#x20;

```sql
// A simple SQL API query

USE {
  "time_agg": {
    "time_grain": "day"
  }
  "start_time": "2024-01-01",
  "stop_time": "2025-01-01"
}

SELECT  customer_id,
        time_agg as date_day,
        count_orders
FROM    entity('customer')
```

The above example will return a record per `customer` and `day`.&#x20;

{% hint style="info" %}
It is recommended to use `start_time` and `stop_time` parameters in the `USE` statement when using `time_agg`.
{% endhint %}

***

## Joining entities

Joining entities is done using the `JOIN` statement. \
Under the hood, Lynk applies a LEFT JOIN operation between each two joined entities, according to the join path specified between the two entities. See [entities relationship](../data-modeling/entities/related-entities.md) for more information on how to specify join paths between two entities.

#### Example for joining entities

```sql
// Joining two entities

SELECT  c.customer_id,
        c.count_orders,
        t.name as team_name
FROM    entity('customer') c
JOIN    entity('team') t
```

Note that `team_name` is a feature that was defined on the entity `team` and joined to each customer on this SQL API query.

***

## Joining entities using join path name

In some cases, there might be more than one way to join two entities. Lynk supports this scenario by supporting the definition of more than one join path between two entities.

If passed to the SQL API query, Lynk will use the join path `name` to  join the two entities. If no join path name stated, the default join path will be applied in order to join the two entities.  See [`NAME`](../data-modeling/entities/related-entities.md#name-optional) section in the [related entities](../data-modeling/entities/related-entities.md) page for more information on this.

```sql
// Joining entities with named join paths

SELECT  c.customer_id,
        c.count_orders,
        sa.name as sales_agent_name,
        la.name as last_support_agent_name
FROM    entity('customer') c
JOIN    entity('agent') sa on sales_agent
JOIN    entity('agent') la on last_support_agent
```

In this example we join the entity `agent` to the main entity `customer` twice. Once via a join path that joins the `sales_agent` to a customer and once via a join path that joins the `last_support_agent` to a customer.

{% hint style="info" %}
Note that in order to use a named join pattern, we use the `ON` keyword and then the join path `NAME`. In order to maintain the concept of a **single source of truth**, only a join path `NAME` can be passed here (not the path itself). Join paths should be centrally defined as [entities relationships](../data-modeling/entities/related-entities.md).
{% endhint %}

***

## Supported SQL statements

#### Lynk supports the following SQL statements:

* `SELECT`
* `FROM`
* `JOIN`
* `WHERE`
* `GROUP BY`
* `HAVING`
* `ORDER BY`
* `LIMIT`

Any of the statements above are supported, using the SQL flavor of the underlying query engine in use.

#### Example:

```sql
// customers per orders histogram

SELECT  c.count_orders,
        count(c.customer_id) as count_customers
FROM    entity('customer') c
JOIN    entity('team') t
WHERE   t.size >= 100
GROUP BY c.count_orders
ORDER BY c.count_orders ASC
LIMIT 20
```

The above query will return a histogram of the number of customers per number of orders, for customers which their team size is 100 or more. It will also order the results by the number of orders in an ascending order, and return only 20 rows.

{% hint style="info" %}
N**ot** supported

* CTEs ("WITH" statements)
* DDLs
* DMLs

CTEs are not supported for a reason; \
In order to keep the source of truth clean and trusted, Lynk encourages to add business logic to entities and features - and avoid adding business logic to the consumption layer, as it will result in in-accessible and in-reusable logic.
{% endhint %}

***

## `USE`

Passing query-level configurations is done using the `USE` config block.

The supported query level configurations are:

### `branch`

Specify which git `branch` to use.

By default Lynk will retrieve semantic definitions from the default git branch, according to the project's repository. In case the `branch` option is passed to the `USE` block, Lynk will take the semantic definitions (entities, features, join paths etc) from the specified branch.

#### Example using a custom branch

```sql
// Using a custom branch

USE {
  "branch": "dev"
}

SELECT  customer_id,
        count_orders
from    entity('customer')
```

In the above example we are using the `branch` "dev"

### `context`

Specify which `context` to use.&#x20;

By default Lynk will retrieve semantic definitions from the default context ("shared"). In case the `context` option is passed to the `USE` block, Lynk will take the semantic definitions (entities, features, join paths etc) from the specified context.

```sql
// Using a custom context
​
USE {
  "context": "marketing"
}
​
SELECT  customer_id,
        is_active_customer
from    entity('customer')
```

See [contexts](../data-modeling/context.md) for in depth information on this.

***

### `time_agg`

Use `time_agg` to specify how to aggregate the query features, in terms of time aggregation.&#x20;

See [time aggregation](time-aggregation.md) for in depth information on this.

### `start_time`

### `stop_time`



***

## Understanding the process

Under the hood, the process between sending a query to Lynk and receiving the results does the following:

#### Step 1: Parsing the query

Parsing the SQL API query to the relevant query engine

* Reading the query configuration from the [`USE`](sql-api.md#use) statement
* Scanning for errors
* Translating the query, including:
  * Translating features to their business logic as defined in Lynk
  * Using the correct [`time_agg`](time-aggregation.md) as stated in the `USE` config
  * Using the correct [`context`](../data-modeling/context.md) as stated in the `USE` config
  * Using the correct `git branch` as stated in the `USE` config
* Composing the final parsed query including all SQL statements and feature definitions

#### Step 2: Sending the parsed SQL query to the query engine

Sending the parsed SQL query to the underlying query engine

#### Step 3: Receiving the results&#x20;

Receiving the results (data) from the query engine.

#### Step 4: Streaming the results to the requesting client

Streaming the results back to the requesting client.\
In case of SQL error occurs on the query engine, the original error will return.

***



***

## Pushdowns

if not entity - passes directly to the engine







