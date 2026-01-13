# Glossary

The Glossary is your business dictionary—a structured collection of acronyms, jargon, and domain-specific terms that your organization uses.

## Overview

Glossary nodes provide quick, concise definitions for business terms and acronyms. They're used by both the Head (agent brain) and Hands (task executors) to understand the language your team uses.

## When to Use Glossary

Use Glossary context when you need to:

- Define acronyms (ARR, CAC, MQL, etc.)
- Explain industry jargon or technical terms
- Provide quick reference definitions
- Standardize terminology across teams
- Translate between business and technical terms

## Fields

| Field | Required | Description |
| --- | --- | --- |
| `type` | Required | Must be `glossary` |
| `domain` | Required | Which domain(s) this applies to: `"*"`, `"marketing"`, etc. |

## Glossary Format

Glossary entries use a structured YAML format:

```yaml
---
type: glossary
domain: "*"
---

TERM_ABBREVIATION:
  term: Full Term Name
  description: Brief explanation of what it means.

ANOTHER_TERM:
  term: Another Term Name
  description: Concise definition.
```

## Examples

### Example 1: Company-Wide Glossary

```yaml
---
type: glossary
domain: "*"
---

ARR:
  term: Annual Recurring Revenue
  description: Yearly value of active subscriptions.

MRR:
  term: Monthly Recurring Revenue
  description: Monthly value of active subscriptions.

CAC:
  term: Customer Acquisition Cost
  description: Total cost to acquire a new customer.

LTV:
  term: Lifetime Value
  description: Total revenue expected from a customer over their lifetime.

Churn:
  term: Customer Churn
  description: Rate at which customers cancel or don't renew.

DAU:
  term: Daily Active Users
  description: Number of unique users active on a given day.

MAU:
  term: Monthly Active Users
  description: Number of unique users active in a given month.
```

### Example 2: Marketing Glossary

```yaml
---
type: glossary
domain: "marketing"
---

MQL:
  term: Marketing Qualified Lead
  description: A lead with engagement score > 50.

SQL:
  term: Sales Qualified Lead
  description: A lead vetted by sales as ready for direct outreach.

CAC:
  term: Customer Acquisition Cost
  description: Total marketing and sales cost divided by new customers acquired.

CPC:
  term: Cost Per Click
  description: Amount paid for each click on a paid advertisement.

CPM:
  term: Cost Per Mille (Thousand Impressions)
  description: Cost to show an ad 1,000 times.

CTR:
  term: Click-Through Rate
  description: Percentage of people who click an ad after seeing it.

CRO:
  term: Conversion Rate Optimization
  description: Process of improving website conversion rates.

ROAS:
  term: Return On Ad Spend
  description: Revenue generated per dollar spent on advertising.
```

### Example 3: Finance Glossary

```yaml
---
type: glossary
domain: "finance"
---

ARR:
  term: Annual Recurring Revenue
  description: Yearly value of active subscriptions normalized to 12 months.

GAAP:
  term: Generally Accepted Accounting Principles
  description: Standard accounting framework used in financial reporting.

EBITDA:
  term: Earnings Before Interest, Taxes, Depreciation, and Amortization
  description: Measure of company profitability excluding financing and accounting decisions.

NRR:
  term: Net Revenue Retention
  description: Revenue retained from existing customers including expansions and churn.

GRR:
  term: Gross Revenue Retention
  description: Revenue retained from existing customers excluding expansions.

Bookings:
  term: Bookings
  description: Total value of signed contracts in a period.

Billings:
  term: Billings
  description: Amount invoiced to customers in a period.

Collections:
  term: Collections
  description: Actual cash received from customers in a period.

DSO:
  term: Days Sales Outstanding
  description: Average number of days to collect payment after a sale.
```

### Example 4: Product/Engineering Glossary

```yaml
---
type: glossary
domain: "product"
---

API:
  term: Application Programming Interface
  description: Interface that allows applications to communicate with each other.

SLA:
  term: Service Level Agreement
  description: Commitment to uptime, performance, or response time.

P95:
  term: 95th Percentile
  description: The value below which 95% of observations fall (used for latency metrics).

WAU:
  term: Weekly Active Users
  description: Number of unique users active in a 7-day period.

Cohort:
  term: User Cohort
  description: Group of users who share a common characteristic or start date.

Funnel:
  term: Conversion Funnel
  description: Series of steps users take toward a desired action.

Feature Flag:
  term: Feature Flag
  description: Toggle that enables or disables functionality without deploying code.

A/B Test:
  term: A/B Test
  description: Experiment comparing two versions to see which performs better.
```

### Example 5: Sales Glossary

```yaml
---
type: glossary
domain: "sales"
---

ACV:
  term: Annual Contract Value
  description: Total value of a contract normalized to 12 months.

TCV:
  term: Total Contract Value
  description: Total value of a contract over its entire term.

ARR:
  term: Annual Recurring Revenue
  description: Yearly value of recurring revenue from subscriptions.

MRR:
  term: Monthly Recurring Revenue
  description: Monthly value of recurring revenue from subscriptions.

Upsell:
  term: Upsell
  description: Selling additional features or higher tiers to existing customers.

Cross-sell:
  term: Cross-sell
  description: Selling complementary products to existing customers.

Churn:
  term: Customer Churn
  description: Rate at which customers cancel or don't renew contracts.

Pipeline:
  term: Sales Pipeline
  description: Total value of all deals in progress across all stages.

Quota:
  term: Sales Quota
  description: Target revenue or number of deals expected from a salesperson.
```

