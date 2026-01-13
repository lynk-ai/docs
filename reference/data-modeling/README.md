# Data modeling

At its core, Lynk has a structured and opinionated data modeling framework with **governance built in**.\
Data is modeled as **Entities** and **Features** - a structure that is both intuitive for business users and optimized for AI applications.

{% hint style="info" %}
While the Star-Schema approach is to **normalize** data with FACT and DIM tables, the Entity-Centric-Data-Modeling approach is to **denormalize** data around business entities.

Entity-Centric-Data-Modeling can be built on top of a Star Schema architecture, creating a denormalized table per entity (with all the entity features).

This approach is more suitable for creating a central source of truth and specially for making it easy and accessible for AI and business teams.
{% endhint %}

The framework is opinionated - meaning it applies rules and governance out of the box - and is "self aware" of what's being built and how.&#x20;

Read below to understand more how it works;

## Core concepts

* Each level of granularity represented only once as entity (including different time aggregation levels)
* Time aggregations (e.g., daily, monthly, rolling 90 days) are not pre-materialized or hardcoded. Instead, they are dynamically generated at query time, enabling flexible and efficient analysis without bloating the model.
* Entities, relationships, features, measures and fields are defined once and reused across the model. This promotes consistency, reduces duplication, and ensures governed, reliable outputs.
* Feature definitions, functions, and transformations are built using templated patterns - making the model easy to extend, replicate, and audit.
* Unlike traditional semantic layers, Lynk supports feature chaining: the ability to build features on top of features, supporting complex multi-step transformations and aggregations.\
  This is critical for enabling AI agents to not only answer questions, but also derive and define new features, metrics and trends - as well as performing real root cause analysis.

By following these principles, Lynk provides governance and simplicity in one unified model - a clear, consistent, and scalable approach to data modeling that’s accessible to both technical and non-technical users.

## Dive Deeper

Dive deeper into each of the framework's components below to learn more and see code examples&#x20;

### [Entities](entities.md)

Entities are real-world concepts like customers, orders, payments etc.  These are first-class citizens in Lynk, meaning everything we build and consume is around entities. Each business entity is attached with everything we to know about it. We call these pieces of information on an entity level "Features".

### [Features](features/)

Features are entity-level attributes, representing all the things we know of entities. \
In practice, features hold the business logic of what we know of our entity.&#x20;

Lynk supports 4 types of features:

#### [Field](features/field.md)

Field features are commonly used to enrich an entity with simple, non aggregate fields from related assets or entities.

#### [Metric](features/metric.md)

Metric features are commonly used to enrich an entity with aggregated fields from one-to-many related assets or entities.&#x20;

#### [First-Last](features/first-last.md)

First-Last features are commonly used to enrich an entity with fields of the first or last appearance of a one-to-many related assets or entities.

#### [Formula](features/formula.md)

Formula features are used when we need to create features on top of other features, commonly used to enrich an entity with calculations that require multiple aggregations or calculations to be done first.

{% hint style="info" %}
Lynk holds all the business logic but does not materialize entities and features on the underlying data warehouse. This enables flexibility for slice and dice capabilities and different time aggregations.&#x20;

For performance optimizations, we have plans on our roadmap to enable entities and features materialization with dbt. If that's something you would like to see coming soon, please [contact us](https://www.getlynk.ai/book-a-demo) and let us know.
{% endhint %}

### [Chaining features](features/chaining-features.md)

Features are reusable. This means it is possible to create robust data pipelines within Lynk - by chaining features across entities.

{% hint style="info" %}
Common challenges in data modeling are questions like "how should I model this?" and "was this done before, somewhere else?"

Lynk takes care of such challenges by providing a structured way to model data (defining features on entities via YAML files), governing it with the [Governance](../governance.md) layer and making it all easily accessible via the Studio interface.
{% endhint %}

### [Measures](measures.md)

Entities can be further aggregated ("how many active users bought at least once in the past 7 days?). To apply aggregation logic on entities, we define "Measures" on entities.&#x20;

### [Data assets](data-assets.md)

Data assets are tables and views from the underlying data source (a data warehouse). Data assets are being used for creating features.

For example, if we have a data asset that holds all the payment attempts done by customer, we can define features like first / last payment, aggregating payments to a customer level etc..

### [Domains](domains.md)

Domains allow us to create business definitions specific to a business unit like marketing / sales / product etc. For example, the definition of "active user" can differ between the product team and the marketing team. Domains make it possible to have more than one definition of "active\_user" - one for marketing team and one for sales team.&#x20;

### [Time aggregation](time-aggregation.md)

Time aggregations include many options to aggregate features in different time frames like calendric aggregations (day, week, month, year etc) or rolling window aggregations (last 7 days etc).&#x20;

Lynk applies these aggregate definitions on the consumption level, to keep the feature definition level with pure business logic, and enable flexibility when consuming entities and features.
