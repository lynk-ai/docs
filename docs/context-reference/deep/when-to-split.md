---
description: The evidence behind when to split — the five-question test with thresholds, and the retrieval research behind chunk sizing.
icon: magnifying-glass-chart
layer: deep
concept: ../concepts/when-to-split.md
---

# When to split — evidence, procedure, and over-use detection

`progressive-disclosure.md` argues *why* lazy loading pays and *how* the three rings work. This page answers the operational question it leaves open: **given one file in a system, should it be broken up — and how would I know I've broken up too much?**

## Part 1 — Why size is the wrong criterion

The available size constants are all borrowed and all medium-specific: **≤500 lines** for a SKILL.md body, **~2KB** for a session-hook note before the host truncates it, **256–512 tokens** as the common RAG chunk band (minimum ~200 for complex documents; a 2023 LlamaIndex sweep found 1024 peaked on faithfulness, a 2026 vendor benchmark put recursive-512 first at 69% accuracy — the spread is the point). None of them transfers to a file type you invented.

Worse, the strongest evidence available says structure-by-size *loses to* structure-by-meaning: a 2025 clinical-decision-support study found adaptive chunking aligned to logical topic boundaries hit **87% accuracy vs 13%** for fixed-size baselines ([MDPI Bioengineering, Nov 2025](https://www.mdpi.com/journal/bioengineering)). And McMillan's 1,650-session factorial found config-file **size (25–500 lines) had no detectable effect** on instruction compliance at all ([arXiv 2605.10039](https://arxiv.org/pdf/2605.10039)).

So: size is a *prompt to investigate*, never a verdict. The criterion is **who needs which part, when**.

## Part 2 — The split test, run against one file

**Q1. Trigger inventory — how many distinct situations open this file?**
Write down every task type that loads it. One trigger ⇒ don't split, whatever the length: a single-purpose 600-line runbook is one unit, and splitting it only adds hops. Several triggers with *different needs* ⇒ split along the trigger boundary, not the length boundary. This is the criterion; everything below is refinement.

**Q2. Per-section usage fraction.** For each section, estimate the share of the file's loads that actually consume it. The economics from `progressive-disclosure.md` are per-*part*, not per-file: a section used on fraction *f* costs its full length on every load but earns only *f* of the time. Below ~20% it should be a linked file with an explicit load trigger ("read `x.md` **if** the API returns non-200" — an untriggered reference is either never read or always read; both lose).

**Q3. Co-load test — the merge counterweight.** If every reader of part A also needs part B, they are one unit. This is imported straight from service decomposition, where "if two or more services are always used together, or communicate excessively, merge them" is standard guidance ([microservices.io](https://microservices.io/post/antipatterns/2019/05/21/antipattern-more-the-merrier.html)), and from cohesion metrics: *"a cohesive module is one where all the parts should be packaged together, because breaking them into smaller pieces would require coupling the parts together via calls between modules to achieve useful results."* High LCOM (methods sharing no state) says split; low LCOM says leave it alone.

**Q4. Sideways or deeper.** Still one concept, just long → sibling files at the same level. Several concepts readers cite *independently* → the sub-part earns its own index, a new disclosure level. The tell: *you find yourself wanting an index for it.* An index over one page is pure overhead; a pile of siblings with no index is an unnavigable shelf.

**Q5. Cascade check.** Grep every reference to this file **and to every name defined inside it**, across schemas *and* prose, before and after. Splitting silently invalidates the files that described the old shape — the most common way a well-intentioned split ships a clash.

**Deriving a bar for a file type nobody has a constant for**: run the ablation from `measuring-context.md` on the file's largest section. Accuracy unchanged ⇒ it was never earning its place; accuracy improves ⇒ it was a distractor; accuracy drops ⇒ keep it and record the number. Three sections measured gives you an empirical bar for that file type, which beats any borrowed constant.

## Part 3 — Over-splitting: the failure with two literatures behind it

**Shallow modules (Ousterhout, *A Philosophy of Software Design*).** A module is *deep* when its interface is small relative to its implementation, *shallow* when the reverse. His named antipattern is **classitis** — the belief that more, smaller units are automatically better: *"small classes don't contribute much functionality, so there have to be many of them, each with its own interface, and these accumulate to increase complexity."* Translate directly: a context file's interface is its **name + description + load trigger + index row + inbound links**. A 40-line file carries roughly as much interface as a 400-line one. Ten 40-line files therefore cost ~10× the interface for the same content — the corpus got *more* complex, not less. **Split into deep files: small routing surface, rich body.**

**Nanoservices (SOA antipattern).** The formal definition transfers with no adaptation: *"a service whose overhead (communications, maintenance) outweighs its utility"*, producing "poor performance, fragmented logic and overhead" ([DZone](https://dzone.com/articles/soa-anti-pattern-nanoservices)). A nano-page is a file whose navigation cost exceeds its content value. The prescribed cure is also the same: **start coarse, split only when a concrete problem forces it** — "start with fewer, larger services and split them only when necessary as you understand usage patterns."

**The hop tax is measured.** Every split converts an in-context read into a navigation decision, and navigation is not free:
- Agentic multi-hop retrieval runs **2–10s per query at 3–10× the token cost** of single-pass RAG; query decomposition "delivers marginal quality gains at substantial latency cost", and in multi-hop settings actually **reduced ranking precision** ([Agent-Orchestrated Adaptive RAG, arXiv 2606.05658](https://arxiv.org/html/2606.05658v1)).
- Teams that route only the queries that need multi-hop report **~70% cost reduction** vs. sending everything through it — i.e. most questions shouldn't be paying the hop tax at all.
- **Nested references cause partial reads**: Anthropic's skill guidance warns that when a reference points at another reference, the agent may preview with `head -100` instead of reading the file, "resulting in incomplete information" — hence *keep references one level deep from SKILL.md*. Depth doesn't just cost time; past one level it silently degrades into truncation.

**Each hop is an abandonment opportunity (information foraging).** Readers — human or agent — follow *information scent*: they estimate from the link label whether a destination pays, and abandon weak trails. Strong scent correlates with **~40% higher task completion**; *misleading* scent (a label promising more than the destination delivers) is singled out as the most damaging failure ([NN/g](https://www.nngroup.com/articles/information-scent/)). Splitting multiplies the number of scent judgements between the question and the answer, and each one is a chance to stop early or turn the wrong way. This is the human-factors restatement of `distinguishability.md`: more files ⇒ more sibling pairs ⇒ more chances the surfaces don't discriminate.

**Fragmentation destroys the context that made content answerable.** Anthropic's canonical example: the chunk *"The company's revenue grew by 3% over the previous quarter"* — which company, which quarter? Split cleanly, individually valid, jointly useless. This is the cost the whole splitting literature is trying to price.

## Part 4 — Three patterns that let you split without paying the fragmentation cost

| Pattern | What it does | Measured effect |
|---|---|---|
| **Contextual retrieval** (prepend situating context) | 50–100 tokens per fragment explaining where it sits in the whole | Top-20 retrieval failure **5.7% → 3.7%** (−35%); with contextual BM25 **→ 2.9%** (−49%); plus reranking **→ 1.9%** (−67%). ~$1.02 per million document tokens with caching ([Anthropic](https://www.anthropic.com/engineering/contextual-retrieval)) |
| **Parent-child / auto-merging** ("retrieve small, return large") | Match on 100–200-token children for precision; deliver the 500–1500-token parent for completeness; merge back to the parent when enough children from it hit | The standard production answer to context fragmentation — precision of a small unit, context of a large one |
| **Late chunking** | Embed the *whole* document, then derive per-chunk vectors from the full-document token embeddings | **+6.5 nDCG@10** on longer documents; **zero gain on short texts** — which is the proof: the benefit *is* the cross-fragment dependency that naive splitting destroys |

The general rule these encode: **split the addressing, not the meaning.** Make the unit of *retrieval* small and the unit of *delivery* whole.

## Part 5 — Detecting over-use in a corpus you already have

Six checks, cheapest first. Every one is computable from the files plus a read log.

| # | Check | Signal | Verdict |
|---|---|---|---|
| 1 | **Orphans** — files/definitions nothing references and no trigger reaches | never read | Delete or re-trigger. Unreachable content is worse than absent: it still occupies the index and competes in routing |
| 2 | **Co-read matrix** — pairs opened together in the same task | co-read rate > ~80% | Merge. You split a cohesive unit and are paying a hop for it every time |
| 3 | **Hop depth per question** — files opened to answer one common ask | ≥3 | Boundary is misplaced; hoist the common path into one file |
| 4 | **Interface-to-body ratio** — (name + description + trigger + index row) ÷ body tokens | > ~15% | Shallow module. Merge siblings until the ratio drops |
| 5 | **Index growth vs content growth** | index growing faster | You're adding files, not knowledge — and the discovery layer has a hard truncation cliff (`progressive-disclosure.md`) |
| 6 | **Sibling cross-references** — links between files at the same level | dense mutual linking | High coupling / low cohesion: those files are one concept wearing several names |

**Two failure signatures to name out loud:**
- **Stub sprawl** — files that exist only to point elsewhere. Legitimate exactly once, as a graduation marker for a concept that moved. Otherwise it's a hop with no payload.
- **Reassembly burden** — the reader must open 3+ files and mentally rejoin them to answer a routine question. That's the shallow-module tax made visible; it means the split ran along the wrong seam (an authoring convenience, not a usage boundary).

## Part 6 — Order of operations

1. **Start coarse.** The nanoservice literature's consensus and the strongest default: one file per trigger, split only when a measured problem forces it. Over-splitting early is harder to undo than over-consolidating, because merging requires finding every referrer.
2. **Split only on trigger heterogeneity or a measured per-section usage gap.**
3. **When you split, re-contextualise** (parent-child, or a situating line per fragment) and **fix every referrer in the same change**.
4. **Re-measure** — ablation and the co-read matrix — and merge back what the numbers say you over-cut.

## By implementation type

| Implementation | Split when | Merge when |
|---|---|---|
| RAG corpus | Sections answer different questions; chunk boundaries can align to topic boundaries | Retrieval keeps needing neighbours → parent-child or late chunking instead of finer chunks |
| Coding-agent context files | A rule applies only to one subtree → move it to that subtree's file | Two config files are read on every task → one file |
| Agent skills | Domains are mutually exclusive (`reference/finance.md` vs `reference/sales.md`) | References are one level deep already and each is <1 screen → inline them into SKILL.md |
| Long-horizon agent notes | Distinct phases with distinct re-read patterns | Every resume reads all of them → one state file |
| Semantic layer | A sub-part has several independently-queried concepts → own entity/domain | Two entities are always joined and never queried alone → one entity |
