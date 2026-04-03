# Project Structure

This page describes the canonical folder layout, naming conventions, and placement rules for every file type in a Lynk semantic layer project.

---

## Folder Layout

```
.lynk/
├── default/                              # Primary domain — all entity definitions live here
│   ├── entities/
│   │   ├── {entity}.yml                  # Entity definition (features, metrics, related_sources)
│   │   └── {entity}/                     # Context files for this entity
│   │       ├── {entity}__knowledge.md
│   │       └── {entity}__task_inst__text_to_sql.md
│   ├── domain_context/
│   │   ├── {domain}_knowledge.md         # Domain-wide business context
│   │   └── {domain}__task_inst__text_to_sql.md  # Domain-wide SQL rules
│   ├── agent/
│   │   ├── clarification_policy.md       # When and how to ask clarifying questions
│   │   └── output_format.md              # Table formatting, tone, insights pattern
│   ├── {domain}_glossary.md              # Term and acronym dictionary
│   ├── entities_relationships.yml        # All entity-to-entity relationships
│   └── evaluations.yml                   # Evaluation test cases
│
└── {custom_domain}/                      # Custom domain — overrides only
    ├── entities/
    │   ├── {entity}.yml                  # Only if feature definitions differ from default
    │   └── {entity}/
    │       └── {entity}__knowledge.md    # Domain-specific knowledge override
    └── evaluations.yml                   # Domain-specific evaluation test cases
```

---

## Naming Conventions

**Double underscore (`__`) is the file name delimiter** for all context files. This distinguishes file segments and makes parsing unambiguous.

| Pattern | Meaning |
|---|---|
| `{entity}__knowledge.md` | Knowledge file scoped to this entity |
| `{entity}__task_inst__text_to_sql.md` | Task instructions for text-to-sql, scoped to this entity |
| `{domain}__task_inst__text_to_sql.md` | Task instructions for text-to-sql, scoped to the domain |
| `{domain}_glossary.md` | Glossary file for the domain (single underscore — it is a standalone file, not a context override) |

---

## What Goes Where

| File type | Location | Scope | Read by |
|---|---|---|---|
| Entity YAML | `default/entities/{entity}.yml` | Entity | Agent + Tasks |
| Entity knowledge | `default/entities/{entity}/{entity}__knowledge.md` | Entity + domain | Agent + Tasks |
| Entity task instructions | `default/entities/{entity}/{entity}__task_inst__text_to_sql.md` | Entity + domain | Tasks only |
| Domain knowledge | `default/domain_context/{domain}_knowledge.md` | Domain-wide | Agent + Tasks |
| Domain task instructions | `default/domain_context/{domain}__task_inst__text_to_sql.md` | Domain-wide | Tasks only |
| Glossary | `default/{domain}_glossary.md` | Domain-wide | Agent + Tasks |
| Behavior files | `default/agent/{kind}.md` | Domain-wide | Agent only |
| Relationships | `default/entities_relationships.yml` | All entities | Agent + Tasks |
| Evaluations | `default/evaluations.yml` | Domain | Evals only |

---

## The Entity Subfolder Pattern

Every entity YAML file has a sibling subfolder with the same name. Context files for that entity live inside this subfolder.

```
entities/
├── player.yml              ← entity definition
└── player/                 ← context files for player
    ├── player__knowledge.md
    └── player__task_inst__text_to_sql.md
```

The entity YAML and its context files are always co-located. When adding a new entity, create both the YAML and the subfolder.

---

## Custom Domain Rules

Custom domains override the default, not replace it. Three rules apply:

1. **Entity YAML files always live in `default/entities/`.** If a custom domain needs all the same features with different context, it only adds context files — not a new entity YAML.

2. **Create a custom domain entity YAML only if feature definitions must differ.** For example, if `marketing` defines `is_active` differently than `default`, create `.lynk/marketing/entities/player.yml` with just the changed features.

3. **Custom domain context files shadow the default.** When the agent is scoped to the `marketing` domain and looks up entity knowledge for `player`, it reads `marketing/entities/player/player__knowledge.md` if it exists, otherwise falls back to `default/entities/player/player__knowledge.md`.

---

## Domain Feature Resolution

When the agent queries an entity in a specific domain, features resolve in this priority order:

1. **Domain-specific feature** (in the custom domain's entity YAML) — highest priority
2. **Multi-domain feature** (matched by `domain: ["marketing", "sales"]` in the feature) — used if no domain-specific override
3. **Wildcard feature** (matched by `domain: "*"`) — used if nothing more specific exists
4. **Default feature** (in `default/entities/{entity}.yml`) — lowest priority, the fallback

This lets a `marketing` domain expose a different definition of `customer_segment` without changing the `default` entity used by analytics teams.
