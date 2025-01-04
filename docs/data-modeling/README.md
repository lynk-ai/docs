---
description: lynk Data modeling framework
---

# Data modeling

This page summarizes the core concepts of Lynk data modeling framework.

## A central source of truth

The main concept of Lynk is to create a central source of truth for each of the entities in the business, in a trusted and accessible way. In other words, from a business perspective, for each business entity it should be clear what we know of it, how was it defined, and where we can find it. We call these pieces of information on an entity level "features".

## [Entities](entities/)

Entities are real-world concepts like customers, orders, payments etc.  These are first-class citizens in Lynk, meaning everything we build and consume is around entities.

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

## [Data assets](data-assets.md)

Data assets are tables and views from the underlying data source (a data warehouse). Data assets can be related to entities and they are being used mostly for creating entity features.

## Contexts

## Time aggregation

Efficiency and performance\





consume
