---
description: Deciding what an agent may write into the layer itself and what a person must approve first, set by how much damage a bad entry would do.
icon: user-pen
---

# Self-compiled vs. curated knowledge

**Claim** — agent-written (self-compiled) and human-authored (curated) knowledge are not rival systems; they are **the same artifact at two trust stages**. A self-compiled draft becomes curated truth by passing review — the PR shape: the agent proposes, the merge makes it truth. What varies by system is *who* holds merge rights, and that should be set by **blast radius**, not ideology.

**Why it matters — both failure directions are now measured** —
- *Ungated agent writes rot the shared layer*: memory-security surveys find write-gate validation is a shared blind spot across examined memory systems; contaminated entries persist and reinforce across sessions. Verified-memory systems (VerificAgent and successors) show human-vetted memory measurably improves task success over unvetted accumulation.
- *Unreviewed human writes rot it too*: the ETH Zurich AGENTS.md evaluation found context files tend to **reduce task success while inflating inference cost >20%**; LLM-generated context files were net-negative (recommendation: omit them), human ones help only when confined to non-inferable project facts. And a 1,650-session factorial study (McMillan) found file *structure* (size, position, even cross-file contradictions) doesn't detectably matter — **what's admitted matters; instructions then decay in use** (~5.6% lower compliance odds per generated function). Curation is a *quality bar*, not an authorship label.

**The gradient (set merge rights by blast radius)** —

| Layer | Blast radius of a wrong merge | Door |
|---|---|---|
| Session notes, working memory | One session | Agent writes freely |
| Shared operational memory | Every future session of one agent | Agent writes through a validation gate |
| Team knowledge base | Every reader, human and agent | Agent proposes; automated gate checks; human merges |
| Constitution / standards / definitions | Every decision downstream | Human-only merge, always |

**Rules** —
- Never let content skip a stage: "confident draft" is not a trust level.
- The gate can be automated wherever criteria are checkable (structure, sources, consistency); the *authority* to declare truth scales with blast radius because downstream readers stop re-checking — trust is the thing being manufactured.
- Mark provenance on every entry (who wrote, who reviewed, when) — unmarked prose all reads equally true to a model.
- Gate the write, not just the read: retrieval-time filtering of a poisoned store is strictly harder than admission control.

## Evidence & practice

### The two measured failure directions

