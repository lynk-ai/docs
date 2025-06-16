# POP

`POP` is a [Lynk Function](./) that simplifies **period-over-period** calculations. Use it on SQL API or SQL REST API request to dynamically add period-over-period calculations.

## How `POP` works

You can also think of `POP` as follows:

"Given a dataset with granularity that includes a `time_grain` (day/week/month/etc.), take this `metric` for the `current_period`. Then move `direction` through time by `time_grain`: skip `num_skip_periods` periods, `num_compare_periods` times to collect the same `metric`, and aggregate them using `agg_function` to create the `compare_period`. Finally, apply `pop_formula` to calculate the relationship between `current_period` and **`compare_period`**."

{% hint style="warning" %}
As `POP` is a time-based function, using `time_agg` is mandatory for using it. &#x20;

The `time_agg` parameters `time_grain`, `direction` and `window_size` will be used by the `POP` function.
{% endhint %}

***

## Simple POP example

In this example, we define simple `POP` function for the entity `customer`, on the feature&#x20;

```sql
-- A simple SQL API query with POP()
USE {
  "time_agg": {
    "time_grain": "day",
    "direction": "backward",
    "window_size": 1
  },
  "start_time": "2024-01-01",
  "stop_time": "2025-01-01"
}

SELECT  customer_id,
        POP(
          feature => 'total_sales',
          offset => 1,
          repeats => 6,
          offset_operator => ‘avg’,
          pop_operator => ‘absolute_difference’
        ) as tota_sales_over_average_of_last_6_days
FROM    entity('customer')
LIMIT   100
```

In the above example, for each `customer` and `day`,  we are calculating the absolute\_difference of the feature `total_sales` over the average of `total_sales` in the last 6 days.

### `time_grain` (from `time_agg`)

Used for defining the period size. For example, choosing `time_grain` **day**, defines the period as day.

### `direction` (from `time_agg`) \[optional]

Used for defining the direction of the period over period calculation. Defaults to `backward`.

* Choosing direction `backward`, will result by calculating the compare period over a set of datapoints that occurred **before** the datapoint we refer to.\
  For example: Comparing total\_sales of each month, to the average of total\_sales on the **previous** 4 months.
* Choosing direction `forward`, will result by calculating the compare period over a set of datapoints that occurred **after** the datapoint we refer to.\
  For example: Comparing total\_sales of each month, to the average of total\_sales on the **following** 4 months.

### `window_size` (from `time_agg`) \[optional]

Used for defining the size of the cumulative window of the period over period calculation. Defaults to **1**.

### `feature`

The **feature** or **measure** name to apply the POP (period over period) on.

### `offset` \[optional]

Define how many datapoints to "jump over" when calculating the compare period using the `offset` parameter. Defaults to **1**.&#x20;

For example: For comparing total\_sales of each day, to the average of total\_sales on the previous 4 same days of week, we can use `offset` = 7 and `repeats` = 4 along with `time_grain` = day and `direction` = backward.

### `repeats` \[optional]

Define how many datapoints to **repeat** when calculating the compare period using the `repeats` parameter. In other words, how many data points to include in the compare period. Defaults to **1**.

For example: For comparing total\_sales of each day, to the average of total\_sales on the previous 4 same days of week, we can use `offset` = 7 and `repeats` = 4 along with `time_grain` = day and `direction` = backward.

### `offset_operator`

The function to apply on the datapoints of the compare period.&#x20;

You can use the following presets:

* absolute\_difference
* avg

### `pop_operator`

The function to apply on the main datapoint and the result of the compare period dataponts after we applied the `offset_operator` on them.

You can use the following presets:

* absolute\_difference
* avg

Or define a custom function using the parameters `a` and `b`, where `a` is the main data point and b is the group of data points we are comparing to, after we applied the `offset_operator` on them.

Example for custom `pop_operator`:

```sql
// custom pop_operator
    pop_operator => "({a} - {b}) / 2"
```
