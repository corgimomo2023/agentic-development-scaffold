# Agentic AI workflow

This page is the single map of how a human and AI agents deliver work in this repository. It does not replace the executable risk-lane instructions in [`../../workflows/`](../../workflows/README.md).

## Default path

```text
Human request / GitHub Issue
→ feature definition (L1/L2 when durable)
→ focused plan
→ smallest vertical implementation
→ deterministic verification
→ independent review
→ GitHub PR + CI evidence
→ human merge decision
```

The order is deliberate: **feature intent comes before plan**. A plan answers how to deliver an agreed outcome; it must not invent the outcome.

## Choose one risk lane

| Lane | Use for | Minimum path |
|---|---|---|
| L0 | docs, typo, mechanical maintenance, bounded non-behavioural refactor | change → relevant validation → PR → human merge |
| L1 | normal feature, bug fix, non-sensitive UI work | Issue / feature → plan → implementation + relevant tests → PR/CI + independent review → human merge |
| L2 | auth, PII, payment, migration, public contract, deploy, destructive or costly-to-reverse work | L1 + only the focused security / migration / operations / accessibility / ADR control required by risk |

Read the detailed instructions: [L0](../../workflows/low-risk.md), [L1](../../workflows/standard.md), [L2](../../workflows/elevated.md).

## Feature, use case, story, and task

```text
Feature (FTR-xxx) ── contains ──> use cases
       │
       └── links to ──> delivery stories (GitHub Issues)
                                  │
                                  └── contains ──> [ ] / [x] tasks
```

- **Feature** — a user or operational capability. `feature.md` records intent, scope, non-goals, acceptance, and use cases.
- **Use case** — a behavioral scenario and expected result. It may span multiple delivery stories.
- **Story** — an independently deliverable work slice represented by a GitHub Issue.
- **Task** — a checked/unchecked item in that Issue. The Issue is the live task source of truth.

A feature is **merged** when its revision lands, but **accepted** only when its feature-level acceptance is confirmed. `docs/features/active.md` keeps merged-but-not-accepted features visible.

## Agent responsibilities

| Role | May do | Must not do |
|---|---|---|
| Builder | read authoritative context, select lane, make the smallest change, run checks, provide evidence | merge, deploy, accept risk, invent scope |
| Reviewer | independently test the candidate against intent, diff, and evidence | author the revision it approves, merge |
| Security reviewer (L2 only) | assess trust boundaries, data exposure, authorization, secret handling, and residual risk | waive material risk, merge, deploy |
| Human | clarify intent, resolve blockers, accept residual risk, approve merge/release | delegate final authority away |

Agent contracts: [builder](../../.github/agents/builder.agent.md), [reviewer](../../.github/agents/reviewer.agent.md), [security reviewer](../../.github/agents/security-reviewer.agent.md).

## Evidence and state placement

| What changes | Where it goes | When to update |
|---|---|---|
| Live task completion | GitHub Issue checklist | Whenever task state changes |
| Feature state / handoff | `docs/features/FTR-xxx/status.md` | Handoff, blocked, or PR-ready only |
| Stage / POC acceptance | `docs/product/roadmap.md` | When feature acceptance changes |
| Commands, CI, review, residual risk | GitHub PR | During review |
| Consequential decision | ADR | When a durable decision is accepted |

Do not create a chronological agent activity log. The Issue, PR, CI, and Git history already hold the evidence; `status.md` is a concise resume bookmark.

## Stop conditions

Agents stop and ask a human when scope, authority, credentials, environment access, or a risk decision is missing. They also stop for an unresolved high-severity finding or a requested irreversible action.

No agent may auto-merge, auto-deploy, auto-publish, self-prioritize work, or expand scope without human approval.
