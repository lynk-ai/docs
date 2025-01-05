# Time aggregation

When [consuming](./) entities and their features, we can tell Lynk on which time frame to aggregate the features, by using the `time_agg` property in the `USE` config block.&#x20;

#### Examples for time aggregations:

* **Calendric**:  day / month  / year etc
* **Rolling windows** : "last 30 days" / "first 7 days after signup" etc
* **No time frame** (full date range)

{% hint style="info" %}
Lynk decouples features business logic from time aggregation logic.\
A feature's business logic is defined on the feature definition level, while how to apply time aggregate logic to a feature is defined on the consumption level.
{% endhint %}

For example, let's assume we have an entity `customer` and it has a simple metric feature `count_orders` that counts how many orders a customer has.&#x20;

```sql
// SQL API

SELECT  customer_id,
        count_orders
FROM    entity('customer')

```

The above SQL API request will calculate for each `customer` the count of total orders on all available time range in the underlying data asset - in this case `orders` (where the measure `count_orders` comes from).

If we would like to get the **daily** amount of `count_orders` per customer, we can change the query as follows:

```sql
// SQL API

USE {
  time_agg {
    time_grain : day
    }
}

SELECT  customer_id,
        time_agg as date_day,
        count_orders
FROM    entity('customer')

```

In the above example, a record per customer and day will return, counting the amount of orders per customer and day.

***

## Using `time_agg`

### `USE`

Set this object on the SQL API / REST API query, to define all the query level configurations, including time\_agg. See [USE](sql-api/use.md) for in depth information on this.

### `time_agg`

`time_agg` is an object that holds all the options on how to apply time aggregation to our query.

The options for `time_agg` are:

* `time_grain`
* `window_size`
* `direction`
* `is_cumulative`
* `anchor`

{% hint style="info" %}
If `time_agg` is defined, the data Lynk will return on SQL API requsts will be on the level of the main entity + the selected time grain. If no `time_agg` was defined, Lynk will return one record per `entity`.
{% endhint %}

### `time_grain` \[optional]

Optional, defaults to `day`. &#x20;

A time grain refers to the level of granularity at which time is divided in the result of the API query. It determines how entity-level aggregations or calculations (e.g., sums, averages, counts) are grouped.

For example, if the time grain is `day` and the main entity is `customer`, the returned result will be on a customer + day level.

The supported values for `time_grain` are:

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
}

SELECT  customer_id,
        time_agg as date_week,
        count_orders
FROM    entity('customer')
```

The above example returns the result of the feature `count_orders` for each `customer` and `week`.

{% hint style="info" %}
When using small time grains such as `minute`, `hour` and even `day`, it is recommended to use `start_time` and `stop_time` in order to cap the underlying data assets with dates, preventing inefficiencies and unnecessary scan of large data assets.
{% endhint %}

### `window_size` \[optional]

Optional, defaults to `1`.&#x20;

Window size is for aggregating rolling windows - this property will determine the window size of the rolling window. Note that the time grain will be taken into account here for determining the "size" of the window as well.&#x20;

The supported values for `window_size` are:&#x20;

* integer values
* `unbounded`

`window_size` example, using an integer value:

```sql
// SQL API

USE {
  time_agg {
    time_grain : month,
    window_size: 1,
    direction: backward
    }
}

SELECT  customer_id,
        time_agg as date_month,
        count_orders
FROM    entity('customer')
```

The above example returns the cumulative results of the feature `count_orders` in the last `3` months, for each `customer` and `month`.

{% hint style="info" %}
Choosing `window_size` = `1` is equivalent to not choosing a window size.\
For example, if the `time_grain` is set to `day` and `window_size` is set to `1`, the returned result will be aggregated to the level of the entity and `1` day.
{% endhint %}

`window_size` example, using `unbounded`:

```sql
// SQL API

USE {
  time_agg {
    time_grain : month,
    window_size: unbounded,
    direction: backward
    }
}

SELECT  customer_id,
        time_agg as date_month,
        count_orders
FROM    entity('customer')
```

The above example returns for each `customer` and `month`,  the cumulative results of `count_orders` up until that hour. The window of time in this case starts from the first order of each `customer` that matches the business logic of the metric `count_orders`.&#x20;

If we would choose `direction: forward`, the returned results would be the cumulating the feature `count_orders` for each data point (`customer` and `month`) up until the last known order in the underlying data asset.

{% hint style="info" %}
When using `window_size` , Lynk doesn’t introduce new aggregation logic but extends the time window for the existing feature logic to calculate **cumulative** results.
{% endhint %}

### `direction` \[optional]

Optional, defaults to `backward`.

Determines the direction of the rolling window.

The supported values for `direction` are:

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
}

SELECT  customer_id,
        time_agg as date_day,
        count_orders
FROM    entity('customer')
```

The above example returns the result of the feature `count_orders` in the **next** `7` days for each `customer` and `day`.

***

## Query level aggregation

When using `time_agg`, the time aggregation will apply to **all features in the query,** except features that their origin `data_asset` does not have a `default_time_field` and the feature does not have any `aggregate_time_field.`

### Asset default time field

time\_agg will apply only to&#x20;

### Feature aggregate time field

time\_agg will apply only to&#x20;

{% hint style="info" %}
Currently Lynk supports time aggregations on a query level. We have plans on our roadmap to add feature level time aggregations. If this is something you are interested in, please [contact us](https://www.getlynk.ai/book-a-demo) and let us know.
{% endhint %}



***

## Using time\_agg with BI tools

The best way to leverage the power of time aggregations with BI tools, is by passing parameters with the time\_agg properties. This way, you can dynamically change time aggregations from the BI tool without ease.









