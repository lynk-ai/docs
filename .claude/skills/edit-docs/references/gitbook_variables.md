# GitBook Variables & Expressions

GitBook supports dynamic variables that render values inline using JavaScript expression syntax.

---

## Variable Storage

**Space-level** — defined in `/.gitbook/vars.yaml`, available across all pages:

```yaml
# .gitbook/vars.yaml
latest_version: v3.0.4
company_name: Acme Corp
support_email: help@example.com
```

**Page-level** — defined in the page's frontmatter under `vars:`, available only on that page:

```markdown
---
vars:
  page_version: v2.1.0
  api_key: example_key
---
```

---

## Expression Syntax

Expressions use JavaScript syntax wrapped in `<code class="expression">` tags. They are evaluated when the page renders.

```markdown
<code class="expression">JavaScript expression here</code>
```

**Examples:**

```markdown
<!-- Space-level variable -->
<code class="expression">space.vars.latest_version</code>

<!-- Page-level variable -->
<code class="expression">page.vars.page_version</code>

<!-- String concatenation -->
<code class="expression">"Download version " + space.vars.latest_version</code>

<!-- Conditional -->
<code class="expression">space.vars.latest_version === "v3.0.4" ? "Latest" : "Outdated"</code>

<!-- Simple math -->
<code class="expression">1 + 1</code>
```

---

## Variable Scope

| Variable type | Define in | Access with |
|---|---|---|
| Used across multiple pages | `/.gitbook/vars.yaml` | `space.vars.variableName` |
| Specific to one page | Frontmatter `vars:` | `page.vars.variableName` |

---

## Notes

- Expressions support any valid JavaScript — they're evaluated at render time
- The GitBook UI provides a visual variable editor, but variables are fully editable in files
- Space variables edited locally in `vars.yaml` sync to GitBook on commit
