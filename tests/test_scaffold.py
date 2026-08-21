from pathlib import Path
import re
import subprocess
import tomllib

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "AGENTS.md",
    ".github/copilot-instructions.md",
    ".github/dependabot.yml",
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
    "discovery-analyst",
    "architect",
    "implementation-planner",
    "tdd-developer",
    "debugger",
    "test-specialist",
    "accessibility-reviewer",
    "security-reviewer",
    "spec-reviewer",
    "code-reviewer",
    "operational-readiness-reviewer",
    "release-verifier",
    "knowledge-curator",
]

AGENT_TOOLS = {
    "orchestrator": ["read", "search", "agent", "todo"],
    "product-manager": ["read", "search"],
    "discovery-analyst": ["read", "search", "web"],
    "architect": ["read", "search"],
    "implementation-planner": ["read", "search"],
    "tdd-developer": ["read", "search", "edit", "execute"],
    "debugger": ["read", "search", "edit", "execute"],
    "test-specialist": ["read", "search", "edit", "execute"],
    "accessibility-reviewer": ["read", "search", "execute"],
    "security-reviewer": ["read", "search", "execute"],
    "spec-reviewer": ["read", "search", "execute"],
    "code-reviewer": ["read", "search", "execute"],
    "operational-readiness-reviewer": ["read", "search", "execute"],
    "release-verifier": ["read", "search", "execute"],
    "knowledge-curator": ["read", "search", "edit", "execute"],
}

PROMPTS = [
    "00-intake",
    "10-proposal",
    "15-discovery",
    "20-design",
    "25-threat-model",
    "30-adr",
    "40-plan",
    "45-test-strategy",
    "50-implement-tdd",
    "55-debug",
    "60-delegate-subagents",
    "70-spec-review",
    "80-quality-security-review",
    "82-security-review",
    "85-operational-readiness",
    "90-verify-release",
    "92-knowledge-writeback",
    "95-retrospective",
]

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

