# Governed Agentic Skills First Release Tasks

| Task | Outcome | Owner | Status |
|---|---|---|---|
| TASK-001 | Validator mutation contract | agent:implementer-01 | COMPLETE |
| TASK-002 | Governed skills catalog | agent:implementer-01 | COMPLETE |
| TASK-003 | Lifecycle integration | agent:implementer-01 | COMPLETE |
| TASK-004 | Feature package and verification | agent:implementer-01 | COMPLETE |
| TASK-005 | Spec-review blocker fixes | agent:implementer-spec-fix-01 | COMPLETE |
| TASK-006 | Symlink-escape spec-review blocker fix | agent:implementer-spec-fix-02 | COMPLETE |
| TASK-007 | Canonical `.github/skills` migration | agent:implementer-path-migration-01 | COMPLETE |
| TASK-008 | Ancestor-symlink and stale-path blocker fixes | agent:implementer-ancestor-symlink-fix-01 | COMPLETE |
| TASK-009 | Final tool/owner, trust-boundary, and offline-attestation blockers | agent:implementer-final-blockers-01 | COMPLETE |

## TASK-001 TDD evidence
- Exact files: `tests/test_skills_validator.py`, `scripts/validate_scaffold.py`
- Exact command: `uv run --frozen --extra test pytest tests/test_skills_validator.py -q`
- Expected RED failure: New tests fail because `validate_skills` does not exist.
- Actual RED result / exit status: Eight expected AttributeError failures; exit 1.
- GREEN result / exit status: Eight tests passed; exit 0.
- Full-suite evidence: Pending final canonical run after all artifacts are complete.
- Environment: Python 3.11 with frozen uv lock.
- Artifact/link: `verification.md`
- Recorded by: agent:implementer-01
- Timestamp: 2026-08-23T05:38:11Z
- Commit/revision: Base 17d954fc7d08603e7075f407c40fbd40850ce521 plus uncommitted candidate.
- Dependencies: Existing PyYAML and pytest dependencies.
- Risks: Semantic validator and schema can drift; regression tests cover the required fail-closed rules.
- Commit boundary: No commit authorized in this task; hand off the complete uncommitted candidate.

## TASK-002 TDD evidence
- Exact files: `.github/skills/*/SKILL.md`, `.github/skills/manifest.yaml`, `.github/skills/manifest.schema.json`, `skills.lock.yaml`
- Exact command: `uv run --frozen --extra test pytest tests/test_skills_validator.py -q`
- Expected RED failure: Initial acceptance test cannot call the missing catalog validator and all eight tests fail.
- Actual RED result / exit status: Covered by TASK-001 initial focused run; exit 1.
- GREEN result / exit status: Catalog semantics returned an empty error list; focused suite exit 0.
- Full-suite evidence: Pending final canonical run after all artifacts are complete.
- Environment: Python 3.11 with frozen uv lock.
- Artifact/link: `verification.md`
- Recorded by: agent:implementer-01
- Timestamp: 2026-08-23T05:38:11Z
- Commit/revision: Base 17d954fc7d08603e7075f407c40fbd40850ce521 plus uncommitted candidate.
- Dependencies: Approved pinned source references and verified licenses.
- Risks: Editing SKILL.md invalidates lock hash; validator fails closed.
- Commit boundary: No commit authorized; catalog and lock must move together.

