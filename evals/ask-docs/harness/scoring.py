"""Deterministic scoring of a case run, and rendering of its artifacts.

Verdicts (SUSPECT idea borrowed from lynk-build PR #4):
  PASS    reached every source + every expectation happened
  SUSPECT expectations happened but sources were NOT read — the answer likely
          came from model prior or a grep leak, not the docs. Inspect.
  FAIL    one or more expectations didn't happen
  ERROR   the session or the judge died — errored, never misread as wrong
"""

import re
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from .cases import DOCS_DIR, PROTOCOL_READS, EvalCase


class Verdict(StrEnum):
    PASS = "PASS"
    SUSPECT = "SUSPECT"
    FAIL = "FAIL"
    ERROR = "ERROR"


def result_event(events: list[dict]) -> dict:
    """The terminal `result` event of a session, or {} if none."""
    return next((e for e in events if e.get("type") == "result"), {})


def _all_happened(judged: list[tuple[str, bool, str]]) -> bool:
    """True iff there is at least one judged claim and all of them happened."""
    return bool(judged) and all(ok for _, ok, _ in judged)


@dataclass
class CaseResult:
    verdict: Verdict
    error: str | None
    # recall
    recall_hits: list[bool]
    # expectations: (claim, happened, evidence)
    judged: list[tuple[str, bool, str]]
    # hops
    reads: list[str]
    hops_to_complete: int | None
    efficiency: float
    extra: list[str]
    searches: int
    rereads: int
    # subagent arms: first-touch reads per context (main = the answering
    # context, sub = forked). `reads` is the union in event order.
    reads_main: list[str]
    reads_sub: list[str]
    spawns: int
    # run metadata
    model: str
    num_turns: int | str
    duration_ms: float
    cost: float
    # grounding gates (deterministic, run before trusting the judge):
    # happened-claims whose quoted evidence doesn't appear in the answer
    unverified_evidence: list[str] = field(default_factory=list)
    # doc paths the answer cites that the session never read — fabrications
    cited_not_read: list[str] = field(default_factory=list)

    @property
    def recall_ok(self) -> bool:
        return all(self.recall_hits)

    @property
    def expectations_ok(self) -> bool:
        return _all_happened(self.judged)

    @property
    def happened(self) -> int:
        return sum(1 for _, ok, _ in self.judged if ok)


def get_trace(events: list[dict], root: Path = DOCS_DIR) -> dict:
    """Ordered first-touch reads (docs-root-relative), re-read and search
    counts. Subagent events carry parent_tool_use_id. First-touch is tracked
    PER CONTEXT — the same page read by the scout and then by the main agent
    is a first touch in each, not a re-read — so main-context grounding
    stays visible on subagent arms. `reads` is the union in event order.
    Paths are resolved before relativizing (macOS tempdirs alias
    /var <-> /private/var)."""
    root = root.resolve()
    reads, reads_main, reads_sub = [], [], []
    searches, rereads, spawns = 0, 0, 0
    for ev in events:
        if ev.get("type") != "assistant":
            continue
        in_sub = bool(ev.get("parent_tool_use_id"))
        for block in ev.get("message", {}).get("content", []):
            if block.get("type") != "tool_use":
                continue
            if block["name"] == "Read":
                p = Path(block["input"].get("file_path", "")).resolve()
                try:
                    rel = str(p.relative_to(root))
                except ValueError:
                    rel = str(p)
                bucket = reads_sub if in_sub else reads_main
                if rel in bucket:
                    rereads += 1
                else:
                    bucket.append(rel)
                if rel not in reads:
                    reads.append(rel)
            elif block["name"] in ("Grep", "Glob"):
                searches += 1
            elif block["name"] in ("Task", "Agent") and not in_sub:
                spawns += 1
    return {"reads": reads, "reads_main": reads_main, "reads_sub": reads_sub,
            "searches": searches, "rereads": rereads, "spawns": spawns}


def _norm(s: str) -> str:
    """Normalize for quote matching: case, whitespace, and every character
    class judges are told to rewrite (quotes) or that markdown decorates."""
    return re.sub(r"[\s`'\"*_]+", " ", s.lower()).strip()


