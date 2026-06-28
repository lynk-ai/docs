---
description: A domain is an agent — one team's analytical surface, with its own vocabulary, entities, skills, and policies. A user talks to one at a time.
icon: users
---

# Domain

A domain is an agent. Each domain is one team's analytical agent — marketing's agent, sales' agent, finance's agent — with its own vocabulary, its own data of interest, and its own way of reasoning.

## Contents

1. [What it is](#what-it-is)
2. [Where it lives](#where-it-lives)
3. [What a domain contains](#what-a-domain-contains)
4. [Sizing a domain](#sizing-a-domain)
5. [Isolation](#isolation)
6. [Cross-domain references](#cross-domain-references)
7. [Examples](#examples)
8. [Validation](#validation)
9. [Related](#related)

## What it is

When a user picks a domain, they are picking which agent answers their question. A user always talks to one agent at a time. Designing a domain *is* designing an agent — every choice about what entities to include, what to call them, what skills to write, and what policies to set is a choice about how that team's agent thinks and answers.

The triple **domain + branch + build** addresses one queryable agent. See [Project](../project.md) for how builds and branches scope a query.

## Where it lives

One folder per domain under `domains/`. The folder name is the domain's name — the domain is derived from the path, with no `domain:` field anywhere.

```
.lynk/domains/<domain>/
├── LYNK.md
├── GLOSSARY.yml
├── entities/
├── skills/
└── policies/
```

Folder names are lowercase alphanumeric with underscores (`marketing`, `core`, `customer_success`) — a domain name can appear in a cross-domain reference (`core.customer` in an [`identity:`/`imports:`](../entity/schema-yml/identity-and-imports.md)). `core` is the conventional shared domain under medallion but is not a reserved name. See [Layout and naming](../../reference/layout-and-naming.md).

## What a domain contains

Everything its agent needs to answer questions in its team's language:

- [Entities](../entity/README.md) the team thinks about — some native to this domain, some pulled in from elsewhere.
- [Skills](../skill.md) for the team's recurring analytical reasoning.
- [Policies](../policy.md) for how the team wants the agent to communicate.
- The team's [`GLOSSARY.yml`](glossary.md) and [`LYNK.md`](lynk-md.md).

What goes in is the team's choice. Marketing's agent might pull in `deals` (a sales concept) because attribution requires it; sales' agent might not. The structure provides the primitives; each team composes their agent.

## Sizing a domain

Create a new domain when you have a new audience whose questions, vocabulary, or definitions would be hurt by another team's bleeding into their answers. Marketing and sales both ask about "leads" — but the term means different things to each, so they get different agents.

Don't create a domain per entity. A domain is a *coherent analytical surface*, not a folder around one thing. A domain with one entity and no skills is probably a placeholder, not yet an agent. Conversely, when one domain starts to feel incoherent — terms meaning different things in different parts, sub-teams disagreeing on definitions — that's the signal to split.

## Isolation

Each domain's agent sees only its own world. Sales' agent doesn't know marketing's definitions; marketing's agent doesn't see finance's metrics unless marketing pulled them in. This is the *definition* of a domain, not a constraint added on top.

When a question can't be answered in the active agent's world, the answer is one of:

- ask a different agent (a different domain);
- expand this agent's world to include what's needed;
- move shared content into a domain that multiple agents can pull from (typically `core`).

Cross-domain reasoning is not a runtime mode. It is a modeling decision the customer makes by choosing what each agent should see.

## Cross-domain references

Isolation is about what an agent *sees*. Whether a domain may *reference* another — via `imports:` or an `@`/file reference — is **not** a domain setting. It's governed by the project [topology](../lynk-yml.md#topology), declared once at the root in `lynk.yml`. Under medallion, a domain reaches its own files, the root reference files, and — when a `shared_domain` is configured — that shared domain (conventionally `core`); peers can't reach each other. See [lynk.yml → topology](../lynk-yml.md#topology) for the rules.

## Examples

**A single domain.** The whole project is one agent.

```
.lynk/domains/core/
└── entities/
    └── customer/
        ├── ENTITY.md
        └── schema.yml
```

**A team domain building on `core`.** Marketing reuses `core.customer` and adds its own skill.

```
.lynk/domains/marketing/
├── LYNK.md
├── GLOSSARY.yml
├── entities/
│   └── customer/        # identity: core.customer
│       ├── ENTITY.md
│       └── schema.yml
└── skills/
    └── attribution-analysis/
        └── SKILL.md
```

## Validation

- A domain folder name is lowercase alphanumeric with underscores.
- A domain with no entities passes with a **warning** — an agent with no entities can't answer anything.
- Cross-domain references that violate the declared topology are build errors.

## Related

- [LYNK.md](lynk-md.md) · [GLOSSARY.yml](glossary.md) — the domain's orientation and vocabulary
- [Entity](../entity/README.md) · [Skill](../skill.md) · [Policy](../policy.md) — what a domain holds
- [lynk.yml → topology](../lynk-yml.md#topology) — where the reference pattern is declared
- [Project](../project.md) — how domain + branch + build address an agent
