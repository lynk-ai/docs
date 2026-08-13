---
description: The evidence behind authoring standing surfaces — the six rules for always-loaded files, with the studies behind each.
layer: deep
concept: ../concepts/authoring-standing-surfaces.md
---

# Authoring standing surfaces — evidence & practice

One artifact class, three members: **system prompts** (always loaded), **skills** (metadata always, body on trigger), **config files** (loaded per session). All are instruction surfaces the model consults rather than data it processes — and the evidence for how to write them is now substantial. Primary sources: [Anthropic, effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents); [Anthropic, skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices); [Agent Skills engineering post](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills); McMillan ([arXiv 2605.10039](https://arxiv.org/pdf/2605.10039)); the ETH Zurich AGENTS.md evaluation.

## What the evidence says about the whole class

| Finding | Consequence for authoring |
|---|---|
| Context files tend to reduce success + inflate cost >20% (ETH Zurich) | The burden of proof is on *inclusion*, not exclusion |
| File size 25–500 lines, instruction position, architecture, cross-file conflict: all nulls (McMillan, affirmative Bayes support for size/conflict) | Stop optimizing arrangement; optimize admission |
| Compliance decays ~5.6% odds per generated function; median first omission by function 4 (McMillan) | Standing rules are a *floor*, not enforcement — pair with recitation or gates |
| No config file → 0% compliance; with → 67.7% (McMillan) | The surface absolutely works — for behaviors the model can't infer; the question is only what earns a line |
| Task identity swamps file structure (26.2pp between tasks) | Test your surface against your *hardest* task types, not an average |

## System prompts: the altitude calibration

Anthropic's verified framing — system prompts fail at two altitudes:

- **Too low (hardcoded)**: brittle if-then logic enumerating cases. Breaks on the first novel input; maintenance grows unboundedly; and long rule lists age into the attention dead-zone (`position-and-ordering.md`).
- **Too high (vague)**: "be helpful and accurate" — assumes shared context the model doesn't have; provides no decision procedure.
- **The Goldilocks zone**: "specific enough to guide behavior effectively, yet flexible enough to provide strong heuristics." Give the *decision rule*, not the case table: "prefer the older API when the user's runtime is unknown" beats forty runtime-specific branches.

Structure guidance (same source): organize into distinct sections (background, instructions, tool guidance, output description) with headers/XML tags; start minimal, test on the hardest tasks, add only against observed failures — the additive direction, never write-big-then-prune, because every speculative line is a measured liability (ETH).

## Skills: the routing surface and the body

A skill is progressive disclosure productized (three levels: metadata always → SKILL.md on trigger → bundled files on demand; "the amount of context that can be bundled is effectively unbounded" since scripts execute without loading). The authoring rules, from the primary doc:

**Ground it in real expertise — the #1 authoring pitfall.** Asking an LLM to generate a skill from general training knowledge yields "vague, generic procedures ('handle errors appropriately')" — weight without lift. Effective skills are *extracted*, not generated: from a hands-on task that worked (including the corrections made along the way), or synthesized from real artifacts — runbooks, incident reports, review comments, VCS history, actual failure cases. Corollary: **gotchas sections are the highest-value content** in many skills — environment facts that defy assumptions ("re-running is safe, reports `already exists`"; "the thread cap is not a quota") are precisely what no model can infer. If your skill has no gotchas, ask whether it contains any experience at all.

**The description is the routing interface** — the skill is selected from name+description alone, potentially among 100+ skills:
- **Third person, always** ("Processes Excel files…") — the description is injected into the system prompt; inconsistent POV measurably harms discovery.
- **What it does AND when to use it**, with the key terms an asker would use: `Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.` Limits: name ≤64 chars (lowercase-hyphen), description ≤1,024 chars. Err *pushy* — "even if they don't explicitly mention 'CSV'" — implicit asks are the common miss.
- This is `distinguishability.md` applied: among sibling skills, descriptions must partition the trigger space contrastively.
- **Tune it like a classifier, not like prose.** The method: ~20 labeled queries — 8–10 that *should* trigger (varying phrasing and explicitness) and 8–10 that should *not*, where the valuable negatives are **near-misses sharing keywords**. Split 60/40 train/validation; run each train query cold ×3; iterate the description on train failures (~5 rounds suffices); **pick the winning wording by validation pass rate, never train** — choosing on train is memorizing your own test phrasings. Symmetric failure fixes: misses implicit asks → add user-intent keywords; fires on near-misses → sharpen the "when NOT" clause.

**Body discipline**:
- **≤500 lines** for optimal performance; split beyond that — and when moving overflow to `references/`, attach **explicit load triggers**: "Read references/api-errors.md *if the API returns non-200*" beats "see references/" (an untriggered reference is either never read or always read; both lose).
- **Moderate detail, not exhaustive** — a different rule than concision: over-comprehensive skills actively hurt because the agent "pursues unproductive paths triggered by instructions that don't apply." Every instruction is a live wire; unused ones don't sit idle, they misfire.
- **Scope like a function**: too narrow → multiple skills co-load and conflict; too broad → hard to activate precisely. One coherent capability per skill.
- **References one level deep** from SKILL.md — nested reference chains cause partial reads (`head -100` previews) and silently incomplete information.
- **TOC on any reference file >100 lines** — so partial reads still see the full scope.
- Split by domain so mutually-exclusive contexts never co-load (the BigQuery pattern: `reference/finance.md`, `reference/sales.md` — a sales question loads zero finance tokens).
- Concision test per line: "does this paragraph justify its token cost?" — assume the model knows what a PDF is.

**Degrees of freedom** — match specificity to fragility (the narrow-bridge/open-field analogy):
| Freedom | Form | When |
|---|---|---|
| High | Heuristic checklists | Many valid paths; context decides (code review) |
| Medium | Templates/pseudocode with parameters | Preferred pattern, variation OK (report generation) |
| Low | Exact script, "do not modify" | Fragile, sequence-critical (migrations) |

**Scripts beat prose where operations are deterministic**: pre-made utilities are more reliable than generated code, cost zero context (only output returns), and enforce consistency. Make execution intent explicit ("Run X" vs. "See X for the algorithm"). Handle errors *in the script* — don't defer failures to the model; no unexplained constants (if you can't justify the timeout value, the model can't either). For high-stakes batch work, use plan→validate→execute with a machine-checkable intermediate file.

**Known patterns with teeth**: workflow checklists the agent copies and ticks (prevents skipped validation steps); validator feedback loops (run validator → fix → repeat); example input/output pairs over descriptions; conditional workflows ("creating? → A; editing? → B"); no time-sensitive content (use a collapsed "old patterns" section); one term per concept throughout ("field", not field/box/element rotating).

**Evaluation-driven authoring** (the doc's strongest advice, and pure `measuring-context.md`): build ≥3 evaluations *before* writing extensive content — baseline the model without the skill, write the minimum that closes observed gaps, iterate against real trajectories. Watch how the agent actually navigates: files it never reads are dead weight; files it always reads belong in SKILL.md; unexpected read orders mean the structure isn't as intuitive as you thought. The two-instance loop: author with one Claude, test on a fresh one, feed observed failures back — refine from behavior, not assumption.

## Before authoring: is this even the right container?

The same capability can live in a skill, a subagent, or a hook — and the placement decides both how it fires and how far it travels across hosts (the portability ladder):

| Need | Container | Portability |
|---|---|---|
| Knowledge & procedure | **Skill** | Ports everything — copy the folder, write once |
| Heavy isolated work behind a brief | **Subagent** | Content ports; wrapper re-serialized per host |
| A guaranteed lifecycle intervention that must fire itself, fail-closed | **Hook** | Only event *names* port — expect to rewrite per host |

Two placement bugs this table catches: *procedures stuffed into config files* (they belong in a skill, where they load on match instead of always — the whole standing-surface cost problem disappears), and *guarantees stated as instructions* (a "must always" that lives in prose is a hook-shaped need implemented as a hope — `hook-vs-router.md`). Same logic as the disclosure layering stack (`progressive-disclosure.md`): each knowledge type has a surface built for it; the wrong surface pays the wrong price.

## Config files (CLAUDE.md / AGENTS.md): the admission-only surface

Everything above applies, minus the routing layer (config files load unconditionally — which is exactly why they're the most dangerous member of the class):

1. **Non-inferable only.** The repo is self-describing; the file earns lines only for what exploration can't recover: invisible conventions ("always exclude test accounts"), cross-repo decisions, prohibitions with invisible reasons. The ETH result is the measured cost of ignoring this.
2. **Don't reorganize — cut.** Size/position/architecture nulls (McMillan) mean the improvement path for a misbehaving config file is deletion and enforcement, not restructuring.
3. **Durable rules get machinery.** The 5.6%/function decay means "always run the linter" belongs in a hook, not (only) in prose; `hook-vs-router.md` has the ladder (prompt ask < hook < in-path gate).
4. **Agent-drafted lines pass the same review as agent-drafted memory** — "capture your learnings into the config" is a memory write with session-steering blast radius (`self-compiled-vs-curated.md`).

## The class-level checklist

Before shipping any standing surface:
- [ ] Every line passes "would the model get this wrong without it?"
- [ ] Altitude: decision rules, not case tables; heuristics, not vibes
- [ ] Trigger surface (name/description) written third-person, contrastive with siblings, containing the asker's words
- [ ] Body ≤500 lines; depth in files one level deep, TOCs on long ones
- [ ] Deterministic work in scripts with explicit execution intent
- [ ] Rules that must survive step 20 have recitation or a gate behind them
- [ ] ≥3 evals existed before the content did; ablation re-run after every addition (`measuring-context.md`)
- [ ] No timestamps/volatile content (cache churn — `caching-economics.md`)

## By implementation type

| Implementation | The standing surface that matters most | Its top rule |
|---|---|---|
| RAG chatbot | System prompt (grounding + refusal policy) | Altitude: decision rules for "answer vs. abstain vs. escalate" |
| Coding agent | CLAUDE.md/AGENTS.md | Non-inferable only; enforcement in hooks, not prose |
| Long-horizon agent | System prompt + recited plan | Recitation beats residence for rules that must survive |
| Multi-agent | Sub-agent briefs (a per-spawn standing surface) | The four-part formula: objective, output format, tool guidance, boundaries |
| Text-to-SQL | The semantic layer's descriptions (the model's "system prompt" about the data) | Contrastive metric descriptions; the layer is a standing surface too |
