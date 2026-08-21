# GitHub Copilot Repository Instructions

Read `AGENTS.md` before acting. Treat approved feature artifacts, accepted ADRs, and architecture baseline as authoritative. Never infer missing product facts; mark them `TBD` with an owner.

Follow the complete lifecycle: proposal -> discovery -> design/ADR -> plan/tasks -> strict TDD -> spec review -> quality/security review -> verification -> human-approved release -> retrospective and knowledge write-back.

For behavior changes, preserve RED evidence before implementation, then GREEN and full-suite evidence. Do not weaken tests to obtain a pass. Keep tasks small, vertical, and traceable to acceptance criteria.

Use specialized agents from `.github/agents/` when appropriate. The orchestrator provides complete dispatch packets and never permits overlapping write scopes. Implementers cannot approve their own work; spec review precedes quality/security review.

Never commit secrets, credentials, personal paths, private infrastructure, or production data. Use placeholders and mocks until approved secret-store access exists. Stop for conflicting requirements, missing authority, destructive operations, production access, or unverifiable state.

Before proposing completion, run:

```bash
python3 scripts/validate_scaffold.py
uv run --extra test pytest
```

Report exact commands, actual results, changed files, residual risks, and the next lifecycle state.