**Direction 1: ungated agent writes contaminate.** The long-term-memory security literature converges on one blind spot: systems validate at *retrieval* time, rarely at *write* time. The [survey on long-term memory security (arXiv 2604.16548)](https://arxiv.org/html/2604.16548) reports write-gate validation and post-deletion verification as shared gaps across every system examined. Mechanisms and countermeasures now have names:

- Hallucinations "emerge across the memory lifecycle — writing, retrieval, reasoning — where incorrect knowledge persists and *reinforces* over time" ([Mem0, grounded memory](https://mem0.ai/blog/reducing-hallucinations-llms-with-grounded-memory)) — the poisoning loop, measured.
- [MemGuard (arXiv 2605.28009)](https://arxiv.org/pdf/2605.28009): admission control against memory contamination. [TRUSTMEM (arXiv 2606.25161)](https://arxiv.org/pdf/2606.25161): learned *trustworthy consolidation* — verifying intermediate memory transitions to stop omission/corruption/hallucination before they become persistent. [VerificAgent (arXiv 2506.02539)](https://arxiv.org/pdf/2506.02539): domain-specific human vetting of accumulated memory, with measured task-success gains over unvetted accumulation — direct evidence that the *review step itself* adds capability, not just safety.
- Proactive self-verification exists but is weaker: agents generating questions to test their own candidate memories catch some hallucinations — the same model grading its own homework bounds how much.

**Direction 2: unreviewed context is net-negative even when humans could have written it.** Two separate studies, often conflated in coverage (primary sources verified):

- **The ETH Zurich AGENTS.md evaluation** (real-world Python task suite): context files **tend to reduce task success while inflating inference cost by over 20%**; press coverage of the line of work adds that LLM-generated context files were net-negative (recommendation: omit them) and human-written ones help only when limited to **non-inferable** project facts ([Upsun](https://developer.upsun.com/posts/ai/agents-md-less-is-more), [Engineer's Codex](https://www.engineerscodex.com/agents-md-making-ai-worse/)).
- **McMillan's factorial study** ([arXiv 2605.10039](https://arxiv.org/pdf/2605.10039) — 1,650 Claude Code sessions, 16,050 function-level observations, marker-instruction compliance): within tested ranges, **none of the four structural variables mattered** — file size 25–500 lines, instruction position in the file, single-vs-multi-file architecture, even a *directly contradicting instruction in a second file* produced no detectable compliance change (size and conflict nulls carry affirmative Bayes support). What did matter: **compliance decays within the session** (~5.6% lower odds per additional generated function, median first omission by function 4) and **task identity** (26.2pp gap between a refactor task, 45.1%, and a greenfield task, 71.3%). With no config file at all: 0% compliance — the file is what creates the behavior; its formatting is not what erodes it.

Two lessons: (a) self-compiled content that merely restates the inferable is rot at any trust level — admission (what goes in) beats formatting (how it's arranged); (b) "a human wrote it" is not the bar — *reviewed against an admission test* is the bar, and instructions decay in use regardless, so durable rules need enforcement (`hook-vs-router.md`), not just residence in a file.

### The PR shape, generalized

| Stage | Artifact state | Who acts | What the action does |
|---|---|---|---|
| Draft | Agent's observation/derivation — a working opinion | Agent | Proposes; content is private (see `one-concept-one-home.md`'s shared/private test) |
| Checked | Same content + machine-verifiable properties confirmed | Automated gate | Verifies structure, sources marked, no conflict with existing homes, admission test (non-inferable? durable?) |
| Merged | Same words — now shared truth others rely on blindly | Merge authority | Accepts liability; manufactures the trust downstream readers spend |

The insight that dissolves the "agent-written vs. human-written" debate: **the artifact doesn't change at the merge — its trust class does.** Same file, same words; the review is the only difference, and it's the difference that matters, because downstream consumers (especially agents) do not re-verify what the shared layer tells them.

Production proof the shape ships: Letta's MemFS runs agent memory as markdown in git — every change a commit, a background *sleep-time agent* reviewing and merging session commits via worktrees ([Letta, sleep-time compute](https://www.letta.com/blog/sleep-time-compute/)). Memory writes as reviewed commits is a deployed architecture, not a metaphor.

### Setting merge rights: the blast-radius calculus

"Human must merge" is not a principle; it's the correct *setting* for one band of a dial. The dial:

- **What can an automated gate verify?** Checkable properties: structure, provenance marks, source presence, consistency with existing corpus, admission tests, even execution (docs-as-tests, schema diffs). Where criteria are executable, agent-gated merges are sound — this is Voyager's lesson (memory as verified, runnable methods; see `memory-shapes.md`).
- **What can't it?** Whether a claim is *true of the world*, whether a rule is *wise*, whether a definition matches business intent. These need an authority — and the authority requirement scales with how blindly the layer is trusted and how expensive a wrong entry is (constitution > KB > operational memory > session notes).
- **Honest statement of the residual**: routing high-blast-radius merges to humans is a liability-and-calibration argument, not proof humans catch more errors — reviewers rubber-stamp too. The gate's real function is *making the trust boundary explicit and audited*; who stands at it is a governance choice you should make deliberately (and revisit as automated verification improves).

### Practice checklist

1. **Classify each store** in your system into the four blast-radius bands; write down the door for each. "We never decided" = everything is effectively agent-merged.
2. **Admission test before style review**: is it non-inferable? durable? does it have (or need) a home already? The ETH result says most proposed context content should die here.
3. **Provenance on every entry**: author, reviewer, date, source class (observed / derived / told-by-user / imported). Unmarked prose reads equally true to a model.
4. **Gate writes, not reads**: retrieval-time trust scoring of a contaminated store is the expensive, lossy fallback; admission control is the cheap, complete version of the same idea.
5. **Diff at session end** (the archive-diff ritual, `memory-shapes.md`): "did this session *earn* a write?" makes persistence a decision instead of a side effect — the single cheapest poisoning defense.

### By implementation type

| Implementation | The self-compiled artifact | Door that fits |
|---|---|---|
| Coding agent | CLAUDE.md/AGENTS.md additions, "lessons learned" | Admission test (non-inferable only) + human merge — this file steers every future session |
| RAG KB | Agent-drafted KB articles from tickets/chats | Gate (structure+sources) + human merge; auto-drafts never publish directly |
| Long-horizon agent | Episodic → semantic memory promotion | Automated validation gate (MemGuard/TRUSTMEM-style); periodic human audit |
| Multi-agent | Shared scratchpads, registries | Worker writes are private by default; one owner promotes to shared |
| Text-to-SQL / semantic layer | Agent-proposed metric definitions | Human merge, always — a wrong metric definition is wrong in every dashboard downstream |
