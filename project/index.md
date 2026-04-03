# Building a Lynk Project: Top-Down Walkthrough

This walkthrough builds a working Lynk semantic layer from scratch — from business understanding to queryable, accurate entities — in about an hour.

---

## Why Top-Down?

There are two ways to start a Lynk project.

**Bottom-up** — open your warehouse, find a table, write entity YAML for it, add features, repeat. You end up with files that mirror your schema. But the agent has no idea what your business is, what your terms mean, or what filters always apply. SQL is technically correct and semantically wrong.

**Top-down** — write down what the business is and what language it uses. Define who asks questions and what they care about. Give each audience the context they need. Only then model entities.

Top-down produces a semantic layer that answers real business questions because the foundation is business understanding, not schema structure.

---

## What This Walkthrough Builds

The running example is **Grove** — a B2B SaaS company that sells subscription software to businesses. ARR is the primary revenue metric, customers have plan types and NPS scores, and the customer success team has its own view of the data compared to the analytics team.

Every file in this walkthrough is complete and uses real Grove data. No placeholders.

By the end you will have:

- A knowledge file and glossary that define what Grove is and what its terms mean
- Two domains: the main domain (`default`) for analytics, and `cs` for the customer success team
- Domain-wide SQL rules, a clarification policy, and an output format
- Two entities: `customer` (dimension) and `subscription` (fact)
- A relationship connecting them
- Feature chaining so `customer` exposes MRR aggregated from `subscription`
- Entity context files for both entities
- Example questions to validate agent accuracy before going live

Replace `customer` with `user`, `subscription` with `order`, `arr` with `gmv` — the structure is the same.

---

## Steps

1. [Business Context](./01-business-context.md) — Write what Grove is and what its language means
2. [Domains](./02-domains.md) — Define the audiences and when they need different context
3. [Domain Context](./03-domain-context.md) — SQL rules and agent behavior for each domain
4. [Entities](./04-entities.md) — Model `customer` and `subscription`, add relationships and feature chaining
5. [Examples](./05-examples.md) — Add test questions to validate before going to production

---

## Time Estimate

| Step | Time |
|---|---|
| Business context | 10–15 min |
| Domains | 5 min |
| Domain context | 10 min |
| Entities | 20–25 min |
| Examples | 5–10 min |
