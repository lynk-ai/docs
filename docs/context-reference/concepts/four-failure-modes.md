---
description: The agent got worse and you need to name which kind of broken — poisoned, distracted, confused, or holding two facts that disagree. Each has a different fix and the symptoms look identical.
icon: triangle-exclamation
layer: concept
deep: ../deep/four-failure-modes.md
---

# The four failure modes

**Claim** — context breaks agents in four distinguishable ways (Drew Breunig's taxonomy, 2025): **poisoning**, **distraction**, **confusion**, **clash**. They present as the same symptom — "the agent got dumb" — but each has a different mechanism and a different fix. Diagnosing the wrong mode means applying the wrong fix.

**Go deeper** — [`deep/four-failure-modes.md`](../deep/four-failure-modes.md) has measured onsets for each mode and how to tell them apart from a transcript. Read it when an agent is misbehaving and you need the diagnostic procedure, the fix menu with evidence, or the knowledge-conflict handling patterns.

**The four** —

| Mode | Mechanism | Canonical fix |
|---|---|---|
| **Poisoning** | An error/hallucination enters context and gets *repeatedly referenced* as truth | Quarantine + validate before anything persists; make history auditable |
| **Distraction** | Context grows so long the model over-attends to accumulated history instead of reasoning from training | Compact/summarize; reset at task boundaries |
| **Confusion** | Superfluous (not wrong) content — extra docs, unused tools — degrades the answer | Curate harder; RAG over tool/doc loadout; prune near-misses |
| **Clash** | Two pieces of in-context information contradict; the model silently picks one | Detect, then **escalate** — resolution needs an authority, not a coin-flip |

**Three honest edges of the taxonomy** —
- The modes *overlap in practice*: distraction and confusion co-occur; poisoning is clash with a time delay (the wrong fact eventually meets the right one). Use it as a diagnostic checklist, not a partition.
- Three modes have mechanical fixes; **clash alone requires an authority decision** — an agent can notice a contradiction but has no standing to resolve one. Knowledge-conflict research backs the seriousness: ~70% of enterprise KBs contain directly contradictory article pairs (Gartner, via Fini Labs).
- Diagnose by *what changed*: wrong fact repeating → poisoning; quality falling with length → distraction; quality falling with breadth → confusion; inconsistent answers to the same question → clash.
