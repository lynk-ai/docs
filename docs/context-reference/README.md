---
description: Map of the context reference — how context behaves and how to write for it. One page per principle; the decision-ready summary sits on top, the evidence and procedures below it.
icon: compass-drafting
---

# Context Reference

What the best context is, and how to write it — grounded in the research (Chroma, NoLiMa, RULER, Lost-in-the-Middle, the knowledge-conflicts literature, the ETH Zurich config-file study, production reports from Anthropic, Manus, Letta, Cognition) and organized for different implementation types.

**How to read a page**: every page opens with the claim, the strongest numbers, and the rules — routine decisions resolve from that summary alone. The `## Evidence & practice` section below it holds the study findings with sources, procedures, and failure catalogs; keep reading only when you need the numbers, the provenance, or the step-by-step.

## The map

**Foundations — why context degrades and what to call it**

- [context-rot.md](context-rot.md) — how much a model actually holds before answers get worse. All 18 tested models degrade with length; effective context is a fraction of the marketed window (GPT-4.1: 16K effective vs 1M claimed). Treat the window as an attention budget, not storage.
- [four-failure-modes.md](four-failure-modes.md) — the agent got worse: name which broken. Poisoning, distraction, confusion, clash — symptoms look identical, fixes differ; misdiagnosis applies the wrong one.
- [four-operations.md](four-operations.md) — the levers: WRITE, SELECT, COMPRESS, ISOLATE — plus the two the taxonomy misses (exclude at the source; fix the content itself).
- [measuring-context.md](measuring-context.md) — prove a change helped. Ablation before/after is the instrument; a degradation claim without one is a vibe.

**Getting the right things picked**

- [selection-quality.md](selection-quality.md) — the agent retrieved something plausible-but-wrong. Near-misses damage more than junk; rerank and prune before generation.
- [distinguishability.md](distinguishability.md) — the wrong sibling keeps getting chosen. Name + one-line description are all a chooser reads; siblings must differ in exactly those.
- [position-and-ordering.md](position-and-ordering.md) — where the load-bearing content goes. Attention is U-shaped: edges strong, middle weak — content buried mid-file can score worse than absent.
- [tool-output-shaping.md](tool-output-shaping.md) — a tool returns too much, or truncates silently and the agent reports partial as complete. Shape and mark what comes back.

**Structuring a corpus that stays healthy**

- [progressive-disclosure.md](progressive-disclosure.md) — what loads always vs on demand. Cost must scale with what's used, not what exists; a pointer index up front, bodies fetched when the task demands.
- [when-to-split.md](when-to-split.md) — should this file become two? Split on trigger heterogeneity — different tasks needing different parts — never on size alone; a section used by <~20% of loads gets linked out.
- [one-concept-one-home.md](one-concept-one-home.md) — the same fact stated twice is a defect, not redundancy. Copies drift, then disagree, and the agent silently picks one. One authoritative home, pointers elsewhere.
- [living-sources.md](living-sources.md) — files blur as they grow and drift as they age, and no build check will say so. The signals that say split, and the ones that say merge back.
- [authoring-standing-surfaces.md](authoring-standing-surfaces.md) — writing a file that loads every session (LYNK.md, a policy, a glossary). Only non-inferable content earns permanent residence; every token there taxes every question.
- [hook-vs-router.md](hook-vs-router.md) — should a rule be an instruction or a chokepoint? Passive "always check X" instructions silently fail to fire; what must always happen needs a gate on the path.

**Costs, memory, and safety**

- [caching-economics.md](caching-economics.md) — why a lean layer can still be expensive. Cached tokens cost ~10× less than fresh; churn drives the bill, so keep the prefix stable and append.
- [context-governance.md](context-governance.md) — nothing cleans itself up. A signal, a policy, and a named owner per surface, or the layer drifts until someone notices in production.
- [memory-shapes.md](memory-shapes.md) — what an agent may write down, and when. Append-only memory reliably rots; the write-time gate is the design.
- [self-compiled-vs-curated.md](self-compiled-vs-curated.md) — what the agent may write into the layer itself vs what a person must approve, set by the blast radius of a bad entry.
- [trust-boundaries.md](trust-boundaries.md) — anything the agent reads can instruct it. What that means when the layer pulls in warehouse data, documents, or tool results you don't control.

**Applying it to your system**

- [implementation-profiles.md](implementation-profiles.md) — which rule matters most for a RAG chatbot, coding agent, long-horizon agent, multi-agent system, or text-to-SQL layer. Read first when tuning a specific workload; it orders the other pages for your case.

## Fast routes

**By symptom** — quality sags in long sessions → context-rot, then context-governance (compaction) · missed something that was present → position-and-ordering · wrong doc/tool/metric picked → distinguishability + selection-quality · skill won't trigger / system prompt ignored / config file bloating → authoring-standing-surfaces · file feels too big, or corpus feels fragmented → when-to-split · contradictory answers → one-concept-one-home + four-failure-modes (clash) · agent "got dumber" generally → four-failure-modes diagnostic · costs creeping → caching-economics · memory store drifting → memory-shapes + self-compiled-vs-curated · agent reads anything you didn't write, or you're wiring MCP → trust-boundaries · agent confidently misreports data from a tool → tool-output-shaping (silent truncation) · session went off the rails and won't recover → four-failure-modes (the conversation section).

**Writing context for agents right now?** The five rules that pay most, in order: (1) admit only non-inferable content; (2) one home per fact, pointers elsewhere; (3) make sibling names/descriptions contrastive; (4) stable prefix, volatile tail, append-only; (5) measure with an ablation before and after.
