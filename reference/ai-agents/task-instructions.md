# Task Instructions

Task Instructions tell the Hands (task executors) how to perform their work—SQL syntax rules, query patterns, search strategies, and execution guidelines.

## Overview

Task Instructions bypass the Head (agent brain) and go directly to the specific task executor that needs them. The Head never sees these instructions—they're meant for the Hands only.

{% hint style="warning" %}
**Task Instructions are task-specific**

Unlike Knowledge (which is seen by both Head and Hands), Task Instructions only reach the specific task that needs them. SQL generation rules only go to the Text-to-SQL task, not to Semantic Search.
{% endhint %}

## When to Use Task Instructions

Use Task Instructions when you need to:

- Define SQL generation standards and patterns
- Set query performance guidelines
- Specify how to handle edge cases in query generation
- Enforce data access rules at the SQL level
- Configure search behavior or ranking criteria
- Set formatting rules for generated queries

## Fields

| Field | Required | Description |
| --- | --- | --- |
| `type` | Required | Must be `task-instructions` |
| `domain` | Required | Which domain(s) this applies to: `"*"`, `"marketing"`, etc. |
| `tasks` | Required | Which task(s) this targets: `"*"`, `"text-to-sql"`, etc. |
| `entity` | Optional | Limit to specific entity: `"customer"`, etc. |

## Available Tasks

| Task Name | Purpose |
| --- | --- |
| `text-to-sql` | Converts natural language questions to SQL queries |
| `semantic-search` | Searches documentation and knowledge bases |
| `data-story` | Generates insights and narrative explanations |
| `*` | Applies to all tasks (use sparingly) |

## Text-to-SQL Instructions

The most common use case for Task Instructions is guiding SQL query generation.

### Example: Global SQL Standards

```yaml
---
type: task-instructions
domain: "*"
tasks: "text-to-sql"
---

# SQL Generation Rules

## Always Do
- Include a date filter (default: last 12 months)
- Add LIMIT 1000 for exploratory queries
- Use CTEs for queries with more than 2 joins
- Add comments explaining complex logic

## Always Exclude
- Test data: WHERE is_test = false
- Deleted records: WHERE deleted_at IS NULL
- Internal accounts: WHERE account_type != 'internal'

## Performance
- Avoid SELECT * (specify columns explicitly)
- Use indexes when available (check query plan)
- For large tables (>10M rows), require date filters
```

### Example: Domain-Specific SQL Rules

```yaml
---
type: task-instructions
domain: "finance"
tasks: "text-to-sql"
---

# Finance SQL Standards

## Compliance Requirements
- Always use `recognized_revenue`, not `gross_revenue`
- Default date ranges to fiscal year (April 1 - March 31)
- Round all currency to 2 decimal places
- Include audit trail: created_by, created_at in SELECT

## Exclusions
Finance reporting must exclude:
- Pending transactions: WHERE status = 'completed'
- Inter-company transfers: WHERE transaction_type != 'internal_transfer'
- Proforma invoices: WHERE invoice_type = 'final'

## Required Aggregations
When calculating revenue metrics:
```sql
SUM(CASE
  WHEN status = 'completed'
    AND is_refund = false
    AND transaction_type != 'internal_transfer'
  THEN recognized_revenue
  ELSE 0
END) as total_revenue
```
```

### Example: Entity-Specific SQL Instructions

```yaml
---
type: task-instructions
domain: "marketing"
tasks: "text-to-sql"
entity: "customer"
---

# Customer Query Instructions (Marketing)

## Schema
Use the `marketing.dim_customer` table, not `sales.customers`.

## Required JOINs
When querying customer data:
- Always join to `campaign_attribution` for acquisition source
- Join to `engagement_scores` for activity metrics
- Join to `customer_segments` for current segmentation

## Default Filters
Unless explicitly requested otherwise:
- Include only customers with `is_valid_email = true`
- Exclude customers with `opt_out_marketing = true`
- Default to customers acquired in last 2 years

## Example Query Pattern
```sql
SELECT
  c.customer_id,
  c.email,
  ca.campaign_name,
  es.engagement_score,
  cs.segment_name
