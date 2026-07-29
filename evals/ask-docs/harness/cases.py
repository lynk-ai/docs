"""Typed eval cases loaded from datasets/questions.yaml — the suite's answer key.

Loading validates the key itself: unique ids, non-empty `expect`, and every
source path present on disk (a typo would otherwise fail every run silently).
"""

from dataclasses import dataclass
from pathlib import Path

import yaml

EVAL_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = EVAL_DIR.parent.parent / "docs"
DATASET = EVAL_DIR / "datasets" / "questions.yaml"

# The two reads the ask-docs skill mandates before any navigation.
PROTOCOL_READS = ("SUMMARY.md", "concepts/README.md")


# The question-space spectrum (reviews/retrieval-eval-loop.md §1) — each band
# stresses a different component of the retrieval system, so pass rates are
# reported per band, never only in aggregate.
BANDS = (
    "orientation", "first-build", "vocabulary", "mechanics",
    "debugging", "judgment", "context-engineering", "limits",
)


@dataclass(frozen=True)
class EvalCase:
    id: str
    question: str
    # Each need is a tuple of alternative paths; reading any one satisfies it.
    sources: tuple[tuple[str, ...], ...]
    # Claims a correct answer makes; the judge classifies each happened/not.
    expect: tuple[str, ...]
    optimal_hops: int
    # Which band of the question spectrum this case covers.
    band: str = "mechanics"
    # Hold-outs are scored every round but never read during diagnosis.
    holdout: bool = False

    @property
    def source_paths(self) -> set[str]:
        return {opt for need in self.sources for opt in need}


def load_cases() -> list[EvalCase]:
    raw = yaml.safe_load(DATASET.read_text())["cases"]
    cases: list[EvalCase] = []
    seen: set[str] = set()
    for q in raw:
        if q["id"] in seen:
            raise ValueError(f"duplicate case id {q['id']!r} in {DATASET.name}")
        seen.add(q["id"])
        if not q.get("expect"):
            raise ValueError(f"{q['id']}: every case needs a non-empty `expect` list")
        sources = tuple(
            tuple(e) if isinstance(e, list) else (e,) for e in q["sources"]
        )
        missing = [p for need in sources for p in need if not (DOCS_DIR / p).is_file()]
        if missing:
            raise ValueError(f"{q['id']}: paths in {DATASET.name} don't exist in docs/: {missing}")
        band = q.get("band", "mechanics")
        if band not in BANDS:
            raise ValueError(f"{q['id']}: unknown band {band!r} — one of {BANDS}")
        cases.append(EvalCase(
            id=q["id"],
            question=q["question"],
            sources=sources,
            expect=tuple(q["expect"]),
            optimal_hops=q.get("optimal_hops", len(PROTOCOL_READS) + len(sources)),
            band=band,
            holdout=bool(q.get("holdout", False)),
        ))
    return cases
