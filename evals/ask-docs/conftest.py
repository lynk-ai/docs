"""Suite wiring: case parametrization, per-case dirs, run provenance, and the
suite collector whose teardown writes REPORT.md / meta.json / RESULTS.md.

Artifact layout per pytest invocation:
    results/<timestamp>/
      meta.json        docs sha, verdict per case, total cost
      REPORT.md        one line per case + totals, links to case reports
      <case-id>/       report.md · answer.md · transcript.jsonl · judge.json
plus one row per case-run in results/RESULTS.md — the trend table.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import pytest

from harness.cases import DOCS_DIR, EVAL_DIR, load_cases
from harness.runner import judge_expectations, run_subject
from harness.scoring import Verdict, result_event

RESULTS_HEADER = (
    "| run | question | arm | band | verdict | recall | expectations | hops (eff) | extra reads | cost | model | docs sha |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|---|\n"
)


def pytest_addoption(parser):
    parser.addoption(
        "--subject-model", default=None,
        help="pin the subject session's model (e.g. claude-sonnet-4-6); "
             "the judge stays on the CLI default",
    )
    parser.addoption(
        "--arm", default="a",
        help="retrieval configuration under test: 'a' runs the shipped "
             "docs/.claude as-is; any other name materializes a docs copy "
             "with arms/<name>/.claude swapped in",
    )
    parser.addoption(
        "--concurrency", type=int, default=4,
        help="how many subject sessions run at once (subject+judge are "
             "pooled up front; scoring and asserts stay sequential)",
    )
    parser.addoption(
        "--repeat", type=int, default=1,
        help="independent subject runs per case (pass^k: a case passes only "
             "if every rep passes; mixed verdicts are reported as flips). "
             "K=3 captures most reducible variance; use on flip-suspects.",
    )


@pytest.fixture(scope="session")
def subject_model(request) -> str | None:
    return request.config.getoption("--subject-model")


@pytest.fixture(scope="session")
def arm(request) -> str:
    return request.config.getoption("--arm")


@pytest.fixture(scope="session")
def arm_root(arm):
    """The docs root the subject runs in — ALWAYS a temp copy, even for the
    shipped arm 'a'. Two reasons: overlay arms swap .claude in, and the temp
    root moves the subject out of /Users so the runner's Read(/Users/**)
    fence can hold (a subject once escaped into sibling repos via absolute
    Read paths). Non-'a' arms get arms/<name>/.claude swapped in."""
    tmp = Path(tempfile.mkdtemp(prefix=f"ask-docs-arm-{arm}-"))
    root = tmp / "docs"
    shutil.copytree(DOCS_DIR, root)
    if arm != "a":
        overlay = EVAL_DIR / "arms" / arm / ".claude"
        if not overlay.is_dir():
            raise pytest.UsageError(f"unknown arm {arm!r}: no overlay at {overlay}")
        shutil.rmtree(root / ".claude")
        shutil.copytree(overlay, root / ".claude")
    yield root
    shutil.rmtree(tmp, ignore_errors=True)


def pytest_generate_tests(metafunc):
    """Every eval that takes a `case` runs once per case in the dataset."""
    if "case" in metafunc.fixturenames:
        cases = load_cases()
        metafunc.parametrize("case", cases, ids=[c.id for c in cases])


@pytest.fixture
def case_dir(run_dir, case):
    """This case's artifact dir inside the run dir (the pooled runner
    creates it first)."""
    d = run_dir / case.id
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture(scope="session")
def case_runs(request, run_dir, arm_root, subject_model):
    """The expensive half of every case — subject session + judge — executed
    up front in a bounded thread pool (--concurrency). Tests then score and
    assert sequentially, so the run dir, per-case verdicts, and the aggregate
    report keep their single-run shape. Returns {case_id: [(events, error,
    judge), ...]} — one tuple per rep (--repeat; rep 1 writes to the case
    dir, reps 2+ to rep<N>/ inside it). Honors -k: only collected cases
    run."""
    n = request.config.getoption("--concurrency")
    reps = request.config.getoption("--repeat")
    selected = {item.callspec.params["case"].id: item.callspec.params["case"]
                for item in request.session.items if hasattr(item, "callspec")}
    allow_task = (arm_root / ".claude" / "agents").is_dir()

    def one(case, rep):
        d = run_dir / case.id if rep == 1 else run_dir / case.id / f"rep{rep}"
        d.mkdir(parents=True, exist_ok=True)
        try:
            events, error = run_subject(
                case.question, d / "transcript.jsonl",
                model=subject_model, cwd=arm_root, allow_task=allow_task)
            answer = result_event(events).get("result", "")
            (d / "answer.md").write_text(answer or "(no answer)")
            judge = {} if error else judge_expectations(case, answer, d)
        except Exception as e:  # one crashed worker must not kill the suite
            events, error, judge = [], f"runner crashed: {e!r}", {}
        return case.id, rep, (events, error, judge)

    results: dict = {cid: [None] * reps for cid in selected}
    jobs = [(c, r) for c in selected.values() for r in range(1, reps + 1)]
    with ThreadPoolExecutor(max_workers=n) as pool:
        futures = [pool.submit(one, c, r) for c, r in jobs]
        for done, fut in enumerate(as_completed(futures), start=1):
            cid, rep, payload = fut.result()
            results[cid][rep - 1] = payload
            print(f"[case-runs] {done}/{len(futures)} {cid} rep{rep} done",
                  file=sys.stderr, flush=True)
    return results


@pytest.fixture(scope="session")
def docs_sha() -> str:
    out = subprocess.run(["git", "-C", str(DOCS_DIR), "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True)
    return out.stdout.strip() or "?"


@pytest.fixture(scope="session")
def run_dir():
    d = EVAL_DIR / "results" / datetime.now().strftime("%Y%m%d-%H%M%S")
    d.mkdir(parents=True)
    return d


@pytest.fixture(scope="session")
def suite(run_dir, docs_sha, arm):
    """Collects one entry per case; teardown writes the run-level artifacts."""
    results: list[dict] = []
    yield results
    if not results:
        return
    verdicts = [r["verdict"] for r in results]
    totals = f"{verdicts.count(Verdict.PASS)}/{len(verdicts)} PASS" + "".join(
        f" · {verdicts.count(v)} {v}"
        for v in (Verdict.SUSPECT, Verdict.FAIL, Verdict.ERROR) if v in verdicts
    )
    bands: dict[str, list] = {}
    for r in results:
        bands.setdefault(r.get("band", "?"), []).append(r["verdict"])
    band_lines = "".join(
        f"- {band}: {vs.count(Verdict.PASS)}/{len(vs)} PASS\n"
        for band, vs in sorted(bands.items())
    )
    (run_dir / "REPORT.md").write_text(
        f"# eval run {run_dir.name} — {totals}\n\n"
        f"arm {arm} · docs {docs_sha} · total ${sum(r['cost'] for r in results):.2f}\n\n"
        f"Per band (aggregate hides the ends of the spectrum):\n{band_lines}\n"
        + "".join(
            f"- {r['summary']}{' · HOLDOUT — score only, do not diagnose' if r.get('holdout') else ''}"
            f" → [{r['id']}/report.md]({r['id']}/report.md)\n"
            for r in results)
    )
    (run_dir / "meta.json").write_text(json.dumps({
        "run": run_dir.name,
        "arm": arm,
        "docs_sha": docs_sha,
        "total_cost_usd": round(sum(r["cost"] for r in results), 4),
        "verdicts": {r["id"]: r["verdict"] for r in results},
    }, indent=2) + "\n")

    log = EVAL_DIR / "results" / "RESULTS.md"
    if not log.exists() or not log.read_text().startswith(RESULTS_HEADER.split("\n")[0]):
        if log.exists():
            # timestamped so a second header change never clobbers the first bak
            log.rename(log.with_name(f"RESULTS-{run_dir.name}.md.bak"))
        log.write_text(RESULTS_HEADER)
    with log.open("a") as f:
        f.writelines(r["row"] for r in results)
