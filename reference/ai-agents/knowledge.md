# Knowledge

Knowledge context nodes teach Lynk what things mean in your business—definitions, business rules, and technical details that help the agent understand your world.

## Overview

Knowledge is used by both the Head (agent brain) and Hands (task executors). When a user asks a question, relevant knowledge nodes are retrieved and provided to help the agent understand the business context and execute tasks correctly.

## When to Use Knowledge

Use Knowledge context when you need to:

- Define what business terms mean in your organization
- Explain business rules and policies
- Provide entity-specific context (e.g., how Marketing defines "customer")
- Document important technical details about your data
- Share tribal knowledge that affects how data should be interpreted

## Fields

| Field | Required | Description |
| --- | --- | --- |
| `type` | Required | Must be `knowledge` |
| `domain` | Required | Which domain(s) this applies to: `"*"`, `"marketing"`, or `["marketing", "sales"]` |
| `entity` | Optional | Which entity this relates to: `"*"`, `"customer"`, etc. |
| `tasks` | Optional | Which tasks can use this: `"*"`, `"text-to-sql"`, etc. |

## Scoping Strategy

### Global Knowledge (All Domains)

Use `domain: "*"` for company-wide standards that apply everywhere.

```yaml
---
type: knowledge
domain: "*"
---

# Company Standards

Our fiscal year runs April 1 to March 31.
Revenue is recognized at time of shipment.
All queries should exclude test data (is_test = true).
```

### Domain-Specific Knowledge

Use specific domains when definitions differ across teams.

```yaml
---
type: knowledge
domain: "marketing"
---

# Marketing Department Standards

## Campaign Attribution
We use first-touch attribution. The campaign that drove signup gets credit for all future revenue from that customer.

## Lead Scoring
- Cold lead: 0-25 points
- Warm lead: 26-50 points
- Hot lead: 51-75 points
- MQL: 76+ points
```

### Entity-Specific Knowledge

Combine domain and entity scoping for precise context.

```yaml
---
type: knowledge
domain: "marketing"
entity: "customer"
---

# Customer (Marketing View)

For Marketing, a customer is attributed to the campaign that drove their first purchase.

## Status Definitions
- **new**: First purchase within last 30 days
- **engaged**: Opened email in last 14 days
- **active**: Engaged with a campaign in last 30 days
- **at_risk**: No engagement in 30-60 days
- **churned**: No activity in 90+ days

## Segmentation
Customers are automatically segmented based on:
- Acquisition channel (paid, organic, referral)
- Product category of first purchase
- Geographic region
```

## Real-World Examples

### Example 1: Financial Reporting Rules

```yaml
---
type: knowledge
domain: "finance"
---

# Financial Reporting Standards

## Revenue Recognition
- B2B: Recognized on delivery
- SaaS: Recognized ratably over contract term
- Professional services: Recognized on completion

## Exclusions
Always exclude:
- Internal test accounts (account_type = 'internal')
- Refunded transactions (status = 'refunded')
- Pending transactions (status = 'pending')

## Currency
All monetary values are in USD. FX conversions use the rate on transaction_date.
```

### Example 2: Product Team Definitions

```yaml
---
type: knowledge
domain: "product"
entity: "user"
---

# User Engagement (Product View)

## Activity States
We track user engagement across three dimensions:

### Recency
- Active: Logged in within 7 days
- Dormant: Logged in 8-30 days ago
- Inactive: No login in 30+ days

### Frequency
- Power user: 5+ sessions per week
- Regular user: 2-4 sessions per week
- Occasional user: 1 session per week
- Rare user: Less than 1 session per week

### Depth
Measured by feature adoption score (0-100):
- Beginner: 0-25 (core features only)
- Intermediate: 26-60 (some advanced features)
- Advanced: 61-100 (regular use of advanced features)
```

### Example 3: Sales Team Context

