# Dataset v3 candidates — stress tests for the promoted constraints

Parked 2026-07-21, from the constraint-prominence sweep's auditor. NOT yet
cases: answer keys must be written FROM the current docs before any of these
enter questions.yaml, and the hold-out rotation should happen in the same
revision. Origin is the promoted-constraint list (allowed by the anti-overfit
rules — these derive from the coverage matrix, not from failing transcripts).

Design principles (keep these when wiring in):
- The honest test of a prominence fix is not "does a plain question retrieve
  the rule" but "does the model surface the constraint when the prompt
  actively tempts the compressed, wrong answer."
- Score constraint-presence, not phrasing.
- Cases 2, 6, 9, 10 are the discriminating ones; 10 is a regression tripwire
  for over-correction — keep it.

## policy.md — override fully replaces

1. Leading-toward-append: "Lynk's default output-format policy is fine, I
   just also want to require a currency symbol on money values. What do I
   add?" → must say: an output-format policy fully replaces the default;
   restate every default bullet you keep.
2. Cross-page confusion (strongest): "LYNK.md composition is additive —
   domain extends root. Policies work the same way, so my clarification
   override just extends Lynk's defaults, right?" → must say no — policies
   don't merge; override replaces.
3. Partial-file inference: "If I write a clarification policy with a single
   bullet, which of Lynk's default clarification behaviors still apply?"
   → none — your file becomes the whole policy.

## lynk.yml — no shared domain by default

4. Debugging framing (no keyword): "core and marketing; marketing declares
   identity: core.customer and the build fails with a topology error. Why?"
   → shared_domain unset by default; declare shared_domain: core.
5. Default-only project: "lynk.yml has only schema_version. Can a domain
   import from core?" → no.
6. Half-true adversarial: "Medallion is the default and medallion lets a
   domain reference the shared domain, so cross-domain imports work out of
   the box — correct?" → no; shared_domain must be set explicitly.

## glossary.md — no structured pointer

7. Invent-a-field temptation: "What field links a glossary term to its
   entity/metric?" → none exists; meaning lives in the prose.
8. Terse-entry reliance: "Can I keep descriptions to one word and let the
   agent follow the term to the entity?" → no; description must stand alone.

## Cross-constraint / controls

9. Multi-hop (policy composition + topology): "Can I put a policy in core
   and have marketing and sales inherit it?" → policies don't merge across
   scopes; use a reference file / shared domain via @ injection, legal only
   with shared_domain set.
10. NEGATIVE CONTROL (over-correction tripwire): "Do domain glossaries and
    domain LYNK.md fully replace the root the way a policy override does?"
    → no — those compose (LYNK.md additive; glossary merges, domain wins).

Also fold into the same revision (from DECISIONS.md deferred list):
- rotate h003/h005 into dev with fresh hold-outs
- near-miss refusal perturbations (RefusalBench pattern) + over-refusal axis
- one case per remaining promoted constraint not covered above (identity
  2-segment and metric no-arguments already have q004/q006)
