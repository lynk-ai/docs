"""ask-docs eval suite — one eval per case in datasets/questions.yaml.

The expensive half of every case (subject session + judge) runs up front in
the `case_runs` fixture's bounded thread pool (--concurrency); each eval here
then scores its case and asserts. Artifacts are written before the asserts so
a failing case still leaves its full trace for agentic analysis.

Run:  uv run pytest                            (whole suite)
      uv run pytest -k q001                    (one case)
      uv run pytest --arm b --concurrency 6    (an arm, 6 subjects at once)
"""

import pytest

from harness.scoring import (
    Verdict,
    render_report,
    results_row,
    score,
    summary_line,
)


@pytest.mark.evaluation
def eval_ask_docs(case, case_dir, run_dir, docs_sha, suite, arm, arm_root, case_runs):
    reps = [score(case, ev, j, err, root=arm_root)
            for ev, err, j in case_runs[case.id]]
    res = reps[0]  # rep 1 owns the artifacts; extra reps refine the verdict
    verdicts = [r.verdict for r in reps]
    flaky = len(set(verdicts)) > 1

    report = render_report(case, res, run_dir.name, docs_sha, arm)
    if len(reps) > 1:
        report += (f"\nReps (pass^{len(reps)}): "
                   f"{' / '.join(v for v in verdicts)}"
                   + (" — FLAKY: verdict flips across reps; suspect an "
                      "ambiguous key or real subject variance\n" if flaky
                      else " — stable\n"))
    (case_dir / "report.md").write_text(report)
    verdict_cell = "/".join(verdicts) if len(reps) > 1 else str(res.verdict)
    suite.append({
        "id": case.id,
        "band": case.band,
        "holdout": case.holdout,
        # a case is only as good as its worst rep (pass^k)
        "verdict": max(verdicts, key=list(Verdict).index),
        "cost": sum(r.cost for r in reps),
        "summary": summary_line(case, res) + (f" · reps {verdict_cell}" if flaky else ""),
        "row": results_row(case, res, run_dir.name, docs_sha, arm),
    })

    failed = [(i + 1, r) for i, r in enumerate(reps) if r.verdict is not Verdict.PASS]
    if not failed:
        return
    rep_n, worst = failed[0]
    where = case_dir if rep_n == 1 else case_dir / f"rep{rep_n}"
    if worst.verdict is Verdict.ERROR:
        pytest.fail(f"rep{rep_n}: {worst.error} — see {where}/")
    if worst.verdict is Verdict.SUSPECT:
        pytest.fail(
            f"rep{rep_n} SUSPECT: expectations happened but sources were not "
            f"read (answer may come from model prior) — see {case_dir}/report.md"
        )
    missed = [claim for claim, ok, _ in worst.judged if not ok]
    pytest.fail(
        f"rep{rep_n}{' (FLAKY across reps)' if flaky else ''}: expectations "
        f"that didn't happen: {missed} — see {case_dir}/report.md"
    )
