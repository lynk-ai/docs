# Concepts

**Deep-dive reference for how specific systems behave.**

This section explains the cross-cutting concepts that affect multiple parts of the semantic layer. These pages are not tied to a single file type — they cover how domains, entities, context, and the agent work as a system.

Read these when you already understand the basics and want to understand *why* something works the way it does, or when you need to troubleshoot unexpected behavior.

---

## What's in this section

| Page | What it covers |
|---|---|
| [Domains](domains.md) | How domains scope context to specific audiences — inheritance, overrides, `domain: "*"` vs named domains, conflict handling |
| [Entities](entities.md) | Entity anatomy — key_source, keys, the four feature types, entity metrics, feature chaining, how context compounds |
| [Context](context.md) | The semantic graph — how YAML (data model) and Markdown (context) work together, the five context file types, scoping, compounding |
| [Agent](agent.md) | How the agent works — the 6-step question-to-answer lifecycle, dynamic context loading, text-to-sql, debugging wrong answers |
| [Evaluations](evaluations.md) | How evaluations work — test case structure, running evaluations in the UI, the branch-to-main workflow |
| [Lynk SQL API](lynk-sql-api.md) | Lynk SQL syntax — `entity()`, `metric()`, joining entities with named join paths, supported statements |

---

## What you can do with this

After reading this section, you will understand:
- Why `domain: "*"` and `domain: "default"` behave differently — and when to use each
- How metric features, entity metrics, and relationships connect into feature chaining
- How context compounding works — which files load when, and in what order
- What the agent does step-by-step when it receives a question
- How to write Lynk SQL for evaluation test cases

**Where to go next:**
- Need exact field-by-field documentation for a specific file? → [File-Types Reference](../file-types/README.md)
- Want to see a complete working example? → [Project Walkthrough](../project/index.md)
