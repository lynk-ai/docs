---
description: Whether a rule should be a passive instruction or something every path must pass through. Explains why an instruction like “always check X” silently never fires.
icon: route
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

## Evidence & practice

### The distinction, grounded

Mental models: git hook / DB trigger / event listener (hook) vs. API gateway / switch-with-no-default-case (router). The load-bearing property is not *when* they run but *what silence means*: a hook that didn't match produces the same observable as a hook that worked — nothing. A router that didn't approve produces a block. Every check in a pipeline is one or the other, whether you chose or not — and the default, absent design, is hook.

### Evidence from the guardrail literature

- **Fail-open is the industry default and it's wrong at doors**: production guardrail implementations mostly pass traffic when the guardrail infrastructure errors or times out, prioritizing availability — "a guardrail that fails open isn't actually a guardrail under adverse conditions" ([Genta, LLM guardrails in production](https://genta.dev/resources/llm-guardrails-production-guide)). Availability-vs-safety is a *per-door* decision: fail-open is fine for a tone-checker, a bug for a data-exfiltration gate.
- **Deterministic gates beat reflection at the chokepoint**: ["Reason Less, Verify More" (arXiv 2607.07405)](https://arxiv.org/pdf/2607.07405) — deterministic predicates over proposed tool calls (cheap, reproducible, auditable) recover a *silent policy-violation* failure mode that reflection/output-review approaches miss. Asking the model to check itself is a hook on its own attention; a predicate in the call path is a router.
- **Prompt instructions are hooks**: "you MUST check the library before answering" injected at session start relies on the model attending to it every time — and nothing fires when it doesn't. Framework-level interceptors that run *before the model sees a tool result* enforce at the architecture level, "rather than through prompts alone" ([AWS, rules LLMs cannot bypass](https://dev.to/aws/ai-agent-guardrails-rules-that-llms-cannot-bypass-596d)). The reliability ladder: prompt ask < hook < in-path gate.
- **Boundary coverage in multi-agent systems**: an orchestrator that only checks the final response misses sub-agent damage — "if a sub-agent is manipulated to take a harmful action and only the orchestrator's final response is checked, the damage happens regardless" ([Arthur, agent guardrails](https://www.arthur.ai/blog/best-practices-for-building-agents-guardrails)). Gates go where trust changes hands: user→agent, agent→sub-agent, sub-agent→shared memory, agent→external action.
- **Layered architecture** as consensus: input validation (pre-model) + output filtering (post-model) + architectural containment (capability limits) — three layers, each fail-closed at its own severity ([Kalvium](https://www.kalviumlabs.ai/blog/guardrails-for-llm-applications/)).

### Placement calculus

For each check, three questions:

1. **Is silence a bug?** The gate question. Provenance stamping: no (hook). Admission of an agent-written fact to shared memory: yes (router — see `self-compiled-vs-curated.md`).
2. **Can the predicate be deterministic?** Deterministic predicates (schema valid? source marked? path allowed? size under budget?) are cheap enough to run in-line — no excuse for hook placement. Judgment calls (is this claim true?) need an LLM or a human — put the *dispatch* to them in-line (router), even if the judgment is async.
3. **What's the failure posture?** Router down → block and surface (fail-closed) for doors; hook down → proceed (fail-open) for floors. Write the posture down per check; the un-decided ones are all fail-open in practice.

### Hooks feed the router (the composition pattern)

The two shapes multiply when layered:

- **Hooks (every step, cheap)**: stamp provenance, count tokens, tag epistemic class, log tool-call shapes, annotate which sources were consulted.
- **Router (one chokepoint, decisive)**: at the transition that matters — publish, merge, execute, escalate — rule on the accumulated annotations. The gate doesn't re-derive evidence; it *audits* what the hooks collected.

This division keeps the expensive fail-closed check narrow (one door) while the observation surface stays wide (every step) — the floor rises for free; the door stays cheap enough to actually enforce.

Concrete instance: session-start hooks inject "check the library" (floor: helps when heeded, costs nothing when not); a fail-closed gate at *publish* time refuses unverified pages (door: cannot be skipped silently). The complementary failure to watch for: a system whose *read* path has a router but whose *write* path has only hooks — writes are where poisoning enters (`four-failure-modes.md`).

### Failure catalog

- **The pious prompt**: policy stated in the system prompt, enforced nowhere. Works in demos; decays with *use* — measured: compliance with a config-file instruction drops ~5.6% in odds per additional function the agent generates in a session, median first omission by function 4 (McMillan, [arXiv 2605.10039](https://arxiv.org/pdf/2605.10039)). An instruction that must hold at step 20 needs a hook that re-injects it or a router that checks it — residence in the prompt is not enforcement.
- **The optional gate**: a review step agents are "supposed to" invoke. An explicit call that callers can skip is a hook with extra steps.
- **The fail-open door**: validation service times out → request sails through. Under load — exactly when quality drops — the guardrail evaporates.
- **The terminal-only gate**: one router at final output; sub-agent boundaries unguarded.
- **The silent skip you already have**: audit your pipeline for checks whose non-execution is unobservable; each one is a hook standing where you believed a router stood.

### By implementation type

| Implementation | Floor (hooks) | Door (router, fail-closed) |
|---|---|---|
| RAG chatbot | Log retrieval sets, stamp chunk provenance | Grounding check before answer ships (citations resolve?) |
| Coding agent | Lint/annotate on file events | Tests+review before merge; permission gate on destructive tools |
| Long-horizon agent | Telemetry on context size, drift flags | Compaction checkpoint approval; memory-write admission gate |
| Multi-agent | Per-step trace annotations | Gate at each trust boundary; one decision-owner per merge |
| Text-to-SQL | Query logging, schema-touch tags | Validation against the semantic layer before execution on the warehouse |
