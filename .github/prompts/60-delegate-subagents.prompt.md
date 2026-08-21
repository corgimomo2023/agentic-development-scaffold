---
description: Create safe, complete subagent dispatch packets and dependency ordering.
agent: orchestrator
---

# Delegate Subagents

## Inputs

Approved plan, tasks, dependency graph, role catalog, tools and authority limits.

## Process

Read `AGENTS.md`, confirm the active lifecycle state and authority, inspect only relevant canonical artifacts, and make no assumption that is not supported by evidence or an explicit decision.

## Required output

Dispatch packets, parallel/serial schedule, integration owner, review assignments, stop conditions.

Include artifact paths, traceability links, risks, evidence, owner, and recommended next lifecycle state.

## Stop conditions

Stop if write scopes overlap, context is incomplete, or a subagent would approve its own work.
