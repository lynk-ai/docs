---
description: Anything the agent reads can instruct it. What that means for a layer that pulls in warehouse data, documents, or tool results you do not control.
icon: shield-halved
layer: concept
deep: ../deep/trust-boundaries.md
---

# Trust boundaries in context

**Claim** — every other page here treats context as *information*. The model treats it as **instructions**. Anything that enters the window — a retrieved document, a tool result, a web page, a filename, an MCP tool's description — can direct the agent, and no amount of prompting reliably teaches it to tell your instructions from text it merely read. Curation quality and trust are orthogonal: a perfectly curated context can be perfectly hostile.

**Go deeper** — [`deep/trust-boundaries.md`](../deep/trust-boundaries.md) has the lethal trifecta and what actually contains it. Open before connecting an agent to data it does not control. Read it when designing an agent that reads anything you didn't write, choosing a defense pattern, wiring MCP servers, or auditing what could leave.

**The structural rule — the lethal trifecta** (Willison, 2025). Risk is not a property of any one capability; it appears when an agent has **all three**:

1. **Access to private data** (the point of most tools)
2. **Exposure to untrusted content** (any text an attacker could influence)
3. **A way to communicate externally** (HTTP, email, a URL it can render)

Any two are workable. All three is exploitable, and the exploit needs no code vulnerability — just text. Documented against shipped products (Microsoft 365 Copilot, GitHub's MCP server, GitLab Duo, and many more).

**Why "just add a guardrail" isn't an answer** — detection is probabilistic against an infinite space of phrasings. Willison's bar: a vendor claiming 95% detection is describing *"a failing grade"* in security terms. Filtering alone reportedly blocks only 60–70% of direct injection attempts; over 45% of RAG systems remain exploitable in benchmark testing. **Break the trifecta architecturally; don't try to out-prompt it.**

**Rules** —
- **Classify every source on entry**: trusted (you authored it, reviewed it, it's in your repo) vs. untrusted (retrieved, fetched, user-supplied, third-party tool output/descriptions). Untrusted is the default for anything you didn't write.
- **Untrusted content must not be able to trigger consequential actions.** Once it's in, constrain what can happen next — that's the shared principle behind every published defense pattern.
- **Cut one leg of the trifecta per workflow**: no private data in the same agent that reads the open web; or no external channel in the agent that reads untrusted text; or no untrusted text in the privileged one.
- **Tool definitions are untrusted content too.** Descriptions and parameter schemas are read as instructions, and can change *after* you approved them (the MCP rug-pull class).
- **The exfiltration channel is often invisible** — a rendered image URL, a markdown link, a redirect. Enumerate outbound paths, not just tools named "send".
