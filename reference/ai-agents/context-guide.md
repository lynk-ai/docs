# Context Guide

Teach Lynk your business—your definitions, your rules, your preferences.

Lynk is an AI analytics assistant. Ask questions in plain English, get answers from your data.

Out of the box, Lynk is powerful—but it doesn't know _your_ business. It doesn't know that "active customer" means someone who purchased in the last 90 days. It doesn't know that revenue excludes refunds. It doesn't know that Marketing and Finance define "customer" differently.

**Context** is how you teach Lynk your world. This guide shows you how.

## The Semantic Graph

Before Lynk can answer questions, it needs to understand your business structure. The semantic graph is that structure—a map of your business objects, their properties, and how they connect.

### Why a Graph?

Think of a traditional database: tables with columns, connected by foreign keys. You need to know which tables exist, how they join, and write SQL to get answers.

The semantic graph abstracts this away. Instead of tables and columns, Lynk sees **business concepts**: Customers, Orders, Products. Instead of JOINs, it sees **relationships**: Customers _place_ Orders, Orders _contain_ Products.

### The Building Blocks

The semantic graph consists of four core building blocks:

**Entities**
The core objects you ask questions about

**Features**
Properties that describe each entity

**Metrics**
Pre-defined calculations and KPIs

**Relationships**
How entities connect to each other

#### Entities

An entity represents a core business object—something you ask questions about. Customer, Order, Product, Campaign. Each entity maps to a table in your database, but you think in business terms.

#### Features

Features are the attributes of an entity—the things you filter by, group by, or display. A Customer has `segment`, `region`, `signup_date`. Features can be direct fields or calculated formulas.

#### Metrics

Metrics are pre-defined aggregations—your business KPIs. Instead of everyone writing their own "revenue" calculation, you define it once: `SUM(order_total) WHERE status != 'refunded'`.

#### Relationships

Relationships link entities together. A Customer _places_ Orders. An Order _contains_ Products. These connections let you ask questions that span multiple entities.

### Defining Entities in YAML

```yaml
name: customer
description: Customer information and purchase history
key_table: sales.dim_customer
keys:
  - customer_id

features:
  - type: field
    name: segment
    data_type: string
    field: segment

  - type: formula
    name: is_active
    data_type: boolean
    sql: CASE WHEN {last_engagement} >= DATEADD(day, -30, CURRENT_DATE) THEN TRUE ELSE FALSE END

metrics:
  - name: customer_count
    sql: 'COUNT(*)'
```

{% hint style="info" %}
**Structure without meaning**

The semantic graph defines what exists—entities, features, relationships. But it doesn't define what things _mean_ to your business. That's the missing piece.
{% endhint %}

## Domains

A domain is a business unit—Marketing, Finance, Sales. Each domain gets its own view of the semantic graph.

### Why Domains?

Different teams see the same data differently:

| Domain | Customer means... | They care about... |
| --- | --- | --- |
| Marketing | Someone attributed to a campaign | Acquisition channel, lead score |
| Finance | A revenue source | Lifetime value, payment history |
| Sales | An account to close | Deal stage, contract value |

### Each Domain Has Its Own View

Think of domains as **lenses** on your data. Each domain can add features, override definitions, and define different metrics.

## The Agent

When you ask Lynk a question, an agent takes over. Think of it like a person with a brain and hands: the brain understands and decides, the hands do the work.

### The Head (Brain)

Understands your question and decides what to do.

### The Hands (Tasks)

Execute the work: query data, search docs, explain insights.

### Task Types

| Task | What it does | Example |
| --- | --- | --- |
| Text-to-SQL | Converts questions to SQL queries | "How many customers ordered?" |
| Semantic Search | Finds information in docs | "What's our churn definition?" |
| Data Story | Explains insights and trends | "Why did revenue drop?" |

## The Missing Piece

The semantic graph gives Lynk structure—entities, features, relationships. But structure alone isn't enough for the agent to perform tasks.

### The Gap

Consider: _"How many active customers do we have?"_

Lynk knows from the graph:
- ✓ "Customer" is an entity
- ✓ There's a feature `is_active`

Lynk doesn't know:
- ✗ What "active" means to Marketing vs Finance
- ✗ That test customers should be excluded

### Context Completes the Graph

**Context nodes are part of the semantic graph.** They attach to entities and provide the information the agent needs to perform tasks correctly.

### Four Types of Context

**Knowledge**
"What things mean"—definitions, business rules.
_Used by: Head + Hands_

**Task Instructions**
"How to execute"—rules for SQL, search, analysis.
_Used by: Hands only_

**Glossary**
"What terms mean"—your business dictionary.
_Used by: Head + Hands_

**Agent Behavior**
"How to communicate"—tone, formatting.
_Used by: Head only_

{% hint style="warning" %}
**Task Instructions bypass the Head**

Task Instructions go directly to the Hands—the Head never sees them. The Head doesn't need SQL syntax rules; the Text-to-SQL task does.
{% endhint %}

## Knowledge

Knowledge teaches Lynk what things mean—definitions, business rules, and technical details that help the agent understand your world.

### Fields

| Field | Required | Options |
| --- | --- | --- |
| `type` | Required | `knowledge` |
| `domain` | Required | `"*"`, `"marketing"`, or `["marketing", "sales"]` |
| `entity` | Optional | `"*"`, `"customer"` |
| `tasks` | Optional | `"*"`, `"text-to-sql"` |

### Example: Company-Wide Knowledge

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

### Example: Entity-Specific Knowledge

