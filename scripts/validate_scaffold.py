#!/usr/bin/env python3
"""Validate scaffold structure, contracts, links, and public-repository safety."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "AGENTS.md",
    ".github/copilot-instructions.md",
    ".github/dependabot.yml",
    ".github/agents/README.md",
    ".github/prompts/README.md",
    ".github/instructions/README.md",
    ".github/workflows/validate-scaffold.yml",
    "apps/README.md",
    "packages/README.md",
    "wiki/README.md",
    "wiki/SCHEMA.md",
    "wiki/architecture/decisions/README.md",
    "wiki/index.md",
    "wiki/log.md",
    "wiki/raw/index.md",
    "wiki/delivery/features/README.md",
    "wiki/guides/lifecycle/state-machine.md",
    "wiki/guides/lifecycle/gates.md",
    "wiki/guides/lifecycle/delegation.md",
    "wiki/governance/exception-policy.md",
    "wiki/governance/security.md",
    "wiki/governance/traceability-policy.md",
    "wiki/delivery/templates/feature/manifest.yaml",
    "wiki/delivery/templates/feature/discovery.md",
    "wiki/delivery/templates/feature/delegations.yaml",
    "wiki/delivery/templates/feature/exceptions.json",
    "wiki/delivery/templates/feature/reviews.md",
    "workflows/00-intake.md",
    "workflows/10-proposal.md",
    "workflows/20-discovery.md",
    "workflows/30-design-and-adr.md",
    "workflows/40-plan-and-tasks.md",
    "workflows/50-tdd-implementation.md",
    "workflows/60-review.md",
    "workflows/70-verification.md",
    "workflows/80-release.md",
    "workflows/90-retrospective.md",
    ".github/prompts/15-discovery.prompt.md",
}

AGENT_HEADINGS = (
    "## Mission",
    "## When to use this agent",
    "## Responsibilities",
    "## Inputs",
    "## Workflow",
    "## Decision rules",
    "## Output contract",
    "## Guardrails",
    "## Handoff",
    "## Completion criteria",
)
PROMPT_HEADINGS = (
    "## Inputs",
    "## Preconditions",
    "## Procedure",
    "## Required output",
    "## Validation",
    "## Stop conditions",
)
AGENT_TOOLS = {
    "orchestrator": "['read', 'search', 'agent', 'todo']",
    "product-manager": "['read', 'search']",
    "discovery-analyst": "['read', 'search', 'web']",
    "architect": "['read', 'search']",
    "implementation-planner": "['read', 'search']",
    "tdd-developer": "['read', 'search', 'edit', 'execute']",
    "debugger": "['read', 'search', 'edit', 'execute']",
    "test-specialist": "['read', 'search', 'edit', 'execute']",
    "accessibility-reviewer": "['read', 'search', 'execute']",
    "security-reviewer": "['read', 'search', 'execute']",
    "spec-reviewer": "['read', 'search', 'execute']",
    "code-reviewer": "['read', 'search', 'execute']",
    "operational-readiness-reviewer": "['read', 'search', 'execute']",
    "release-verifier": "['read', 'search', 'execute']",
    "knowledge-curator": "['read', 'search', 'edit', 'execute']",
}
PROMPT_AGENTS = {
    "00-intake": "orchestrator",
    "10-proposal": "product-manager",
    "15-discovery": "discovery-analyst",
    "20-design": "architect",
    "25-threat-model": "security-reviewer",
    "30-adr": "architect",
    "40-plan": "implementation-planner",
    "45-test-strategy": "test-specialist",
    "50-implement-tdd": "tdd-developer",
    "55-debug": "debugger",
    "60-delegate-subagents": "orchestrator",
    "70-spec-review": "spec-reviewer",
    "80-quality-security-review": "orchestrator",
    "82-security-review": "security-reviewer",
    "85-operational-readiness": "operational-readiness-reviewer",
    "90-verify-release": "release-verifier",
    "92-knowledge-writeback": "knowledge-curator",
    "95-retrospective": "orchestrator",
}
CANONICAL_LIFECYCLE = (
    "intake -> proposal -> discovery -> design/ADR -> plan/tasks -> "
    "TDD implementation -> spec review -> quality/security review -> "
    "verification -> release -> retrospective/knowledge write-back"
)
INSTRUCTIONS = {
    "agents",
    "apps",
    "documentation",
    "packages",
    "prompts",
    "security-sensitive",
    "source",
    "tests",
    "wiki",
    "workflows",
}
WORKFLOW_HEADINGS = ("## Entry criteria", "## Activities", "## Required artifacts", "## Exit evidence", "## Failure and revision")

LEGACY_ROOT_PATHS = (
    "01-product",
    "02-knowledge-base",
    "03-architecture-decisions",
    "04-delivery",
    "raw",
    "docs",
    "governance",
    "SCHEMA.md",
    "index.md",
    "log.md",
)

FORBIDDEN = {
    "private key": re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "generic API secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "personal home path": re.compile(r"/(?:home|Users)/[A-Za-z0-9._-]+/"),
    "private IPv4 address": re.compile(
        r"(?<![0-9])(?:"
        r"10(?:\.(?:25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])){3}|"
        r"192\.168(?:\.(?:25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])){2}|"
        r"172\.(?:1[6-9]|2[0-9]|3[01])(?:\.(?:25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])){2}"
        r")(?![0-9])"
    ),
    "private hostname": re.compile(r"\b[a-z0-9-]+\.(?:internal|local|corp)\b", re.IGNORECASE),
    "credential assignment": re.compile(
        r"\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*['\"]?"
        r"(?!\$\{|\{\{|<|\[)[A-Za-z0-9_./+=-]{16,}",
        re.IGNORECASE,
    ),
}

LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def find_forbidden(text: str) -> list[str]:
    """Return safety-rule labels found in any text artifact."""
    return [label for label, pattern in FORBIDDEN.items() if pattern.search(text)]


def collect_text_files() -> list[tuple[Path, str]]:
    """Read repository text files while excluding generated and VCS state."""
    excluded = {".git", ".venv", ".pytest_cache", "__pycache__"}
    files: list[tuple[Path, str]] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or excluded.intersection(path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        files.append((path, text))
    return files


def validate_exception_records(
    records: object, today: str | None = None
) -> list[str]:
    """Validate machine-readable lifecycle exception records."""
    if not isinstance(records, list):
        return ["exceptions root must be a JSON list"]
    current = date.fromisoformat(today) if today else date.today()
    required = {
        "exception_id",
        "feature_id",
        "gate",
        "scope",
        "reason",
        "risk",
        "approved_by",
        "expires",
        "compensating_controls",
    }
    errors: list[str] = []
    broad_scope = re.compile(
        r"\b(?:entire|whole|full|all|any|every|everything|global|repo|repository|repository-wide)\b",
        re.IGNORECASE,
    )
    for index, record in enumerate(records):
        label = f"exception[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{label}: record must be an object")
            continue
        missing = sorted(key for key in required if not record.get(key))
        if missing:
            errors.append(f"{label}: missing required fields {', '.join(missing)}")
        approver = str(record.get("approved_by", ""))
        if not approver.startswith("human:") or len(approver) <= len("human:"):
            errors.append(f"{label}: a named human approver is required")
        scope = str(record.get("scope", ""))
        if broad_scope.search(scope):
            errors.append(f"{label}: scope is too broad")
        controls = record.get("compensating_controls")
        if not isinstance(controls, list) or not controls or not all(
            isinstance(item, str) and item.strip() for item in controls
        ):
            errors.append(f"{label}: compensating controls are required")
        expiry = str(record.get("expires", ""))
        try:
            expiry_date = date.fromisoformat(expiry)
            if expiry_date < current:
                errors.append(f"{label}: exception is expired")
        except ValueError:
            errors.append(f"{label}: expires must be an ISO date")
        gate = str(record.get("gate", "")).lower()
        documentation_only = re.fullmatch(
            r"(?:one |single )?(?:documentation|docs)-only (?:file|change)(?: [a-z0-9._/-]+)?",
            scope.lower(),
        )
        if ("test" in gate or "tdd" in gate) and not documentation_only:
            errors.append(f"{label}: TDD cannot be waived for executable behavior")
    return errors


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    try:
        _, raw, body = text.split("---", 2)
    except ValueError as exc:
        raise ValueError("unterminated YAML frontmatter") from exc
    metadata: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip("'\"")
    return metadata, body


def validate_links(path: Path, text: str) -> list[str]:
    failures = []
    for target in LINK.findall(text):
        target = target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "{{")):
            continue
        if not (path.parent / target).resolve().exists():
            failures.append(f"{path.relative_to(ROOT)}: broken link {target}")
    return failures


def main() -> int:
    failures: list[str] = []
    for name in sorted(REQUIRED):
        if not (ROOT / name).is_file():
            failures.append(f"missing required file: {name}")

    for name in LEGACY_ROOT_PATHS:
        if (ROOT / name).exists():
            failures.append(f"legacy root path must not exist: {name}")

    text_files = collect_text_files()
    for path, text in text_files:
        rel = path.relative_to(ROOT)
        for label in find_forbidden(text):
            failures.append(f"{rel}: forbidden {label}")

    markdown = [(path, text) for path, text in text_files if path.suffix == ".md"]
    for path, text in markdown:
        rel = path.relative_to(ROOT)
        if not text.strip():
            failures.append(f"{rel}: empty Markdown file")
        failures.extend(validate_links(path, text))

    agents = sorted((ROOT / ".github/agents").glob("*.agent.md"))
    agent_names = {path.name.removesuffix(".agent.md") for path in agents}
    if agent_names != set(AGENT_TOOLS):
        failures.append("custom agent catalog must exactly match the governed role matrix")
    for path in agents:
        try:
            metadata, body = parse_frontmatter(path)
        except ValueError as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        if metadata.get("name") != path.name.removesuffix(".agent.md"):
            failures.append(f"{path.relative_to(ROOT)}: name must match filename")
        if not metadata.get("description"):
            failures.append(f"{path.relative_to(ROOT)}: description is required")
        expected_tools = AGENT_TOOLS.get(path.name.removesuffix(".agent.md"))
        if metadata.get("tools") != expected_tools:
            failures.append(f"{path.relative_to(ROOT)}: tools must match governed least-privilege matrix")
        if len(body.splitlines()) < 60:
            failures.append(f"{path.relative_to(ROOT)}: agent contract must be at least 60 lines")
        for heading in AGENT_HEADINGS:
            if heading not in body:
                failures.append(f"{path.relative_to(ROOT)}: missing {heading}")
    prompts = sorted((ROOT / ".github/prompts").glob("*.prompt.md"))
    prompt_names = {path.name.removesuffix(".prompt.md") for path in prompts}
    if prompt_names != set(PROMPT_AGENTS):
        failures.append("lifecycle prompt catalog must exactly match the governed prompt matrix")
    for path in prompts:
        try:
            metadata, body = parse_frontmatter(path)
        except ValueError as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        prompt_name = path.name.removesuffix(".prompt.md")
        if metadata.get("name") != prompt_name:
            failures.append(f"{path.relative_to(ROOT)}: name must match filename")
        for key in ("description", "argument-hint", "agent"):
            if not metadata.get(key):
                failures.append(f"{path.relative_to(ROOT)}: {key} is required")
        if metadata.get("agent") != PROMPT_AGENTS.get(prompt_name):
            failures.append(f"{path.relative_to(ROOT)}: agent must match governed prompt-role matrix")
        for heading in PROMPT_HEADINGS:
            if heading not in body:
                failures.append(f"{path.relative_to(ROOT)}: missing {heading}")
        if len(body.splitlines()) < 40:
            failures.append(f"{path.relative_to(ROOT)}: prompt contract must be at least 40 lines")

    instructions = sorted((ROOT / ".github/instructions").glob("*.instructions.md"))
    instruction_names = {path.name.removesuffix(".instructions.md") for path in instructions}
    if instruction_names != INSTRUCTIONS:
        failures.append("path-specific instruction catalog must exactly match the governed matrix")
    for path in instructions:
        try:
            metadata, _ = parse_frontmatter(path)
        except ValueError as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        if not metadata.get("applyTo"):
            failures.append(f"{path.relative_to(ROOT)}: applyTo is required")

    for path in sorted((ROOT / "workflows").glob("[0-9][0-9]-*.md")):
        body = path.read_text(encoding="utf-8")
        for heading in WORKFLOW_HEADINGS:
            if heading not in body:
                failures.append(f"{path.relative_to(ROOT)}: missing {heading}")

    features_root = ROOT / "wiki/delivery/features"
    for feature_dir in sorted(path for path in features_root.iterdir() if path.is_dir()):
        manifest = feature_dir / "manifest.yaml"
        exceptions = feature_dir / "exceptions.json"
        if not manifest.is_file():
            failures.append(f"{feature_dir.relative_to(ROOT)}: missing manifest.yaml")
        if not exceptions.is_file():
            failures.append(f"{feature_dir.relative_to(ROOT)}: missing exceptions.json")
            continue
        try:
            records = json.loads(exceptions.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"{exceptions.relative_to(ROOT)}: invalid JSON: {exc.msg}")
            continue
        for error in validate_exception_records(records):
            failures.append(f"{exceptions.relative_to(ROOT)}: {error}")

    contract = (ROOT / "AGENTS.md").read_text(encoding="utf-8") if (ROOT / "AGENTS.md").exists() else ""
    copilot_contract = (ROOT / ".github/copilot-instructions.md").read_text(encoding="utf-8") if (ROOT / ".github/copilot-instructions.md").exists() else ""
    if CANONICAL_LIFECYCLE not in contract or CANONICAL_LIFECYCLE not in copilot_contract:
        failures.append("AGENTS.md and Copilot instructions must share the canonical lifecycle string")
    for phrase in (
        "RED evidence",
        "Spec-compliance reviewer",
        "dispatch packet",
        "Human authority",
        "different assignments",
        "named human approver",
    ):
        if phrase.lower() not in contract.lower():
            failures.append(f"AGENTS.md: missing contract phrase {phrase!r}")

    if failures:
        print("VALIDATION FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(
        f"VALIDATION PASS: {len(markdown)} Markdown files and "
        f"{len(text_files)} text files checked"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
