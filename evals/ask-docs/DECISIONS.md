# Retrieval eval loop — decisions log

One entry per loop iteration: what changed, why (gate + evidence), and the
measured effect. This log is what stops us from re-trying reverted ideas.
Strategy and mental model: `reviews/retrieval-eval-loop.md` (build lane).

Format per entry:

```
## <date> — round <n>, arm <A|B|C|D>, dataset <version>
- Change: <one lane, one change>
- Reason: <gate G1–G4 + the failing cases as evidence>
- Effect: <verdict/aggregate diff vs. previous round>
- Verdict: keep / revert
```

---

## 2026-07-20 — round 0, arm A, dataset v1 (9 cases)

- Change: none — re-baseline only. Subject pinned to `claude-sonnet-4-6`
  via the new `--subject-model` harness option; judge stays on the default
  strong model.
- Reason: the existing 9/9 was measured with the subject on the big model;
  it says nothing about the small-model floor.
- Effect — **the Sonnet floor: 7/9 PASS, recall 9/9, both failures G4.**
  Runs 20260720-174024 (8 clean cases) + 20260720-174833 (q005 re-run after
  the harness fix below).
  - q005 first run: total derailment — skill invoked then ignored, zero doc
    reads, subject ran `Bash find` across sibling repos (harness leak, see
    below), found real `.lynk` projects, stalled on "which project should I
    edit?". After closing the leak: protocol perfect, right pages, correct
    trap answer, 3/4 — misses only the cite-the-page-path output rule (named
    the section instead of the path). Gate: **G4** (skill output-contract
    adherence).
  - q007: routing/navigation perfect (3 hops, eff 1.00), 3/4 — dropped the
    load-bearing constraint "snapshot grain is materialized upstream; an
    entity's identity cannot be a query", which the guide states inside the
    example it read. Gate: **G4** (small-model synthesis compression).
  - Signal for the arms: on this (Lynk-vocabulary-heavy) dataset, Sonnet's
    problem is NOT navigation — no G1/G2 after the harness fix. Both misses
    are answer-side adherence. Arm B's grep map targets a failure mode v1
    doesn't exhibit; lane-2 skill wording ("always cite the page path",
    "state the constraints the docs flag") targets what does. Dataset v2's
    naive/orientation bands are where G2 may actually appear.
- Harness bug fixed (allowed in round 0): `--allowedTools` only
  auto-approves, it does not fence — user-level settings let `Bash` through
  and the subject escaped the docs sandbox. Added explicit
  `--disallowedTools Bash Write Edit NotebookEdit Task WebFetch WebSearch`
  to `run_subject`. Verified the other 8 baseline transcripts used only
  Skill/Read/Glob/Grep, so their runs stand.
- Verdict: baseline recorded. No skill/docs/case changes made.

## 2026-07-20 — round 1, dataset v2 authored

- Change (lane 1): dataset v1 (9) → v2 (29 = 24 dev + 5 hold-outs). Every
  case tagged with its band; per-band pass rates now in REPORT.md and a band
  column in RESULTS.md. Harness gained `band`/`holdout` fields on EvalCase
  (validated against the BANDS list) and per-band tallies.
- Reason: v1 lived in the middle of the question spectrum (Lynk-vocabulary
  mechanics/limits) — no orientation, first-build, or context-engineering
  coverage, and almost no naive phrasing. The band ends are the canaries.
- Method: cases written from the coverage matrix, not from transcripts; all
  answer keys written FROM the docs (source pages re-read this round:
  README, project, feature, identity-and-imports, relationships, glossary,
  context-engineering, where-knowledge-goes, designing-domains,
  metrics-time-and-state; h005's negative-space line grepped to
  api/lynk-sql.md). Band tags added to v1 cases; no v1 key text changed.
- Hold-outs: h001 (naive orientation), h002 (extension), h003 (glossary
  routing), h004 (policy-vs-skill), h005 (metric tests = negative space).
  Scored every round, never diagnosed.
- Effect: pending user review, then round 2 (arm bake-off) runs v2.