def verify_evidence(judged: list, answer: str) -> list[str]:
    """The mechanical gate on the judge's grounding: for every happened=true
    claim, at least one >=8-char fragment of its quoted evidence (split on
    ellipses) must appear in the answer. Returns the claims that fail —
    evidence the judge asserted but the answer doesn't contain."""
    answer_n = _norm(answer)
    bad = []
    for claim, ok, evidence in judged:
        if not ok:
            continue
        frags = [f for f in re.split(r"\.\.\.|…", str(evidence))
                 if len(_norm(f)) >= 8]
        if frags and not any(_norm(f) in answer_n for f in frags):
            bad.append(claim)
    return bad


def find_cited_not_read(answer: str, reads: list[str], root: Path) -> list[str]:
    """Doc paths the answer cites but the session never read. A citation to
    an unread page is a guaranteed fabrication — checkable here because the
    harness sees the whole trajectory."""
    cited = set(re.findall(r"[\w][\w./-]*\.md", answer))
    read_set = set(reads)
    return sorted(
        c for c in cited
        if (root / c).is_file()          # a real docs page, not a stray token
        and c not in read_set
        and not any(r.endswith("/" + c) or r == c for r in read_set)
    )


def score(case: EvalCase, events: list[dict], judge: dict, error: str | None,
          root: Path = DOCS_DIR) -> CaseResult:
    result = result_event(events)
    init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), {})
    if not error and (not result or result.get("is_error")):
        error = f"session errored: {result.get('subtype', 'no result event')}"
    if not error and "error" in judge:
        error = judge["error"]

    trace = get_trace(events, root)
    reads = trace["reads"]
    recall_hits = [any(opt in reads for opt in need) for need in case.sources]
    judged = judge.get("results", [])

    answer = result_event(events).get("result", "") or ""
    unverified = verify_evidence(judged, answer)
    cited_not_read = find_cited_not_read(answer, reads, root)
    ok_claims = [c for c, ok, _ in judged if ok]
    if not error and ok_claims and len(unverified) == len(ok_claims):
        # every "happened" verdict rests on evidence the answer doesn't
        # contain — the judge is confabulating; never let that become a PASS
        error = "judge errored: no quoted evidence found in the answer"

    # Hops: first-touch reads until every source need is satisfied.
    hops_to_complete = None
    if all(recall_hits):
        seen: set = set()
        for i, r in enumerate(reads, start=1):
            seen.add(r)
            if all(set(need) & seen for need in case.sources):
                hops_to_complete = i
                break
    efficiency = min(1.0, case.optimal_hops / hops_to_complete) if hops_to_complete else 0.0
    in_sources = case.source_paths | set(PROTOCOL_READS)

    expectations_ok = _all_happened(judged)
    if error:
        verdict = Verdict.ERROR
    elif expectations_ok:
        verdict = Verdict.PASS if all(recall_hits) else Verdict.SUSPECT
    else:
        verdict = Verdict.FAIL

    return CaseResult(
        verdict=verdict,
        error=error,
        recall_hits=recall_hits,
        judged=judged,
        reads=reads,
        hops_to_complete=hops_to_complete,
        efficiency=efficiency,
        extra=[r for r in reads if r not in in_sources],
        searches=trace["searches"],
        rereads=trace["rereads"],
        reads_main=trace["reads_main"],
        reads_sub=trace["reads_sub"],
        spawns=trace["spawns"],
        unverified_evidence=unverified,
        cited_not_read=cited_not_read,
        model=init.get("model", "?"),
        num_turns=result.get("num_turns", "?"),
        duration_ms=result.get("duration_ms") or 0,
        cost=(result.get("total_cost_usd") or 0) + judge.get("cost", 0),
    )


def _mark(ok: bool) -> str:
    return "✓" if ok else "✗"


def _jaccard(case: EvalCase, reads: list[str]) -> float:
    """Read-set vs gold-set similarity (localization-style). Gold = protocol
    reads + the satisfied alternative per need (first option if unmet).
    Diagnostic only — collapses recall and over-reading into one number."""
    gold = set(PROTOCOL_READS)
    for need in case.sources:
        hit = next((opt for opt in need if opt in reads), need[0])
        gold.add(hit)
    r = set(reads)
    return len(r & gold) / len(r | gold) if r | gold else 1.0


