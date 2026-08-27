# Agentic Development Scaffold

A small, GitHub-first repository scaffold for AI-assisted delivery with human merge control.

## Default path

```text
Issue / intent → plan → change + relevant tests → PR + CI + review → human merge
```

Choose [L0, L1, or L2](workflows/README.md) from the real risk. Do not force every change through a role chain.

## Repository map

- `AGENTS.md` — the operating contract for people and agents.
- `docs/` — project documentation, feature handoff, architecture, governance, and runbooks.
- `wiki/` — linked reusable knowledge only; not a live delivery tracker.
- `.github/` — lightweight GitHub issue/PR templates, optional specialist agents, prompts, CI, and skills.
- `workflows/` — the three risk-lane paths.
- `apps/`, `packages/` — product code when real consumers exist.
- `scripts/`, `tests/` — scaffold validation.

## Start

1. Create a GitHub Issue for the intended outcome and live checklist.
2. Pick the lowest appropriate lane.
3. For an L1/L2 feature, copy `docs/features/_template/` to a feature ID folder.
4. Work in a branch, run relevant checks, open a PR, and let a human merge.

Run the scaffold baseline before a PR that changes scaffold contracts:

```bash
uv run --frozen --extra test python scripts/validate_scaffold.py
uv run --frozen --extra test pytest
```

## Authority

Agents may research, propose, edit, test, and review within approved scope. Humans decide scope changes, material risk, merge, release, deployment, destructive actions, and credentials.

## License

MIT. See `LICENSE`.
