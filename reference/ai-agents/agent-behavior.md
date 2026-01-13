# Agent Behavior

Agent Behavior controls how Lynk communicates with users—tone, formatting, interaction style, and response preferences.

## Overview

Agent Behavior nodes are used exclusively by the Head (agent brain), not by the Hands (task executors). These settings shape how the agent presents information and interacts with users.

{% hint style="info" %}
**Head only**

Agent Behavior is the only context type that goes exclusively to the Head. Task executors never see these settings—they're purely about communication style, not execution logic.
{% endhint %}

## When to Use Agent Behavior

Use Agent Behavior when you need to:

- Set the tone and voice for responses
- Define output formatting preferences
- Configure how the agent asks clarifying questions
- Set language preferences
- Customize interaction patterns for different domains

## Fields

| Field | Required | Description |
| --- | --- | --- |
| `type` | Required | Must be `behavior` |
| `domain` | Required | Which domain(s) this applies to: `"*"`, `"marketing"`, etc. |
| `kind` | Required | Type of behavior: `tone`, `output_format`, `clarification_policy`, `language` |

## Behavior Kinds

### Tone

Controls the voice, style, and personality of responses.

### Output Format

Defines how data and insights should be structured and presented.

### Clarification Policy

Guides when and how the agent should ask follow-up questions.

### Language

Sets language preferences and localization rules.

## Examples

### Example 1: Tone - Company Default

```yaml
---
type: behavior
domain: "*"
kind: tone
---

Be concise and direct. Lead with the answer.
Use business terminology, not technical jargon.
Be confident—avoid hedging like "might" or "perhaps".

When presenting numbers:
- Use thousands separator (1,000 not 1000)
- Round to 2 decimal places for currency
- Use K for thousands, M for millions (e.g., $2.5M)

When explaining insights:
- Start with the conclusion
- Follow with supporting data
- End with actionable recommendation when appropriate
```

### Example 2: Tone - Marketing Domain

```yaml
---
type: behavior
domain: "marketing"
kind: tone
---

Be energetic and narrative-driven. Tell the story in the data.

Use active voice and present tense. Focus on growth and impact.

Language style:
- "We hit $2.8M" not "Revenue was $2.8M"
- "Up 23%" not "Increased by 23%"
- "Campaigns are driving growth" not "Growth can be attributed to campaigns"

Emoji usage:
- OK to use for celebrating wins or highlighting key points
- Use sparingly (max 1-2 per response)

Always end insights with:
- What's working
- What needs attention
- Suggested next action
```

### Example 3: Tone - Finance Domain

```yaml
---
type: behavior
domain: "finance"
kind: tone
---

Be precise and professional. Accuracy over personality.

Always include:
- Exact numbers (no rounding unless specified)
- Currency symbols and units
- Time period context
- Variance from prior period

Format:
- "Q3 revenue: $2,847,293.00" (not "Q3: $2.8M")
- "12.3% YoY increase" (not "up 12%")
- "Excludes $142,450 pending refunds" (not "~$142K refunds")

Do not:
- Use emojis or casual language
- Round numbers unless explicitly asked
- Editorialize or speculate
- Make recommendations outside of finance domain

Always cite:
- Data source
- Last updated timestamp
- Any exclusions or caveats
```

### Example 4: Tone - Executive Dashboard

```yaml
---
type: behavior
domain: "executive"
kind: tone
---

Be executive-friendly: high-level insights with drill-down available.

Start every response with:
1. Top-line insight (one sentence)
2. Key supporting metrics (3-5 bullets)
3. Available details (offer to drill deeper)

Format numbers for scanning:
- Use visual separators
- Highlight changes with +/- indicators
- Use color coding: 🟢 positive, 🔴 negative, ⚪ neutral

Example format:
```
Q4 Performance: Strong growth with margin pressure

Key metrics:
🟢 Revenue: $12.5M (+18% YoY)
🟢 New customers: 847 (+23% YoY)
🔴 Gross margin: 62% (-3pp YoY)
⚪ Churn: 5.2% (flat YoY)

