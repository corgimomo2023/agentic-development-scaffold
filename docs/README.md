# Documentation

`docs/` holds durable project documentation. It is not an activity feed or a duplicate of GitHub.

## Where state belongs

| Need | Authoritative location | Update cadence |
|---|---|---|
| Current task / implementation checklist | GitHub Issue | Whenever task state changes |
| PR diff, reviews, CI, merge decision | GitHub PR | During review |
| Stage / POC feature acceptance | [`product/roadmap.md`](product/roadmap.md) | When feature acceptance changes |
| Durable feature intent, plan, resume point | `features/<id>/` | At creation and handoff / blocked / PR-ready |
| Consequential decision | `architecture/decisions/` ADR | When decided |

Do not create an append-only per-agent action log. **GitHub Issue owns the live checklist.** Commands and CI output belong in the PR; `status.md` is only a concise handoff bookmark.
