# Canonical Example Companies

All Full Examples sections across all file-type docs use these three companies. Use their exact names, entity names, feature names, metric names, and glossary terms. Never invent alternatives — consistency across files is what makes the docs work as a coherent learning resource.

Examples always appear in this order: B2B SaaS → E-commerce → Mobile gaming.

---

## Company 1 — Grove (B2B SaaS)

Grove sells subscription-based business software to companies. Examples are simple and focused on subscription concepts.

**Entities:** `customer`, `subscription`

**Key features on `customer`:**
- `id`, `company_name`, `status` ('active' / 'churned' / 'trial'), `plan_type` ('starter' / 'growth' / 'enterprise'), `arr` (Annual Recurring Revenue in USD), `churn_date`, `nps_score`, `first_paid_at`, `is_test_account` (boolean), `is_deleted` (boolean)
- Formula: `customer_tier` ('SMB' / 'Mid-Market' / 'Enterprise' — derived from `arr`)

**Key features on `subscription`:**
- `subscription_id`, `customer_id`, `status`, `plan_id`, `billing_cycle` ('monthly' / 'annual'), `amount_cents`, `started_at`, `current_period_end`, `cancelled_at`
- Formula: `mrr` (normalized monthly value in USD — `amount_cents / 100 / 12` for annual, `amount_cents / 100` for monthly)
- Formula: `is_pending_cancellation` (true if status='active' and cancelled_at is set and current_period_end > today)

**Entity metrics on `customer`:** `count_customers`, `total_arr`, `avg_arr`, `churn_rate`
**Entity metrics on `subscription`:** `count_subscriptions`, `total_mrr`, `count_pending_cancellation`, `mrr_at_risk`

**Metric features on `customer` (from `subscription`):** `total_mrr` (sum of active subscription MRR), `active_subscription_count`

**Glossary terms:** `logo_churn`, `revenue_churn`, `expansion`, `ndr` (Net Dollar Retention), `at_risk`, `power_user`

**Fiscal year:** starts February 1. Q1 = Feb–Apr, Q2 = May–Jul, Q3 = Aug–Oct, Q4 = Nov–Jan.

**Default filters:** exclude test accounts (`is_test_account = false`), exclude deleted accounts (`is_deleted = false`)

**Revenue rule:** `arr` is the default revenue metric. `mrr = arr / 12`. Do not use `total_paid` as a proxy for ARR — it includes one-time fees.

---

## Company 2 — Bly (E-commerce)

Bly sells consumer goods directly to shoppers online. Examples are simple and show concepts different from subscription SaaS — transactional orders, product categories, channels, refunds.

**Entities:** `order`, `customer`, `product`

**Key features on `order`:**
- `order_id`, `customer_id`, `status` ('completed' / 'cancelled' / 'refunded' / 'pending'), `channel` ('organic' / 'paid_search' / 'paid_social' / 'email' / 'direct'), `gross_amount` (in USD before discounts/refunds), `net_amount` (in USD after discounts/refunds), `discount_pct`, `order_date` (time_field — use for filtering, not `created_at`), `is_test_order` (boolean)
- First/last: `primary_category` (highest-value item's product category, from `db_prod.core.order_items` via `order_to_items` join)

**Key features on `customer`:**
- `id`, `email`, `status` ('active' / 'lapsed' / 'new'), `first_order_date`, `total_orders`, `total_net_revenue`, `vip` (boolean)

**Key features on `product`:**
- `product_id`, `name`, `category`, `subcategory`, `price`, `margin_pct`

**Entity metrics on `order`:** `count_orders`, `sum_net_revenue`, `avg_order_value`, `refund_rate`
**Entity metrics on `customer`:** `count_customers`, `repeat_purchase_rate`

**Glossary terms:** `repeat_customer`, `new_customer`, `vip`, `winback`, `conversion`

**Default revenue metric:** `net_amount` (after discounts and refunds). Never use `gross_amount` for revenue analysis unless the user explicitly asks for gross.

**Default filter:** always filter `status = 'completed'` for revenue questions. Exclude `is_test_order = true`.

---

## Company 3 — Arcadia (Mobile gaming)

Arcadia makes a casual mobile game monetized through in-app purchases (IAP). Examples are more complex — non-obvious definitions, pre-calculated features, UTC timezone handling, segment staleness, and data quality caveats from a legacy migration.

**Entities:** `player`, `session`, `purchase`, `player_cohort`

**Key features on `player`:**
- `player_id`, `username`, `install_date` (use for cohort analysis — NOTE: pre-migration players have this set to 2022-03-01 regardless of actual install), `last_session_at` (use for activity, not `is_active` which lags 24h), `device_type`, `country`
- `d7_retained` (boolean — pre-calculated, true if player had a session on exactly day 7 post-install)
- `total_spend_usd` (metric feature from `purchase`, hard currency only — does NOT include soft currency)
- `spend_last_30_days_usd` (filtered metric feature from `purchase`)
- Formula: `player_segment` — 'whale' (total_spend_usd > $100 in rolling 30 days) / 'dolphin' ($10–$100) / 'minnow' (<$10 with ≥1 purchase) / 'non-payer' (no purchases). **Calculated weekly in batch — may lag up to 7 days.**

**Key features on `purchase`:**
- `purchase_id`, `player_id`, `purchase_date`, `item_type`, `hard_currency_amount`, `net_revenue_usd`, `purchase_currency`, `store` ('ios' / 'android')

**Key features on `session`:**
- `session_id`, `player_id`, `session_start`, `session_end`, `duration_seconds`, `level_reached`

**Entity metrics on `player`:** `count_players`, `avg_spend_usd`, `count_dau` (players with last_session_at >= today - 7 days)
**Entity metrics on `purchase`:** `count_purchases`, `sum_net_revenue_usd`, `arpdau` (sum_net_revenue_usd / count_dau — computed at domain level, not per player)

**Relationships:**
- `player-session`: one_to_many. Two named joins: `player_to_session` (default, all sessions) and `player_to_meaningful_session` (non-default, filters `duration_seconds > 5` to exclude crash/load sessions)
- `player-purchase`: one_to_many via `player_id`
- `player-achievement`: many_to_many via `player_achievements` bridge table

**Glossary terms:** `whale`, `dolphin`, `minnow`, `lapsed` (30+ days no session), `d7_retention`, `arpdau`, `soft_currency`, `hard_currency`

**Revenue rules:** always filter `purchase_currency = 'USD'` unless multi-currency is explicitly requested. Use `net_revenue_usd` not `hard_currency_amount`. Soft currency transactions are not revenue.

**Activity rule:** "active" = `last_session_at >= CURRENT_DATE - INTERVAL '7 days'`. "Lapsed" = 30+ days no session. Never use `is_active` — it lags 24h behind.

**Retention rule:** D1/D7/D30 retention values are pre-calculated on the `player_cohort` entity. Never re-derive them from session data.

**Timezone:** all timestamps are UTC. Day boundaries for DAU and ARPDAU are UTC midnight.

**Segment rule:** always use the `player_segment` feature — never manually recalculate from `total_spend_usd`. The feature uses a 30-day rolling window from the weekly batch; ad-hoc recalculation gives different results.

**Data quality:** players who installed before 2022-03-01 have `install_date` set to that date (legacy migration). Do not use `install_date` for cohort analysis on pre-migration players.
