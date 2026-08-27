# Feature documentation template

Copy this folder only for durable L1/L2 work. L0 normally needs only its GitHub Issue and PR.

- `feature.md` — intent, scope, non-goals, feature acceptance, and use cases.
- `plan.md` — smallest implementation route, files, tests, and focused risk controls.
- `status.md` — the only current-state / resume file; update only at handoff, blocked, or PR-ready boundaries.

## Relationship model

- **Feature** is a user/operational capability, identified as `FTR-xxx`.
- **Use case** is a behavioral scenario inside `feature.md`; it can span more than one delivery story.
- **Story** is an independently deliverable work slice in GitHub. Its `[ ]` / `[x]` checklist stays in the Issue; link it from `feature.md`, do not create a duplicate file or checklist here.

Create `decision.md`, `threat-model.md`, migration notes, or prototype evidence only when the selected lane needs them.
