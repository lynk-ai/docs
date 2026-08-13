---
description: Map of the context reference — how context behaves and how to write for it. Enter at a concept page, which is decision-ready on its own; open its deep page only on the trigger that page names.
---

# Context Reference

What the best context is, and how to write it — grounded in the research (Chroma, NoLiMa, RULER, Lost-in-the-Middle, the knowledge-conflicts literature, the ETH Zurich config-file study, production reports from Anthropic, Manus, Letta, Cognition) and organized for different implementation types.

## How this reference is layered (it practices what it preaches)

Two layers, progressive disclosure:

- **`concepts/`** — one card per principle: the claim, the strongest numbers, the rules. Cheap enough to load whenever the topic is near. **Routine decisions should resolve from the card alone.**
- **`deep/`** — the evidence and practice behind each card: study findings with sources, procedures, failure catalogs, and a by-implementation table. Load only when the card's "go deeper" trigger matches your situation.

Every card links its deep page and vice versa. Start from the map below, open the concept, escalate only on the card's trigger.

## The map

### The problem
| Concept | One line | Open the deep page when |
|---|---|---|
| [context-rot](concepts/context-rot.md) | Quality degrades as tokens grow — even relevant ones — starting far below the window limit | Sizing a real context budget; need the study numbers |
| [four-failure-modes](concepts/four-failure-modes.md) | Poisoning / distraction / confusion / clash — same symptom, four fixes (Breunig) | An agent is misbehaving and you need the diagnostic + fix menu |

### The levers
| Concept | One line | Open the deep page when |
|---|---|---|
| [four-operations](concepts/four-operations.md) | WRITE / SELECT / COMPRESS / ISOLATE — plus ORDER and CACHE, which the taxonomy misses | Designing an agent's context flow end-to-end |
| [selection-quality](concepts/selection-quality.md) | How SELECT breaks: near-misses beat junk as poison; recall→rerank→prune wins | Building or tuning any retrieval pipeline |
| [position-and-ordering](concepts/position-and-ordering.md) | Context is a sequence: U-curve attention, edges strong, middle dead | Laying out a prompt; "it was in context and it missed it" |
| [caching-economics](concepts/caching-economics.md) | Cached tokens cost ~10%; churn, not size, drives the bill — but cheap ≠ attention-free | Designing the message layout; cost/latency spikes |
| [tool-output-shaping](concepts/tool-output-shaping.md) | Tool results are the biggest token source in an agent loop; silent truncation makes agents lie | Designing a tool's return contract; agent misreports data; trimming the loop's bill |
| [progressive-disclosure](concepts/progressive-disclosure.md) | Pointers always, bodies on demand — cost scales with use, not existence | Structuring a corpus/skill/tool surface |
| [when-to-split](concepts/when-to-split.md) | Split on trigger heterogeneity, not size — and merge back the shallow fragments over-splitting creates | Judging one file; auditing a corpus that feels fragmented |
| [authoring-standing-surfaces](concepts/authoring-standing-surfaces.md) | System prompts, skills, config files are one artifact class: admission before arrangement, Goldilocks altitude, freedom matched to fragility | Writing/pruning a system prompt, SKILL.md, or CLAUDE.md; a skill won't trigger |

### The rules of truth
| Concept | One line | Open the deep page when |
|---|---|---|
| [one-concept-one-home](concepts/one-concept-one-home.md) | One authoritative home per fact; duplicate routes, tether summaries, never fork bodies | Structuring a KB; a contradiction surfaced; handling mirrors |
| [distinguishability](concepts/distinguishability.md) | Coexisting siblings must differ in BOTH name and description — choosers read nothing else | Naming tools/metrics/pages; wrong-item selection |
| [living-sources](concepts/living-sources.md) | Sources split when blurred, merge when duplicated — and nothing forces it (no compiler) | A doc feels overgrown; two docs overlap; planning maintenance |
| [self-compiled-vs-curated](concepts/self-compiled-vs-curated.md) | Agent-written and human-written are one artifact at two trust stages; merge rights scale with blast radius | Designing memory write paths; review policy; context files |
| [trust-boundaries](concepts/trust-boundaries.md) | The model reads context as *instructions*: private data + untrusted content + an outbound channel = exploitable by text alone | Any agent that reads something you didn't write; MCP wiring; audit what can leave |

### The guards
| Concept | One line | Open the deep page when |
|---|---|---|
| [hook-vs-router](concepts/hook-vs-router.md) | Hooks fail open and silent; routers fail closed — ask "is silence a bug?" | Placing validation/gates in a pipeline |
| [context-governance](concepts/context-governance.md) | Clean context is a control loop: instruments → policies → owners → interventions | Standing up maintenance; choosing compaction policy |
| [memory-shapes](concepts/memory-shapes.md) | A write is a decision: earn, judge, restructure, verify — the write-gate is the design | Designing/fixing an agent memory architecture |
| [measuring-context](concepts/measuring-context.md) | Every claim here is measurable in your system: effective length, ablation, canaries | Building the eval harness; arguing a change with numbers |

### The dispatch
| Concept | One line | Open the deep page when |
|---|---|---|
| [implementation-profiles](concepts/implementation-profiles.md) | Best context is implementation-relative: five profiles, each with a priority order | Starting or auditing a system; deciding what to fix first |

## Fast routes

**By symptom** — quality sags in long sessions → context-rot, then governance (compaction) · missed something that was present → position-and-ordering · wrong doc/tool/metric picked → distinguishability + selection-quality · skill won't trigger / system prompt ignored / config file bloating → authoring-standing-surfaces · file feels too big, or corpus feels fragmented → when-to-split · contradictory answers → one-concept-one-home + four-failure-modes (clash) · agent "got dumber" generally → four-failure-modes diagnostic · costs creeping → caching-economics · memory store drifting → memory-shapes + self-compiled-vs-curated · agent reads anything you didn't write, or you're wiring MCP → trust-boundaries · agent confidently misreports data from a tool → tool-output-shaping (silent truncation) · session went off the rails and won't recover → four-failure-modes (the conversation section).

**By implementation** — building a RAG chatbot, coding agent, long-horizon agent, multi-agent system, or text-to-SQL layer → [implementation-profiles](concepts/implementation-profiles.md) first; it orders the other pages for your case.

**Writing context for agents right now?** The five rules that pay most, in order: (1) admit only non-inferable content; (2) one home per fact, pointers elsewhere; (3) make sibling names/descriptions contrastive; (4) stable prefix, volatile tail, append-only; (5) measure with an ablation before and after.