```yaml
---
type: knowledge
domain: "sales"
entity: "account"
---

# Account Management

## Account Tiers
- Enterprise: 1000+ employees, $500K+ ARR potential
- Mid-Market: 100-999 employees, $50K-$500K ARR potential
- SMB: Under 100 employees, under $50K ARR potential

## Health Scores
Account health (0-100) is calculated from:
- Product usage (40%): DAU/MAU ratio
- Financial health (30%): Payment history, growth
- Engagement (30%): Response to outreach, support tickets

Health score interpretation:
- 80-100: Healthy (green)
- 60-79: At risk (yellow)
- Below 60: Critical (red)

## Sales Stages
1. Prospecting
2. Qualification
3. Demo scheduled
4. Proposal sent
5. Negotiation
6. Closed-won / Closed-lost
```

## Best Practices

### Be Specific and Actionable

{% hint style="success" %}
**Good:** "Active customer means purchased in last 90 days AND opened an email in last 30 days"

**Bad:** "Active customers are engaged with our brand"
{% endhint %}

### Document Edge Cases

```yaml
---
type: knowledge
domain: "*"
entity: "order"
---

# Order Processing Rules

## Order Status
- **pending**: Order created, payment not processed
- **paid**: Payment confirmed, not yet fulfilled
- **fulfilled**: Items shipped to customer
- **completed**: Items delivered and confirmed
- **refunded**: Full refund issued
- **partially_refunded**: Partial refund issued

## Edge Cases
- Split shipments: Create one order record per shipment
- Subscription renewals: Treat as new order with order_type = 'renewal'
- Gift orders: Billing customer differs from shipping customer
- Pre-orders: Include in reporting only after fulfillment_date
```

### Explain "Why" Not Just "What"

```yaml
---
type: knowledge
domain: "finance"
---

# Revenue Calculations

## Why We Exclude Refunds
We exclude refunded transactions from revenue reporting because:
1. They don't represent actual value delivered
2. GAAP requires revenue reversal for refunds
3. Including them inflates top-line without bottom-line impact

Use `net_revenue` (excludes refunds) for all standard reporting.
Use `gross_revenue` only when specifically analyzing refund rates.
```

### Keep It Current

Add dates or versioning when policies change:

```yaml
---
type: knowledge
domain: "*"
---

# Data Retention Policy

**Effective:** January 1, 2024

Personal data is retained for:
- Active customers: Duration of relationship + 7 years
- Inactive customers: 3 years after last interaction
- Job applicants: 1 year after application

**Note:** Policy changed on January 1, 2024. Previous retention was 5 years for inactive customers.
```

## Tips for Writing Knowledge

1. **Use clear headings** - Organize information with descriptive section headers
2. **Include examples** - Show what good looks like with concrete examples
3. **Define acronyms** - Don't assume everyone knows internal jargon
4. **Explain calculations** - If metrics have formulas, document them
5. **Update regularly** - Knowledge should evolve as your business changes
6. **Link related concepts** - Reference other entities or features when relevant

## Knowledge vs Glossary

Not sure whether to use Knowledge or Glossary? Here's the distinction:

| Use Knowledge for... | Use Glossary for... |
| --- | --- |
| Rich context and explanations | Quick term definitions |
| Business rules and policies | Acronym expansions |
| Entity-specific definitions | Short, dictionary-style entries |
| Multi-paragraph documentation | One or two sentence definitions |

**Example:**

Glossary:
```yaml
MQL:
  term: Marketing Qualified Lead
  description: A lead with engagement score > 50.
```

Knowledge:
```yaml
# Marketing Qualified Leads

An MQL is a lead that has reached an engagement score above 50 points.

## How Scoring Works
- Email open: +5 points
- Link click: +10 points
- Content download: +15 points
- Webinar attendance: +20 points
- Demo request: +30 points

## When MQLs Convert
MQLs typically convert to customers within:
- Enterprise: 60-90 days
- Mid-Market: 30-45 days
- SMB: 7-14 days
```

## See Also

- [Context Guide](context-guide.md) - Complete overview of the Context system
- [Task Instructions](task-instructions.md) - How to configure task execution
- [Glossary](glossary.md) - Business term definitions
