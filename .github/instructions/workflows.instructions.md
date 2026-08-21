---
applyTo: ".github/workflows/**,scripts/**"
---

Use least-privilege permissions, pinned major action versions, deterministic commands, explicit failure handling, and no inline secrets. Validation must fail closed. Scripts must return non-zero on failure and must not print credentials or claim success from status codes alone.