AGENT_SECTIONS = (
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

PROMPT_SECTIONS = (
    "## Inputs",
    "## Preconditions",
    "## Procedure",
    "## Required output",
    "## Validation",
    "## Stop conditions",
)


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
    assert "*.egg-info/" in (ROOT / ".gitignore").read_text()


@pytest.mark.parametrize("name", AGENTS)
def test_agent_profiles_have_contract(name):
    path = ROOT / ".github/agents" / f"{name}.agent.md"
    assert path.is_file()
    metadata, body = read_frontmatter(path)
    assert metadata["name"] == name
    assert metadata["description"]
    assert metadata["tools"] == AGENT_TOOLS[name]
    assert "target" not in metadata  # portable across GitHub and supported IDE surfaces
    assert len(body.splitlines()) >= 60
    for heading in AGENT_SECTIONS:
        assert heading in body


@pytest.mark.parametrize("name", PROMPTS)
def test_prompt_files_are_agent_ready(name):
    path = ROOT / ".github/prompts" / f"{name}.prompt.md"
    assert path.is_file()
    metadata, body = read_frontmatter(path)
    assert metadata["name"] == name
    assert metadata["description"]
    assert metadata["agent"] == PROMPT_AGENTS[name]
    assert metadata["argument-hint"]
    assert len(body.splitlines()) >= 40
    for heading in PROMPT_SECTIONS:
        assert heading in body


def test_customization_catalogs_are_exact_not_minimum_counts():
    agent_files = {
        path.name.removesuffix(".agent.md")
        for path in (ROOT / ".github/agents").glob("*.agent.md")
    }
    prompt_files = {
        path.name.removesuffix(".prompt.md")
        for path in (ROOT / ".github/prompts").glob("*.prompt.md")
    }
    assert agent_files == set(AGENT_TOOLS)
    assert prompt_files == set(PROMPT_AGENTS)


def test_source_hierarchy_and_lifecycle_match_root_contract():
    agents = (ROOT / "AGENTS.md").read_text()
    copilot = (ROOT / ".github/copilot-instructions.md").read_text()
    assert CANONICAL_LIFECYCLE in agents
    assert CANONICAL_LIFECYCLE in copilot
    assert copilot.index("Approved feature package") < copilot.index("Root `AGENTS.md`")
    assert copilot.index("Accepted ADRs") < copilot.index("Root `AGENTS.md`")


def test_early_phase_prompts_do_not_block_on_outputs_they_create():
    cases = {
        "00-intake": "Do not block merely because proposal scope or acceptance criteria do not exist yet.",
        "10-proposal": "Do not block merely because scope or acceptance criteria do not exist yet; creating them is this prompt's job.",
        "15-discovery": "Do not require feature acceptance criteria to begin evidence gathering.",
    }
    for name, required in cases.items():
        text = (ROOT / ".github/prompts" / f"{name}.prompt.md").read_text()
        assert required in text
        assert "Stop if scope, acceptance criteria, canonical source, or authority is missing." not in text


def test_read_only_roles_handoff_mutation_and_execution_evidence():
    adr = (ROOT / ".github/prompts/30-adr.prompt.md").read_text()
    discovery = (ROOT / ".github/agents/discovery-analyst.agent.md").read_text()
    discovery_prompt = (ROOT / ".github/prompts/15-discovery.prompt.md").read_text()
    assert "ADR draft" in adr
    assert "knowledge-curator" in adr
    assert "Write or update a numbered ADR" not in adr
    assert "update the raw index" not in discovery
    assert "Search repository history" not in discovery
    assert "Store raw evidence" not in discovery
    assert "knowledge-curator" in discovery
    assert "If `web` is unavailable" in discovery_prompt
    for agent in (
        "product-manager",
        "discovery-analyst",
        "architect",
        "implementation-planner",
    ):
        assert "execute" not in AGENT_TOOLS[agent]


def test_post_release_writeback_does_not_mutate_verified_candidate():
    prompt = (ROOT / ".github/prompts/92-knowledge-writeback.prompt.md").read_text()
    curator = (ROOT / ".github/agents/knowledge-curator.agent.md").read_text()
    assert "post-release" in prompt.lower()
    assert "must not alter the released revision" in prompt
    assert "new documentation-only candidate" in prompt
    assert "inclusion in the release candidate" not in curator


def test_path_instructions_declare_apply_to():
    paths = sorted((ROOT / ".github/instructions").glob("*.instructions.md"))
    assert {path.name.removesuffix(".instructions.md") for path in paths} == INSTRUCTIONS
    for path in paths:
        metadata, body = read_frontmatter(path)
        assert metadata["applyTo"]
        assert body.strip()


def test_github_customization_catalogs_are_documented():
    for path in (
        ROOT / ".github/agents/README.md",
        ROOT / ".github/prompts/README.md",
        ROOT / ".github/instructions/README.md",
    ):
        assert path.is_file()
        text = path.read_text()
        assert len(text.splitlines()) >= 25


def test_repository_instructions_cover_monorepo_and_agentic_controls():
    text = (ROOT / ".github/copilot-instructions.md").read_text().lower()
    for phrase in (
        "source-of-truth",
        "apps/",
        "packages/",
        "wiki/",
        "red-green-refactor",
        "independent review",
        "human approval",
        "verification evidence",
        "public repository",
    ):
        assert phrase in text
    assert len(text.splitlines()) >= 100


def test_validation_workflow_is_least_privilege_and_supply_chain_pinned():
    text = (ROOT / ".github/workflows/validate-scaffold.yml").read_text()
    assert "permissions:\n  contents: read" in text
    assert "concurrency:" in text
    assert "timeout-minutes:" in text
    assert "persist-credentials: false" in text
    uses = re.findall(r"uses:\s+([^\s#]+)", text)
    assert uses
    for action in uses:
        assert re.search(r"@[0-9a-f]{40}$", action), action


def test_dependabot_maintains_actions_and_python_dependencies():
    config = yaml.safe_load((ROOT / ".github/dependabot.yml").read_text())
    ecosystems = {entry["package-ecosystem"] for entry in config["updates"]}
    assert ecosystems == {"github-actions", "pip"}
    for entry in config["updates"]:
        assert entry["schedule"]["interval"] == "monthly"
        assert entry["open-pull-requests-limit"] <= 5


def test_pull_request_template_requires_evidence_and_independent_gates():
    text = (ROOT / ".github/pull_request_template.md").read_text().lower()
    for phrase in (
        "why this change is needed",
        "explicitly excluded",
        "red",
        "focused green",
        "specification review pass",
        "security review pass",
        "accessibility review pass",
        "operational-readiness review pass",
        "public repository safety",
        "rollback",
        "human decisions",
    ):
        assert phrase in text


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
