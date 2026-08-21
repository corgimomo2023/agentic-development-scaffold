# Gate Taxonomy

## Pre-flight gate

Checks prerequisites before side effects: clean branch, approved scope, dependencies, credentials channel, commands, rollback, and testability.

## Revision gate

A failed artifact or review returns to its owner with concrete evidence and resumption criteria. Never lower the criterion to make work pass.

## Escalation gate

Use when authority, risk acceptance, credentials, production access, conflicting requirements, or material ambiguity requires a human decision.

## Abort gate

Stop on suspected secret exposure, destructive scope mismatch, unverifiable production state, repeated failed review loops, or loss of rollback. Preserve evidence and do not continue partially.

Every gate records owner, checked inputs, result, evidence, failure reason, and next permitted transition.
