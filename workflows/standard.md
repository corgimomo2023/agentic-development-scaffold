# L1 — standard

Use for normal features, bug fixes, and non-sensitive UI changes.

1. Create or confirm a GitHub Issue. State outcome, scope, non-goals, and acceptance.
2. For a durable feature, add `docs/features/<id>/feature.md` and a focused `plan.md`.
3. For UI work, agree the look-and-feel / interaction prototype before functional migration.
4. Implement the smallest vertical slice and add relevant tests or visual evidence.
5. Update `status.md` with the exact next action, last verified command, and blocker/decision.
6. Open a PR with test/CI evidence and one independent review. A human decides merge.

Do not require PM, architect, separate test specialist, release verifier, retrospective, or knowledge curator by default.
