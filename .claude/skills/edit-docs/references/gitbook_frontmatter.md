# GitBook Page Frontmatter

YAML frontmatter configures page-level settings. Must appear at the very top of the file, before any content.

```markdown
---
description: Page description used for SEO and page previews
icon: book-open
hidden: true
vars:
  page_variable: value
if: visitor.claims.unsigned.isPremium
layout:
  width: default
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---
```

---

## Field Reference

**`description`** — Page description for SEO and previews. Supports multiline:
```yaml
description: >-
  This is a longer description
  that spans multiple lines
```

**`icon`** — Font Awesome icon name (e.g., `book-open`, `bolt`, `stars`, `brackets-curly`). No `fa-` prefix.

**`hidden: true`** — Hides the page from the published table of contents sidebar.

**`vars`** — Page-level variables accessible via expressions:
```yaml
vars:
  version: v1.2.3
  api_key: example_key
```

**`if`** — Adaptive content visibility condition. Controls page visibility based on visitor attributes:
```yaml
if: visitor.claims.unsigned.isPremium
```
Recommended to configure through the GitBook UI instead for team visibility.

**`layout`** — Controls page layout and visible elements:
- `width` — `default` or `wide` (wider content area; also widens tables and code blocks)
- `title.visible` — show/hide the page title
- `description.visible` — show/hide the page description
- `tableOfContents.visible` — show/hide the left sidebar
- `outline.visible` — show/hide the right sidebar headings
- `pagination.visible` — show/hide next/previous page links
- `metadata.visible` — show/hide page metadata section

---

## Example: Landing page with minimal chrome

```yaml
---
description: Get started with Lynk in minutes
icon: rocket
layout:
  width: wide
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: false
  outline:
    visible: false
  pagination:
    visible: false
---
```
