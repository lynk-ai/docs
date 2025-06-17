# POP()

Use `POP()` for **period-over-period** calculations. `POP()` can be applied via a SQL API or SQL REST API request to dynamically add period-over-period calculations.

## How `POP()` works

You can think of `POP()` as a function that acts as follows:

"Given a dataset with a granularity level that includes a `time_grain` (day/week/month/etc), for each granularity level (row)  take the `metric`  as the `current_period`. Then move `direction` through time by `time_grain`: skip `skip_periods` periods, `compare_periods` times to collect the same `metric`, and aggregate them using `agg_function` to create the `compare_period`. Finally, apply `pop_formula` to calculate the relationship between `current_period` and `compare_period`."

{% hint style="warning" %}
As `POP()` is a time-based function, using `time_agg` is mandatory for using it. &#x20;

The `time_agg` parameters `time_grain`, `direction` and `window_size` will be used by the `POP()` function as well as the `POP()` parameters.&#x20;
{% endhint %}

## POP() playground

Click the link below to visit a visual playground where you can play around and see how `POP()` works.

{% embed url="https://lynk-ai.github.io/pop-demo-app/" %}
POP visual playground - click to navigate to site
{% endembed %}

***

## Simple POP example

In this example, we define simple `POP` function for the entity `customer`, on the metric feature `total_sales`&#x20;

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
        time_agg as date_day,
        POP(
          metric => 'total_sales',
          skip_periods => 1,
          compare_periods => 6,
          agg_function => ‘avg’,
          pop_formula => ‘absolute_difference’
        ) as tota_sales_over_average_of_last_6_days
FROM    entity('customer')
LIMIT   100
```

In the above example, for each `customer` and `day`,  we are calculating the absolute\_difference of the metric `total_sales` over the average of `total_sales` in the last 6 days.

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

### `metric`

The metric **feature** or **measure** name of the main entity, to apply the POP (period over period) on.

### `skip_periods` \[optional]

Define how many datapoints to "jump over" when calculating the compare period using the `offset` parameter. Defaults to **1**.&#x20;

For example: For comparing total\_sales of each day, to the average of total\_sales on the previous 4 same days of week, we can use `skip_periods` = 7 and `compare_periods` = 4 along with `time_grain` = day and `direction` = backward.

### `compare_periods` \[optional]

Define how many datapoints to take into include for the compare period. In other words, how many data points to include in the compare period. Defaults to **1**.

For example: For comparing total\_sales of each day, to the average of total\_sales on the previous 4 same days of week, we can use `skip_periods` = 7 and `compare_periods` = 4 along with `time_grain` = day and `direction` = backward.

### `agg_function`

The function to apply on the datapoints of the compare period.&#x20;

You can use the following presets:

* absolute\_difference
* relative\_difference&#x20;
* percent\_change
* ratio

### `pop_formula`

The function to apply on the **current period** and the **compare period**.

#### Preset formulas

* avg
* sum
* min
* max
* count
* p\_\<number> \
  For example:  p\_50 for median

#### Custom formulas

Or define a custom function using the parameters `current_period` and `compare_period`

Example for custom `pop_formula`:

```sql
// custom pop_formula
    pop_formula => "({current_period} - {compare_period}) / 2"
```
