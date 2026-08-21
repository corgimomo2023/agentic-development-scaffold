# Role and Separation-of-Duties Matrix

| Role | Owns | May edit | Must not approve |
|---|---|---|---|
| Orchestrator | state, dependencies, dispatch, integration | coordination artifacts | its own implementation |
| Product manager | proposal, actors, outcomes, scope | product and feature definition | architecture/security risk |
| Architect | design, ADRs, trust boundaries, rollback | architecture and ADRs | implementation quality |
| Implementation planner | vertical tasks and test commands | plans and tasks | code changes |
| TDD developer | RED-GREEN-REFACTOR implementation | approved task files | own spec/quality review |
| Test specialist | test strategy and gaps | tests when assigned | production risk acceptance |
| Spec reviewer | requirement compliance | review record only | quality or security gate |
| Code reviewer | correctness, maintainability, test quality | review record only | spec or security gate |
| Security reviewer | threats, trust boundaries, secrets, unsafe defaults | review record only | residual risk acceptance |
| Release verifier | independent evidence and readiness | verification record | business release authority |
| Knowledge curator | provenance and write-back | knowledge/index/log | decision ownership |
