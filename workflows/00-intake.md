# Intake

## Entry criteria

- Active lifecycle state is `INTAKE` or its first state.
- Prior phase exit evidence is linked and no abort condition is open.
- Owner, scope, and decision authority are named.

## Activities

Capture the request, authority, constraints, sources, urgency, and ambiguity. Apply `intake-sizing-and-escalation` to classify `spike`, `bounded`, or `architectural`; escalation is one-way and never skips lifecycle states. Invoke `brainstorm-and-converge` only when alternatives are genuinely unclear, and compare two or three approaches for architectural work.

## Required artifacts

- Intake record and source links.
- Sizing rationale, escalation triggers, and optional brainstorm/skip evidence.
- Updated feature status and traceability links.
- Gate record with owner and timestamp.

## Exit evidence

- Artifact reviewed against its explicit checklist.
- Open risks and unknowns have owners and resolution gates.
- Next permitted state: `PROPOSAL`.

## Failure and revision

Return to the phase that owns the failed artifact. Escalate authority, risk, credential, production, or material ambiguity decisions to a human. Abort on secret exposure, destructive scope mismatch, or loss of rollback.
