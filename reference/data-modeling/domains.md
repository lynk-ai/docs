# Domains

{% hint style="info" %}
**Note:** This page describes business domains in Lynk's data modeling system. For AI agent context configuration, see the [Context Guide](../ai-agents/context-guide.md).
{% endhint %}

Domains are business units like marketing, sales, product, customer success, etc.

Domains allow creating business definitions specific to each business unit. For example, the definition of "active user" can differ between the product team and the marketing team - domains make it possible to have different feature definitions for different business units.

## Types of domains

There are two types of domains:

* `default` domain
* custom domain

### `default` (the default domain)

`default` is the domain that Lynk comes with out of the box.\
If no other domain is defined, all semantic definitions will be applied and consumed from the `default` domain.

### Custom domain

Creating a custom domain is done via Lynk Studio. In order to add and manage domains navigate to settings > account > domains.

{% hint style="info" %}
Only **admins** can create and manage domains.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption><p>Example for "marketing" as a custom domain</p></figcaption></figure>

***

## Using domains

#### Entities

Entities are created on the `default` domain and available across all domains.

#### Features

Features are domain specific;

* Unless explicitly created on a custom domain, features will be created on the `default` domain.
* Features on the `default` domain are shared across all domains, unless there is a feature with the same name on a custom domain.

The below table shows what would be the result when consuming a feature that was defined on different domains:

| Defined on              | Consumed from | Result                    |
| ----------------------- | ------------- | ------------------------- |
| default only            | default       | `default` definition      |
| default only            | custom        | `default` definition      |
| custom only             | default       | feature not found (error) |
| custom only             | custom        | custom definition         |
| both default and custom | default       | `default` definition      |
| both default and custom | custom        | custom definition         |

***

## Domains in project structure

Looking at the project folders, once created a new domain via the Studio, a new folder will appear with the new domain name, next to the `default` folder. New features that will be added to this domain will be added to the relevant entity under that folder.&#x20;
