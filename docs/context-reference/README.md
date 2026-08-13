---
description: Map of the context reference — how context behaves and how to write for it. Enter at a concept page, which is decision-ready on its own; open its deep page only on the trigger that page names.
icon: compass-drafting
---

# Context Reference

What the best context is, and how to write it — grounded in the research (Chroma, NoLiMa, RULER, Lost-in-the-Middle, the knowledge-conflicts literature, the ETH Zurich config-file study, production reports from Anthropic, Manus, Letta, Cognition) and organized for different implementation types.

## How this reference is layered (it practices what it preaches)

Two layers, progressive disclosure:

- **`concepts/`** — one page per principle: the claim, the strongest numbers, the rules. Cheap enough to load whenever the topic is near. **Routine decisions should resolve from the concept page alone.**
- **`deep/`** — the evidence and practice behind each concept page: study findings with sources, procedures, failure catalogs, and a by-implementation table. Load only when the concept page's "go deeper" trigger matches your situation.

Every concept page links its deep page and vice versa. Enter from the docs router, which lists all twenty concepts and what each answers; escalate only on the trigger the concept page names.

## Fast routes

**By symptom** — quality sags in long sessions → context-rot, then governance (compaction) · missed something that was present → position-and-ordering · wrong doc/tool/metric picked → distinguishability + selection-quality · skill won't trigger / system prompt ignored / config file bloating → authoring-standing-surfaces · file feels too big, or corpus feels fragmented → when-to-split · contradictory answers → one-concept-one-home + four-failure-modes (clash) · agent "got dumber" generally → four-failure-modes diagnostic · costs creeping → caching-economics · memory store drifting → memory-shapes + self-compiled-vs-curated · agent reads anything you didn't write, or you're wiring MCP → trust-boundaries · agent confidently misreports data from a tool → tool-output-shaping (silent truncation) · session went off the rails and won't recover → four-failure-modes (the conversation section).

**By implementation** — building a RAG chatbot, coding agent, long-horizon agent, multi-agent system, or text-to-SQL layer → [implementation-profiles](concepts/implementation-profiles.md) first; it orders the other pages for your case.

**Writing context for agents right now?** The five rules that pay most, in order: (1) admit only non-inferable content; (2) one home per fact, pointers elsewhere; (3) make sibling names/descriptions contrastive; (4) stable prefix, volatile tail, append-only; (5) measure with an ablation before and after.
