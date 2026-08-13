---
description: Whether a rule should be a passive instruction or something every path must pass through. Explains why an instruction like “always check X” silently never fires.
layer: concept
deep: ../deep/hook-vs-router.md
---

# Hook vs. router

**Claim** — there are two ways to make something happen automatically, split by one question: *what happens when it doesn't fire?* A **hook** is an event listener — pattern-matched, nobody invokes it, and when nothing matches, nothing happens and nothing tells you (**fails open, silently**). A **router** stands *in* the control flow — everything passes through it, it decides, and it can refuse (**fails closed, loudly**). Most context-governance bugs are a hook doing a router's job.

**Why it matters** — the guardrail literature found the same law independently: most production guardrails default to passing requests through when their infrastructure is down — "a guardrail that fails open isn't actually a guardrail under adverse conditions." And prompt-level instructions ("you MUST check X") are hooks in disguise: nothing notices when the model ignores them. Deterministic gates in the tool-call path recover policy-violation failures that reflection-style (ask-the-model-to-check) approaches silently miss.

**The design rule** —

| | Hook | Router |
|---|---|---|
| Trigger | Implicit, pattern-matched | Explicit; in-line, unavoidable |
| On no-match / failure | Skips silently | Halts / blocks / escalates |
| Cost | Cheap, fires everywhere | Costlier, one chokepoint |
| Right job | Raising the floor: defaults, annotations, telemetry | Guarding a door: any transition where a silent skip is a bug |

Ask of every automated check: *if this silently didn't run, would that be a bug?* Yes → it must be a router (in-line, fail-closed). No → hook is the cheap right answer.

**The multiplier — hooks feed the router**: hooks observe and annotate cheaply on every step (provenance stamps, metrics, flags); by the time work reaches the gate, the router rules on evidence the hooks already collected. Layers, not rivals.

**Corollary for multi-agent** — a router at the *final* output only is a hole: a sub-agent's damage happens regardless of whether the orchestrator's answer gets checked. Gates belong at each boundary where trust changes hands.

**Go deeper** (`../deep/hook-vs-router.md`) when: placing validation in an agent pipeline, designing gates/guardrails, or auditing which of your checks can silently not-fire.

## Related

- [Deep: the evidence behind this page](../deep/hook-vs-router.md) — open it on the trigger named above.
