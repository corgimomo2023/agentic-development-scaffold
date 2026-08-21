---
description: Perform an independent security review after spec compliance passes.
agent: security-reviewer
---

# Security Review

## Inputs

Spec PASS, reviewed revision, design and threat model, trust boundaries, dependencies, deployment changes, tests, and security evidence.

## Process

Read `AGENTS.md`, verify reviewer separation, inspect the exact reviewed revision, and assess threats, secrets, unsafe defaults, validation, authorization, data handling, dependencies, deployment, and operational abuse cases.

## Required output

Prioritized findings with evidence, impact, required remediation, residual risk owner, and PASS or FAIL. Include reviewed revision, artifact versions, reviewer identity, and recommended next lifecycle state.

## Stop conditions

Stop and FAIL on exploitable behavior, secret exposure, missing trust boundary, unsafe default, unverifiable security claim, or any request to accept residual risk without human authority.
