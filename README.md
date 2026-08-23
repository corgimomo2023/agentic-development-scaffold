# Agentic Development Scaffold

A public-safe, monorepo-ready software delivery scaffold for humans, GitHub Copilot, and other coding agents. It turns an idea into traceable evidence through proposal, discovery, design, ADRs, bite-sized tasks, strict TDD, independent reviews, verification, release, and knowledge write-back.

## What this repository provides

- `AGENTS.md`: repository-wide operating contract for humans and agents.
- `.github/copilot-instructions.md`: comprehensive repository, lifecycle, evidence, safety, and handoff contract.
- `.github/agents/`: [15 specialist profiles](.github/agents/README.md) with least-privilege tools and explicit role boundaries.
- `.github/prompts/`: [18 reusable lifecycle prompts](.github/prompts/README.md) from intake through retrospective.
- `.github/instructions/`: [10 path-specific contracts](.github/instructions/README.md) for apps, packages, wiki, tests, workflows, and customization files.
- `.github/workflows/` and `.github/dependabot.yml`: least-privilege validation plus bounded dependency maintenance.
- `apps/`: independently deployable applications such as web, API, and workers.
- `packages/`: shared libraries, schemas, components, SDKs, and tool configuration.
- `wiki/`: the consolidated product knowledge control plane and its [canonical index](wiki/index.md).
- `workflows/`: the complete delivery lifecycle, with entry/exit gates and evidence.
- `.github/skills/manifest.yaml` and `skills.lock.yaml`: governed, vendor-neutral GitHub Copilot project-skill catalog and immutable provenance/integrity lock. GitHub documents `.github/skills` as a supported project-skill location; this location reference does not confer supply-chain trust on mutable content.
- `scripts/validate_scaffold.py`: zero-dependency structural and safety validator.

## Start a project

1. Use this repository as a template or copy it into a new repository.
2. Create deployable units under `apps/` and shared code under `packages/` only when it has real consumers.
3. Replace the example feature with your first real feature package.
4. Add immutable source material to `wiki/raw/` and register it in `wiki/raw/index.md`.
5. Start with `.github/prompts/00-intake.prompt.md` or the `orchestrator` agent.
6. Do not implement until proposal, design, plan, acceptance criteria, and required ADRs pass their gates.
7. Use strict RED-GREEN-REFACTOR and preserve command output as verification evidence.
8. Run `uv run --frozen --extra test python scripts/validate_scaffold.py` and `uv run --frozen --extra test pytest` before every PR.

Before adding or upgrading any externally sourced skill, run the `skill-supply-chain-review` procedure and pin its public source, full commit, skill-level license, declared side effects, dependencies, update path, and rollback evidence. Sources are selectively adapted references, not vendored runtime code.

## Lifecycle

```mermaid
flowchart LR
  I[Intake] --> P[Proposal]
  P --> D[Discovery]
  D --> A[Design + ADR]
  A --> T[Plan + Tasks]
  T --> R[RED]
  R --> G[GREEN]
  G --> F[Refactor]
  F --> V[Reviews]
  V --> E[Verification]
  E --> L[Release]
  L --> K[Retrospective + Knowledge]
  V -->|revision| T
  E -->|failure| R
```

## Human authority

Agents may analyze, propose, edit, test, and review within an approved task. Humans retain authority over scope, risk acceptance, architecture decisions, credentials, production deployment, destructive actions, and merge approval.

## Copilot surface compatibility

GitHub Copilot cloud agent consumes repository instructions and `.github/agents/*.agent.md` profiles. VS Code local agents additionally discover `.github/prompts/*.prompt.md` as explicit slash commands; current Agent Host cloud runs do not consume prompt files. The Markdown lifecycle under `workflows/` remains the vendor-neutral source, so a workflow is not lost when a Copilot surface lacks prompt-file support.

The design rationale and commit-pinned public repository comparison are recorded in [GitHub Copilot customization research](wiki/knowledge-base/copilot-customization-research.md).

Official references:

- [GitHub: agent skills and supported project-skill locations](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- [GitHub: repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)
- [GitHub: custom agents for Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents)
- [VS Code: prompt files](https://code.visualstudio.com/docs/agent-customization/prompt-files)

## Public repository safety

This template contains no organization-specific domains, credentials, account IDs, host paths, or infrastructure details. Keep project secrets in approved secret stores, never Markdown or Git history.

## License

MIT. See `LICENSE`.