## TASK-003 TDD evidence
- Exact files: `README.md`, `workflows/00-intake.md`, `workflows/30-design-and-adr.md`, `workflows/50-tdd-implementation.md`, `workflows/60-review.md`, `.github/prompts/00-intake.prompt.md`, `.github/prompts/20-design.prompt.md`, `.github/prompts/50-implement-tdd.prompt.md`, `.github/prompts/80-quality-security-review.prompt.md`, `wiki/guides/lifecycle/state-machine.md`, `wiki/guides/lifecycle/gates.md`, `wiki/index.md`, `wiki/log.md`
- Exact command: `uv run --frozen --extra test python scripts/validate_scaffold.py`
- Expected RED failure: Before catalog implementation the validator reports missing governed skill files.
- Actual RED result / exit status: Initial focused tests established missing catalog behavior; docs integration was configuration-only.
- GREEN result / exit status: Pending final canonical validator run after documentation edits.
- Full-suite evidence: Pending final canonical run after all artifacts are complete.
- Environment: Python 3.11 with frozen uv lock.
- Artifact/link: `verification.md`
- Recorded by: agent:implementer-01
- Timestamp: 2026-08-23T05:38:11Z
- Commit/revision: Base 17d954fc7d08603e7075f407c40fbd40850ce521 plus uncommitted candidate.
- Dependencies: Existing canonical lifecycle and prompt contracts.
- Risks: Over-integration could create a competing lifecycle; edits are limited to substages/evidence.
- Commit boundary: No commit authorized; documentation and behavior remain one candidate.

## TASK-004 TDD evidence
- Exact files: `wiki/delivery/features/FTR-002-governed-agentic-skills/*`
- Exact command: `uv run --frozen --extra test pytest`
- Expected RED failure: Before the package existed the required feature evidence and handoff were absent.
- Actual RED result / exit status: Configuration artifact gap established by the approved requirement; no executable behavior was added in this task.
- GREEN result / exit status: Focused suite passed 13 tests and canonical validator passed; exit 0 at 2026-08-23T05:50:10Z.
- Full-suite evidence: `uv run --frozen --extra test pytest -q` passed 85 tests; exit 0 at 2026-08-23T05:50:10Z.
- Environment: Python 3.11 with frozen uv lock.
- Artifact/link: `verification.md`
- Recorded by: agent:implementer-01
- Timestamp: 2026-08-23T05:38:11Z
- Commit/revision: Base 17d954fc7d08603e7075f407c40fbd40850ce521 plus uncommitted candidate.
- Dependencies: Feature package validator contract.
- Risks: Independent review cannot bind an uncommitted working tree; review remains pending.
- Commit boundary: Stop before commit and hand off to an authorized orchestrator.

## TASK-005 TDD evidence
- Exact files: `tests/test_skills_validator.py`, `scripts/validate_scaffold.py`, `wiki/delivery/features/FTR-002-governed-agentic-skills/discovery.md`, `wiki/delivery/features/FTR-002-governed-agentic-skills/tasks.md`, `wiki/delivery/features/FTR-002-governed-agentic-skills/verification.md`
- Exact command: `uv run --frozen --extra test pytest tests/test_skills_validator.py -q`
- Expected RED failure: The nested orphan mutation at `.github/skills/nested/escape/SKILL.md` is not discovered by the one-level glob and therefore is not rejected.
- Actual RED result / exit status: 1 failed and 12 passed; `test_skills_catalog_rejects_nested_orphan_skill` failed because no nested-orphan error was returned; exit 1.
- GREEN result / exit status: After recursive discovery, 13 focused tests passed; exit 0 at 2026-08-23T05:50:10Z.
- Full-suite evidence: Canonical validator passed, 85 full-suite tests passed, 11 YAML and 4 JSON files parsed, and `git diff --check` passed; all exit 0 at 2026-08-23T05:50:10Z.
- Environment: Python 3.11 with frozen uv lock.
- Artifact/link: `verification.md`
- Recorded by: agent:implementer-spec-fix-01
- Timestamp: 2026-08-23T05:50:10Z
- Commit/revision: Base 17d954fc7d08603e7075f407c40fbd40850ce521 plus uncommitted candidate; no frozen review revision claimed.
- Dependencies: Existing PyYAML and pytest dependencies; completed 2026-08-22 read-only pinned-source audits.
- Risks: Recursive catalog bypass and missing fail-closed mutation coverage; focused negative tests now preserve the behavior.
- Commit boundary: No commit authorized; hand off the verified uncommitted candidate.

