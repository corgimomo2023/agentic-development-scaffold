# Lifecycle State Machine

| State | Owner | Required exit evidence | Next |
|---|---|---|---|
| INTAKE | Orchestrator | problem, requester, constraints, source links | PROPOSAL |
| PROPOSAL | Product manager | outcome, scope/non-goals, actors, risks, approval | DISCOVERY |
| DISCOVERY | Product manager / curator | evidence, rules, unknowns, provenance | DESIGN |
| DESIGN | Architect | approved design, threat model, ADRs | PLANNED |
| PLANNED | Planner | ordered vertical tasks and exact tests | IMPLEMENTING |
| IMPLEMENTING | TDD developer | RED and GREEN evidence per task | SPEC_REVIEW |
| SPEC_REVIEW | Independent spec reviewer | requirement-by-requirement PASS | QUALITY_SECURITY_REVIEW |
| QUALITY_SECURITY_REVIEW | Independent quality and security reviewers | separate PASS verdicts with no blocker | VERIFYING |
| VERIFYING | Release verifier | canonical independent evidence | RELEASE_READY |
| RELEASE_READY | Human approver | release and rollback approval | RELEASED |
| RELEASED | Curator / product owner | measured outcome and write-back | CLOSED |

Any gate failure returns to the artifact-owning state. Scope or risk changes return to PROPOSAL or DESIGN. A stop condition moves work to BLOCKED until a named human resolves it.
