# Review

## Entry criteria

- Active lifecycle state is `SPEC_REVIEW -> QUALITY_SECURITY_REVIEW` or its first state.
- Prior phase exit evidence is linked and no abort condition is open.
- Owner, scope, and decision authority are named.

## Activities

Run independent requirement-by-requirement spec review. After spec PASS, run separate correctness/maintainability/test-quality review and security/threat review with different assignments.

## Required artifacts

- Two ordered pass verdicts with evidence.
- Updated feature status and traceability links.
- Gate record with owner and timestamp.

## Exit evidence

- Artifact reviewed against its explicit checklist.
- Open risks and unknowns have owners and resolution gates.
- Next permitted state: `VERIFYING`.

## Failure and revision

Return to the phase that owns the failed artifact. Escalate authority, risk, credential, production, or material ambiguity decisions to a human. Abort on secret exposure, destructive scope mismatch, or loss of rollback.