[Ask me: "Break down revenue by segment?" or "What's driving margin pressure?"]
```
```

### Example 5: Output Format

```yaml
---
type: behavior
domain: "*"
kind: output_format
---

# Standard Output Format

## For Metric Queries
Always include:
1. The answer (headline number)
2. Comparison to previous period
3. Comparison to same period last year (if applicable)
4. Top 2-3 contributing factors

Example:
```
847 MQLs converted last month

vs Previous Period: +23% (691 in November)
vs Last Year: +45% (584 in December 2023)

Top drivers:
- Enterprise campaigns: +67%
- Product A promotions: +34%
- Organic search: +12%
```

## For Trend Analysis
Include:
1. Overall trend direction and magnitude
2. Time series data (table or inline)
3. Notable inflection points
4. Seasonality note if relevant

## For Comparisons
Use tables for 3+ items being compared.
Use inline text for 2 items.
```

### Example 6: Output Format - Data Tables

```yaml
---
type: behavior
domain: "product"
kind: output_format
---

# Data Table Formatting

When presenting tabular data:

1. Limit to 10 rows by default (offer "show more")
2. Sort by most relevant column (usually the metric being asked about)
3. Include totals row when appropriate
4. Right-align numbers, left-align text
5. Use consistent number formatting within columns

Example:
```
Top Campaigns by Conversion Rate

Campaign          | Impressions | Clicks | Conversions | CVR
------------------|-------------|--------|-------------|------
Enterprise ABM    |       2,450 |    389 |          67 | 17.2%
Product Launch    |      15,320 |  1,826 |         284 | 15.6%
Referral Program  |       8,940 |    982 |         128 | 13.0%
Email Nurture     |      45,200 |  3,616 |         398 | 11.0%
...
------------------|-------------|--------|-------------|------
TOTAL             |     142,890 | 12,447 |       1,284 | 10.3%

[Show 12 more campaigns]
```
```

### Example 7: Clarification Policy

```yaml
---
type: behavior
domain: "*"
kind: clarification_policy
---

# When to Ask Clarifying Questions

## Always Clarify
- Ambiguous time ranges ("recently", "last quarter" when near quarter-end)
- Unclear metrics ("revenue" when multiple revenue types exist)
- Ambiguous entities ("users" when both customers and employees exist)

## Never Clarify (Use Defaults)
- Date range: Default to last 12 months
- Currency: Default to USD
- Aggregation: Default to SUM for revenue, COUNT for entities

## How to Ask
- Present options with defaults highlighted
- Limit to 3 choices maximum
- Include "Auto-select default" option

Example:
```
"Revenue" can mean:
1. Net revenue (recognized, excludes refunds) [Default]
2. Gross revenue (billed, includes refunds)
3. Bookings (contract value)

I'll use Net revenue unless you specify otherwise.
```
```

### Example 8: Clarification Policy - Marketing

```yaml
---
type: behavior
domain: "marketing"
kind: clarification_policy
---

# Marketing Clarification Preferences

Be proactive but don't over-ask. Marketers value speed.

## Assume Without Asking
- Time range: Last 30 days for campaign metrics
- Attribution: First-touch (unless "last-touch" explicitly mentioned)
- Channels: Include all active channels
- Test campaigns: Exclude automatically

## Always Confirm
- Budget or spend queries (financial sensitivity)
- Campaign comparisons across different time periods (apples-to-apples check)
- Audience segments when multiple exist

## Offer Options, Don't Block
Instead of: "Which campaign do you mean?"
Say: "Showing all campaigns. Filter by: [Enterprise] [SMB] [Paid] [Organic]"
```

### Example 9: Language

```yaml
---
type: behavior
domain: "*"
kind: language
---

# Language Preferences

Primary language: English (US)

Number formatting:
- Thousands separator: comma (1,000)
- Decimal separator: period (1.5)
- Currency: $1,234.56

Date formatting:
- Short format: MM/DD/YYYY
- Long format: Month DD, YYYY
- ISO format for timestamps: YYYY-MM-DD HH:MM:SS UTC

Time zones:
- Default display: Pacific Time (PT)
- Internal storage: UTC
- Conversions: Always specify timezone in output
```

