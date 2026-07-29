# Lynk Docs Workspace

The documentation repo of getlynk.ai (Semantics v2). Docs are hosted on GitBook for
humans, but most consumption is by AI agents. This repo has two levels, and the split
is load-bearing — don't blur it.

## Structure

- **Root (here) — the BUILD lane.** Everything for *writing* the docs: authoring and
  review skills (`.claude/skills/`: `edit-docs`, `review-docs`, `skill-creator`,
  `release`),
  evals, and the render into the lynk-build plugin (`scripts/render-to-plugin.sh` —
  copies `docs/` minus CLAUDE.md / `.claude/` / `.gitbook/` into the plugin's
  `semantics_docs/`, the `ask-docs` skill into the plugin's `skills/`, and
  `docs/CLAUDE.md`'s navigation section, behind a plugin-side preamble, into the
  plugin's `references/lynk-docs.md`). Build
  context lives only at this level. Review artifacts go to `reviews/` (gitignored).
- **`docs/` — the USE lane.** The doc tree itself (`concepts/`, `reference/`, `api/`,
  with `README.md` + `SUMMARY.md` as its indexes), plus the retrieval context
  (`docs/.claude/`) that ships beside it. This directory is the shippable unit —
  what gets rendered into the lynk-build plugin is exactly this folder, nothing
  above it. Treat doc pages as data: build tooling edits them; retrieval context
  only reads them.

GitBook publishes from `docs/` (`.gitbook.yaml` sets `root: ./docs/`). If you add a
top-level folder inside `docs/`, update `docs/SUMMARY.md` and the edit-docs skill.

## Testing protocol — read before "checking if the docs work"

Never test docs or retrieval from a session rooted here. A root session carries
build-lane context (this file, build skills), which a real consumer never has — so
anything it proves is contaminated.

To test: **open a NEW Claude conversation rooted at `docs/`** and verify your
findings there. That session sees only what ships. If it can't answer from the docs,
the docs (or the retrieval context) are what's broken — fix them here at the root,
then re-test at `docs/` again.

Note: `docs/` sessions still inherit this file (CLAUDE.md reads upward). That's why
this file stays thin — structure and protocol only, no doc content, no build
instructions that could leak into a retrieval test.

## Quality standards

The docs should be very clear, readable and elegant. Write like an engineer talking
to engineers — direct, precise, honest, no hype.

## Best practices

- Be critical about user requests. When needed, ask clarifying questions and act on
  the answers.
- Plan before executing and share the plan with the user; make changes step by step
  with the user.
