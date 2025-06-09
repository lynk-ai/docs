# Context

Contexts are business domains like marketing, sales, product, customer success etc.

Contexts allow creating business definitions specific to a business context like marketing / sales / product etc. For example, the definition of "active user" can differ between the product team and the marketing team - contexts make it possible to have different feature definitions for different contexts.

## Types of contexts

There are two types of contexts:

* `default` context
* custom context

### `default` (the default context)

`default` is the context that Lynk comes with out of the box.

### Custom context

Creating a custom context is done via settings > account > contexts on the Studio.\
Only **admins** can create and manage contexts.

<figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption><p>Example for "marketing" as a custom context</p></figcaption></figure>

***

## Using contexts

#### Entities

Entities are being created on the `default` context and available on all contexts.

#### Features

Features are context specific;

* Unless explicitly created on a custom context, features will be created on the `default` context.
* Features on the `default` context are shared across all contexts, unless there is a feature with the same name on a custom context.

The below table shows what would be the result when consuming a feature that was defined on different contexts:

| Defined on              | Consumed from | Result                    |
| ----------------------- | ------------- | ------------------------- |
| default only            | default       | `default` definition      |
| default only            | custom        | `default` definition      |
| custom only             | default       | feature not found (error) |
| custom only             | custom        | custom definition         |
| both default and custom | default       | `default` definition      |
| both default and custom | custom        | custom definition         |

***

## Contexts in project structure

Looking at the project folders, once created a new context via the Studio, a new folder will appear with the new context name, next to the `default` folder. New features that will be added to this context will be added to the relevant entity under that folder.&#x20;
