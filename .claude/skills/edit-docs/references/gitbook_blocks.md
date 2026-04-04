# GitBook Custom Blocks

GitBook extends standard Markdown with custom block syntax using `{% %}` tags and special HTML. Standard Markdown works inside all custom blocks.

---

## Quick Reference

| Need | Use |
|---|---|
| Sequential, ordered instructions | `{% stepper %}` |
| Alternative options (languages, platforms) | `{% tabs %}` |
| Important warnings or tips | `{% hint %}` |
| Optional or collapsible detail | `<details>` |
| Side-by-side comparisons | `{% columns %}` |
| Changelog / release notes | `{% updates %}` |
| Visual navigation cards | `<table data-view="cards">` |
| Downloadable files | `{% file %}` |
| Call-to-action links | `<a class="button">` |
| Embedded external content (video, demo) | `{% embed %}` |
| Reusable content across pages | `{% include %}` |
| Code block with a filename title | `{% code title="..." %}` |

---

## Hints

Colored callout blocks. Styles: `info`, `warning`, `danger`, `success`.

```markdown
{% hint style="info" %}
This is an informational hint.
{% endhint %}

{% hint style="warning" %}
Be careful when running this in production.
{% endhint %}

{% hint style="danger" %}
This action cannot be undone.
{% endhint %}

{% hint style="success" %}
Configuration saved successfully.
{% endhint %}
```

---

## Tabs

Present alternative content (different languages, platforms, or options).

````markdown
{% tabs %}
{% tab title="JavaScript" %}
```javascript
const greeting = 'Hello World';
```
{% endtab %}

{% tab title="Python" %}
```python
greeting = "Hello World"
```
{% endtab %}
{% endtabs %}
````

---

## Stepper

Sequential multi-step processes where order matters.

```markdown
{% stepper %}
{% step %}
## First step

Complete the initial setup.
{% endstep %}

{% step %}
## Second step

Configure your environment.
{% endstep %}
{% endstepper %}
```

---

## Expandable (details)

Collapsible content for optional detail that would clutter the page.

````markdown
<details>
<summary>Advanced Configuration Options</summary>

Content here is hidden by default.

```yaml
advanced:
  option1: value1
```
</details>
````

---

## Columns

Side-by-side content. Maximum 2 columns.

```markdown
{% columns %}
{% column %}
### Before

Old implementation.
{% endcolumn %}

{% column %}
### After

New optimized approach.
{% endcolumn %}
{% endcolumns %}
```

---

## Updates

Changelog entries or release notes in reverse chronological order.

```markdown
{% updates format="full" %}
{% update date="2024-01-15" %}
# Version 2.0 Released

Added dark mode and improved search.
{% endupdate %}

{% update date="2024-01-01" %}
# Bug Fixes

Fixed several community-reported issues.
{% endupdate %}
{% endupdates %}
```

---

## Cards

Visual clickable navigation tiles.

```markdown
<table data-view="cards">
    <thead>
        <tr>
            <th>Title</th>
            <th data-card-target data-type="content-ref">Target</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Getting Started</td>
            <td><a href="getting-started/quickstart.md">Quick Start</a></td>
        </tr>
        <tr>
            <td>API Reference</td>
            <td><a href="api-reference/overview.md">API Docs</a></td>
        </tr>
    </tbody>
</table>
```

---

## Embeds

Inline external content (videos, interactive demos, social media).

```markdown
{% embed url="https://www.youtube.com/watch?v=dQw4w9WgXcQ" %}

{% embed url="https://codepen.io/username/pen/example" %}
```

---

## Files

Downloadable file with caption.

```markdown
{% file src="https://example.com/document.pdf" %}
Complete documentation in PDF format.
{% endfile %}
```

---

## Buttons

Call-to-action links. Styles: `primary`, `secondary`.

```markdown
<a href="https://example.com/download" class="button primary">Download Now</a>

<a href="https://docs.example.com" class="button secondary">View Documentation</a>
```

With icon (Font Awesome name, no `fa-` prefix):

```markdown
<a href="https://github.com/user/repo" class="button primary" data-icon="github">View on GitHub</a>
```

---

## Code Blocks with Title

```markdown
{% code title="index.js" %}
```javascript
const foo = 'bar';
```
{% endcode %}
```

---

## Reusable Content

Sync content blocks across multiple pages. Blocks are created through the GitBook UI and assigned unique IDs.

```markdown
{% include "/reusable-content/rc12345" %}
```

---

## OpenAPI

OpenAPI specs cannot be embedded directly in Markdown — they must be uploaded via the GitBook API, CLI, or UI first. Once uploaded, reference them as:

```markdown
{% openapi src="https://api.example.com/openapi.json" path="/users" method="get" %}
[https://api.example.com/openapi.json](https://api.example.com/openapi.json)
{% endopenapi %}
```

---

## Common Pitfalls

- Always close blocks properly (`{% endtab %}`, `{% endhint %}`, `{% endstepper %}`, etc.)
- Match opening and closing tags exactly
- Standard Markdown (bullets, bold, code blocks) works inside all custom blocks
- Test custom blocks in GitBook after editing locally — some render only on the platform