## TASK-006 TDD evidence
- Exact files: `tests/test_skills_validator.py`, `scripts/validate_scaffold.py`, `wiki/delivery/features/FTR-002-governed-agentic-skills/tasks.md`, `wiki/delivery/features/FTR-002-governed-agentic-skills/verification.md`
- Exact command: `uv run --frozen --extra test pytest tests/test_skills_validator.py -q`
- Expected RED failure: A canonical `.github/skills/<id>/SKILL.md` symlink to an external file with a matching lock hash, and a broken discovered `SKILL.md` symlink, are accepted instead of failing closed.
- Actual RED result / exit status: 2 failed and 14 passed; both symlink assertions failed because the validator followed or omitted the symlinks; exit 1.
- GREEN result / exit status: After requiring regular non-symlink governed files before frontmatter/hash reads and discovering broken symlinks, 16 focused tests passed; exit 0 at 2026-08-23T05:57:36Z.
- Full-suite evidence: Canonical validator passed, 88 full-suite tests passed, 11 YAML and 4 JSON files parsed, and `git diff --check` passed; all exit 0 at 2026-08-23T05:57:36Z.
- Environment: Python 3.11 with frozen uv lock.
- Artifact/link: `verification.md`
- Recorded by: agent:implementer-spec-fix-02
- Timestamp: 2026-08-23T05:57:36Z
- Commit/revision: Base 17d954fc7d08603e7075f407c40fbd40850ce521 plus uncommitted candidate; no frozen review revision claimed.
- Dependencies: Existing PyYAML and pytest dependencies; platform symlink support, with regression tests skipping only when symlink creation is genuinely unavailable.
- Risks: Symlink targets could escape the repository or disappear between discovery and reads; direct symlink prohibition removes the accepted indirection without resolve-based complexity.
- Commit boundary: No commit authorized; hand off the verified uncommitted candidate without changing review verdicts.

## TASK-007 TDD evidence
- Exact files: `tests/test_skills_validator.py`, `scripts/validate_scaffold.py`, `.github/skills/**`, `skills.lock.yaml`, `README.md`, `wiki/index.md`, `wiki/delivery/features/FTR-002-governed-agentic-skills/*`
- Exact command: `uv run --frozen --extra test pytest tests/test_skills_validator.py -q`
- Expected RED failure: Fixtures and assertions require `.github/skills`, while the validator still requires and scans root `skills/`.
- Actual RED result / exit status: 16 failed; the acceptance test reported `missing skills/manifest.yaml`, and every negative mutation assertion lacked its expected diagnostic; exit 1.
- GREEN result / exit status: After migrating the catalog and updating the validator, all 16 preserved focused tests passed; exit 0 at 2026-08-23T06:03:35Z.
- Full-suite evidence: Catalog semantics returned `[]`, canonical validator passed its public-safety scan, 88 tests passed, 11 YAML and 4 JSON files parsed, the schema regex matched the literal `.github/skills` path, root `skills/` was absent, eight canonical files were present, and `git diff --check` passed; all exit 0.
- Environment: Python 3.11 with frozen uv lock.
- Artifact/link: `verification.md`
- Recorded by: agent:implementer-path-migration-01
- Timestamp: 2026-08-23T06:03:35Z
- Commit/revision: Base `17d954fc7d08603e7075f407c40fbd40850ce521` plus uncommitted candidate; no frozen review revision claimed.
- Dependencies: GitHub's location documentation at https://docs.github.com/en/copilot/concepts/agents/about-agent-skills is compatibility evidence only and grants no mutable-content security trust.
- Risks: Discovery must remain rooted at `.github/skills` so unrelated `.github` Markdown is never treated as a skill; recursive orphan and symlink checks remain fail closed inside that bounded subtree.
- Commit boundary: Do not commit, push, open a PR, merge, or alter independent PENDING review gates.

