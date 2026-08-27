import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync_active_features.py"
SPEC = importlib.util.spec_from_file_location("sync_active_features", SCRIPT)
assert SPEC is not None
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def _feature(root: Path, feature_id: str, state: str) -> None:
    directory = root / feature_id
    directory.mkdir()
    (directory / "feature.md").write_text(f"# {feature_id} — Example\n", encoding="utf-8")
    (directory / "status.md").write_text(
        f"- Stage: Stage 1 — POC\n- State: {state}\n- GitHub Issue: #12\n- Next action: verify outcome\n",
        encoding="utf-8",
    )


def test_active_feature_index_keeps_merged_until_accepted(tmp_path, monkeypatch):
    features = tmp_path / "docs/features"
    features.mkdir(parents=True)
    _feature(features, "FTR-001", "merged")
    _feature(features, "FTR-002", "accepted")
    _feature(features, "FTR-003", "cancelled")
    monkeypatch.setattr(MODULE, "FEATURES", features)

    rendered = MODULE.render(MODULE.active_features())

    assert "FTR-001" in rendered
    assert "merged" in rendered
    assert "FTR-002" not in rendered
    assert "FTR-003" not in rendered


def test_active_feature_index_has_empty_state(tmp_path, monkeypatch):
    features = tmp_path / "docs/features"
    features.mkdir(parents=True)
    monkeypatch.setattr(MODULE, "FEATURES", features)

    assert "No active features." in MODULE.render(MODULE.active_features())