## Glossary vs Knowledge

The key difference between Glossary and Knowledge is depth and format:

| Glossary | Knowledge |
| --- | --- |
| Structured YAML format | Free-form Markdown |
| Short, dictionary-style definitions | Rich, detailed explanations |
| One or two sentences | Multiple paragraphs |
| Term + description | Context, examples, rules |

### When to Use Glossary

Use Glossary for:
- Simple acronym expansions
- Quick term lookups
- Standardizing vocabulary
- Terms that need only a sentence or two

**Example:**
```yaml
MQL:
  term: Marketing Qualified Lead
  description: A lead with engagement score > 50.
```

### When to Use Knowledge

Use Knowledge for:
- Detailed explanations
- Business rules and context
- Multi-paragraph documentation
- Examples and edge cases

**Example:**
```yaml
---
type: knowledge
domain: "marketing"
---

# Marketing Qualified Leads (MQL)

An MQL is a lead that has reached an engagement score above 50 points.

## How Scoring Works
- Email open: +5 points
- Link click: +10 points
- Content download: +15 points
- Webinar attendance: +20 points
- Demo request: +30 points

## Conversion Rates
MQLs typically convert to customers within:
- Enterprise: 60-90 days
- Mid-Market: 30-45 days
- SMB: 7-14 days

## Handling in CRM
Once a lead reaches MQL status:
1. Auto-assign to appropriate sales rep based on territory
2. Add to nurture email sequence
3. Schedule follow-up task within 48 hours
```

## Best Practices

### Keep Definitions Concise

{% hint style="success" %}
**Good:** "Total revenue expected from a customer over their lifetime."

**Bad:** "Lifetime Value (LTV) is a really important metric that we use to understand how much revenue we can expect from a customer throughout their entire relationship with our company, which helps us make decisions about how much we should spend on customer acquisition."
{% endhint %}

### Be Domain-Specific When Needed

The same acronym can mean different things in different domains:

**Marketing ARR:**
```yaml
---
type: glossary
domain: "marketing"
---

ARR:
  term: Annual Recurring Revenue
  description: Yearly subscription value used for customer segmentation.
```

**Finance ARR:**
```yaml
---
type: glossary
domain: "finance"
---

ARR:
  term: Annual Recurring Revenue
  description: Yearly subscription value recognized according to GAAP standards.
```

### Avoid Circular Definitions

{% hint style="success" %}
**Good:**
```yaml
DAU:
  term: Daily Active Users
  description: Number of unique users who performed at least one action in a 24-hour period.
```

**Bad:**
```yaml
DAU:
  term: Daily Active Users
  description: The DAU metric for a given day.
```
{% endhint %}

### Include Units or Thresholds

When relevant, specify units or thresholds:

```yaml
P95_Latency:
  term: 95th Percentile Latency
  description: API response time in milliseconds below which 95% of requests fall. Target is <200ms.

Large_Account:
  term: Large Account
  description: Customer with more than 1,000 seats or $100K+ ARR.
```

### Standardize Across Teams

Use the company-wide glossary (`domain: "*"`) for terms that should mean the same thing everywhere:

```yaml
---
type: glossary
domain: "*"
---

Active_Customer:
  term: Active Customer
  description: Customer with at least one login or transaction in the last 90 days.

Fiscal_Year:
  term: Fiscal Year
  description: Company fiscal year runs April 1 to March 31.
```

## Organizing Large Glossaries

For organizations with many terms, consider organizing by domain:

**Structure:**
- `context/glossary-company.md` - Company-wide terms
- `context/glossary-marketing.md` - Marketing-specific terms
- `context/glossary-finance.md` - Finance-specific terms
- `context/glossary-product.md` - Product-specific terms
- `context/glossary-sales.md` - Sales-specific terms

This makes glossaries easier to maintain and update.

## Common Pitfalls

### Don't Mix Glossary with Instructions

{% hint style="danger" %}
**Wrong:**
```yaml
SQL:
  term: Structured Query Language
  description: Use CTEs for complex queries and always filter by date.
```

**Right:**
```yaml
SQL:
  term: Structured Query Language
  description: Language for querying relational databases.
```

Put the instructions in Task Instructions, not Glossary.
{% endhint %}

### Don't Use Glossary for Long Explanations

If your description is more than 2-3 sentences, use Knowledge instead.

### Don't Forget to Update

Glossaries become stale. Review and update regularly:
- When business processes change
- When new products launch
- When teams adopt new terminology
- At least quarterly

## See Also

- [Context Guide](context-guide.md) - Complete overview of the Context system
- [Knowledge](knowledge.md) - Detailed business definitions and rules
- [Task Instructions](task-instructions.md) - Task execution guidelines
