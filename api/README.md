# API Reference

**Interfaces for querying and managing your Lynk semantic layer.**

This section documents the programmatic interfaces exposed by Lynk — how to write queries against your semantic layer, and how to call Lynk's HTTP endpoints to validate semantics, manage schemas, and inspect the data catalog.

---

## What's in this section

| Page | What it covers |
|---|---|
| [Lynk SQL](lynk-sql.md) | The SQL dialect the agent uses internally and you use when writing evaluation test cases — bare entity references, `METRIC()`, joins (default, `USING`, `ON`), CTEs, supported statements |
| [REST API](rest-api.md) | HTTP endpoints for validating the semantic layer, managing schemas, and inspecting the data catalog (sources and columns) |

---

**Where to go next:**
- Need to understand how entities and metrics are defined? → [Concepts](../concepts/README.md)
- Writing evaluation test cases that use Lynk SQL? → [Evaluations YAML](../file-types/evaluations-yaml.md)