## 2026-07-20 — round 2, arm A × dataset v2 (run 20260720-193749)

- Change: none — bake-off baseline. Harness gains: `--arm` + overlay
  materialization, per-context read attribution (reads_main/reads_sub,
  resolved paths — two bugs found via the arm C smoke), `--concurrency`
  (subject+judge pooled up front; scoring stays sequential), spawn tool is
  "Agent" in current CLIs (counted + fenced alongside "Task").
- Score: **23/29 PASS (dev 21/24, hold-outs 2/5) · $8.89 · 23 min.**
  Per band: orientation 2/2, first-build 3/3, mechanics 4/4,
  context-engineering 3/3, vocabulary 3/4, judgment 3/4, debugging 2/4,
  limits 3/5.
- Dev failures — all G4, navigation was perfect in every one (recall 29/29,
  protocol followed, efficiency 1.00 on all three):
  - q005: right trap answer, cited the guide instead of a
    concepts/entity/schema-yml/ path (2nd occurrence — stable).
  - q007: dropped "materialized upstream / identity cannot be a query"
    (2nd occurrence — stable).
  - q014: listed 5 of 6 feature fields, omitted `filter`.
- Hold-outs: h001 PASS, h002 PASS, h003 FAIL, h004 FAIL, h005 FAIL —
  scores recorded, not diagnosed.
- Signal: dataset v2's new bands did NOT break navigation — Sonnet + the
  shipped skill routes the whole spectrum. Every dev failure is answer-side
  adherence/compression (G4): citation contract, dropped constraint,
  dropped field. Lane-2 candidates for round 3; arms C/D's return contracts
  (CONSTRAINTS section, "state constraints the docs flag") target exactly
  this — the bake-off tests it.
- Verdict: baseline recorded. No skill/docs/case changes.

## 2026-07-20 — round 2, bake-off complete (arms B/C/D × dataset v2)

- Runs: B 20260720-210125 ($9.28, 5.5m) · C 20260720-210655 ($10.19, 7.6m)
  · D 20260720-211432 ($10.05, 9.0m). Concurrency 5.
- Scores: **A 23 · B 24 · C 24 · D 24 (of 29).** Dev-only: A 21/24,
  B 22/24, C 22/24, D 21/24. Hold-outs: A 2/5, B 2/5, C 2/5, D 3/5.
