# Governed Agentic Skills First Release Use Cases

## UC-01: Select a governed skill
- Actor: Orchestrator or specialist agent.
- Trigger: A request reaches a declared lifecycle state and matches a trigger.
- Preconditions: Manifest entry, required inputs, and approval boundaries are available.
- Success flow: Agent checks anti-trigger, invokes the skill, records required outputs, and hands off to the next legal state.
- Alternate flow: Optional skill is skipped with a concrete rationale.
- Failure flow: Missing input, conflicting authority, or unsafe side effect stops and escalates.
- Postconditions: Canonical lifecycle and evidence remain intact.
- Observable acceptance evidence: Manifest metadata and matching SKILL.md procedure.

## UC-02: Review an external skill change
- Actor: Security reviewer.
- Trigger: An external skill source is proposed or upgraded.
- Preconditions: URL, candidate revision, files, license, and intended capability are supplied.
- Success flow: Reviewer pins revision, inspects execution/network/write/dependency scope, records update/rollback, and permits bounded manifest/lock change.
- Alternate flow: Selective ideas are locally rewritten and attributed without code import.
- Failure flow: Mutable revision, missing license, hidden executable scope, or undeclared side effect is rejected.
- Postconditions: Lock and manifest agree or no external change proceeds.
- Observable acceptance evidence: Supply-chain skill plus validator mutation tests.

## UC-03: Detect catalog tampering or drift
- Actor: Release verifier.
- Trigger: Validation runs before review or merge.
- Preconditions: Repository checkout and frozen dependencies are available.
- Success flow: Validator parses catalog, compares lock, hashes skills, scans orphans, and returns PASS.
- Alternate flow: No side effects are declared for a read-only skill.
- Failure flow: Any mismatch returns non-zero with a concrete finding.
- Postconditions: Invalid catalogs cannot pass CI.
- Observable acceptance evidence: Focused negative tests and canonical validator output.
