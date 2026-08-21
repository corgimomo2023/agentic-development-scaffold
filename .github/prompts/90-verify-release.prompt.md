---
description: Independently verify acceptance, operations, rollback, and release readiness.
agent: release-verifier
---

# Verify Release

## Inputs

Candidate revision, acceptance matrix, canonical commands, release and rollback plan.

## Process

Read `AGENTS.md`, confirm the active lifecycle state and authority, inspect only relevant canonical artifacts, and make no assumption that is not supported by evidence or an explicit decision.

## Required output

Fresh command results, verification table, environment, limitations, release readiness verdict.

Include artifact paths, traceability links, risks, evidence, owner, and recommended next lifecycle state.

## Stop conditions

Stop on command failure, environment mismatch, missing rollback, missing observability, or unresolved blocker.