- Case-level signal (the matrix, not the totals, is the finding):
  - **q014 fails on ALL four arms** — every arm reads feature.md, lists 5
    fields, omits `filter`. For "how do I add a calculated column", the
    filter field is not load-bearing; the key over-demands an exhaustive
    enumeration. Lane-1 candidate (q006 precedent: universal failure +
    claim irrelevant to the question).
  - **q007 passes ONLY on D** — the researcher's mandatory CONSTRAINTS
    section is the only thing that got "materialized upstream / identity
    can't be a query" across. Same for **h005** (NOT COVERED section →
    only D refuses correctly). D's contract fixes G4 compression.
  - **But D pays in G3**: q021 relayed a broken answer ("Both agents are
    running", 0/4) while the fork had read the right guide — the
    catastrophic silent-loss case the strategy predicted. q012's relay
    dropped the citation, and its researcher toured 12 pages (no
    narrowest-set discipline), 156s.
  - q005 (citation contract): A fail, B/C/D pass → variance-prone, mark
    for --repeat. h001/h004 flips across arms — hold-outs, scored only.
  - h003 fails on all four arms (scored, not diagnosed).
- Verdict: **no arm dominates.** B ≈ A (map targets a failure mode that
  doesn't exist — navigation is 100% everywhere). C ≈ A at +15% cost with
  no G4 fix. D uniquely fixes constraint/negative-space transfer but adds
  catastrophic relay risk and double reads.
- Round 3 hypothesis (lane 2, one change): **arm E = inline A + D's
  contract, no boundary** — add to the skill's answer spec: cite the page
  path always; state every constraint the pages flag; complete field
  enumerations when citing a spec. Targets q005/q007/q014-class G4 without
  D's G3 exposure.

## 2026-07-20 — harness upgrades from web research (two-agent sweep)

Reports: LLM-judge practice + file-navigation retrieval eval design (user
constraint honored: no RAG — file-search retrieval only). Adopted:

- **Evidence-quote gate** (deterministic): judge prompt now demands verbatim
  spans for happened=true; scoring fuzzy-matches each span against the
  answer (normalize case/ws/quotes, split on ellipses, >=8-char fragment).
  Unverified evidence → flagged per claim in the report; ALL happened-claims
  unverified → forced ERROR, never PASS. (Datadog/hamel.dev pattern; the
  documented defense against judge confabulation.)
- **Cited-but-never-read detector** (deterministic): doc paths in the answer
  that exist in the tree but never appear in the read trajectory are
  reported as fabricated citations — a check unique to trajectory-observable
  harnesses (chunk-RAG evals can't do it).
- **--repeat K (pass^k)**: K independent subject runs per case; case passes
  only if all reps pass; mixed verdicts flagged FLAKY (ambiguous key or real
  variance). K=3 captures most reducible variance (Anthropic error-bars
  paper, arXiv:2411.00640); between-case variance dominates beyond that.
- **compare.py**: paired per-case diff of two runs (McNemar-style). At n=29
  aggregate SE is ±8-9pp, so aggregate deltas are noise; verdict flips are
  the comparison unit. Validated on A-vs-D: 3 improved / 2 regressed /
  3 both-fail — statistically "B better" is NOT yet supported.
- **Read-set Jaccard** vs gold (localization-literature metric) in reports —
  diagnostic, collapses recall + over-reading.

Adopted as process (no code): universal failure across arms/reps → suspect
the key before the model (q014 already followed this, now validated as the
standard rule); grow the suite from real failures; per-band reporting stays.

## 2026-07-20 — round 3: arm E (inline + answer contract) + q014 key fix

- Changes: (lane 2) arm E = shipped skill + answer contract — cite every
  page by path, carry the constraints, complete enumerations; (lane 1)
  q014's field-enumeration claim relaxed (see dataset case-edit log).
  Bundling disambiguated by a judge-only re-run of arm A's FROZEN q014
  transcript against the new key → 4/4, so q014's flip is the key fix, not
  the contract.
- Score: **25/29 (run 20260720-214811, $10.35, 6.5m).** Paired diff vs
  arm A baseline: +3 (q014 key-fix; h003, h004 plausibly contract)
  −1 (q003) · still-failing q005, q007, h005.
- Diagnosis:
  - **q003 regression = the s03 hijack under variance** (G1): subject read
    ~/.claude/settings.json + ~/.claude/CLAUDE.md — left the docs tree,
    zero doc reads, recommended editing CLAUDE.md. Not a harness leak; the
    real product failure mode this case pins, now shown to be
    variance-prone rather than fixed.
  - **q007 4th reproduction on inline arms** — same claim, same page. The
    inline "carry the constraints" instruction did NOT transfer the
    materialized-upstream rule; arm D's structured return section did.
    Qualifies for lane 3 (≥2 independent failures on one page): the
    constraint lives in prose + a YAML comment mid-pattern; promote it to
    an unmissable warning in guides/metrics-time-and-state.md.
  - **q005 flipped failure modes** (citation fixed by contract; build-rule
    claim dropped this rep) — flip-prone, needs repeats before conclusions.
- Follow-up: --repeat 3 on q003/q005/q007/h005 (arm E) to classify stable
  vs flaky before Round 4 commits. (First attempt hit a transient API
  outage — all four sessions errored in seconds; ERROR verdicts, retried.)

## 2026-07-21 — round 3 close: repeat-3 classification (arm E)

- q003: 3/3 PASS — the ~/.claude hijack was a rare tail event; the case
  stays as the canary. q005: 3/3 PASS — the contract stabilized it.
- q007: FAIL/FAIL/PASS — mostly-fails (6 of 8 runs across configs, same
  claim, same page). Lane-3 threshold met.
- h005: FAIL/SUSPECT/FAIL — hold-out, scored only.

## 2026-07-21 — round 4: lane-3 docs edit for q007 (arm E re-run)

- Change (lane 3, guarded by q007): in guides/metrics-time-and-state.md,
  the materialized-upstream constraint promoted from mid-paragraph prose +
  YAML comment to a bolded standalone sentence opening the snapshot
  pattern ("Materialize the snapshot table upstream first — Lynk cannot
  create it: an entity's identity is never a query."), with compensating
  trims to hold the 10k char budget. Lint 63/63. NOTE: docs tree dirty —
  run 20260721-060707 still shows sha a2beed2.
- Score: **26/29 ($10.24, 6.4m).** Paired diff vs round 3: +3 (q007 —
  the target — plus q003/q005 re-passing per their stable-pass repeat
  classification) −2 (h003 flip-back — hold-out, scored only; q024 — see
  below) · h005 still failing.
- **q007 FAIL→PASS: the docs edit did what four rounds of skill wording
  could not.** Constraint compression is a docs-shape problem: models
  synthesize a pattern but drop preconditions buried mid-paragraph;
  a bolded lead sentence survives.
- q024 single-run regression: answer invented a VIEW-backed identity
  ("point identity at the view's fully-qualified name") — repeat-3 run
  launched to classify. Also logged to the product-questions lane:
  **does Lynk accept a warehouse view as a 3-segment identity?** The docs
  say "physical table"; a view is addressable identically, and the model's
  inference is plausible — engineering should confirm so the docs can say
  it either way.

## 2026-07-21 — round 4 close + promotion

- q024 repeat-3 on arm E: **3/3 PASS** — the view-backed-identity invention
  was a one-run tail event, not caused by the docs edit. The product
  question (views as identity) stays open in the product lane.
- **Arm E promoted**: the answer contract (cite-by-path / carry the
  constraints / complete enumerations) merged into the shipped skill at
  docs/.claude/skills/ask-docs/SKILL.md — verified byte-identical to
  arms/e. Arm "a" and arm "e" are now the same configuration; future
  rounds baseline on the promoted skill.
- End state on Sonnet 4.6, dataset v2: **26/29** (dev 23/24, hold-outs
  3/5), vs 23/29 at round 2 baseline. Remaining: h003 + h005 (hold-outs,
  scored only — if the next dataset revision rotates hold-outs, their
  failure modes can then be diagnosed) and residual single-run variance
  (q003-class hijack ≈ rare tail; repeats are the guard).
- Arms B (grep map), C (scout), D (researcher) remain in arms/ as
  experiments; none dominated. D's structured-return idea survives INSIDE
  the inline skill via the contract.

## 2026-07-21 — constraint-prominence sweep (lane 3, generalizing the q007 fix)

- Motivation: q007 proved constraint compression is a docs-shape problem —
  a precondition buried mid-paragraph/in a code comment was dropped from
  75% of answers; a bolded lead sentence survived. Swept the whole corpus
  for the same shape.
- Method: 3 parallel auditors (core concepts / entity tree /
  reference+api+guides) with strict criteria — act-on-while-applying
  constraint + failed-build-or-silently-wrong + currently buried; existing
  facts only, ≈net-zero chars, Validation enumerations out of scope.
  Auditors also reported disciplined exclusions (already-prominent rules).
- Applied: **10 promotions across 9 pages** —
  1. policy.md: override fully replaces, never merges (also a q003 claim)
  2. lynk-yml.md: default topology has NO shared domain — cross-domain
     composition needs shared_domain set first
  3. glossary.md: no structured pointer — descriptions must stand alone
  4. identity-and-imports.md: 2-segment identity is always domain.entity
     (q004's trap) — now the bullet's bolded lead
  5. identity-and-imports.md: extension requires shared_domain,
     cross-domain only
  6. feature.md: state-the-scale rule out of a table cell into a bolded
     Format lead
  7. metric.md: "a metric takes no arguments" bolded (q006's trap)
  8. api/lynk-sql.md: SELECT/WHERE names are declared features, keys
     included — now leads the entity-references paragraph
  9. guides/metrics-time-and-state.md: aggregate inside each CTE before
     any join — now leads the cohort pattern
  10. guides/designing-domains.md: imports can't be renamed — bolded in
     the promotion protocol
- Rule encoded in the build lane: edit-docs template Rules ("Constraint
  prominence", with the measured 75% evidence) + guide Rules clause;
  review-docs standing concern added.
- Guard: lint 63/63 after all edits; full 29-case run (20260721-105639,
  promoted skill + swept docs): **26/29, paired diff vs round 4 is 2 up /
  2 down — exactly the noise band, no regression signal.** The sweep's
  direct value is prophylactic (most promoted constraints aren't asked
  about by current dev cases); the guard proves no harm. q005's
  citation-format claim keeps flipping (~75% pass) despite the contract —
  recorded as the known residual variance case alongside the q003 tail.
- Verdict: keep. Sweep closed.
- Addendum (same day): the core-concepts auditor ran an unprompted second
  pass over the entity/reference layer and surfaced 3 more items, applied
  after verification: (11) sql-expressions.md `filter` grain-preservation
  promoted to the section's bolded lead (silent wrong-result trap — WHERE
  intuition says rows drop; they nullify); (12) sql-expressions.md
  first()/last() determinism requirement bolded in place; (13) **a real
  Format-vs-Validation contradiction in metric.md** — the Format table
  said `name` is "unique within the entity" while Validation (and the
  consolidated rule from commit 5756c23) requires domain-wide uniqueness;
  Format cell corrected to the stronger rule. Lint 63/63. Total sweep:
  13 fixes across 10 pages. The auditor also drafted 10 adversarial cases
  stress-testing the promoted constraints — parked in
  datasets/candidates-v3.md for the next dataset revision.
- Final addendum: (14) api/lynk-sql.md CTE-join rule bolded — manual ON
  required; USING('join_name')/default join work only between entities
  (a derived table has no relationship to resolve). The auditor's third
  pass also independently re-verified the applied edits as prominent and
  cleared guides+api as otherwise saturated. **Sweep final: 14 fixes,
  11 pages.** Lint 63/63.

## 2026-07-21 — round 5: dataset v3 (rotation + stress tests) + q026 docs fix

- Changes: (lane 1) dataset v2→v3: h003→q025 and h005→q026 rotated to dev;
  q027–q033 wired from candidates-v3.md (constraint stress tests + q032
  negative control + q033 near-miss refusal); fresh hold-outs h006–h010.
  41 cases = 33 dev + 8 hold-outs. (lane 3, disambiguated per case) the
  "evaluations planned" fact homed in project.md's Lifecycle — justified by
  five independent h005 failures at the same buried parenthetical.
- Score (run 20260721-122645, $14ish, 7.7m): **35/41 — dev 29/33,
  hold-outs 6/8.**
- **Headline: the sweep's lift is now measured — all 7 stress tests
  PASSED, including q032, the over-correction negative control.** The
  promoted constraints survive adversarial framing (cross-page analogy,
  half-true premise, invent-a-field, multi-hop), and composition semantics
  didn't over-generalize to "everything replaces".
- q026 (ex-h005): the docs fix worked — found "planned, not yet available"
  at Jaccard 1.00 after five rounds of misses. Residual failure was a KEY
  BUG of a new kind: a claim groundable from only one source alternative
  (project.md) while sources accepted api/lynk-sql.md alone. Claim dropped;
  rule recorded in the dataset log: every claim must be groundable from
  EVERY source alternative.
- q003: no hijack; 4/5 with only the cite-path flip (known variance).
  q005: FAILED via a NEW harness gap — the subject Read
  matan-test-lynk-project/.lynk/.../order.yml (sibling repo): the Bash
  fence doesn't cover Read/Glob absolute paths. Fix queued: materialize
  every arm (incl. a) into a temp root + permission-deny reads outside it.
- q024: view-backed-identity invention recurred (~25% rate across runs) —
  blocked on the open product question (views as identity). One sentence
  in identity-and-imports.md settles it once engineering answers.
- Hold-outs: h001 ✓ h002 ✓ h004 ✗ (flips across rounds) · fresh h006, h007,
  h009, h010 ✓, h008 ✗ (lifecycle question; scored only). Fresh-hold-out
  first showing: 4/5.

## 2026-07-21 — round 5 close: product truth, fence, and the surviving canary

- **Views-as-identity resolved by the product owner: views work.** So
  q024's two "invention" failures were CORRECT answers penalized by a
  wrong key — negative-space keys must be product-verified, not
  docs-inferred (rule added to the key discipline). Fixed in three
  layers: identity-and-imports.md now says "a warehouse table or view —
  never an inline query" (frontmatter, bullet, Format, Validation; router
  regenerated), metrics guide updated, q024 key rewritten. Rerun: PASS.
- **Read/Glob escape fence closed** (2nd harness sandbox hole, after
  round 0's Bash): every arm now materializes into a temp root (arm 'a'
  included) and the runner denies Read/Glob/Grep on /Users/** — probe
  verified (subject reports FENCED). q005 rerun: PASS.
- q026 rerun: still ~50% — this run walked metric.md → api/ →
  evolving-the-layer and missed both homes of the "planned" fact. Root
  cause is structural: NOTHING in SUMMARY.md/router surfaces
  testing/evaluations, so discovery is grep-luck. Key stays as-is
  (the claim is right); q026 is the standing canary for the
  negative-space-page gap (product-questions lane: an explicit "what
  Lynk doesn't do yet" home, added to SUMMARY).
- Round 5 end state: full run 35/41; with the verified fixes, effective
  **37/41 (dev 31/33, hold-outs 6/8)**, q026 flaky-by-structure, q003/q005
  citation flips as known variance. h004/h008 hold-out failures stand
  unread.

## 2026-07-21 — round 6: structural — the capability-boundary index

- Change (lane 3, structural): **reference/what-lynk-does-not-do.md** — the
  negative-space home. Every boundary in one page, each tagged by-design /
  planned / upstream's-job with the supported alternative + owner link.
  Wired everywhere discovery happens: SUMMARY entry, README find-your-way
  row, docs/CLAUDE.md routing line, ask-docs skill capability-boundary
  routing rule, edit-docs one-home row, lint TEMPLATE_EXEMPT (list-of-links
  by design, router precedent), router regenerated. q026/h010 sources
  gained the page as an alternative.
- Guard (run 20260721-130626, $14.27, 8.2m): **38/41 — best run to date.**
  Dev 31/33, hold-outs 7/8. Per band: orientation 2/2, first-build 4/4,
  vocabulary 5/5, judgment 5/5, CE 4/4, limits 9/10, debugging 4/5,
  mechanics 5/6.
- **q026 PASSED at optimal: SUMMARY → router → boundary index, 3 hops.**
  The class it canaried (negative space undiscoverable by structure) is
  fixed by structure, not luck. h004 and h008 also passed this run.
- Residual failures — both documented variance flips: q005 (cited the
  guide, not a schema-yml path — the ~75% citation-format flip), q025
  (dropped the always-loaded claim — the ex-h003 flip). h006 hold-out
  failed (scored only).
- Verdict: keep. Structural rounds close at: trajectory 79% → 90% → 93%,
  on a dataset that got harder each revision.

Deferred, with reasons: judge calibration vs ~30 hand-labeled claim verdicts
(needs the user's labels — highest-consensus practice, do it when possible);
cross-family judge self-preference check (no second provider wired);
relay-fidelity judge for arm D (D lost the bake-off); near-miss refusal
perturbations + separate under/over-refusal axes (dataset v3 candidate);
context-economy token frontier (answering-context tokens vs score);
router/SUMMARY ablation as a docs-quality measurement (own study).
