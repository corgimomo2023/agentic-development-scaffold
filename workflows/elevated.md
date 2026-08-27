# L2 — elevated

Use for auth/authorization, PII, payments, schema or data migration, public API/event contracts, production/deploy, destructive action, or a consequential architecture choice.

Follow L1, plus only the targeted control that matches the risk:

- threat model / security review for trust boundaries;
- migration, compatibility, backup, and rollback plan for data changes;
- operations review for deploy, infrastructure, capacity, or observability changes;
- accessibility review for material user-facing interaction changes;
- ADR for durable decisions with alternatives and a high reversal cost.

The PR records the specialist evidence, residual risk, and explicit human decision. Human approval is required before merge and any release/deploy action.
