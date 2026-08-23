# Governed Agentic Skills First Release Design

## Constraints and assumptions
- `.github/skills/manifest.yaml` is catalog SSOT; `skills.lock.yaml` is immutable integrity/provenance lock.
- GitHub documents `.github/skills` as a supported project-skill location: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills. This mutable documentation establishes location compatibility only, not source-content security trust.
- Canonical files use one directory per skill and no runtime loader is introduced.

## Proposed design
Eight concise Markdown skills expose process contracts. A zero-new-dependency validator loads YAML, enforces exact fields and enums, checks owner/lifecycle references, requires every declared tool to be canonical and a subset of the owning agent's least-privilege matrix, maps dangerous tools to side effects, validates pinned provenance, detects missing/orphan/duplicate/path-escape entries, compares lock data, and hashes bytes.

## Interfaces and data
- Manifest schema version 1 contains invocation, ownership, lifecycle, evidence, tool, side-effect, concurrency, and provenance metadata.
- Lock schema version 1 repeats identity/path/provenance and stores lowercase SHA-256.
- JSON Schema documents the manifest contract; semantic cross-file rules remain in Python.
- Every external source repeats deterministic source-review evidence in manifest and lock: URL, resolved 40-character commit, license identifier, safe repository-relative license blob path, lowercase license SHA-256, reviewer, and audit date/UTC time. CI verifies this evidence offline and never depends on source-host reachability.

## Failure modes
Malformed YAML/JSON, unknown fields/tools/owners, owner/tool privilege mismatch, mutable revisions, missing or malformed license attestations, unsafe license paths, undeclared side effects, missing/orphan skills, mismatch, or hash drift fail closed. The repository root, `.github`/catalog path components, manifest, schema, lock, and all governed skill files must be real non-symlink nodes before any parse/read/hash; a non-following repository walk rejects every remaining symlink and the public text scan never reads symlink targets.

## Security and privacy
No external code executes. Source URLs are public HTTPS references. The final security-review audit independently reverified source reachability and pinned license bytes, while formal review remains PENDING after this candidate change. Browser/source tooling is invoked through each owner's existing `execute` capability; truthful network/browser-navigation/screenshot side effects remain declared without inventing `web` or `browser` privileges. Public scanner reads real non-symlink text artifacts only.

## Operations and rollback
Validation runs in existing CI. Rollback removes the catalog/docs/tests and validator extension together; partial rollback is invalid because required files fail closed.

## ADR links
No ADR required: no deployable/runtime architecture or public product interface changes.

## Test strategy
Focused TDD exercises valid catalog plus required negative mutations. Canonical validator, full pytest, YAML/JSON parse, hash replay, and diff whitespace checks provide regression evidence.
