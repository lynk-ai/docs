#!/usr/bin/env bash
# Render the shippable unit (docs/) into the lynk-build plugin.
#
# Three targets, same source, one render — so none can drift from the others:
#   docs/ minus the three non-content items (CLAUDE.md, .claude/, .gitbook/)
#     -> <plugin>/semantics_docs/
#   docs/.claude/skills/ask-docs/ (the retrieval skill, maintained and eval'd
#     here beside the docs it navigates; a nested .claude/ wouldn't be
#     discovered inside a plugin, so it renders into the plugin's own skills/)
#     -> <plugin>/skills/ask-docs/
#   docs/CLAUDE.md's "How to navigate the docs" section (the navigation
#     contract), behind a plugin-side preamble that sets the docs root and
#     the ask-docs pointer — environment framing the shared source can't carry
#     -> <plugin>/references/lynk-docs.md
#
# The transform is deliberately dumb: copy, and delete anything in the target
# that no longer exists in the source. Which docs a plugin release carries is
# pinned by the plugin version — the render adds no provenance of its own.
#
# Usage: scripts/render-to-plugin.sh [path-to-plugin-dir]
#   default target: ../plugin (the shipped plugin dir in this repo)
#
# After rendering: review the diff in the plugin repo, bump the plugin version
# in .claude-plugin/plugin.json, and commit there.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_ROOT/docs"
PLUGIN_DIR="${1:-$REPO_ROOT/../plugin}"
TARGET="$PLUGIN_DIR/semantics_docs"

[ -f "$SRC/SUMMARY.md" ] || { echo "error: $SRC has no SUMMARY.md — not a docs root" >&2; exit 1; }
[ -d "$PLUGIN_DIR" ]     || { echo "error: plugin dir not found: $PLUGIN_DIR" >&2; exit 1; }

# The router in concepts/README.md is generated from page frontmatter — refresh
# it so the rendered bundle can't ship a stale index.
python3 "$REPO_ROOT/scripts/generate_router.py"

# Gate the render on the static docs lint (template, links, orphans, budgets).
# Skip only with RENDER_SKIP_LINT=1 — a shipped dead link is the expensive kind.
if [ "${RENDER_SKIP_LINT:-0}" != "1" ] && [ -d "$REPO_ROOT/evals/ask-docs" ]; then
  (cd "$REPO_ROOT/evals/ask-docs" && uv run pytest -m "not evaluation" -q) \
    || { echo "error: docs lint failed — fix or rerun with RENDER_SKIP_LINT=1" >&2; exit 1; }
fi

rsync -a --delete \
  --exclude 'CLAUDE.md' \
  --exclude '.claude/' \
  --exclude '.gitbook/' \
  "$SRC/" "$TARGET/"

SKILL_SRC="$SRC/.claude/skills/ask-docs"
SKILL_TARGET="$PLUGIN_DIR/skills/ask-docs"
[ -d "$SKILL_SRC" ] || { echo "error: ask-docs skill not found at $SKILL_SRC" >&2; exit 1; }
rsync -a --delete "$SKILL_SRC/" "$SKILL_TARGET/"

REF_TARGET="$PLUGIN_DIR/references/lynk-docs.md"
NAV="$(awk '/^## How to navigate the docs$/{f=1; print; next} f && /^## /{exit} f' "$SRC/CLAUDE.md")"
[ -n "$NAV" ] || { echo "error: no '## How to navigate the docs' section in $SRC/CLAUDE.md" >&2; exit 1; }
{
  cat <<'PREAMBLE'
# Lynk docs — navigation guide

How skills walk the Lynk docs. The docs **ship with the plugin**: they live at `${CLAUDE_PLUGIN_ROOT}/semantics_docs/`, read them with the Read tool — all paths below are relative to that root. The docs are data: never edit them from here. For *answering the user's* Lynk questions, use the `ask-docs` skill — it packages this navigation into a full answer procedure; this page is for skills reading the docs mid-task (planning, placing content, verifying).

PREAMBLE
  printf '%s\n' "$NAV"
} > "$REF_TARGET"

echo "rendered $SRC -> $TARGET"
echo "rendered $SKILL_SRC -> $SKILL_TARGET"
echo "rendered $SRC/CLAUDE.md (navigation section) -> $REF_TARGET"
echo "next: review the diff in the plugin repo, bump the version in"
echo "      $PLUGIN_DIR/.claude-plugin/plugin.json, and commit."
