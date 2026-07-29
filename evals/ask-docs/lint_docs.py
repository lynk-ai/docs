"""Static docs lint — the zero-LLM lane of the docs' build system.

Enforces the structural contract declared in the edit-docs skill: template
sections per genre, no dead links, no orphans, token budgets, index/filesystem
sync, and router freshness. Runs free and deterministic:

    uv run pytest -m "not evaluation"     # this file only
    uv run pytest -m evaluation           # the live LLM evals

scripts/render-to-plugin.sh gates every render on this lane.
"""

import re
import subprocess
from pathlib import Path

import pytest

from harness.cases import DOCS_DIR

SCRIPTS = DOCS_DIR.parent / "scripts"

SPEC_SECTIONS = ["What it is", "Where it lives", "Format", "Examples", "Validation", "Related"]
GUIDE_SECTIONS = ["When you need this", "The principle", "Patterns", "Anti-patterns", "The bar", "Related"]

# Pages allowed to deviate from their genre's section list, with the reason.
TEMPLATE_EXEMPT = {
    "guides/complete-example.md",  # worked example: adapted structure by design
    "concepts/README.md",          # the generated router — different shape by design
    "reference/what-lynk-does-not-do.md",  # boundary index: list-of-links by design
}

# Hard budgets in characters (~4 chars/token). Guides are read whole and lazy —
# bloat there taxes exactly the questions that asked for depth.
CHAR_BUDGETS = {"concepts": 12_000, "reference": 12_000, "guides": 10_000, "api": 14_000}
CHAR_BUDGETS_EXEMPT = {"guides/complete-example.md": 18_000}


def content_pages() -> list[Path]:
    # Filter on the path relative to the docs root — the absolute path may
    # legitimately contain .claude/.gitbook components (e.g. a git worktree
    # under .claude/worktrees/) that must not exclude every page.
    return sorted(
        p for p in DOCS_DIR.rglob("*.md")
        if ".claude" not in p.relative_to(DOCS_DIR).parts
        and ".gitbook" not in p.relative_to(DOCS_DIR).parts
        and p.name != "CLAUDE.md"
    )


def rel(p: Path) -> str:
    return str(p.relative_to(DOCS_DIR))


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return re.sub(r"`[^`\n]*`", "", text)


def h2_sections(p: Path) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"^## (.+)$", strip_code(p.read_text()), re.MULTILINE)]


def summary_paths() -> list[str]:
    return re.findall(r"\* \[[^\]]*\]\(([^)]+)\)", (DOCS_DIR / "SUMMARY.md").read_text())


# --- template ---------------------------------------------------------------

def genre_pages(folder: str) -> list[Path]:
    return [p for p in content_pages()
            if rel(p).startswith(f"{folder}/") and rel(p) not in TEMPLATE_EXEMPT]


@pytest.mark.parametrize("page", genre_pages("concepts") + genre_pages("reference"), ids=rel)
def test_spec_page_template(page):
    got = h2_sections(page)
    assert got == SPEC_SECTIONS, f"{rel(page)}: sections {got} != {SPEC_SECTIONS}"


@pytest.mark.parametrize("page", genre_pages("guides"), ids=rel)
def test_guide_template(page):
    got = h2_sections(page)
    assert got == GUIDE_SECTIONS, f"{rel(page)}: sections {got} != {GUIDE_SECTIONS}"


def test_no_contents_sections():
    offenders = [rel(p) for p in content_pages() if "## Contents" in strip_code(p.read_text())]
    assert not offenders, f"'## Contents' is retired (dead tokens): {offenders}"


def test_frontmatter_description_present():
    missing = []
    for p in content_pages():
        if p.name == "SUMMARY.md":
            continue
        if not re.match(r"---\n.*?^description:", p.read_text(), re.DOTALL | re.MULTILINE):
            missing.append(rel(p))
    assert not missing, f"pages without frontmatter description (router needs it): {missing}"


# --- graph ------------------------------------------------------------------

def page_links(p: Path) -> list[str]:
    """Resolved doc-relative link targets, code fences stripped."""
    out = []
    for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", strip_code(p.read_text())):
        if target.startswith(("http", "mailto:", "#", "/")):
            continue  # external, same-page anchor, or product-path example
        path = target.split("#")[0]
        if not path:
            continue
        try:
            out.append(str((p.parent / path).resolve().relative_to(DOCS_DIR)))
        except ValueError:
            out.append(f"OUTSIDE:{target}")
    return out


def test_no_dead_links():
    dead = []
    for p in content_pages():
        for t in page_links(p):
            if t.startswith("OUTSIDE:") or not (DOCS_DIR / t).is_file():
                dead.append(f"{rel(p)} -> {t}")
    assert not dead, f"dead links: {dead}"


def test_no_orphan_pages():
    """Every page is reachable from at least one content page (SUMMARY doesn't count)."""
    pages = {rel(p) for p in content_pages()}
    linked = set()
    for p in content_pages():
        if p.name == "SUMMARY.md":
            continue
        linked.update(page_links(p))
    orphans = [n for n in pages
               if n not in linked
               and n not in ("SUMMARY.md", "README.md")
               and n not in TEMPLATE_EXEMPT]
    assert not orphans, f"orphan pages (in-degree 0 excluding SUMMARY): {orphans}"


def test_summary_matches_filesystem():
    listed = set(summary_paths())
    on_disk = {rel(p) for p in content_pages() if p.name != "SUMMARY.md"}
    dangling = listed - on_disk
    unlisted = on_disk - listed
    assert not dangling, f"SUMMARY entries with no file: {sorted(dangling)}"
    assert not unlisted, f"pages missing from SUMMARY: {sorted(unlisted)}"


def test_router_fresh():
    proc = subprocess.run(
        ["python3", str(SCRIPTS / "generate_router.py"), "--check"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


# --- budgets ----------------------------------------------------------------

@pytest.mark.parametrize("page", [p for p in content_pages() if rel(p).split("/")[0] in CHAR_BUDGETS], ids=rel)
def test_token_budget(page):
    budget = CHAR_BUDGETS_EXEMPT.get(rel(page), CHAR_BUDGETS[rel(page).split("/")[0]])
    size = len(page.read_text())
    assert size <= budget, (
        f"{rel(page)} is {size} chars (budget {budget}) — split depth into a "
        f"lazily-linked page; every token taxes every load"
    )
