# Governed Agentic Skills First Release Discovery

## Evidence and provenance
| Source | Owner | Audit date | Trust level | Relevant finding |
|---|---|---|---|---|
| Approved task context | human:alan | 2026-08-23 | Authoritative scope | Eight selective capabilities; no wholesale copies |
| [GitHub agent skills documentation](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) | agent:controller-01 | 2026-08-23 | Location documentation only; not supply-chain trust | Project skills are supported under `.github/skills`; this repository uses that primary GitHub Copilot adapter path |
| [obra/superpowers](https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797) | agent:controller-01 | 2026-08-22 | Read-only pinned-source audit | Brainstorm/compare/converge discipline; MIT |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/bc826e2267a36d98a2dcf5231e16c30ff546770f) | agent:controller-01 | 2026-08-22 | Read-only pinned-source audit | Selective UX and visual-direction ideas; MIT |
| [dietrichgebert/ponytail](https://github.com/dietrichgebert/ponytail/tree/2ed6c52c9d7e5e56942508591085fd45dea277d3) | agent:controller-01 | 2026-08-22 | Read-only pinned-source audit | Minimality ladder only; MIT |
| [anthropics/skills frontend-design](https://github.com/anthropics/skills/tree/3b3fad96af16a10759d930941b4520ba0c40edae/skills/frontend-design) | agent:controller-01 | 2026-08-22 | Read-only pinned-source audit | Intentional visual direction and self-critique; skill-level Apache-2.0 |
| [garrytan/gstack](https://github.com/garrytan/gstack/tree/85fd9db554ae4aaaa6d356d2daf873121ee85bdd) | agent:controller-01 | 2026-08-22 | Read-only pinned-source audit | Report-only browser QA evidence patterns; MIT |

## Pre-change supply-chain intake audit (completed 2026-08-22)
The controller completed these read-only audits at the exact pinned commits **before implementation began**. Local read-only audit reports were historical development evidence only and are deliberately not referenced here because local filesystem paths are not public-safe. The pinned GitHub links below are the public evidence. Every intake decision was **PASS to proceed with manual, selective adaptation only**: no installer ran, no upstream code or vendor runtime executed, and no upstream code, binary, font, dataset, hook, plugin, package, or lockfile was installed or copied. This intake PASS is not the independent final security-review verdict; that review remains PENDING in `reviews.md`.

Each external source now also carries an offline-verifiable attestation in both manifest and lock: repository URL/identity, resolved immutable commit, repository-relative license blob path, SHA-256 of the audited license bytes, audit date, and reviewer identity. The final security-review audit independently reverified source reachability, pinned repository identity, and license bytes against the read-only pinned checkouts; because this blocker fix changes the candidate, the formal verdict in `reviews.md` correctly remains PENDING for re-review. CI validates attestation shape and manifest/lock consistency only and performs no live network call.

### Superpowers
- **Source/revision/license evidence:** [repository at `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`](https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797); [MIT `LICENSE`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/LICENSE).
- **Selectively adapted pattern:** short option generation, explicit comparison, convergence, and approval boundary for `brainstorm-and-converge`; ideas were rewritten for this repository's lifecycle.
- **Scripts/binaries and hooks/tools audited:** shell/command hooks including session start, plugin adapters for multiple agent harnesses, TypeScript/JavaScript/Python helpers, tests/evals, and a visual brainstorming server. The package declares no production dependency list, but its harness plugins and scripts are runtime surfaces.
- **Network/secret/write scope:** upstream integrations can execute commands, write configuration/worktree state, start local services, and invoke browser/network flows; secret handling depends on the host harness. None of those surfaces are used here.
- **Transitive dependencies/exclusions:** no upstream package or transitive dependency is inherited. All hooks, plugin loaders, visual companion/server, worktree automation, subagent dispatch, installers, evals, and runtime bootstrap are excluded.
- **Risk/update/rollback:** medium upstream-runtime risk reduced to low reference-only prose risk. Updates require a new immutable commit, repeated license/scope audit, manifest/lock review, and independent security review. Rollback removes the adapted prose/provenance entry and restores the prior manifest/lock together.

### UI UX Pro Max
- **Source/revision/license evidence:** [repository at `bc826e2267a36d98a2dcf5231e16c30ff546770f`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/bc826e2267a36d98a2dcf5231e16c30ff546770f); [MIT `LICENSE`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/bc826e2267a36d98a2dcf5231e16c30ff546770f/LICENSE).
- **Selectively adapted pattern:** UX journey/state coverage, intentional visual direction, responsive considerations, and design-system checks for `ux-product-design` and `frontend-design-direction`.
- **Scripts/binaries and hooks/tools audited:** Python and CommonJS generators/validators, search and rendering scripts, CLI/installer/plugin metadata, large CSV knowledge datasets, templates, and bundled font binaries.
- **Network/secret/write scope:** upstream fetch/generation tooling can access the network and write generated design assets, tokens, and code; installer/plugin execution can modify host configuration. No secret access is required by the adapted prose and no upstream tool runs here.
- **Transitive dependencies/exclusions:** all CLI/runtime dependencies and their transitives are excluded; no package manager install occurs. The engine, datasets, templates, bundled fonts/binaries, fetchers, generators, validators, installers, hooks/plugins, and auto-implementation behavior are excluded.
- **Risk/update/rollback:** medium due to broad generation/runtime and binary/data surface, reduced to low for manual reference-only adaptation. Update only by newly pinned commit plus repeat audit and lock review. Roll back both adapted prose entries and corresponding provenance/lock records.

### Ponytail
- **Source/revision/license evidence:** [repository at `2ed6c52c9d7e5e56942508591085fd45dea277d3`](https://github.com/dietrichgebert/ponytail/tree/2ed6c52c9d7e5e56942508591085fd45dea277d3); [MIT `LICENSE`](https://github.com/dietrichgebert/ponytail/blob/2ed6c52c9d7e5e56942508591085fd45dea277d3/LICENSE).
- **Selectively adapted pattern:** only the staged minimality ladder—reuse/configure before extending or building—for `implementation-minimality`.
- **Scripts/binaries and hooks/tools audited:** JavaScript and shell/PowerShell hooks, multi-harness plugins/rules, MCP and Pi extension packages, mode/status tracking, uninstall script, benchmarks, and test/eval tooling.
- **Network/secret/write scope:** upstream hooks/plugins can execute automatically, inspect or modify repository/session state, write mode/status data, invoke subagents, and use network-backed model/eval paths; host credentials may be visible to those runtimes. None is used here.
- **Transitive dependencies/exclusions:** no npm/Python/MCP package or transitive dependency is inherited. Plugin runtime, hooks, modes, MCP server, extensions, status line, subagent behavior, benchmarks/evals, installer/uninstaller, and automatic enforcement are excluded.
- **Risk/update/rollback:** high if installed as an active hook/plugin, reduced to low as rewritten guidance. A new revision requires repeat hook/runtime audit and security review. Rollback removes the minimality wording and provenance/lock entry atomically.

### Anthropic frontend-design
- **Source/revision/license evidence:** [skill at `3b3fad96af16a10759d930941b4520ba0c40edae`](https://github.com/anthropics/skills/tree/3b3fad96af16a10759d930941b4520ba0c40edae/skills/frontend-design); [skill-level Apache-2.0 `LICENSE.txt`](https://github.com/anthropics/skills/blob/3b3fad96af16a10759d930941b4520ba0c40edae/skills/frontend-design/LICENSE.txt).
- **Selectively adapted pattern:** subject-grounded visual direction, deliberate typography/layout, a compact token plan, restraint, responsive/accessibility checks, and self-critique for `frontend-design-direction`.
- **Scripts/binaries and hooks/tools audited:** the selected skill consists of Markdown guidance plus its license; it declares no executable script, binary, hook, tool, or package manifest in that skill directory.
- **Network/secret/write scope:** none intrinsic to the selected source text; any later code/image/browser action belongs to the host task and its separately declared tools/side effects, not this reference.
- **Transitive dependencies/exclusions:** no direct or transitive runtime dependency is inherited. Other Anthropic repository skills, fonts/assets, templates, generators, and unrelated runtime instructions are excluded.
- **Risk/update/rollback:** low reference-text risk, with prompt-scope drift as the main concern. Updates require a newly pinned commit and skill-level license/content review. Rollback removes the adapted design-direction wording and its provenance/lock record.

### gstack
- **Source/revision/license evidence:** [repository at `85fd9db554ae4aaaa6d356d2daf873121ee85bdd`](https://github.com/garrytan/gstack/tree/85fd9db554ae4aaaa6d356d2daf873121ee85bdd); [MIT `LICENSE`](https://github.com/garrytan/gstack/blob/85fd9db554ae4aaaa6d356d2daf873121ee85bdd/LICENSE).
- **Selectively adapted pattern:** bounded, report-only browser QA matrix, screenshots/reproduction evidence, and explicit no-auto-fix/no-auto-commit behavior for `visual-browser-qa`.
- **Scripts/binaries and hooks/tools audited:** Bun/TypeScript and shell CLI fleet, browser server/client, Playwright-patched runtime, extension code, analytics/telemetry, egress helpers, redaction/pre-push hooks, background jobs, local/remote browser support, and generated binaries.
- **Network/secret/write scope:** upstream can browse arbitrary pages, expose local services through ngrok, send telemetry/egress, read browser/session data, execute commands, write artifacts/configuration, and interact with credentials present in target pages. This repository uses only its own explicitly gated browser QA contract.
- **Transitive dependencies/exclusions:** direct packages (`playwright`, `@ngrok/ngrok`, `@huggingface/transformers`, `cross-spawn`, `diff`, `html-to-docx`, `marked`, `socks`) and all transitives/dev dependencies are excluded. No Bun install, patched Playwright, binaries, server, extension, telemetry, hooks, auto-fix, commit, or runtime plumbing is included.
- **Risk/update/rollback:** high upstream runtime/network/credential surface, reduced to low-to-medium for a report-only prose adaptation whose actual browser use remains explicit and gated. Updates require newly pinned source, dependency/egress review, and independent security review. Rollback removes the QA wording and provenance/lock entry; generated QA evidence is retained or deleted per the owning feature's policy.

## Intake decision and boundaries
- **Decision:** PASS on 2026-08-22 to proceed with manual selective adaptation from the five pinned references.
- **Boundary:** references only; no upstream code/vendor runtime installed, no installer or external code executed, and no upstream dependencies inherited.
- **Final review:** independent quality and security reviews remain PENDING and must not treat this pre-change intake PASS as their verdict.
- **Update policy:** never follow a branch/tag implicitly. Pin a new 40-character commit, repeat license/script/binary/hook/tool/dependency/side-effect audit, update manifest and lock together, rerun focused/full validation, and obtain independent review.
- **Rollback:** revert the affected skill prose plus manifest and lock provenance as one unit; never leave a stale lock or undeclared skill.

## Actors and workflows
Existing orchestrator, architect, implementer, code reviewer, security reviewer, accessibility reviewer, and verifier own the relevant skills. No new agent is needed.

## Constraints and dependencies
- Preserve the canonical lifecycle and current validator behavior.
- Use existing PyYAML; no JSON Schema runtime dependency.
- Public repository artifacts cannot contain private paths, domains, secrets, or infrastructure.

## Risks and assumptions
- Selective adaptation can drift into implied vendoring; explicit adaptation statements prevent this.
- Hashes must be regenerated only when the reviewed SKILL.md changes.

## Open questions
| Question | Owner | Due | Status |
|---|---|---|---|
| Is an ADR required? | agent:architect-01 | 2026-08-23 | Resolved: no architecture boundary change |

Unknown facts remain explicitly unresolved. Discovery records the completed pre-change intake decision but does not select architecture or authorize implementation by itself.
