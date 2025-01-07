# Data modeling

Data modeling is core for succeeding with data, specially in the era of AI. This page summarizes the core concepts of Lynk data modeling framework.

## Entity Centric Data Modeling

Lynk has a built-in data modeling framework, which is based on the **Entity-Centric-Data-Modeling** (ECM) architecture, derived from the **Domain Driven Design** (DDD) architecture.&#x20;

While the Star-Schema approach is to **normalize** data with FACT and DIM tables, the Entity-Centric-Data-Modeling approach is to **denormalize** data around business entities. This approach is more suitable for creating a central source of truth and specially for making it easy and accessible for business teams and AI.

{% hint style="info" %}
Entity-Centric-Data-Modeling can be built on top of a Star Schema architecture, creating a denormalized table per entity (with all the entity features) on top of the Dim and Fact tables.
{% endhint %}

### The ECM architecture advantages

The Entity-Centric-Data-Modeling architecture advantages include:

* Making data accessible to business users
* Better for creating a central source of truth
* Connecting data silos
* Easier to Keep the data model clean (following the DRY pattern)
* Better for AI enablement

{% hint style="info" %}
On top of the data modeling layer, lynk applies the [governance](../governance.md) layer to make sure our data model is consistent, clean and efficient.
{% endhint %}

## [Entities](entities/)

Entities are real-world concepts like customers, orders, payments etc.  These are first-class citizens in Lynk, meaning everything we build and consume is around entities. Each business entity is attached with everything we to know about it. We call these pieces of information on an entity level "features".

## [Features](features/)

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

## [Chaining features](chaining-features.md)

Features are reusable. This means it is possible to create robust data pipelines within Lynk - by chaining features across entities.

{% hint style="info" %}
Common challenges in data modeling are questions like "how should I model this?" and "was this done before, somewhere else?"

Lynk takes care of such challenges by providing a structured way to model data (defining features on entities via YAML files), governing it with the [Governance](../governance.md) layer and making it all easily accessible via the Studio interface.
{% endhint %}

## [Data assets](data-assets/)

Data assets are tables and views from the underlying data source (a data warehouse). Data assets are being used for creating features.

For example, if we have a data asset that holds all the payment attempts done by customer, we can define features like first / last payment, aggregating payments to a customer level etc..

## [Context](context.md)

Contexts allow us to create business definitions specific to a business context like marketing / sales / product etc. For example, the definition of "active user" can differ between the product team and the marketing team. Contexts make it possible to have more than one definition of "active\_user" - one for marketing team and one for sales team.&#x20;

## [Time aggregation](../consume-and-apis/time-aggregation.md)

Time aggregations include many options to aggregate features in different time frames like calendric aggregations (day, week, month, year etc) or rolling window aggregations (last 7 days etc).&#x20;

Lynk applies these aggregate definitions on the consumption level, to keep the feature definition level with pure business logic, and enable flexibility when consuming entities and features.
