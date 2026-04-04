# GitBook Structure & Navigation

How GitBook organizes files, configures spaces, and manages navigation.

---

## File Structure

```
/
  .gitbook/
    assets/              # GitBook-managed images and files
    includes/            # Reusable content blocks
    vars.yaml            # Space-level variables
  .gitbook.yaml          # Configuration
  README.md              # Homepage
  SUMMARY.md             # Table of contents
  getting-started/
    installation.md
    quickstart.md
  api-reference/
    authentication.md
    endpoints.md
```

---

## .gitbook.yaml

Configures your GitBook space. Place at the root of your documentation directory.

```yaml
root: ./

structure:
  readme: ./README.md
  summary: ./SUMMARY.md

redirects:
  old-page: new-page.md
  help: support.md
```

**Options:**
- `root` — root directory for documentation (default: `./`)
- `structure.readme` — path to homepage (default: `./README.md`)
- `structure.summary` — path to table of contents (default: `./SUMMARY.md`)
- `redirects` — key-value pairs mapping old URLs to new page paths

**Monorepo support:** place a `.gitbook.yaml` in each subdirectory and set "Project directory" in Git Sync config accordingly.

**Important:** paths in `.gitbook.yaml` are relative to `root`. Redirects are space-specific. Manage `README.md` only through your repository when using Git Sync.

---

## The .gitbook Directory

Created by GitBook when using Git Sync.

```
.gitbook/
  assets/      # Images and files uploaded via GitBook UI
  includes/    # Reusable content blocks (one .md file each)
  vars.yaml    # Space-level variables
```

- Images are referenced as `![alt](../.gitbook/assets/image-name.svg)`
- Reusable blocks are referenced as `{% include "/reusable-content/rc12345" %}`
- The `includes/` folder may appear in the sidebar TOC — hide manually if needed
- In monorepos, `.gitbook/` is created at the root of each synced space

---

## SUMMARY.md

Defines the table of contents and sidebar navigation.

```markdown
# Summary

## Use headings to create page groups

* [First page](page1/README.md)
    * [Child page](page1/page1-1.md)
* [Second page](page2/README.md)

## Another group

* [Another page](another-page.md)
```

**Rules:**
- `#` for the main title
- `##` headings create page groups (section headers in the sidebar)
- `*` lists define pages; indent with spaces (not tabs) for nesting
- Each item is a markdown link: `[Link text](path/to/file.md)`
- Paths are relative to the `root` in `.gitbook.yaml`
- You cannot reference the same file twice
- Optional: a quoted title sets the sidebar label separately from the page title — `* [Page title](page.md "Sidebar label")`

SUMMARY.md is optional — if absent, GitBook infers structure from the directory layout.

---

## Working with Existing Content

1. **Read SUMMARY.md first** — shows all pages, hierarchy, and file paths
2. **If no SUMMARY.md** — browse the directory structure to understand organization
3. **Check .gitbook.yaml** — understand root path, custom README/SUMMARY locations, redirects
4. **Check .gitbook/assets/** — images and files referenced in docs
5. **Check .gitbook/vars.yaml** — space-level variables if any are defined

---

## Git Sync

- Changes in Git automatically update GitBook; changes in GitBook automatically commit to Git
- GitBook maintains SUMMARY.md based on UI edits
- Resolve merge conflicts in Git
- Make structural changes (navigation) via SUMMARY.md in Git
- Use branch-based workflows for significant updates
- Test changes in preview before merging to main
