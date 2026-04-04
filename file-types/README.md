# File-Types Reference

**The complete field-by-field reference for every file type in Lynk.**

This section documents the exact structure, required fields, allowed values, and behavior of every file you write in a Lynk semantic layer project. Use these pages when you need to know precisely what a field does, what values it accepts, or how a file is loaded.

---

## What's in this section

### YAML Files

| Page | What it covers |
|---|---|
| [Entity YAML](entity-yaml.md) | Features (field, first_last, formula, metric), entity metrics, related_sources, examples, common pitfalls |
| [Relationships YAML](relationships-yaml.md) | Relationship types, join definitions (sql / lookup), multiple named joins, feature chaining dependencies |
| [Evaluations YAML](evaluations-yaml.md) | Test case structure, eval tags, difficulty levels, common pitfalls |

### Markdown Context Files

| Page | What it covers |
|---|---|
| [Knowledge Files](knowledge-md.md) | Business definitions, data quality notes, domain and entity scoping, what belongs here vs. other file types |
| [Task Instructions](task-instructions-md.md) | SQL patterns, default filters, field choices, domain-level vs. entity-level instructions |
| [Glossary Files](glossary-md.md) | Entry format, what terms belong in the glossary vs. knowledge files or entity YAML |
| [Output Format Files](output-format-md.md) | Table structure, tone, insights, data notes, domain-specific formatting |
| [Clarification Policy Files](clarification-policy-md.md) | When to ask vs. when to proceed, default assumptions, response tone |

---

## What you can do with this

Use this section to:
- Look up the exact fields and syntax for a file you're writing
- Understand what goes in each file type vs. the others (when to use knowledge vs. glossary vs. task instructions)
- See annotated full examples for three different company types (B2B SaaS, e-commerce, mobile gaming)
- Debug a file that isn't behaving as expected — the common pitfalls sections cover the most frequent mistakes

**Where to go next:**
- Want step-by-step guidance for adding a new entity or feature? → [Guides](../guides/README.md)
- Want to understand how these file types interact as a system? → [Concepts](../concepts/README.md)
