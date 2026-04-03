# File Types Quick Reference

A single-page summary of every file type in Lynk. For full field documentation and annotated examples, follow the links to the reference pages.

---

## YAML Files

| File | Purpose |
|---|---|
| Entity YAML | Features, metrics, related sources for one entity |
| Relationships YAML | Entity-to-entity join definitions |
| Evaluations | Test cases for regression testing |

---

## Markdown Context Files

| File type | Frontmatter | When the agent loads it |
|---|---|---|
| Knowledge | `type: knowledge` | When the domain is active (domain-level) or when the entity is identified (entity-level) |
| Task Instructions | `type: task-instructions` | Only when the agent performs that specific task |
| Glossary | `type: glossary` | When the scoped domain is active |
| Output Format | `type: behavior` / `kind: output_format` | Always — governs how responses are structured |
| Clarification Policy | `type: behavior` / `kind: clarification_policy` | Always — governs when the agent asks before executing |

---

## Context File Frontmatter

Every markdown context file starts with a YAML frontmatter block:

**Knowledge file:**
```yaml
---
type: knowledge
domain: "default"        # or "*" for all domains, or a specific domain name
entity: customer         # optional — omit for domain-wide knowledge
---
```

**Task instructions file:**
```yaml
---
type: task-instructions
domain: "default"        # or "*" for all domains, or a specific domain name
tasks: "text-to-sql"     # which task this applies to
entity: customer         # optional — omit for domain-wide instructions
---
```

**Glossary file:**
```yaml
---
type: glossary
domain: "*"              # or a specific domain name
---
```

**Behavior file:**
```yaml
---
type: behavior
kind: output_format      # one of: output_format, clarification_policy
domain: "*"              # or a specific domain name
---
```

---

## Key Distinctions

**Knowledge vs. Task Instructions**

Use knowledge files for definitions, business rules, and data context — things the agent needs to understand the question. Use task instructions for SQL-specific guidance — filters, field choices, query patterns — things the agent needs to execute the task correctly.

**Knowledge vs. Glossary**

Use the glossary for quick term lookups (one or two sentences). Use knowledge files for multi-paragraph explanations, data quality caveats, governance rules, and business context that requires interpretation.

**Behavior vs. Everything Else**

Behavior files control how the agent communicates with users — output format and clarification policy. SQL guidance and business definitions do not belong in behavior files.

---

## Reference Pages

- [Entity YAML](../file-types/entity-yaml.md)
- [Relationships YAML](../file-types/relationships-yaml.md)
- [Knowledge files](../file-types/knowledge-md.md)
- [Task Instructions files](../file-types/task-instructions-md.md)
- [Glossary files](../file-types/glossary-md.md)
- [Output Format files](../file-types/output-format-md.md)
- [Clarification Policy files](../file-types/clarification-policy-md.md)
- [Evaluations YAML](../file-types/evaluations-yaml.md)
