---
description: Review correctness, maintainability, test quality, and operations after spec PASS; security has a separate gate.
agent: code-reviewer
---

# Quality Review

## Inputs

Spec PASS, exact reviewed revision, diff, design, tests, operations, and dependency changes.

## Process

Read `AGENTS.md`, confirm the active lifecycle state and authority, inspect only relevant canonical artifacts, and make no assumption that is not supported by evidence or an explicit decision.

## Required output

Prioritized quality findings, evidence, remediation, residual risks, and PASS or FAIL verdict. A separate security PASS from `82-security-review.prompt.md` is required before verification.

Include artifact paths, traceability links, risks, evidence, owner, and recommended next lifecycle state.

## Stop conditions

Stop and FAIL on incorrect behavior, unhandled critical failure, missing tests, unsafe operational behavior, or unverifiable claim. Send security concerns to the independent security reviewer as blockers.
