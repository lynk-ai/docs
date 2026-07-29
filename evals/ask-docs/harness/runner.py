"""The two LLM calls of a case run: the subject session and the judge.

Subject: `claude -p` in a fresh headless session rooted at docs/ — the
uncontaminated consumer the root CLAUDE.md testing protocol requires. Only
Skill/Read/Glob/Grep are allowed; --strict-mcp-config keeps user MCP out.

Judge: a second `claude -p`, no tools, sees only question + answer + claims.
Session failures are returned as data (error strings), never raised — an
errored session must report as ERROR, not crash the suite.
"""

import json
import re
import subprocess
from pathlib import Path

from .cases import DOCS_DIR, EvalCase

SUBJECT_TIMEOUT_S = 600
JUDGE_TIMEOUT_S = 180

JUDGE_PROMPT = """You are classifying which expectations an answer fulfills.
Judge each expectation INDEPENDENTLY against the answer below. An expectation
"happened" only if the answer affirmatively states or clearly implies it — an
expectation that is absent, hedged away, or contradicted did NOT happen, even
if its keywords appear. Use no outside knowledge; the answer text is the only
evidence.

<question>
{question}
</question>

<answer>
{answer}
</answer>

<expectations>
{expectations}
</expectations>

Respond with ONLY a JSON array, one object per expectation in order:
[{{"n": 1, "happened": true, "evidence": "<see below>"}}, ...]
For happened=true, evidence MUST be a verbatim span copied from the answer
(the harness string-matches it against the answer; a paraphrase fails the
check). For happened=false, evidence states briefly why not.
No markdown fences, no other text. The output must be valid JSON: keep each
evidence under 20 words and replace any double quotes inside it with single
quotes."""


def run_subject(question: str, transcript_path: Path,
                model: str | None = None, cwd: Path = DOCS_DIR,
                allow_task: bool = False) -> tuple[list[dict], str | None]:
    """Ask the question; returns (events, error). `model` pins the subject
    session (the judge is pinned separately) — None uses the CLI default.
    `cwd` is the docs root the session runs in (an arm's materialized copy).
    `allow_task` opens the Task tool for subagent arms (C/D)."""
    # --allowedTools only auto-approves; user-level settings can still let other
    # tools through (a Sonnet run escaped via `Bash find` into sibling repos).
    # --disallowedTools is the actual fence.
    # The subagent-spawn tool is "Agent" in current CLIs, "Task" in older ones.
    allowed = ["Skill", "Read", "Glob", "Grep"] + (["Task", "Agent"] if allow_task else [])
    # Path-qualified denies: the subject must not read outside its docs copy.
    # The arm root always lives in the system temp dir (see conftest
    # arm_root), so denying /Users/** blocks sibling-repo and homedir escapes
    # without touching the docs themselves.
    fenced = ["Bash", "Write", "Edit", "NotebookEdit", "WebFetch", "WebSearch",
              "Read(/Users/**)", "Glob(/Users/**)", "Grep(/Users/**)"]
    if not allow_task:
        fenced += ["Task", "Agent"]
    cmd = ["claude", "-p", question, "--output-format", "stream-json", "--verbose",
           "--allowedTools", *allowed,
           "--disallowedTools", *fenced,
           "--strict-mcp-config",
           *(["--model", model] if model else [])]
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                              timeout=SUBJECT_TIMEOUT_S)
    except subprocess.TimeoutExpired as e:
        transcript_path.write_text(e.stdout or "")
        return parse_events(e.stdout or ""), f"session errored: timeout after {SUBJECT_TIMEOUT_S}s"
    transcript_path.write_text(proc.stdout)
    error = None
    if proc.returncode != 0:
        error = f"session errored: exit {proc.returncode}: {proc.stderr.strip()[:300]}"
    return parse_events(proc.stdout), error


def parse_events(stdout: str) -> list[dict]:
    events: list[dict] = []
    for line in stdout.splitlines():
        if line.strip():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return events


def judge_expectations(case: EvalCase, answer: str, workdir: Path) -> dict:
    """Classify each expect claim; returns {'results': [(claim, happened, evidence)],
    'cost': float} or {'error': str, 'cost': float}. One retry — judges
    occasionally emit invalid JSON; raw output lands in judge.json."""
    numbered = "\n".join(f"{i}. {e}" for i, e in enumerate(case.expect, 1))
    prompt = JUDGE_PROMPT.format(question=case.question, answer=answer, expectations=numbered)
    cost, last_error = 0.0, "judge errored"
    for _attempt in (1, 2):
        try:
            proc = subprocess.run(
                ["claude", "-p", prompt, "--output-format", "json",
                 "--disallowedTools", "*", "--strict-mcp-config"],
                cwd=workdir, capture_output=True, text=True, timeout=JUDGE_TIMEOUT_S,
            )
        except subprocess.TimeoutExpired:
            last_error = f"judge errored: timeout after {JUDGE_TIMEOUT_S}s"
            continue
        (workdir / "judge.json").write_text(proc.stdout)
        if proc.returncode != 0:
            last_error = f"judge errored: exit {proc.returncode}: {proc.stderr.strip()[:300]}"
            continue
        try:
            wrapper = json.loads(proc.stdout)
            cost += wrapper.get("total_cost_usd") or 0
            text = wrapper.get("result", "")
            match = re.search(r"\[.*\]", text, re.DOTALL)
            items = json.loads(match.group(0)) if match else None
            if not isinstance(items, list) or len(items) != len(case.expect):
                last_error = f"judge errored: expected {len(case.expect)} verdicts, got: {text[:300]}"
                continue
            return {
                "results": [(claim, bool(item.get("happened")), str(item.get("evidence", "")))
                            for claim, item in zip(case.expect, items)],
                "cost": cost,
            }
        except (json.JSONDecodeError, AttributeError) as e:
            last_error = f"judge errored: unparseable output ({e}): {proc.stdout[:300]}"
    return {"error": last_error, "cost": cost}
