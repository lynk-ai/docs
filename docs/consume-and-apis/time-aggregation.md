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

### `time_grain [optional]`

The supprted time grains are:

* year
* quarter
* month
* week
* day
* hour
* minute

### direction

### window\_size

### is\_cumulative

## Using time\_agg with BI tools

The best way to leverage the power of time aggregations with BI tools, is by passing parameters with the time\_agg properties. This way, you can dynamically change time aggregations from the BI tool without ease.









