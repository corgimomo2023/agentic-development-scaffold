# Design And Adr

## Entry criteria

- Active lifecycle state is `DESIGN` or its first state.
- Prior phase exit evidence is linked and no abort condition is open.
- Owner, scope, and decision authority are named.

## Activities

Create system design, threat model, failure handling, operations, rollback, and ADRs for consequential choices. For user-facing scope, run `ux-product-design` and then `frontend-design-direction` as separate conditional DESIGN substages. Use `prototype-spike` only for one throwaway high-risk question; only its decision/evidence carries forward, and retained code restarts governed intake.

## Required artifacts

- Approved design and adrs.
- Conditional UX/frontend direction or concrete N/A rationale; spike disposal/re-intake evidence when applicable.
- Updated feature status and traceability links.
- Gate record with owner and timestamp.

## Exit evidence

- Artifact reviewed against its explicit checklist.
- Open risks and unknowns have owners and resolution gates.
- Next permitted state: `PLANNED`.

## Failure and revision

Return to the phase that owns the failed artifact. Escalate authority, risk, credential, production, or material ambiguity decisions to a human. Abort on secret exposure, destructive scope mismatch, or loss of rollback.
