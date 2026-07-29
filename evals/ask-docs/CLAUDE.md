# ask-docs eval suite

Pytest-based eval harness for the `ask-docs` retrieval skill (which ships in
`docs/.claude/skills/ask-docs/`). Full design rationale and usage in README.md
— read it before changing anything here.

## Layout

- `eval_ask_docs.py` — the eval: one parametrized function, the per-case flow
  (run subject → judge → score → write artifacts → assert). Keep it thin.
- `conftest.py` — fixtures (`case` parametrization via `pytest_generate_tests`,
  `case_dir`, `run_dir`, `docs_sha`) and the `suite` collector whose teardown
  writes the run-level artifacts.
- `harness/` — the library: `cases.py` (typed answer key, validated at load),
  `runner.py` (the two `claude -p` calls: subject + judge), `scoring.py`
  (deterministic scoring, `Verdict` StrEnum, report rendering).
- `datasets/questions.yaml` — the cases. This is the reviewable answer key;
  keys are written FROM the docs, with YAML comments naming the owning page.
  Every case names its `band` (question-spectrum coverage); `holdout: true`
  cases are scored every round but never diagnosed.
- `arms/<name>/.claude/` — retrieval-configuration overlays for A/B testing
  the skill (`--arm <name>` materializes a docs copy with the overlay
  swapped in; arm `a` = the shipped tree as-is).
- `compare.py` — paired per-case diff of two run dirs. At ~29 cases the
  aggregate pass rate is noise (±8-9pp SE); verdict flips are the
  comparison unit.
- `DECISIONS.md` — one entry per eval-loop iteration: what changed, why
  (gate + evidence), measured effect. The loop's memory; keep it current.
- `results/` — gitignored artifacts; one dir per pytest invocation.

## Options

- `--subject-model <id>` pins the subject session (judge stays on the CLI
  default — never judge with the subject's model tier).
- `--arm <name>` picks the retrieval configuration under test.
- `--concurrency N` (default 4) — subject+judge run pooled up front in a
  thread pool; scoring/asserts stay sequential, artifacts stay single-run.
- `--repeat K` — pass^k: K independent runs per case, a case passes only if
  all reps pass; mixed verdicts are flagged FLAKY. K=3 captures most
  reducible variance; prefer new cases over more reps beyond that.

## Rules

- Run with `uv run pytest` (`-k <case-id>` for one case). Every case costs
  real money (~$0.65, two live LLM calls) — don't run the suite casually.
- Deterministic gates guard the judge: happened-claims need verbatim
  evidence found in the answer (wholesale fabrication → ERROR), and cited
  doc paths must appear in the read trajectory (else flagged as fabricated
  citations).
- A case failing identically across all arms/reps → suspect the key before
  the model; key fixes are logged in the dataset's case-edit log. Judge-only
  re-runs on frozen transcripts (see DECISIONS) split judge noise from
  subject noise for free.
- Keep it lean: pytest + pyyaml only; no new abstractions without need.
- Artifacts are written BEFORE asserts — never reorder; failing cases must
  keep their trace.
- Verdict semantics (PASS / SUSPECT / FAIL / ERROR) are load-bearing —
  ERROR means the session/judge died and must never be reported as FAIL;
  SUSPECT means expectations passed without reading the sources.
- The subject runs in a fresh session rooted at `docs/` — never "test" the
  skill from a session that carries this workspace's context (see the root
  CLAUDE.md testing protocol).
