# Main Concepts

This page defines the core concepts and vocabulary used throughout the product and in this documentation.

---

## Semantic Graph

The full set of YAML and Markdown files in your project that define what your data is and how the agent should work with it. Entity YAML files form the data layer — what tables exist, what fields mean, how to aggregate. Context Markdown files form the knowledge layer — what your terms mean, how the agent should behave, what SQL rules apply.

Together, these two layers are what the agent reads to answer questions. Building and maintaining the semantic graph is the primary work of a Semantic Engineer.

---

## Domain

A business unit or audience that has its own view of the data. Domains let you present different feature definitions, context, and language to different consumers without duplicating the underlying entity model.

**Examples:** `finance`, `marketing`, `customer_success`, `sales`, `product`. Each team sees the data through their own lens — same entities, different definitions, different context.

**Key rules:**
- Entities are always defined in the main domain (`default`) — they are shared across all audiences.
- Custom domains (e.g., `marketing`, `finance`) override only what differs. Everything else falls back to `default`.
- A domain does not replicate entity YAML files unless it needs to change feature definitions for that audience.

**Example:** A `customer` entity exists in the main domain. The `finance` domain defines "active customer" as one with a paid invoice in the last 30 days. The `marketing` domain defines it as anyone who opened an email last month. Same entity, different definitions per audience.

---

## Entity

A modeled business concept — the authoritative definition of a real-world thing. An entity is not a database table; it is the governed, curated representation of what the business knows about that concept.

Each entity is defined in a YAML file (the source of truth for its data model) and enriched with Markdown files that carry its business knowledge and task instructions.

**Characteristics:**
- Has a `key_source` (the primary warehouse table) and one or more `keys` (the fields that uniquely identify a row).
- Has `features` — the attributes you can query.
- Has `metrics` — aggregation logic you can apply to roll up rows.
- Can be related to other entities, enabling joins and feature chaining.

**Examples:** `customer`, `order`, `session`, `invoice`.

---

## Source

A raw warehouse table or view used to enrich an entity with additional fields. Sources are not entities — they have no metrics, no relationships, and no independent existence in the model.

**What sources are used for:**
- `field` features that pull a column directly from a source table.
- `first_last` features that retrieve the first or last value from a source table, ordered by a field.

**What sources cannot do:**
- Define metrics.
- Appear as targets in relationships.
- Be queried directly.

**Example:** `db.public.customer_info` is a source used by the `customer` entity to pull `country`, `plan_type`, and `signup_date`. The entity governs the meaning; the source provides the raw data.

---

## Feature

An attribute of an entity — something you can select, filter, or group by in a query. Every column you expose to users is a feature. There are four feature types:

| Type | What it does | Example |
|---|---|---|
| `field` | Pulls a column directly from a source table | `email` from `db.public.customers` |
| `metric` | Pulls an aggregated value from a metric defined on a related entity | `total_revenue` pulling `sum_amount` from `order` |
| `first_last` | Retrieves the first or last value from a source, ordered by a field | `first_order_date` (first by `created_at`) from `orders` |
| `formula` | A derived value computed from other features on the same entity | `days_since_signup` computed from `signup_date` |

Features of type `metric` are the mechanism of **feature chaining** — they bridge entities and make aggregated facts available as attributes of a dimension entity.

---

## Metrics and Feature Chaining

**Entity metrics** are aggregation expressions defined on an entity — they describe how to roll up its rows. Defined in the `metrics:` section of an entity YAML.

**Example:** On the `order` entity, the metric `sum_amount` is `SUM({amount})`. It aggregates revenue across all order rows for a given customer.

**Feature chaining** is how you surface that aggregation on a related entity. A `customer` entity can define a `total_revenue` feature of type `metric` that points to `order.sum_amount` — making revenue a queryable attribute of every customer, without duplicating the aggregation logic.

The chain has three parts:
1. A fact entity (`order`) defines a metric (`sum_amount`).
2. A relationship connects the dimension entity to the fact entity (`customer → order`).
3. The dimension entity (`customer`) defines a metric feature (`total_revenue`) pointing to `order.sum_amount`.

Aggregation logic lives once — on the fact entity — and is reused by any entity that relates to it.

---

## Relationship

A connection between two entities that enables joins and feature chaining. Relationships are defined in `entities_relationships.yml`, not inside individual entity files.

**Key rule:** Relationships are defined once, regardless of direction. A `customer → order` relationship covers both "a customer's orders" and "this order's customer".

Relationships have a type (`one_to_many`, `many_to_many`, etc.) and one or more **joins** that specify how to connect the entities in SQL. Joins can be direct SQL expressions, field-based, or multi-hop lookups through a bridge table.

---

## Context

The collection of markdown files that teach the agent what things mean and how to work with your data. Context files do not contain SQL logic — they contain knowledge, guidance, terminology, and behavioral rules.

There are four context file types:

| Type | Frontmatter | When the agent loads it |
|---|---|---|
| `knowledge` | `type: knowledge` | When the domain is active (domain-level) or when the entity is identified (entity-level) |
| `task-instructions` | `type: task-instructions` | Only when the agent performs that specific task (e.g. text-to-sql) |
| `glossary` | `type: glossary` | When the scoped domain is active |
| `behavior` | `type: behavior` | Always — governs how the agent communicates |

Context compounds — the agent loads all applicable files together, from broadest scope to most specific.

---

## Agent and Tasks

The agent is the reasoning layer. It reads the user's request, selects the relevant context, and decides what to do. When it needs to produce output — like writing SQL — it performs a task.

**Tasks** are specific operations the agent executes, like `text-to-sql`. Each task has its own task instructions file that tells the agent how to perform that task correctly — which filters to apply, how to handle edge cases, naming conventions.

For guidance on which context file type to use for what, see [Context](#context) above.
