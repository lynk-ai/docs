---
description: The evidence behind tool output shaping — the four shapes for a large result and the truncation contract. Open when designing a tool's return, not reading one.
layer: deep
concept: ../concepts/tool-output-shaping.md
---

# Tool output shaping — evidence & practice

`distinguishability.md` covers tool *names and descriptions* — the input surface. This page covers the output surface, which is where the tokens actually are. In a loop averaging ~50 tool calls per task at ~100:1 input:output ([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)), observations dominate the window; the system prompt is a rounding error by comparison.

## The silent-truncation failure

Agent harnesses cap tool output — commonly **2,000 lines or ~50KB**, sometimes as low as 8KB. Two behaviours follow, and only one of them is safe:

- **Marked truncation**: the model sees `[truncated — 8,200 of 41,000 chars]`, knows the result is partial, and can page, filter, or narrow.
- **Silent truncation**: the model receives a syntactically complete-looking result and reasons over it **as if it were whole**. It then reports a confident, wrong answer, and no error surfaces anywhere.

Practitioners describe this as one of the most expensive failure modes in production agents precisely because *the agent never tells you it happened* ([tool-result truncation](https://dev.to/gabrielanhaia/tool-result-truncation-the-silent-bug-that-makes-agents-lie-3epe); [silent 8KB caps](https://tianpan.co/blog/2026-05-10-silent-tool-truncation-8kb-default-agent-reasons-blind)). It is the observation-layer twin of trusting a green-looking summary over the authoritative surface it was derived from — and it fails the same silent way a hook does (`hook-vs-router.md`).

**Rule: truncation must be a message, not an event.** If your harness truncates, it must append a marker. If your tool truncates, it must say so in the payload.

## The four return shapes, and how to choose

| Shape | Contract | Choose when | Watch for |
|---|---|---|---|
| **Full** | Everything, no cap | Small and entirely load-bearing | Growth: today's 40 rows is next quarter's 40,000 |
| **Truncated + marker** | Head (and/or tail) + explicit omission notice + how to get the rest | A peek answers most questions | Marker must state *how much* was omitted and *how to continue* |
| **Paginated** | One page + `next_page` cursor, and a tool that accepts the cursor | The agent should traverse deliberately | Page size — too small multiplies hops (`when-to-split.md`'s hop tax) |
| **Handle** | An identifier — path, ID, row count — instead of the payload | The next step is computation, not reading | The handle must be resolvable later (stable path/URL) |

**The handle shape is the highest-leverage and least used.** `"Wrote 12,431 rows to results.csv"` costs ~10 tokens; the rows cost 200,000. This is `progressive-disclosure.md`'s read-vs-execute distinction applied to returns — *the cheapest observation is one that never enters the window*. Manus's filesystem-as-context is exactly this: the agent writes results to files and re-reads only what it needs, keeping paths so nothing is unrecoverable.

## Errors are context, and most of them are wasted

Two responses to the same condition:

```
413 Payload Too Large
```
```
Result too large: 41,203 rows (limit 1,000).
Retry with cursor="eyJvZmZzZXQiOjB9" or narrow with filter=season_year=2023.
```

The first produces a confused retry loop — often the identical call. The second produces a correct next action. An error message is a *prompt you are writing for the model*, and the admission test from `authoring-standing-surfaces.md` applies: state the thing the model cannot infer — here, the recovery path.

**Keep failures in the transcript.** Manus's verified finding: leaving failed actions and error traces in context lets the model implicitly update its beliefs and avoid repeating the mistake — they call error recovery "one of the clearest indicators of true agentic behavior." This sits in tension with compaction (`context-governance.md`), and the resolution is by *phase*: keep errors while the task is live (they're steering signal), drop them at compaction boundaries once the sub-task resolved (they're then history).

## Shaping happens at the boundary, not per tool

Individually well-behaved tools are not a strategy — you don't control third-party or MCP tools, and behaviour drifts. Intercept results *before* they enter context:

- Trim long strings, cap list lengths (`[…270 items omitted]`), collapse repeated structure.
- Strip known-noise fields (HTML boilerplate, ANSI codes, base64 blobs, verbose stack frames below the first app frame).
- Normalize/sanitize untrusted returns here too — the same chokepoint serves `trust-boundaries.md`.

This is floor-raising work that must run on every call, which makes it hook-shaped (`hook-vs-router.md`); the router sits later, at the action that matters.

## Format economics

Two cheap wins that are easy to overlook:

- **Structured beats prose for machine-consumed results** — a typed object the model can index into avoids re-parsing prose on every subsequent turn, and makes downstream extraction deterministic.
- **Repetition is compressible**: 500 rows sharing a schema don't need 500 copies of the field names. Emit the header once. Long homogeneous results are where naive JSON is most wasteful.

But don't over-rotate: shape for the *consumer*. If the model must reason over nuance, prose with the nuance intact beats a lossy table.

## Diagnostic: is your loop paying an observation tax?

1. **Token attribution per turn** — split the window by origin (system / instructions / tool results / conversation). If tool results aren't the largest slice in an agent loop, verify your measurement before believing it.
2. **Truncation audit** — grep the harness and every tool for caps; for each, confirm a marker exists. Any unmarked cap is an open silent-lie bug.
3. **Re-read count** — how often does the agent re-fetch something it already had? High counts mean results were dropped or unfindable; consider handles + stable paths.
4. **Error-to-recovery rate** — what fraction of tool errors are followed by an identical retry? High means your error strings carry no recovery action.
5. **Ablate a verbose tool's payload** (`measuring-context.md`): replace it with a summary+handle and measure. This is usually where the biggest painless token cut lives.

## By implementation type

| Implementation | The heavy return | Shape it as |
|---|---|---|
| Coding agent | File reads, test output, build logs, greps | Ranged reads + handles; keep only the first failing frame, not the whole trace |
| RAG chatbot | Retrieved chunks | Rerank + prune before admission (`selection-quality.md`); return passages, never whole documents |
| Long-horizon agent | Accumulated intermediate results | Write to files, keep paths; the transcript holds pointers, not payloads |
| Multi-agent | Sub-agent returns | Typed, condensed, cited — ~1,000–2,000 tokens (Anthropic's production figure); never a transcript |
| Text-to-SQL | Query result sets | Row cap + total count + "N of M rows shown"; large sets to a file/handle, and never feed raw rows back as instructions |