```yaml
---
type: knowledge
domain: "marketing"
entity: "customer"
---

# Customer (Marketing View)
For Marketing, a customer is attributed to the campaign that drove their first purchase.

## Status Definitions
- new: First purchase within last 30 days
- engaged: Opened email in last 14 days
- churned: No activity in 90+ days

"Active" means engaged with a campaign in last 30 days.
```

## Task Instructions

Task Instructions tell the Hands how to execute—SQL syntax, query patterns, and execution guidelines.

{% hint style="warning" %}
**Instructions go directly to Tasks**

The Head never sees Instructions. They bypass the brain and go straight to the task that needs them.
{% endhint %}

### Fields

| Field | Required | Options |
| --- | --- | --- |
| `type` | Required | `task-instructions` |
| `domain` | Required | `"*"`, `"marketing"` |
| `tasks` | Required | `"*"`, `"text-to-sql"` |
| `entity` | Optional | `"*"`, `"customer"` |

### Example: Global SQL Rules

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

## Always Exclude
- Test data: WHERE is_test = false
- Deleted records: WHERE deleted_at IS NULL
```

## Glossary

The Glossary is your business dictionary—acronyms, jargon, and domain-specific terms that your organization uses.

### Glossary vs Knowledge

**Use Glossary for...**
Quick definitions

"MQL = Marketing Qualified Lead, score > 50"

**Use Knowledge for...**
Rich context

"How Marketing tracks customer lifecycle and engagement"

### Example

```yaml
---
type: glossary
domain: "*"
---

ARR:
  term: Annual Recurring Revenue
  description: Yearly value of active subscriptions.

CAC:
  term: Customer Acquisition Cost
  description: Total cost to acquire a new customer.

MQL:
  term: Marketing Qualified Lead
  description: A lead with engagement score > 50.
```

## Agent Behavior

Agent Behavior controls how Lynk communicates—tone, formatting, and interaction style.

### Fields

| Field | Required | Options |
| --- | --- | --- |
| `type` | Required | `behavior` |
| `domain` | Required | `"*"`, `"marketing"` |
| `kind` | Required | `tone`, `output_format`, `clarification_policy`, `language` |

### Example: Tone

```yaml
---
type: behavior
domain: "*"
kind: tone
---

Be concise and direct. Lead with the answer.
Use business terminology, not technical jargon.
Be confident—avoid hedging like "might" or "perhaps".
```

### Same Data, Different Style

**Finance (precise)**
"Q3 revenue: $2,847,293.00

12.3% YoY increase. Excludes $142K pending refunds."

**Marketing (narrative)**
"We hit $2.8M in Q3—up 12%!

Enterprise drove the growth. Break down by campaign?"

## Full Walkthrough

Let's trace a complete example from question to answer.

{% hint style="success" %}
**The Scenario**

"How many MQLs converted to customers last month?"

**User:** Sarah, Marketing Analyst
{% endhint %}

**Step 1: Head receives the question**
Parses key concepts: "MQLs," "converted," "customers," "last month"

**Step 2: Head identifies scope**
- Domain: Marketing
- Entity: Customer
- Task: Text-to-SQL

**Step 3: Head gathers context**
- **Knowledge:** Marketing Department, Customer (Marketing View)
- **Glossary:** MQL = Marketing Qualified Lead (score > 50)
- **Agent Behavior:** Concise tone, format numbers as K/M

**Step 4: Head delegates to Text-to-SQL**
- **Knowledge:** "MQL conversion = lead with score > 50 who purchased"
- **Task Instructions:** "Use marketing schema, exclude test campaigns"

**Step 5: Text-to-SQL executes**
```sql
SELECT COUNT(*) FROM marketing.dim_customer
WHERE lead_score > 50
  AND first_purchase_date >= DATEADD(month, -1, CURRENT_DATE)
  AND campaign_id NOT LIKE 'TEST_%'
```
**Result:** 847

**Step 6: Head formats response**
"847 MQLs converted to customers last month"—up 23% from previous month.

### What Made This Work

**Glossary**
Lynk knew "MQL" means Marketing Qualified Lead with score > 50.

**Knowledge**
Lynk understood Marketing's definition of "conversion."

**Task Instructions**
SQL task knew to use marketing schema and exclude test campaigns.

**Agent Behavior**
Response was concise with relevant comparison.

## Scoping Rules

Context can be scoped to apply exactly where needed using three dimensions.

| Scope | What it targets | Examples |
| --- | --- | --- |
| Domain | Business unit | `"*"`, `"marketing"`, `["marketing", "sales"]` |
| Task | Execution type | `"*"`, `"text-to-sql"`, `"semantic-search"` |
| Entity | Business object | `"*"`, `"customer"`, `["customer", "order"]` |

### Specificity Rules

When multiple context pieces match, **more specific wins**:

1. `domain: "*"` — lowest priority
2. `domain: ["marketing", "sales"]` — medium
3. `domain: "marketing"` — highest priority

## Quick Reference

| Type | Purpose | Required Fields | Optional | Used By |
| --- | --- | --- | --- | --- |
| `knowledge` | What things mean | `domain` | `entity`, `tasks` | Head + Hands |
| `task-instructions` | How to execute | `domain`, `tasks` | `entity` | Hands only |
| `glossary` | Term definitions | `domain` | — | Head + Hands |
| `behavior` | Communication style | `domain`, `kind` | — | Head only |

{% hint style="success" %}
**Getting Started**

Start simple: add domain knowledge, then entity definitions, then task instructions. Refine based on results—Lynk learns immediately from any context you add.
{% endhint %}