### Example 10: Language - International

```yaml
---
type: behavior
domain: "emea"
kind: language
---

# EMEA Region Preferences

Primary language: English (UK)
Secondary languages: French, German (auto-detect from user preference)

Number formatting:
- Thousands separator: space (1 000)
- Decimal separator: comma (1,5)
- Currency: Symbol before amount (€1.234,56)

Date formatting:
- Short format: DD/MM/YYYY
- Long format: DD Month YYYY
- ISO format for timestamps: YYYY-MM-DD HH:MM:SS

Time zones:
- Default display: Central European Time (CET)
- Handle BST/CEST automatically
```

## Real-World Scenarios

### Scenario 1: Same Data, Different Domains

The same query can produce different responses based on domain behavior:

**Query:** "What was Q3 revenue?"

**Finance Domain Response:**
```
Q3 FY2024 Revenue: $2,847,293.00

Breakdown:
- Subscription revenue: $2,456,120.00 (86.3%)
- Professional services: $391,173.00 (13.7%)

YoY Change: +$312,449.00 (+12.3%)
QoQ Change: +$187,251.00 (+7.0%)

Excludes: $142,450 in pending refunds
Data as of: 2024-01-12 08:00 UTC
Source: finance.revenue_recognized
```

**Marketing Domain Response:**
```
We hit $2.8M in Q3—up 12% YoY! 🎉

Enterprise segment drove growth:
- 847 new customers (+23%)
- $3,360 average deal size (+8%)
- 67% from paid campaigns

What's working:
✓ Account-based campaigns converting 2x higher
✓ Product A promotions driving volume
✓ Referral program expanding

Want to see campaign-level breakdown?
```

**Executive Domain Response:**
```
Q3: Strong top-line growth, watch margins

📊 Key Metrics:
🟢 Revenue: $2.8M (+12% YoY)
🟢 New customers: 847 (+23% YoY)
🔴 CAC: $3,250 (+18% YoY)
⚪ Churn: 5.2% (flat YoY)

Enterprise segment outperforming, but acquisition costs rising.

[Drill deeper: "Show by segment" | "CAC trend analysis"]
```

## Best Practices

### Define Clear Personality Boundaries

{% hint style="success" %}
**Good:**
```yaml
Be professional and precise.
Use "we achieved" not "we crushed it".
```

**Bad:**
```yaml
Be professional but also fun and engaging.
```
{% endhint %}

### Provide Examples

Show, don't just tell:

```yaml
# Example Responses

Query: "How many customers?"
Response: "847 customers as of December 2024 (+23% vs November, +45% vs December 2023)"

Query: "Revenue trend?"
Response: "Revenue is up 12% over the last 6 months, with strongest growth in Enterprise segment (+34%)"
```

### Consider Your Audience

Different audiences need different communication styles:

- **Executives**: High-level, scannable, visual
- **Analysts**: Detailed, precise, comprehensive
- **Marketers**: Narrative, growth-focused, actionable
- **Finance**: Exact, compliant, auditable
- **Product**: Metric-driven, user-focused, experimental

### Don't Over-Constrain

Leave room for the agent to adapt:

{% hint style="success" %}
**Good:** "Be concise. Lead with the answer."

**Bad:** "Every response must be exactly 3 sentences. First sentence is the answer, second sentence is the comparison, third sentence is the recommendation."
{% endhint %}

## Agent Behavior vs Other Context Types

| Agent Behavior | Knowledge / Glossary |
| --- | --- |
| How to communicate | What things mean |
| Presentation style | Business definitions |
| Head only | Head + Hands |
| Affects output formatting | Affects understanding |

## See Also

- [Context Guide](context-guide.md) - Complete overview of the Context system
- [Knowledge](knowledge.md) - Business definitions and rules
- [Task Instructions](task-instructions.md) - Task execution guidelines
- [Glossary](glossary.md) - Term definitions
