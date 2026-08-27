import importlib.util
from pathlib import Path

VALIDATOR_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_scaffold.py"
SPEC = importlib.util.spec_from_file_location("validate_scaffold", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def test_forbidden_scanner_catches_public_safety_shapes():
    samples = [
        "gh" + "p_" + "a" * 24,
        "BEGIN " + "PRIVATE KEY",
        "/" + "home" + "/private-user/work",
        ".".join(("10", "0", "0", "1")),
    ]
    for sample in samples:
        assert VALIDATOR.find_forbidden(sample), sample


def test_forbidden_scanner_allows_clear_placeholders():
    assert VALIDATOR.find_forbidden("API_KEY=${API_KEY}\nTOKEN={{TOKEN}}") == []


def test_validator_accepts_current_lightweight_contract():
    assert VALIDATOR.main() == 0
