# AI Agents

{% hint style="info" %}
AI Agents - coming soon\
Planned to Q3 2025 - we will release a full suite of feature that enable agents work smoothly with Lynk.\
Navigate through this section to learn more on what's coming
{% endhint %}

Data teams can use pre-built AI agents or build custom agents on top of Lynk's MCP and RAG framework.

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

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption><p>High level architecture - enabling AI agents with context and tools</p></figcaption></figure>

## **Tools**

Lynk’s Model Context Protocol (MCP) provides a rich set of tools powered by both the Semantic Layer and Context (RAG) system. These tools enable AI agents to reason over data, generate queries, and explain results in a way that aligns with your business logic and tribal knowledge.

## **Context**

Lynk’s context system uses retrieval-augmented generation (RAG) to inject domain-specific knowledge into agent reasoning. This makes the system more accurate, explainable, and aligned with how your team actually works.

## **The role of the Semantic Layer**

The Semantic Layer plays a central and critical role in enabling Agents with the right tools and context. LLMs, and Agents, are non deterministic by nature. They need a translation layer that translate natural language business terms to structured, governed and trusted SQL queries, and this is exactly the role of the Semantic Layer.