FROM marketing.dim_customer c
LEFT JOIN campaign_attribution ca ON c.customer_id = ca.customer_id
LEFT JOIN engagement_scores es ON c.customer_id = es.customer_id
LEFT JOIN customer_segments cs ON c.customer_id = cs.customer_id
WHERE c.is_valid_email = true
  AND c.opt_out_marketing = false
  AND c.acquisition_date >= DATEADD(year, -2, CURRENT_DATE)
```
```

## Semantic Search Instructions

Configure how the agent searches through documentation and knowledge bases.

### Example: Search Behavior

```yaml
---
type: task-instructions
domain: "*"
tasks: "semantic-search"
---

# Documentation Search Guidelines

## Search Strategy
1. Search in this order:
   - Domain-specific knowledge nodes
   - Entity definitions and documentation
   - Company-wide knowledge
   - External documentation (if enabled)

2. Prioritize recent documents (last 90 days) over older content

3. When multiple results found:
   - Rank by relevance score
   - Prefer domain-specific over general
   - Show top 3 results maximum

## Response Format
When returning search results:
- Quote relevant sections directly
- Include document source and last updated date
- Provide link to full document if available
```

## Data Story Instructions

Guide how the agent explains insights and generates narratives.

### Example: Storytelling Guidelines

```yaml
---
type: task-instructions
domain: "marketing"
tasks: "data-story"
---

# Marketing Insights Guidelines

## Narrative Structure
1. Start with the headline insight
2. Provide supporting data points
3. Explain contributing factors
4. Suggest actionable next steps

## Data Presentation
- Use percentage changes, not absolute numbers (unless specifically requested)
- Compare to previous period and year-ago
- Highlight statistical significance
- Call out anomalies or outliers

## Language Style
- Use active voice and present tense
- Avoid jargon; explain technical terms
- Frame insights around business impact
- Be specific: "23% increase" not "significant increase"

## Example Response Format
```
Campaign Performance: Up 23%

Your email campaigns drove 847 conversions last month—23% higher than
November and 45% above the same period last year.

What's driving growth:
- Enterprise segment: +67% (new account-based campaigns)
- Product category A: +34% (seasonal promotions)
- Organic search: +12% (SEO improvements)

What to watch:
- Mobile conversion rate declined 8% (mobile UX review recommended)
- Weekend campaigns underperforming weekday by 15%

Next steps:
- Double down on enterprise ABM campaigns
- Test mobile checkout improvements
- Shift weekend budget to weekdays
```
```

## Real-World Examples

### Example 1: E-commerce SQL Standards

```yaml
---
type: task-instructions
domain: "*"
tasks: "text-to-sql"
---

# E-commerce Query Standards

## Order Queries
When querying orders:
- Use `order_completed_at` for time ranges, not `order_created_at`
- Include both order-level and item-level metrics
- Always join to `products` table for accurate categorization

## Revenue Calculations
```sql
-- Net Revenue (standard)
SUM(order_total - discount_amount - refund_amount) as net_revenue

-- Gross Revenue (for specific analysis only)
SUM(order_total) as gross_revenue

-- Average Order Value
SUM(order_total - discount_amount - refund_amount) / COUNT(DISTINCT order_id) as aov
```

## Customer Lifetime Value
Use the pre-calculated `customer_ltv` field from `analytics.customer_metrics`.
Do NOT calculate LTV in ad-hoc queries—it requires complex cohort logic.
```

### Example 2: SaaS Metrics Standards

```yaml
---
type: task-instructions
domain: "product"
tasks: "text-to-sql"
---

# SaaS Product Metrics

## Usage Queries
Default time grain: daily aggregates from `product_usage_daily`

For hourly analysis (performance heavy):
- Require date range <= 7 days
- Use `product_usage_hourly` table
- Add LIMIT 10000

## Key Metrics Definitions

### Daily Active Users (DAU)
```sql
COUNT(DISTINCT user_id)
WHERE last_activity_at >= CURRENT_DATE
  AND user_status = 'active'
```

### Monthly Active Users (MAU)
```sql
COUNT(DISTINCT user_id)
WHERE last_activity_at >= DATEADD(day, -30, CURRENT_DATE)
  AND user_status = 'active'
