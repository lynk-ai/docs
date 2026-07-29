# Canonical Example Companies

All `## Examples` sections across the docs use these three companies. Use their exact names — entities, features, metrics, glossary terms — and express them in **v2 schema** form. Never invent alternatives; consistency across pages is what makes the docs cohere.

When a page needs a minimal and a realistic example, the minimal one can be a bare snippet and the realistic one should draw on a canonical company. Examples appear in this order when more than one company is shown: B2B SaaS → E-commerce → Mobile gaming.

## v2 framing reminders

Express every example in the v2 model — do not reach for v1 constructs:

- An entity is a folder: `ENTITY.md` (prose + frontmatter) + `schema.yml` (structure). Its `identity` is a physical table (`maindb.public.customers`) or another entity (`core.customer`).
- A **feature** has six fields: `name`, `description`, `sql`, `data_type`, optional `join_name`, optional `filter`. There are no `field`/`formula`/`first_last`/`metric` feature *types* — derived values are just `sql` expressions; row-selection uses `first()`/`last()`; a cross-entity value carries a `join_name`.
- A **metric** is entity-local (no `join_name`) and is invoked as `metric(entity.metric_name)`.
- A cross-entity aggregate is a **feature** whose `sql` references a metric on a related entity through a `join_name` — not a metric on the consuming entity.
- **Relationships** are `entity_relationships` (or `table_relationships`) with `cardinality`, `steps`, and a `name` used as a feature's `join_name`. Multiple relationships between the same pair are named separately; one may be `default: true`.
- The glossary is `key → name / description` only — no `refers_to`.

---

## Company 1 — Grove (B2B SaaS)

Grove sells subscription-based business software to companies. Examples are simple and focused on subscription concepts.

**Entities:** `customer` (`identity: maindb.public.customers`, key `id`), `subscription` (`identity: maindb.public.subscriptions`, key `subscription_id`)

**Features on `customer`:**
- `company_name`, `status` ('active' / 'churned' / 'trial'), `plan_type` ('starter' / 'growth' / 'enterprise'), `arr` (Annual Recurring Revenue in USD), `churn_date`, `nps_score`, `first_paid_at`, `is_test_account` (boolean), `is_deleted` (boolean)
- `customer_tier` — derived feature, `sql` deriving 'SMB' / 'Mid-Market' / 'Enterprise' from `arr`
- `total_mrr`, `active_subscription_count` — cross-entity features whose `sql` references metrics on `subscription` via the `customer_to_subscription` join

**Features on `subscription`:**
- `customer_id`, `status`, `plan_id`, `billing_cycle` ('monthly' / 'annual'), `amount_cents`, `started_at`, `current_period_end`, `cancelled_at`
- `mrr` — derived feature (normalized monthly value in USD: `amount_cents / 100 / 12` for annual, `amount_cents / 100` for monthly)
- `is_pending_cancellation` — derived boolean (status='active' and `cancelled_at` set and `current_period_end` > today)

**Metrics on `customer`:** `count_customers`, `total_arr`, `avg_arr`, `churn_rate`, `churned_customers`
**Metrics on `subscription`:** `count_subscriptions`, `total_mrr`, `count_pending_cancellation`, `mrr_at_risk`

**Relationship:** `customer_to_subscription` (one_to_many, `customer.id = subscription.customer_id`)

**Glossary terms:** `logo_churn`, `revenue_churn`, `expansion`, `ndr` (Net Dollar Retention), `at_risk`, `power_user`

**Fiscal year:** starts February 1. Q1 = Feb–Apr, Q2 = May–Jul, Q3 = Aug–Oct, Q4 = Nov–Jan.

**Default filters:** exclude test accounts (`is_test_account = false`) and deleted accounts (`is_deleted = false`).

**Revenue rule:** `arr` is the default revenue metric. `mrr = arr / 12`. Do not use `total_paid` as a proxy for ARR — it includes one-time fees.

---

## Company 2 — Bly (E-commerce)

Bly sells consumer goods directly to shoppers online. Examples show transactional concepts — orders, product categories, channels, refunds.

**Entities:** `order` (`identity: maindb.public.orders`, key `order_id`), `customer` (key `id`), `product` (`identity: maindb.public.products`, key `product_id`)

