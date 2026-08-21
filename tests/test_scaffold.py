from pathlib import Path
import subprocess
import tomllib

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "AGENTS.md",
    ".github/copilot-instructions.md",
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
    "scripts/validate_scaffold.py",
]

AGENTS = [
    "orchestrator",
    "product-manager",
    "architect",
    "implementation-planner",
    "tdd-developer",
    "test-specialist",
    "security-reviewer",
    "spec-reviewer",
    "code-reviewer",
    "release-verifier",
    "knowledge-curator",
]

PROMPTS = [
    "00-intake",
    "10-proposal",
    "15-discovery",
    "20-design",
    "30-adr",
    "40-plan",
    "50-implement-tdd",
    "60-delegate-subagents",
    "70-spec-review",
    "80-quality-security-review",
    "82-security-review",
    "90-verify-release",
    "95-retrospective",
]


def read_frontmatter(path: Path):
    text = path.read_text()
    assert text.startswith("---\n"), path
    _, frontmatter, body = text.split("---", 2)
    return yaml.safe_load(frontmatter), body


def test_required_lifecycle_files_exist():
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).is_file()]
    assert missing == []


def test_knowledge_control_plane_is_consolidated_under_wiki():
    assert (ROOT / "wiki/product").is_dir()
    assert (ROOT / "wiki/knowledge-base").is_dir()
    assert (ROOT / "wiki/architecture").is_dir()
    assert (ROOT / "wiki/delivery").is_dir()
    assert (ROOT / "wiki/governance").is_dir()
    for legacy_path in (
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
    ):
        assert not (ROOT / legacy_path).exists(), legacy_path


def test_monorepo_scaffold_disables_python_package_auto_discovery():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert config["tool"]["setuptools"]["packages"] == []


@pytest.mark.parametrize("name", AGENTS)
def test_agent_profiles_have_contract(name):
    path = ROOT / ".github/agents" / f"{name}.agent.md"
    assert path.is_file()
    metadata, body = read_frontmatter(path)
    assert metadata["name"] == name
    assert metadata["description"]
    assert isinstance(metadata["tools"], list)
    assert set(metadata["tools"]) <= {"read", "search", "edit", "execute"}
    for heading in ("## Responsibilities", "## Inputs", "## Outputs", "## Guardrails", "## Handoff"):
        assert heading in body


@pytest.mark.parametrize("name", PROMPTS)
def test_prompt_files_are_agent_ready(name):
    path = ROOT / ".github/prompts" / f"{name}.prompt.md"
    assert path.is_file()
    metadata, body = read_frontmatter(path)
    assert metadata["description"]
    assert metadata["agent"]
    assert "## Inputs" in body
    assert "## Required output" in body
    assert "## Stop conditions" in body


def test_path_instructions_declare_apply_to():
    paths = sorted((ROOT / ".github/instructions").glob("*.instructions.md"))
    assert len(paths) >= 4
    for path in paths:
        metadata, body = read_frontmatter(path)
        assert metadata["applyTo"]
        assert body.strip()


def test_feature_control_plane_contracts():
    required = [
        "wiki/governance/exception-policy.md",
        "wiki/governance/traceability-policy.md",
        "wiki/delivery/templates/feature/manifest.yaml",
        "wiki/delivery/templates/feature/delegations.yaml",
        "wiki/delivery/templates/feature/reviews.md",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    assert missing == []

    manifest = yaml.safe_load((ROOT / required[2]).read_text())
    assert manifest["schema_version"] == 1
    assert manifest["lifecycle_state"]
    assert set(manifest["owners"]) >= {
        "orchestrator",
        "implementer",
        "spec_reviewer",
        "quality_reviewer",
        "security_reviewer",
        "verifier",
    }
    assert manifest["gates"]
    required_gate_fields = {
        "owner",
        "checked_inputs",
        "result",
        "evidence",
        "failure_reason",
        "next_transition",
    }
    for gate in manifest["gates"].values():
        assert set(gate) == required_gate_fields
        assert gate["result"] in {"PENDING", "PASS", "FAIL", "EXCEPTED"}
    assert set(manifest["evidence"]) >= {"tdd_cycles", "full_suite", "verification"}
    assert (ROOT / "wiki/delivery/templates/feature/exceptions.json").is_file()

    delegations = yaml.safe_load((ROOT / required[3]).read_text())
    required_delegation_fields = {
        "delegation_id",
        "task_id",
        "role",
        "goal",
        "authoritative_context",
        "allowed_files",
        "allowed_tools",
        "allowed_side_effects",
        "non_goals",
        "acceptance_criteria",
        "verification_commands",
        "required_return_fields",
        "stop_conditions",
    }
    for delegation in delegations["delegations"]:
        assert set(delegation) == required_delegation_fields
        assert {
            "status",
            "files_changed",
            "commands_run",
            "evidence",
            "risks_or_unknowns",
            "recommended_next_state",
        } <= set(delegation["required_return_fields"])


def test_tdd_and_verification_templates_capture_replayable_evidence():
    tasks = (ROOT / "wiki/delivery/templates/feature/tasks.md").read_text()
    for field in (
        "Exact command",
        "Expected RED failure",
        "Actual RED result / exit status",
        "GREEN result / exit status",
        "Full-suite evidence",
        "Environment",
        "Artifact/link",
        "Recorded by",
        "Timestamp",
    ):
        assert field in tasks

    verification = (ROOT / "wiki/delivery/templates/feature/verification.md").read_text()
    assert "Timestamp" in verification


def test_quality_handoff_requires_independent_security_pass():
    reviewer = (ROOT / ".github/agents/code-reviewer.agent.md").read_text()
    assert "security review" in reviewer.lower()
    assert "security PASS" in reviewer
    assert "PASS goes to verification" not in reviewer


def test_validator_accepts_repository():
    result = subprocess.run(
        ["python3", "scripts/validate_scaffold.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "VALIDATION PASS" in result.stdout
