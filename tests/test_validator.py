import importlib.util
from pathlib import Path

VALIDATOR_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_scaffold.py"
SPEC = importlib.util.spec_from_file_location("validate_scaffold", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def test_forbidden_scanner_covers_non_markdown_secret_shapes():
    samples = [
        "gh" + "p_" + "a" * 24,
        "AK" + "IA" + "A" * 16,
        "BEGIN " + "PRIVATE KEY",
        "/" + "home" + "/private-user/project/file",
    ]
    for sample in samples:
        assert VALIDATOR.find_forbidden(sample), sample


def test_forbidden_scanner_allows_placeholders():
    assert VALIDATOR.find_forbidden("API_KEY=${API_KEY}\nTOKEN={{TOKEN}}") == []


def test_exception_records_require_human_approval_expiry_and_controls():
    valid = {
        "exception_id": "EXC-001",
        "feature_id": "FTR-001",
        "gate": "documentation-validation",
        "scope": "one documentation-only file",
        "reason": "No executable behavior changes",
        "risk": "low",
        "approved_by": "human:repository-owner",
        "expires": "2099-12-31",
        "compensating_controls": ["structural validator"],
    }
    assert VALIDATOR.validate_exception_records([valid], today="2026-08-21") == []

    invalid = dict(valid)
    invalid.update(
        approved_by="agent:orchestrator",
        expires="2020-01-01",
        scope="entire repository",
        compensating_controls=[],
    )
    errors = VALIDATOR.validate_exception_records([invalid], today="2026-08-21")
    assert any("human approver" in error for error in errors)
    assert any("expired" in error for error in errors)
    assert any("scope" in error for error in errors)
    assert any("compensating controls" in error for error in errors)


def test_exception_records_reject_test_gate_and_scope_bypasses():
    base = {
        "exception_id": "EXC-002",
        "feature_id": "FTR-001",
        "gate": "tests",
        "scope": "production code",
        "reason": "Temporary waiver",
        "risk": "high",
        "approved_by": "human:repository-owner",
        "expires": "2099-12-31",
        "compensating_controls": ["manual review"],
    }
    errors = VALIDATOR.validate_exception_records([base], today="2026-08-21")
    assert any("executable behavior" in error for error in errors)

    for gate_name in ("test_gate", "TDD_gate", "unit_test_exception"):
        disguised = dict(base, gate=gate_name)
        errors = VALIDATOR.validate_exception_records([disguised], today="2026-08-21")
        assert any("executable behavior" in error for error in errors), gate_name

    mixed = dict(base, gate="tdd", scope="documentation-only and production code")
    errors = VALIDATOR.validate_exception_records([mixed], today="2026-08-21")
    assert any("executable behavior" in error for error in errors)

    broad = dict(base, gate="documentation-validation", scope="full repo")
    errors = VALIDATOR.validate_exception_records([broad], today="2026-08-21")
    assert any("scope" in error for error in errors)

    across = dict(base, gate="documentation-validation", scope="across the repository")
    errors = VALIDATOR.validate_exception_records([across], today="2026-08-21")
    assert any("scope" in error for error in errors)
