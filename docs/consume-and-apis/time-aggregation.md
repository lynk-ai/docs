# Time aggregation

A diagram that shows the flow - where time aggregations get into play with USE (on consumption level and not on definition level): \[Total sales (show logic)] --> show many ways to tine agg, on consumption level

Time aggregation lets us tell lynk on which timeframe we want to aggregate our features, and how. Time aggregations can be, for example:&#x20;

* **Calendric**:  day / month  / year etc
* **Rolling windows** : "last 30 days" / "first 7 days after signup" etc
* No time frame (full date range)

{% hint style="info" %}
Lynk decouples time aggregation logic from business logic.\
A feature's business logic is defined on the feature definition level, while how to apply time aggregate logic to a feature is defined on the consumption level.&#x20;
{% endhint %}

For example, let's assume we have an entity `customer` and it has a simple metric feature `count_orders` that counts how many orders each customer has.&#x20;

```sql
// SQL API

SELECT  customer_id,
        count_orders
FROM    entity('customer')

```

The above SQL API request will calculate for each customer the count of total orders on all available time we have in the underlying data asset - in this case orders (where the measure count orders comes from).

If we would like to get the daily count or orders, we can simply change the query as follows and Lynk will return a record per customer and day, and for each customer and day the count of orders:

```sql
// SQL API

USE {
  time_agg {
    time_grain : day
}

SELECT  customer_id,
        time_agg as date_day,
        count_orders
FROM    entity('customer')

```

### USE

Set this object on SQL API query to define all the query level configurations. Configurations such as what `time_agg`to use,  which `branch` to use and more are declared here. See [USE](sql-api/use.md) for in depth information on this.

### `time_agg` \[optional]

In this part of USE, we define all the time aggregate related configurations to apply on the query.

The options for `time_agg` are:

* `time_grain`
* `window_size`
* `direction`
* `is_cumulative`
* `anchor`

{% hint style="info" %}
If `time_agg` is defined, the data Lynk will return on SQL API requsts will be on the level of the main entity + the selected time grain. If no `time_agg` was defined, Lynk will return one record per `entity`.
{% endhint %}

#### Using time\_agg in SELECT statements

In case of using a time aggregation via the `time_agg` API property, You will need to add the parameter `time_agg` to the SQL API SELECT clause for Lynk to retrieve the rigth results, aggregated on both the entity and the selected time\_grain (exposed within `time_agg`)

### `time_grain [optional]`

Optional, defaults to `day`. &#x20;

Time grains are time aggregation levels. Lynk will aggregate the whole SQL API / REST API query according to the selected time grain.&#x20;

The supported time grains are:

* year
* quarter
* month
* week
* day
* hour
* minute

For example:&#x20;

```sql
// SQL API

USE {
  time_agg {
    time_grain : week
}

SELECT  customer_id,
        time_agg as date_week,
        count_orders
FROM    entity('customer')
```

The above example returns for each customer and week, the result of the feature count\_orders.

### `window_size` \[optional]

Optional, defaults to `1`.&#x20;

Window size is for aggregating rolling windows - this property will determine the window size of the rolling window. Note that the time grain will be taken into account here for determining the "size" of the window as well.&#x20;

`window sizes` supports **integer** values.&#x20;

For example:&#x20;

```sql
// SQL API

USE {
  time_agg {
    time_grain : month,
    window_size: 3,
    direction: backward
    
}

SELECT  customer_id,
        time_agg as date_month,
        count_orders
FROM    entity('customer')
```

The above example returns for each customer and month, the result of the feature count\_orders in the last 3 months.

### `direction`

Optional, defaults to `backward`.

Determines the direction of the rolling window.

`direction` supports the values

* `backward`
* `forward`

For example:&#x20;

```sql
// SQL API

USE {
  time_agg {
    time_grain : day,
    window_size: 7,
    direction: foreward
    
}

SELECT  customer_id,
        time_agg as date_day,
        count_orders
FROM    entity('customer')
```

The above example returns for each customer and day, the result of the feature count\_orders in the next 7 days.

### is\_cumulative

## Using time\_agg with BI tools

The best way to leverage the power of time aggregations with BI tools, is by passing parameters with the time\_agg properties. This way, you can dynamically change time aggregations from the BI tool without ease.