```

### Stickiness (DAU/MAU)
```sql
WITH dau AS (
  SELECT COUNT(DISTINCT user_id) as daily_active
  FROM users
  WHERE last_activity_at >= CURRENT_DATE
),
mau AS (
  SELECT COUNT(DISTINCT user_id) as monthly_active
  FROM users
  WHERE last_activity_at >= DATEADD(day, -30, CURRENT_DATE)
)
SELECT
  (dau.daily_active * 1.0 / mau.monthly_active) * 100 as stickiness_pct
FROM dau, mau
```
```

### Example 3: Data Quality Rules

```yaml
---
type: task-instructions
domain: "*"
tasks: "text-to-sql"
---

# Data Quality Standards

## Timestamp Handling
- Always use UTC for timestamps
- Convert to local timezone only for display
- Use DATE_TRUNC for daily aggregates
- Use DATE_PART for extracting components

## NULL Handling
Be explicit about NULL handling:
```sql
-- Count with NULL awareness
COUNT(*) as total_records,
COUNT(field_name) as non_null_records,
COUNT(*) - COUNT(field_name) as null_records

-- Aggregations with NULL handling
COALESCE(SUM(revenue), 0) as total_revenue,
AVG(COALESCE(score, 0)) as average_score
```

## Data Freshness
Check data freshness before running queries:
```sql
-- Include data freshness check
SELECT MAX(updated_at) as last_updated
FROM table_name
```

If data is >24 hours old, warn the user before returning results.
```

## Best Practices

### Be Specific About Edge Cases

{% hint style="success" %}
**Good:**
```yaml
## Handling Refunds
- Full refunds: Exclude from revenue (status = 'refunded')
- Partial refunds: Subtract refund_amount from order_total
- Pending refunds: Include in revenue (not yet processed)
```

**Bad:**
```yaml
## Refunds
Handle refunds appropriately
```
{% endhint %}

### Provide Query Templates

Instead of describing what to do, show working SQL examples:

```yaml
## Revenue by Customer Segment
Use this pattern:

```sql
SELECT
  cs.segment_name,
  COUNT(DISTINCT o.customer_id) as customer_count,
  SUM(o.order_total) as total_revenue,
  AVG(o.order_total) as avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN customer_segments cs ON c.segment_id = cs.segment_id
WHERE o.order_date >= DATEADD(month, -12, CURRENT_DATE)
  AND o.status = 'completed'
GROUP BY cs.segment_name
ORDER BY total_revenue DESC
```
```

### Document Performance Considerations

```yaml
## Query Performance

### Large Tables (>10M rows)
These tables require special handling:
- `events` - 50M+ rows, ALWAYS filter by event_date
- `page_views` - 100M+ rows, use `page_views_daily` aggregate table
- `impressions` - 500M+ rows, use pre-computed `campaign_metrics`

### Expensive JOINs
Avoid JOINs between these table pairs (cross-region):
- `customers` ↔ `events` (use pre-joined `customer_events` view)
- `orders` ↔ `sessions` (use `order_sessions` materialized view)

### Timeout Limits
- Standard queries: 30 second timeout
- Complex analytics: 2 minute timeout (requires approval)
```

## Task Instructions vs Knowledge

Not sure which to use? Here's the distinction:

| Task Instructions | Knowledge |
| --- | --- |
| Goes directly to task executor | Seen by both Head and Hands |
| SQL syntax, query patterns | Business definitions, context |
| "How to execute" | "What things mean" |
| Technical implementation | Business logic |

**Example:**

Knowledge:
```yaml
# Active Customer Definition
An active customer has made a purchase in the last 90 days.
```

Task Instructions:
```yaml
# Active Customer Query
```sql
WHERE last_purchase_date >= DATEADD(day, -90, CURRENT_DATE)
  AND customer_status != 'test'
```
```

## See Also

- [Context Guide](context-guide.md) - Complete overview of the Context system
- [Knowledge](knowledge.md) - Business definitions and rules
- [Glossary](glossary.md) - Term definitions
