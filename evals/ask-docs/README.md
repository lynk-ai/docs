# ask-docs eval harness

Measures the `ask-docs` retrieval skill (ships in `docs/.claude/skills/ask-docs/`).
Simple by design: one script, one YAML answer key, plain-text artifacts.

Sibling project: `lynk-build` PR #4 evals the lynk-wiki *plugin* end-to-end (Agent
SDK, authoring pipeline, library track). This harness is the fast inner loop for
doc authors; several measurement ideas (SUSPECT verdict, first-touch hop
efficiency, errored ≠ wrong, run provenance) are borrowed from that PR, and its
human-reviewed cases convert directly into cases here (q002 is one).

## The checks

Each case asks its question via `claude -p` in a **fresh headless session rooted
at `docs/`** (only `Skill`/`Read`/`Glob`/`Grep` allowed; `--strict-mcp-config`
keeps user MCP servers out) and scores the run:

1. **Recall** — did it reach every required source? `sources` lists the needs;
   an entry is a path, or a nested list of alternatives where reading any one
   satisfies the need. Paths are validated against disk at load time, so a
   typo in the answer key fails loudly, not silently.
2. **Expectations** — each `expect` claim is classified **happened / didn't
   happen** by a judge (a second Claude call, no tools, sees only question +
   answer + claims), with a quoted piece of evidence per claim. A claim
   happened only if the answer affirmatively states it — keywords appearing in
   a negated or hedged sentence don't count. Reported as n/m.
3. **Hops** — first-touch reads until the source set completes, vs the case's
   `optimal_hops` (which includes the 2 protocol reads):
   `efficiency = min(1, optimal/actual)`. Re-reads don't count; Grep/Glob are
   reported as `searches`; reads outside `sources` are listed as extra
   (informational). Trend metric — never gates.

## Verdicts

| Verdict | Meaning |
|---|---|
| **PASS** | recall ✓ and every expectation happened |
| **SUSPECT** | expectations happened but required docs were NOT read — the answer likely came from model prior or a grep leak, not the docs. Read the transcript. |
| **FAIL** | one or more expectations didn't happen |
| **ERROR** | the session or the judge died (timeout/CLI) — never misread as a wrong answer |

## Running and reading results

The suite runs via pytest — one eval per case in `datasets/questions.yaml`:

```bash
cd evals/ask-docs
uv run pytest              # whole suite
uv run pytest -k q001      # one case
```

Layout (mirrors the lynkbot architect-agent eval pattern, minus the platform
machinery):

```
eval_ask_docs.py       the eval — thin per-case flow: run → judge → score → artifacts → assert
conftest.py            fixtures: case parametrization (pytest_generate_tests), case_dir,
                       run_dir, docs_sha; suite teardown writes run-level artifacts
harness/
  cases.py             typed answer key (EvalCase), validated at load
  runner.py            the two LLM calls: subject session + judge
  scoring.py           deterministic scoring (Verdict StrEnum) + report rendering
datasets/
  questions.yaml       the cases
```

A case FAILs on missed expectations or a SUSPECT verdict; session/judge death
is reported as ERROR. Artifacts are written *before* the asserts, so failing
cases keep their full trace.

Every pytest invocation gets one directory:

```
results/<timestamp>/
  meta.json        docs git SHA, verdict per case, total cost
  REPORT.md        one line per case + totals, links to case reports
  <case-id>/       report.md · answer.md · transcript.jsonl · judge.json
```

plus one row per case-run in `results/RESULTS.md` — the trend table, which also
records the **docs git SHA and model** so rows are comparable over time.
Discipline: between runs you compare, change the docs *or* the model, never
both. `results/` is gitignored.

**Analysis is agentic, not coded:** point a Claude session at a run dir and ask
why it failed. Retrieval runs are noisy; run a case 3–5× before trusting a
number.

## Adding a case

The whole suite lives in `datasets/questions.yaml` — the answer key is meant
to be reviewable in a single scan. Copy an existing case: `question`,
`sources` (needs; nest a list for alternatives), `expect` (claims, see below),
`optimal_hops`.

Write `expect` claims FROM the docs, positively and independently gradeable —
one fact per claim, quoting the owning page in a YAML comment beside it. The
comments are what keeps the key reviewable later. Include one citation claim
("cites <page>") — that's what separates PASS from SUSPECT-shaped answers. For
trap cases (things the docs don't cover), the claim IS the refusal: "States
that the docs don't cover X" — and a claim like "does not invent syntax for X"
gives the judge the negative side. The lynk-build PR #4 `datasets/*.yaml`
rubric bullets convert directly into `expect` claims.

## Known caveat

A session rooted at `docs/` still inherits the root `CLAUDE.md` and root
`.claude/` skills (config reads upward to the git root). For a fully clean
test, point the subject run at the output of `scripts/render-to-plugin.sh`.