## TASK-008 TDD evidence
- Exact files: `tests/test_skills_validator.py`, `scripts/validate_scaffold.py`, `.github/prompts/00-intake.prompt.md`, `.github/skills/skill-supply-chain-review/SKILL.md`, `skills.lock.yaml`, `wiki/delivery/features/FTR-002-governed-agentic-skills/tasks.md`, `wiki/delivery/features/FTR-002-governed-agentic-skills/verification.md`
- Exact command: `uv run --frozen --extra test pytest -o addopts='' tests/test_skills_validator.py::test_skills_catalog_rejects_canonical_skill_directory_symlink_with_matching_hash tests/test_skills_validator.py::test_skills_catalog_rejects_orphan_skill_directory_symlink -q`
- Expected RED failure: A canonical skill-directory symlink to an external matching-hash artifact and an external orphan skill-directory symlink are both silently accepted.
- Actual RED result / exit status: 2 failed; both new rejection assertions received no symlink diagnostic; exit 1 at 2026-08-23T06:17:16Z.
- GREEN result / exit status: The validator now checks every canonical path component before reading/resolving, bounds resolved files to the catalog and repository, and scans direct catalog entries without following symlinked directories; all 18 focused tests passed; exit 0.
- Full-suite evidence: Catalog semantics returned `[]`, canonical validator passed, 90 tests passed, 11 YAML and 4 JSON files parsed, all eight lock hashes matched (only `skill-supply-chain-review` was recomputed), and `git diff --check` passed; all exit 0 at 2026-08-23T06:17:16Z.
- Environment: Python 3.11 with frozen uv lock.
- Artifact/link: `verification.md`
- Recorded by: agent:implementer-ancestor-symlink-fix-01
- Timestamp: 2026-08-23T06:17:16Z
- Commit/revision: Base `17d954fc7d08603e7075f407c40fbd40850ce521` plus uncommitted candidate; no frozen review revision claimed.
- Dependencies: Existing PyYAML and pytest dependencies; platform symlink support, with regression tests skipping only when symlink creation is genuinely unavailable.
- Risks: Validation must never parse or hash through an untrusted catalog path component; safe-file admission now precedes both operations, while recursive real-directory orphan discovery remains intact.
- Commit boundary: Do not commit, push, open a PR, merge, or alter independent PENDING review gates.

## TASK-009 TDD evidence
- Exact files: `tests/test_skills_validator.py`, `scripts/validate_scaffold.py`, `.github/skills/manifest.yaml`, `.github/skills/manifest.schema.json`, `skills.lock.yaml`, `wiki/delivery/features/FTR-002-governed-agentic-skills/discovery.md`, `wiki/delivery/features/FTR-002-governed-agentic-skills/design.md`, `wiki/delivery/features/FTR-002-governed-agentic-skills/tasks.md`, `wiki/delivery/features/FTR-002-governed-agentic-skills/verification.md`
- Exact command: `uv run --frozen --extra test pytest -o addopts='' tests/test_skills_validator.py -q`
- Expected RED failure: Unknown tools and owner/tool privilege mismatches pass; lock/catalog control symlinks and public-scan symlink targets are followed or omitted; external sources lack deterministic offline review attestations.
- Actual RED result / exit status: Tool/owner/schema slice: 4 failed; trust-boundary slice: 5 failed and 3 passed; attestation slice: 6 failed; each command exited 1 for the expected missing validation.
- GREEN result / exit status: Tool/owner/schema slice 4 passed; trust-boundary slice 8 passed; attestation slice 6 passed; each command exited 0.
- Full-suite evidence: Pending final canonical replay after documentation evidence is complete.
- Environment: Python 3.11 with frozen uv lock.
- Artifact/link: `verification.md`
- Recorded by: agent:implementer-final-blockers-01
- Timestamp: 2026-08-23T06:41:31Z
- Commit/revision: Base `17d954fc7d08603e7075f407c40fbd40850ce521` plus uncommitted candidate; no frozen review revision claimed.
- Dependencies: Existing PyYAML/pytest only; read-only source evidence from pinned local checkouts, with no CI network dependency.
- Risks: Path validation targets static CI trees and does not claim hostile concurrent-mutation protection; global repository symlink rejection and admit-before-read checks close the scoped static trust boundary.
- Commit boundary: Do not commit, push, open a PR, merge, alter PENDING review verdicts, or record accessibility PASS.
