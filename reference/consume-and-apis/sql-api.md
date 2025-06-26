# SQL API

Querying the SQL API is as simple as writing a simple SQL SELECT statement.

{% hint style="info" %}
Lynk SQL API is implemented on Postgres protocol.\
Easily connect any BI tool to Lynk as you would connect to a regular Posgtres DB.
{% endhint %}

## Connecting to Lynk SQL API

Connecting to Lynk SQL API is done via a regular Postgres SQL connector.

In order to successfully connect to Lynk SQL API follow the following steps

1. Create an [authentication token](authentication.md) via the Studio "my account" page and keep that token in a safe place.
2. From your BI tool or any other tool you're using, choose Postgres connection with the following credentials:&#x20;
   1. HOST: `sqlapi.app.getlynk.ai`
   2. PORT: `5433`
   3. PASSWORD: paste the authentication token here
3. You are now ready to connect and start querying Lynk via SQL API

{% hint style="info" %}
No need to specify other parameters like User or Role. If your BI tool requires those, you can type in any value.
{% endhint %}

***

## Query structure

The SQL API supports standard `SELECT` statements.\
The query format is similar to a vanilla (regular) SQL query, using the SQL flavor of your query engine (Snowflake, BigQuery etc).

#### Example:

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

***

## Entities and features

When querying Lynk via the SQL API, we are actually querying **entities** and their **features** and **measures**. As shown in the above example, the `FROM` statement expects an entity using the `entity()` function, and the fields in the `SELECT` statement are actually **features**.

### Main entity

The **main entity** is the first entity passed to the `FROM` statement, using the `entity()` function.

#### For example:

```sql
-- A simple SQL API query
SELECT  customer_id,
        count_orders
FROM    entity('customer')
```

The above example will return a record per `customer`. \
In this case, all customers will return, and for each customer Lynk will return exactly one row. The metric feature `count_orders` will be calculated for each customer across all available time range

#### Another example, with time aggregation:

```sql
-- A simple SQL API query
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

The above example will return a record per `customer` and `day`, for each day in 2024.

{% hint style="info" %}
It is recommended to use `start_time` and `stop_time` parameters when using `time_agg`.

For more information about time aggregations, visit the [Time Aggregations](../data-modeling/time-aggregation.md) page.
{% endhint %}

***

## Entity rollup - using measures

When aggregating an entity (rolling up), in order to apply a predefined measure logic, use the `measure()` function as follows:

```sql
-- using measures to perform entity rollup
USE {
  "start_time": "2024-01-01",
  "stop_time": "2025-01-01"
}

SELECT  nation_name,
        measure(average_orders) as average_orders_per_customer
FROM    entity('customer')
GROUP BY 1
ORDER BY 2 desc
```

In the above example we are using the measure `average_orders` defined on the entity `customer`. It is used to calculate the average orders of all customers - in this case by `nation_name`, which is a feature on a customer level.

{% hint style="info" %}
Measures are reusable aggregate definitions that can be applied on entities.

Just like regular SQL, when using measures (aggregate functions), make sure to put the rest of the entity features in the `GROUP BY` clause.
{% endhint %}

***

## Joining entities

Joining entities is done using the `JOIN` statement.\
Under the hood, Lynk applies a LEFT JOIN operation between each two joined entities, according to the join path specified between the two entities. See [entities relationship](../data-modeling/relationships/related-entities.md) for more information on how to specify join paths between two entities.

#### Example for joining entities

```sql
-- Joining two entities
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

If passed to the SQL API query, Lynk will use the join path `name` to join the two entities. If no join path name stated, the default join path will be applied in order to join the two entities. See [`NAME`](../data-modeling/relationships/related-entities.md#name-optional) section in the [related entities](../data-modeling/relationships/related-entities.md) page for more information on this.

```sql
-- Joining entities with named join paths
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
Note that in order to use a named join pattern, we use the `ON` keyword and then the join path `NAME`. In order to maintain the concept of a **single source of truth**, only a join path `NAME` can be passed here (not the path itself). Join paths should be centrally defined as [entities relationships](../data-modeling/relationships/related-entities.md).
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

{% hint style="info" %}
When querying the SQL API, we refer to **entities** as a "tables" and to **features** as "fields".
{% endhint %}

#### Example:

```sql
-- customers per orders histogram
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

CTEs are not supported for a reason;\
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
-- Using a custom branch
USE {
  "branch": "dev"
}

SELECT  customer_id,
        count_orders
from    entity('customer')
```

In the above example we are using the `branch` "dev"

### `context`

Specify which `context` to use.

By default Lynk will retrieve semantic definitions from the default context ("shared"). In case the `context` option is passed to the `USE` block, Lynk will take the semantic definitions (entities, features, join paths etc) from the specified context.

```sql
-- Using a custom context
USE {
  "context": "marketing"
}
​
SELECT  customer_id,
        is_active_customer
from    entity('customer')
```

The above query will return for each `customer`, it's `customer_id` and the value of the feature `is_active_customer`. In case the context `marketing` has a feature called `is_active_customer` on a customer level, Lynk will use this feature definition to build the query. If the context `marketing` does not have a feature called `is_active_customer`, Lynk will use the definition from the `shared` context for the feature `is_active_customer`.

See [contexts](../data-modeling/context.md) for in depth information on this.

***

### `time_agg`

Use `time_agg` to specify how to aggregate the query features, in terms of time aggregation.

See [time aggregation](../data-modeling/time-aggregation.md) for in depth information on this.

***

### `start_time`

Use `start_time` to specify a lower time barrier for the query.

The `start_time` parameter will be applied to all of the underlying data assets that Lynk will query in order to build the requested features.

{% hint style="info" %}
When using `time_agg` it is highly recommended to use the `start_time` option for performance and cost saving purposes.
{% endhint %}

***

### `stop_time`

Use `stop_time` to specify an upper time barrier for the query.

The `stop_time` option will be applied to all of the underlying data assets that Lynk will query in order to build the requested features.

{% hint style="info" %}
When using `time_agg` it is highly recommended to use the `stop_time` option for performance and cost saving purposes.
{% endhint %}

#### Example

```sql
-- Using start_time and stop_time
USE {
  "start_time": "2024-01-01",
  "stop_time": "2025-01-01"
}
​
SELECT  customer_id,
        count_orders
from    entity('customer')
```

In the above example, Lynk will return for each customer, it's `customer_id` and the feature `count_orders,` where `count_orders` is calculated for each user on the time frame between `2024-01-01` and `2025-01-01`.

***

## Query pushdowns

It is possible to query the query engine directly via Lynk. We call this operation a `pushdown`.

In case the `entity()` function is not passed to the `FROM` statement, Lynk will assume you are not querying entities, and will pass the query as is to the underlying query engine - and return the results.
