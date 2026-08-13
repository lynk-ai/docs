---
description: You are writing a file that loads on every session — LYNK.md, a policy, a glossary — and need to know what earns permanent residence and what quietly taxes every request.
layer: concept
deep: ../deep/authoring-standing-surfaces.md
---

# Authoring standing surfaces (system prompts, skills, config files)

**Claim** — system prompts, skill instructions, and config files (CLAUDE.md/AGENTS.md) are one artifact class: **always-or-often-loaded instruction surfaces**. They share a failure profile — every token is paid on every load, instructions decay in use, and "helpful" content measurably hurts — so they share authoring rules.

**Why it matters** — the measured stakes: context files tend to reduce task success while inflating inference cost >20% (ETH Zurich); within-session compliance decays ~5.6% odds per generated function no matter how the file is structured (McMillan — size, position, and layout were all nulls); and Anthropic's guidance sets the bar as "the smallest possible set of high-signal tokens."

**The six rules of the class** —
1. **Right container first.** Knowledge/procedure → skill (loads on match); isolated heavy work → subagent; a must-fire guarantee → hook. Procedures in a config file and guarantees in prose are placement bugs, not writing problems.
2. **Admission before arrangement.** The default assumption is *the model is already very smart*: challenge every line with "would it get this wrong without this?" Only non-inferable content survives. Formatting a bloated surface is polishing a null variable (McMillan).
3. **Ground in real expertise.** LLM-generated instructions from general knowledge yield "vague, generic procedures" — extract from tasks that actually ran (including the corrections), runbooks, incident reports. **Gotchas are the highest-value content**: environment facts that defy assumptions. No gotchas → probably no experience in it.
4. **Altitude: the Goldilocks zone** (Anthropic). Two failure modes — brittle hardcoded if-then logic that breaks on novelty, and vague high-level guidance that assumes shared context. Aim between: specific enough to steer, heuristic enough to generalize. Moderate detail, not exhaustive — instructions that don't apply *misfire*, they don't sit idle.
5. **Route on the surface, act on the body.** Name + description are the trigger interface (chosen among 100+ — third person, what it does *and when to use it*, key terms). **Tune the description like a classifier**: ~20 labeled queries with near-miss negatives, train/validation split, pick the wording on validation. Body under ~500 lines; depth in files **one level deep**, each reference carrying an explicit load trigger ("read X *if* Y").
6. **Match freedom to fragility.** High freedom (heuristics) where many paths work; medium (pseudocode/templates) where a pattern is preferred; low (exact scripts, "do not modify") where operations are fragile. Scripts beat instructions for anything deterministic — execution costs output tokens only.

**The decay corollary** — a standing rule is *not enforced by residence*. Rules that must hold at step 20 need re-anchoring (recitation near the task) or a gate in the path (`hook-vs-router.md`).

**Go deeper** (`../deep/authoring-standing-surfaces.md`) when: writing or pruning a system prompt, SKILL.md, or CLAUDE.md; a skill won't trigger (or triggers wrongly); deciding instructions vs. scripts.

## Related

- [Deep: the evidence behind this page](../deep/authoring-standing-surfaces.md) — open it on the trigger named above.
