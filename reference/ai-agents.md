# AI Agents

Data teams can use pre-built AI agents or build custom agents on top of Lynk's MCP and RAG framework. Lynk provides a comprehensive Context system for teaching agents about your business, making them more accurate and aligned with how your team actually works.

## Use cases

There are many possible use cases for AI agents - and how they can help data teams and data consumers succeed with data.

Below you can find some examples:

* Self-service analytics ("Ask me anything")
* Explain queries
* Build data (entities, features and measures)
* Perform root-cause analysis
* Perform predictions and apply advanced ML practices
* Detect and fix data quality issues
* Build data visualizations
* Manage data pipeline materialization logic
* Detect and alarm on accounts at risk for churning
* Fraud detection

and more.&#x20;

## High level architecture

AI agents need access to effective tools and the right context;

<figure><img src="../.gitbook/assets/image (1) (1) (1).png" alt=""><figcaption><p>High level architecture - enabling AI agents with context and tools</p></figcaption></figure>

## **Tools**

Lynk’s Model Context Protocol (MCP) provides a rich set of tools powered by both the Semantic Layer and Context (RAG) system. These tools enable AI agents to reason over data, generate queries, and explain results in a way that aligns with your business logic and tribal knowledge.

## **Context**

Lynk's Context system uses retrieval-augmented generation (RAG) to inject domain-specific knowledge into agent reasoning. This makes the system more accurate, explainable, and aligned with how your team actually works.

Context allows you to teach Lynk about your business through four types of context nodes:

- **Knowledge** - Define what things mean in your organization (business rules, definitions, domain-specific context)
- **Task Instructions** - Guide how tasks execute (SQL standards, query patterns, execution rules)
- **Glossary** - Provide quick term definitions (acronyms, jargon, business vocabulary)
- **Agent Behavior** - Control communication style (tone, formatting, interaction patterns)

Each context type can be scoped to specific domains (Marketing, Finance, Sales, etc.), entities, or tasks, allowing different teams to have different definitions and preferences while working from the same data model.

{% hint style="success" %}
**Learn More**

See the [Context Guide](ai-agents/context-guide.md) for a comprehensive walkthrough of the Context system, including detailed examples and best practices.
{% endhint %}

## **The role of the Semantic Layer**

The Semantic Layer plays a central and critical role in enabling Agents with the right tools and context. LLMs, and Agents, are non deterministic by nature. They need a translation layer that translate natural language business terms to structured, governed and trusted SQL queries, and this is exactly the role of the Semantic Layer.



