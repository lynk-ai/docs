# Getting Started

Lynk connects to your Git repository and your data warehouse. Everything the agent knows lives in your repo — you own it entirely.

---

## What You Need Before Starting

- A Git repository (GitHub, GitLab, Bitbucket, or any hosted Git service)
- Read-only credentials for the database schemas you want to connect — Snowflake or BigQuery

That's it. No local installation required.

---

## Setup

**1. Sign in to Lynk**

Go to [app.getlynk.ai](https://app.getlynk.ai) and create your account.

**2. Run the onboarding flow**

First-time setup is at [app.getlynk.ai/onboarding](https://app.getlynk.ai/onboarding). It walks through connecting your Git repository and your data warehouse in one flow.

**Connecting your Git repository:** Provide your repository URL and grant Lynk access. Lynk will create a `.lynk/` folder at the root of your repo. This is where your entire semantic layer lives — entity definitions, context files, relationships, evaluations.

You can edit files in the Lynk UI or directly in your editor (VS Code, Cursor, or any IDE). Both write to the same repository.

**Connecting your data warehouse:** Provide read-only credentials to the database schemas you want Lynk to query. Lynk never writes to your warehouse.

Supported warehouses: **Snowflake**, **BigQuery**. Customers also run Lynk against Presto, Athena, Spark, and Hive.

Once connected, your warehouse tables are available as sources for entity definitions.

---

## What Happens Next

After setup, your repo has a `.lynk/default/` folder. This is your main domain — where all entity definitions live.

The agent can answer questions immediately, but accuracy depends on context. The more you teach it — entity definitions, business rules, glossary terms, SQL patterns — the better it performs.

Build your semantic layer using the project walkthrough. The walkthrough covers two entities for a fictional company and takes 50–60 minutes. Your actual project will take longer depending on the number of entities and the complexity of your data model. Most teams reach their first trusted production answers within 1–2 days.

---

## Next Steps

| If you want to... | Go to |
|---|---|
| Build a semantic layer from scratch | [Project Walkthrough](../project/index.md) |
| Understand the core vocabulary | [Main Concepts](./main-concepts.md) |
| See every file type at a glance | [File Types](./file-types.md) |
| Add an entity to an existing project | [Adding an Entity](../guides/adding-an-entity.md) |