**Features on `order`:**
- `customer_id`, `status` ('completed' / 'cancelled' / 'refunded' / 'pending'), `channel` ('organic' / 'paid_search' / 'paid_social' / 'email' / 'direct'), `gross_amount` (USD before discounts/refunds), `net_amount` (USD after discounts/refunds), `discount_pct`, `order_date` (use for filtering, not `created_at`), `is_test_order` (boolean)
- `primary_category` — feature using `last(...)` row-selection over the `order_items` table via the `order_to_items` table relationship (highest-value item's category)

**Features on `customer`:** `email`, `status` ('active' / 'lapsed' / 'new'), `first_order_date`, `total_orders`, `total_net_revenue`, `vip` (boolean)

**Features on `product`:** `name`, `category`, `subcategory`, `price`, `margin_pct`

**Metrics on `order`:** `count_orders`, `sum_net_revenue`, `avg_order_value`, `refund_rate`, `completed_revenue`
**Metrics on `customer`:** `count_customers`, `repeat_purchase_rate`

**Relationships:** `order_to_customer` (many_to_one), `order_to_items` (one_to_many, to the order-items source)

**Glossary terms:** `repeat_customer`, `new_customer`, `vip`, `winback`, `conversion`

**Default revenue metric:** `net_amount` (after discounts and refunds). Never use `gross_amount` for revenue unless the user explicitly asks for gross.

**Default filter:** filter `status = 'completed'` for revenue questions; exclude `is_test_order = true`.

---

## Company 3 — Arcadia (Mobile gaming)

Arcadia makes a casual mobile game monetized through in-app purchases (IAP). Examples are more complex — non-obvious definitions, pre-calculated features, UTC handling, segment staleness, and data-quality caveats from a legacy migration.

**Entities:** `player` (`identity: maindb.public.players`, key `player_id`), `session` (key `session_id`), `purchase` (key `purchase_id`), `player_cohort`, `achievement`, `player_achievement` (bridge entity — `identity: maindb.public.player_achievements`, links `player` ↔ `achievement`)

**Features on `player`:**
- `username`, `install_date` (use for cohort analysis — NOTE: pre-migration players have this set to 2022-03-01 regardless of actual install), `last_session_at` (use for activity, not `is_active` which lags 24h), `device_type`, `country`
- `d7_retained` (boolean — pre-calculated, true if the player had a session on exactly day 7 post-install)
- `total_spend_usd` — cross-entity feature referencing a metric on `purchase` (hard currency only — excludes soft currency), via the `player_to_purchase` join
- `spend_last_30_days_usd` — cross-entity feature with a `filter` on the purchase window
- `player_segment` — derived feature: 'whale' (>$100 rolling 30d) / 'dolphin' ($10–$100) / 'minnow' (<$10 with ≥1 purchase) / 'non-payer'. **Calculated weekly in batch — may lag up to 7 days.**

**Features on `purchase`:** `player_id`, `purchase_date`, `item_type`, `hard_currency_amount`, `net_revenue_usd`, `purchase_currency`, `store` ('ios' / 'android')

**Features on `session`:** `player_id`, `session_start`, `session_end`, `duration_seconds`, `level_reached`

**Metrics on `player`:** `count_players`, `avg_spend_usd`, `count_dau` (daily active users — players with `last_session_at >= CURRENT_DATE`, UTC midnight boundary)
**Metrics on `purchase`:** `count_purchases`, `sum_net_revenue_usd`
(ARPDAU — `sum_net_revenue_usd / count_dau` — is a domain-level KPI computed at query time from two entities' metrics, **not** an entity-local metric; it lives as a glossary term, not under `metrics:`.)

**Relationships:**
- `player_to_session`: one_to_many (default — all sessions) and `player_to_meaningful_session`: one_to_many (non-default, `filter duration_seconds > 5` to exclude crash/load sessions)
- `player_to_purchase`: one_to_many via `player_id`
- `player_to_achievement`: many_to_many via the `player_achievement` bridge entity (two steps)

**Glossary terms:** `whale`, `dolphin`, `minnow`, `lapsed` (30+ days no session), `d7_retention`, `arpdau`, `soft_currency`, `hard_currency`

**Revenue rules:** filter `purchase_currency = 'USD'` unless multi-currency is explicitly requested. Use `net_revenue_usd`, not `hard_currency_amount`. Soft-currency transactions are not revenue.

**Activity rule:** "active" = `last_session_at >= CURRENT_DATE - INTERVAL '7 days'`. "Lapsed" = 30+ days no session. Never use `is_active` — it lags 24h.

**Retention rule:** D1/D7/D30 retention values are pre-calculated on the `player_cohort` entity. Never re-derive them from session data.

**Timezone:** all timestamps are UTC. Day boundaries for DAU and ARPDAU are UTC midnight.

**Segment rule:** always use the `player_segment` feature — never recalculate from `total_spend_usd`. It uses a 30-day rolling window from the weekly batch; ad-hoc recalculation differs.

**Data quality:** players who installed before 2022-03-01 have `install_date` set to that date (legacy migration). Do not use `install_date` for cohort analysis on pre-migration players.
