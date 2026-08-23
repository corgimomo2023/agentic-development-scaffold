# Governed Agentic Skills First Release Implementation Plan

> Execute task-by-task; implementation cannot approve its own independent reviews.

## Goal
Deliver eight governed skills and fail-closed catalog integrity without changing the lifecycle topology or adding runtime dependencies.

## Architecture
Markdown skills + YAML manifest/lock + JSON Schema + semantic validation in the existing Python validator.

## Technology
Python 3.11, PyYAML already locked, pytest, Markdown, YAML, and JSON.

## Ordered tasks
1. Add focused catalog validator tests and prove expected missing-API RED.
2. Implement minimal semantic validator and prove focused GREEN.
3. Add eight skills, manifest/schema/lock, and verify exact hashes.
4. Integrate lifecycle docs/prompts and create this feature package.
5. Run canonical frozen validator/full suite, parse/integrity checks, and diff checks.
6. Hand the uncommitted candidate to distinct spec, quality, security, and verifier assignments; no commit or merge in this task.
