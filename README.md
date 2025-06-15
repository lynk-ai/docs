---
cover: .gitbook/assets/selected (1).png
coverY: 0
layout:
  cover:
    visible: true
    size: full
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Introduction

Lynk is the Semantic Layer for AI and business users. It empowers companies to build AI-driven applications by creating a centralized, governed, and accessible source of truth for all their data.

## AI is changing the rules

### Enterprise Data Access Prediction (2025-2030)

In the coming years, we anticipate a dramatic shift in how enterprise data is accessed.\
AI will become the primary consumer of enterprise data, with an estimated 90% of queries originating from AI agents.

<figure><img src=".gitbook/assets/image (3).png" alt=""><figcaption><p>Projected shift from traditional human/BI tool access to AI-driven data access</p></figcaption></figure>

### Garbage in garbage out

While AI is poised to revolutionize how we access, build and get value from data, most enterprise data environments are not yet ready. They’re often messy - plagued by duplicated logic, unclear definitions, and outdated, manual processes.&#x20;

For AI to reliably consume and act on data, we must address these foundational issues and fundamentally rethink how data is built, managed, governed and accessed.

## Core concepts

Lynk was designed with AI as both a primary data consumer and contributor, and with business teams in mind. Data teams use it to manage the semantics and make them accessible to AI as the main direct consumer of data.

It makes defining and consuming semantic and business concepts more accessible to both AI and non-technical users, while enforcing strong data modeling and governance practices to maintain a reliable and structured source of truth.

Lynk empowers AI and every member of the data supply chain with the freedom, flexibility, and control to explore and produce data, while keeping data organized, governed, and easily accessible from a central semantic layer.

**The product's core concepts are:**

### **AI first**

The entity-centric data modeling framework resembles a knowledge graph - an ideal structure for AI interaction. With Lynk, you can build a complete RAG (Retrieval-Augmented Generation) system combining semantic definitions, vectorized documents, and more - exposed through the MCP (Model Context Protocol) to AI agents. These agents power self-service analytics, data quality assurance, and beyond.

Visit [AI enablement](reference/ai-agents.md) for in-depth information about this.

### **Rethinking Data Modeling**&#x20;

At its core, Lynk has a structured and opinionated data modeling framework with governance built in.\
Data is modeled as **entities** and **features** - a structure that is both intuitive for business users and optimized for AI applications.

Some of the data modeling framework core concepts are:

* Each level of granularity represented only once as entity (including different time aggregation levels)
* Time aggregations (e.g., daily, monthly, rolling 90 days) are not pre-materialized or hardcoded. Instead, they are dynamically generated at query time, enabling flexible and efficient analysis without bloating the model.
* Fields, measures, joins, and relationships are defined once and reused across the model. This promotes consistency, reduces duplication, and ensures governed, reliable outputs.
* Feature definitions, functions, and transformations are built using templated patterns - making the model easy to extend, replicate, and audit.
* Unlike traditional semantic layers, Lynk supports feature chaining: the ability to build features on top of features, supporting complex multi-step transformations and aggregations.\
  This is critical for enabling AI agents to not only answer questions, but also derive and define new features, metrics and trends - as well as performing real root cause analysis.

By following these principles, Lynk provides governance and simplicity in one unified model - a clear, consistent, and scalable approach to data modeling that’s accessible to both technical and non-technical users.

Visit [data modeling](reference/data-modeling/) for in-depth information about this.

### **Accessibility**

Beyond its native AI accessibility, Lynk is built for both business users and data teams.\
All semantic definitions - such as Entities and Features _-_ are accessible and editable through Lynk Studio, a user-friendly data catalog and business glossary. It enables anyone to explore, create, and govern data with simplicity and control.

### **Governance**

Entities, Features and usage patterns are all constantly governed.\
To make sure our source of truth is trusted and avoid duplicated logic and wasted resources.

Visit [governance](reference/governance.md) for in-depth information about this.

### **Version control**

Everything built on Lynk translates to code and is version controlled, even if built via the Studio. \
Apply coding best practices, CI/CD and tests to semantic definitions - while letting business users and analysts move fast.

Visit [Git integration](reference/integrations/git.md) for in-depth information about this.

### **Efficiency**

Efficiency is critical for query performance and reducing cost.\
Semantic definitions are translated to efficient SQL code. Lynk also governs usage patterns to suggest improvements and applies advanced cache and pre-aggregation mechanism (coming soon)
