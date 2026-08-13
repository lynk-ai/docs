---
description: A tool returns far more than the agent needs, or truncates silently and the agent reports a partial result as complete. How to shape what comes back.
layer: concept
deep: ../deep/tool-output-shaping.md
---

# Tool output shaping

**Claim** — in an agent loop, **tool results are the largest single source of tokens** — larger than the system prompt, the docs, and the user's words combined (Manus reports ~100:1 input:output over ~50 tool calls per task). Yet almost all context engineering effort goes into what you *send* a tool and none into what it *returns*. The return surface is a design artifact, and it's usually the cheapest large win available.

**The one bug that matters most: silent truncation.** Harnesses cap tool output (2,000 lines / 50KB / 8KB are common defaults). When the cap hits without a marker, the agent reasons over a partial result **believing it is complete** — and confidently reports a wrong answer. It never tells you it happened. Every truncation must be visible: `[truncated — showing 8,200 of 41,000 chars]`, `[…270 items omitted]`.

**The four shapes for a large result** —

| Shape | Return | Use when |
|---|---|---|
| **Full** | Everything | It's small, and all of it is load-bearing |
| **Truncated + marker** | Head/tail + explicit omission notice | Peeking is enough; the agent can decide to fetch more |
| **Paginated** | A page + a `next_page` cursor, plus a tool that takes it | The agent should traverse *deliberately* rather than be dumped on |
| **Handle** | An identifier/path, not the payload — "wrote 12,431 rows to `results.csv`" | Big, and the next step is a program, not reading |

**Rules** —
- **Never truncate silently.** A visible marker converts a wrong answer into a decision.
- **Return a handle, not a payload,** whenever the content will be processed rather than reasoned over — this is the read-vs-execute rule (`progressive-disclosure.md`) applied to returns: the cheapest tokens are the ones that never enter the window.
- **Errors are context too.** `"413 Payload Too Large"` yields a confused retry; `"Result too large (41k rows). Use cursor= or narrow with filter="` yields a correct next move. Every error should carry the recovery action.
- **Keep failures in the transcript.** Manus's finding: leaving failed actions and error traces in context lets the model update its beliefs and stop repeating the mistake — deleting them removes the learning signal.
- **Shape once, at the boundary.** Intercept results before they enter context (a post-tool hook) rather than hoping each tool behaves — floor-raising work belongs in a hook (`hook-vs-router.md`).

**Go deeper** (`../deep/tool-output-shaping.md`) when: designing a tool's return contract, debugging an agent that confidently misreports data, or trimming an agent loop's token bill.

## Related

- [Deep: the evidence behind this page](../deep/tool-output-shaping.md) — open it on the trigger named above.
