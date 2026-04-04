# Project Walkthrough

**Build a complete Lynk semantic layer from scratch — in the right order.**

This walkthrough takes you from a blank project to a working, queryable, accurate semantic layer. It follows a top-down approach: business understanding first, entities last. Every file is complete and uses a real running example — no placeholders.

---

## Why top-down?

Starting with entity YAML produces technically valid files but semantically wrong answers — the agent knows your schema but not your business. Starting with business context means every entity you model is grounded in the right definitions, filters, and language from the beginning.

---

## What's in this section

| Page | What you do | Time |
|---|---|---|
| [Building a Lynk Project](index.md) | Understand the approach and what you'll build | 2 min |
| [Step 1: Business Context](01-business-context.md) | Write domain knowledge and glossary before touching any entity | 10–15 min |
| [Step 2: Domains](02-domains.md) | Define audiences and when to create custom domains | 5 min |
| [Step 3: Domain Context](03-domain-context.md) | Create domain-wide SQL rules, clarification policy, and output format | 10 min |
| [Step 4: Entities](04-entities.md) | Model a dimension entity, a fact entity, relationships, and feature chaining | 20–25 min |
| [Step 5: Examples and Evaluations](05-examples.md) | Add evaluation test cases to validate accuracy before going to production | 5–10 min |

Read these pages in order.

---

## What you can do with this

The running example is **Grove** — a B2B SaaS company. By the end you will have built:
- A knowledge file and glossary defining what Grove is and what its terms mean
- Two domains with domain-specific context
- Two entities (`customer` and `subscription`) connected by a relationship with feature chaining
- Evaluation test cases that validate agent accuracy before going live

The structure is directly transferable: replace `customer` with `user`, `subscription` with `order`, `arr` with `gmv` — the pattern is the same.

**Where to go next:**
- Adding to an existing project instead of starting fresh? → [Guides](../guides/README.md)
- Need to understand how a specific concept works? → [Concepts](../concepts/README.md)
- Need exact field documentation? → [File-Types Reference](../file-types/README.md)
