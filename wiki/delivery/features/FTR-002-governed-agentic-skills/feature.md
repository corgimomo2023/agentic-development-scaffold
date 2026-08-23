# Governed Agentic Skills First Release

- Feature ID: FTR-002-governed-agentic-skills
- Owner: human:alan
- Phase: Governance capability
- Status: IN_REVIEW

## Problem and outcome
The scaffold has lifecycle roles and prompts but no governed, vendor-neutral reusable skill catalog. Add eight selective, maintainable skills with machine-enforced provenance, integrity, ownership, lifecycle, and side-effect controls.

## Actors
- Scaffold maintainer approves scope and eventual merge.
- Orchestrator selects skills without bypassing lifecycle.
- Specialist agents execute or review only their declared scope.
- Public adopters inspect provenance and integrity before reuse.

## Scope
- Eight approved first-release skills under `.github/skills/<id>/SKILL.md`.
- Manifest, immutable lock, JSON Schema, validator integration, negative mutation tests, lifecycle integration, and public documentation.

## Non-goals
- Vendoring third-party repositories, runtimes, datasets, installers, plugins, hooks, or auto-fix behavior.
- Adding lifecycle states, reviewer roles, dependencies, production deployment, or merge automation.

## Requirements and business rules
- Canonical lifecycle remains unchanged; skills insert inside existing states.
- External references use HTTPS URLs, exact commits, verified licenses, and selective-adaptation statements.
- Manifest and lock are fail-closed SSOT/integrity controls; all `SKILL.md` files are declared and hashed.
- Dangerous tools require declared side effects; browser QA is independent and report-only.

## Dependencies and risks
- Existing PyYAML dependency and validator conventions.
- Risk: manifest/lock drift; mitigated by SHA-256 and disagreement checks.
- Risk: upstream scope creep; mitigated by pinned provenance and supply-chain review.

## Acceptance criteria
1. All eight skills contain trigger, anti-trigger, lifecycle insertion, inputs, procedure, outputs/evidence, guardrails, and verification.
2. Manifest/schema/lock are parseable and hashes match disk.
3. Validator rejects hash mismatch, mutable revision, orphan, duplicates, unknown owner/state, path escape, disagreement, and undeclared dangerous side effects.
4. Lifecycle docs/prompts integrate the skills without new top-level states or reviewers.
5. Canonical validator and full pytest pass via frozen uv commands; public-safety scan covers new files.

## Evidence and traceability
- Design: `design.md`; tasks and RED/GREEN: `tasks.md`; command evidence: `verification.md`.
