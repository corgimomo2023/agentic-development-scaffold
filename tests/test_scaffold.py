from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_lightweight_scaffold_paths_exist():
    required = {
        "AGENTS.md",
        "README.md",
        ".github/copilot-instructions.md",
        ".github/workflows/validate-scaffold.yml",
        "docs/README.md",
        "docs/workflows/agentic-ai-workflow.md",
        "docs/features/active.md",
        "docs/features/_template/feature.md",
        "docs/features/_template/plan.md",
        "docs/features/_template/status.md",
        "workflows/low-risk.md",
        "workflows/standard.md",
        "workflows/elevated.md",
    }
    missing = [path for path in required if not (ROOT / path).is_file()]
    assert not missing


def test_three_risk_lanes_replace_numbered_lifecycle():
    workflow_paths = {path.name for path in (ROOT / "workflows").glob("*.md")}
    assert {"low-risk.md", "standard.md", "elevated.md"} <= workflow_paths
    assert not list((ROOT / "workflows").glob("[0-9][0-9]-*.md"))


def test_agent_contract_is_github_first_and_human_governed():
    contract = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for marker in ("L0 — low risk", "L1 — standard", "L2 — elevated", "GitHub Issue", "Human approval"):
        assert marker in contract
    assert "INTAKE" not in contract
    assert "knowledge curator" not in contract.lower()


def test_feature_template_is_a_short_handoff_not_a_manifest():
    template = ROOT / "docs/features/_template"
    assert {path.name for path in template.iterdir() if path.is_file()} == {"README.md", "feature.md", "plan.md", "status.md"}
    status = (template / "status.md").read_text(encoding="utf-8")
    for marker in ("Lane:", "State:", "Last verified:", "Next action:", "Blocker / human decision:"):
        assert marker in status


def test_docs_and_wiki_have_separate_roles():
    docs = (ROOT / "docs/README.md").read_text(encoding="utf-8")
    assert "GitHub Issue owns the live checklist" in docs
    assert (ROOT / "wiki").is_dir()
    assert not (ROOT / "wiki/delivery").exists()
