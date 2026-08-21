# Path-specific instruction catalog

Files ending in `.instructions.md` apply automatically to matching paths. They refine the repository-wide contract without creating a second source of truth.

## Instruction map

| File | Applies to | Purpose |
|---|---|---|
| `agents.instructions.md` | custom agent files | role, frontmatter, tools, and gate contracts |
| `prompts.instructions.md` | prompt files | reusable workflow and output contracts |
| `apps.instructions.md` | `apps/**` | independently deployable application boundaries |
| `packages.instructions.md` | `packages/**` | reusable package and dependency boundaries |
| `wiki.instructions.md` | `wiki/**` | canonical knowledge control plane |
| `documentation.instructions.md` | Markdown files | durable writing and link rules |
| `source.instructions.md` | `wiki/raw/**` | immutable evidence and provenance |
| `tests.instructions.md` | test files | behavior, determinism, and regression evidence |
| `workflows.instructions.md` | GitHub Actions | least privilege and untrusted-input safety |
| `security-sensitive.instructions.md` | configuration and automation | safe defaults and trust boundaries |

## Precedence

Always apply the human request, root `AGENTS.md`, repository-wide Copilot instructions, and every matching path-specific instruction. The narrowest applicable rule wins when rules differ. Report unresolved contradictions rather than silently choosing.

## Authoring rules

- Use a precise `applyTo` glob in YAML frontmatter.
- Keep always-on rules short enough to be useful and specific enough to verify.
- Put detailed role workflows in agents and repeatable task workflows in prompts.
- Do not copy full product or architecture knowledge into instruction files; link to the canonical wiki artifact.
- Avoid private project names, domains, accounts, credentials, and local paths.
- Add tests for new structural requirements.
- Update this catalog whenever the instruction set changes.

## Validation

Run:

```bash
python3 scripts/validate_scaffold.py
uv run --extra test pytest -q
```

Inspect Copilot's references in supported clients to confirm the expected instruction files were applied.