def render_report(case: EvalCase, res: CaseResult, ts: str, sha: str,
                  arm: str = "a") -> str:
    # Sources whose only read happened inside a forked (subagent) context —
    # their text never entered the context that wrote the answer.
    sub_only_sources = sorted(
        (set(res.reads_sub) - set(res.reads_main)) & case.source_paths)
    lines = [
        f"# {case.id} — {res.verdict}",
        "",
        f"**Question:** {case.question}",
        f"**Run:** {ts} · arm {arm} · band {case.band}"
        f"{' · HOLDOUT (score only, do not diagnose)' if case.holdout else ''}",
        f"{res.num_turns} turns · ${res.cost:.2f} (incl. judge) "
        f"· {res.duration_ms / 1000:.0f}s · model {res.model} · docs {sha}",
        *([f"**Error:** {res.error}"] if res.error else []),
        *(["**SUSPECT:** expectations happened but sources were not read — "
           "answer may come from model prior, not the docs. Read the transcript."]
          if res.verdict is Verdict.SUSPECT else []),
        "",
        f"## 1. Recall — reached every required source? {_mark(res.recall_ok)}",
        *(f"- {_mark(hit)} {' OR '.join(need)}"
          for need, hit in zip(case.sources, res.recall_hits)),
        "",
        f"## 2. Expectations — {res.happened}/{len(case.expect)} happened "
        f"{_mark(res.expectations_ok)}",
        *(f"- {_mark(ok)} {claim}\n  - evidence: {evidence}"
          + ("\n  - ⚠ evidence NOT FOUND in answer — judge grounding suspect"
             if claim in res.unverified_evidence else "")
          for claim, ok, evidence in res.judged),
        "",
        f"## 3. Hops — {res.hops_to_complete or '∞'} to complete source set, "
        f"optimal {case.optimal_hops} → efficiency {res.efficiency:.2f}",
        f"- {_mark(res.reads[:2] == list(PROTOCOL_READS))} protocol first "
        f"(SUMMARY.md → concepts/README.md)",
        f"- path: {' → '.join(f'{r} [sub]' if r not in res.reads_main else r for r in res.reads) or '(no reads)'}",
        *([f"- main-context reads: {' → '.join(res.reads_main) or '(none)'}"]
          if res.reads_sub else []),
        f"- searches (Grep/Glob): {res.searches} · re-reads: {res.rereads}"
        + (f" · subagents: {res.spawns}" if res.spawns else ""),
        *([f"- grounding: sources read ONLY in a forked context (never in the "
           f"answering context): {', '.join(sub_only_sources)}"]
          if sub_only_sources else []),
        *([f"- ⚠ cited but NEVER READ (fabricated citation): "
           f"{', '.join(res.cited_not_read)}"] if res.cited_not_read else []),
        f"- read-set Jaccard vs gold: {_jaccard(case, res.reads):.2f}",
        *(f"- extra (outside sources): {r}" for r in res.extra),
        "",
        "Answer: answer.md · full trace: transcript.jsonl · judge: judge.json",
    ]
    return "\n".join(lines) + "\n"


def results_row(case: EvalCase, res: CaseResult, ts: str, sha: str,
                arm: str = "a") -> str:
    return (
        f"| {ts} | {case.id} | {arm} "
        f"| {case.band}{' (holdout)' if case.holdout else ''} "
        f"| {res.verdict} "
        f"| {sum(res.recall_hits)}/{len(case.sources)} "
        f"| {res.happened}/{len(case.expect)} "
        f"| {res.hops_to_complete or '∞'} ({res.efficiency:.2f}) | {len(res.extra)} "
        f"| ${res.cost:.2f} | {res.model} | {sha} |\n"
    )


def summary_line(case: EvalCase, res: CaseResult) -> str:
    return (
        f"{case.id}: {res.verdict} · recall {sum(res.recall_hits)}/{len(case.sources)} "
        f"· expectations {res.happened}/{len(case.expect)} "
        f"· hops {res.hops_to_complete or '∞'} ({res.efficiency:.2f})"
    )
