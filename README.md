# Lynk — Documentation

This documentation covers the Lynk framework: how to model your data and teach an AI agent everything it needs to know about your company — so it gives accurate, trusted results.

---

## How to Use These Docs

The docs are organized into five sections. Depending on what you need, start in a different place:

| If you want to... | Go to |
|---|---|
| Set up Lynk for the first time | [Getting Started](overview/getting-started.md) |
| Understand the big picture first | [Overview](#overview) |
| Build a semantic layer from scratch | [Project Walkthrough](#project-walkthrough) |
| Understand how a specific system behaves | [Concepts](#concepts) |
| Look up a specific file type | [File-Types Reference](#file-types-reference) |
| Add a feature or entity to an existing project | [Guides](#guides) |

---

## Overview

**Path:** `overview/`

Start here if you're new. These four files introduce the core concepts and structure without getting into implementation details.

| File | What it covers |
|---|---|
| `overview/getting-started.md` | How to set up Lynk — connect your Git repo, connect your warehouse via the UI, what gets created |
| `overview/overview.md` | The two file types (YAML + Markdown), supported warehouses and dbt compatibility, context scoping, what goes where, and the end-to-end flow |
| `overview/main-concepts.md` | Vocabulary: Domain, Entity, Source, Feature, Metric, Relationship, Agent and Tasks |
| `overview/file-types.md` | Quick-reference table of every file type — location, who reads it, and purpose |
| `overview/project-structure.md` | Canonical folder layout, naming conventions (double underscore delimiter), and feature resolution rules for custom domains |

---

## Project Walkthrough

**Path:** `project/`

A top-down narrative guide for building a complete semantic layer from scratch. Follows the recommended build order: business context first, entities last.

| File | Step |
|---|---|
| `project/index.md` | Why top-down is better; overview of the 5-step process; time estimates |
| `project/01-business-context.md` | Write domain knowledge and glossary before touching any entity |
| `project/02-domains.md` | Define audiences (domains) and when to create custom ones |
| `project/03-domain-context.md` | Create domain-wide task instructions and agent behavior files |
| `project/04-entities.md` | Model entities — dimensions first, then facts, then relationships, then feature chaining |
| `project/05-examples.md` | Add evaluation test cases to validate accuracy before going to production |

Read these files in order if you're building something new.

---

## Concepts

**Path:** `concepts/`

Deep-dive reference pages for how specific systems behave across the platform. These are not tied to a single file type — they explain cross-cutting behavior that affects multiple parts of the semantic layer.

| File | What it covers |
|---|---|
| `concepts/domains.md` | Domain inheritance model — how domains are activated, `domain: "*"` vs named vs multi-domain list, override rules, multi-file merging, and conflict handling |
| `concepts/entities.md` | Entities, features, and metrics — entity anatomy (key_source, keys, sources vs. entities), the four feature types, entity metrics, feature chaining, how context compounds on entities |
| `concepts/context.md` | The semantic graph — how YAML (data model) and Markdown (context) work together; the five context file types, scoping by domain and entity, context compounding at query time |
| `concepts/agent.md` | How the agent works — the 6-step question-to-answer lifecycle, dynamic context loading, text-to-sql tool, evaluations, transparency, debugging wrong answers |
| `concepts/evaluations.md` | How evaluations work — test case structure (English question + expected SQL), running evaluations in the UI, the branch-to-main workflow, building your evaluation suite over time |
| `concepts/lynk-sql-api.md` | Lynk SQL API reference — `entity()`, `metric()`, joining entities with named join paths, supported and unsupported statements |

---

## File-Types Reference

**Path:** `file-types/`

Deep-dive reference for every file type in the semantic layer. Use these when you need to know the exact structure, allowed fields, or behavior of a specific file type.

| File | Covers |
|---|---|
| `file-types/entity-yaml.md` | Entity YAML structure — features (field, first_last, formula, metric), entity metrics, related_sources, common pitfalls |
| `file-types/relationships-yaml.md` | `entities_relationships.yml` — relationship types, join definitions (sql / fields / lookup), enabling feature chaining |
| `file-types/knowledge-md.md` | Knowledge files — business definitions, data quality notes, context |
| `file-types/task-instructions-md.md` | Task instruction files — SQL patterns, join guidance, naming rules |
| `file-types/output-format-md.md` | Output format files — table structure, insights, tone, data notes |
| `file-types/clarification-policy-md.md` | Clarification policy files — when to ask, when to proceed, when to redirect |
| `file-types/glossary-md.md` | Glossary files — short term and abbreviation definitions. 1–2 sentences per entry |
| `file-types/evaluations-yaml.md` | `evaluations.yml` — test cases for regression testing before production pushes |

---

## Guides

**Path:** `guides/`

Task-focused how-to guides for the most common operations. Use these when you're extending an existing project.

| File | Task |
|---|---|
| `guides/adding-an-entity.md` | 6-step checklist for adding a new entity (YAML → relationships → knowledge → task instructions → evaluations → verify) |
| `guides/adding-a-feature.md` | Decision tree to pick the right feature type (field / first_last / formula / metric), then step-by-step instructions for each |

---

## Key Concepts at a Glance

**Feature types:**

| Type | When to use |
|---|---|
| `field` | Direct column from a source table |
| `first_last` | First or last value ordered by another field |
| `formula` | Derived from other features on the same entity |
| `metric` | Aggregated value pulled from a related entity (feature chaining) |

**Naming convention:** File names are up to you — scoping is controlled by frontmatter, not file names.

**Context compounding:** Context loads at multiple levels simultaneously. For a query about the `customer` entity in the `default` domain, domain-wide knowledge, entity knowledge, and domain-wide task instructions all load together.
