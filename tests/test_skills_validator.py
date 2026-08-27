import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest
import yaml


VALIDATOR_PATH = Path(__file__).resolve().parents[1] / "scripts/validate_scaffold.py"
SPEC = importlib.util.spec_from_file_location("validate_scaffold", VALIDATOR_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(VALIDATOR)


def _write_catalog(root: Path) -> tuple[dict, dict]:
    skill_path = root / ".agents/skills/example-skill/SKILL.md"
    skill_path.parent.mkdir(parents=True)
    skill_path.write_text(
        "---\nname: example-skill\ndescription: Use when testing the governed skill catalog.\n---\n"
        "# Example\n\n## Trigger\nTest fixtures.\n\n## Anti-trigger\nUnrelated work.\n\n"
        "## Lifecycle insertion\nINTAKE.\n\n## Inputs\n- Request.\n\n## Procedure\n1. Validate.\n\n"
        "## Outputs and evidence\n- Result.\n\n## Guardrails\n- Read only.\n\n## Verification\n- Catalog passes.\n",
        encoding="utf-8",
    )
    source = {
        "url": "https://example.com/reference.git",
        "revision": "a" * 40,
        "license": "MIT",
        "adaptation": "Selective ideas only; no code copied.",
        "license_path": "LICENSE",
        "license_sha256": "b" * 64,
        "verified_at": "2026-08-22",
        "verified_by": "agent:controller-01",
    }
    manifest = {
        "schema_version": 1,
        "skills": [
            {
                "id": "example-skill",
                "path": ".agents/skills/example-skill/SKILL.md",
                "lifecycle_states": ["INTAKE"],
                "owning_agent": "orchestrator",
                "triggers": ["A governed fixture is requested."],
                "anti_triggers": ["The request is unrelated."],
                "required_inputs": ["request"],
                "required_outputs": ["classification"],
                "tools": ["read"],
                "side_effects": [],
                "concurrency": "independent",
                "allow_implicit_invocation": True,
                "provenance": {
                    "origin": "composite",
                    "license": "MIT",
                    "sources": [source],
                },
            }
        ],
    }
    lock = {
        "schema_version": 1,
        "skills": [
            {
                "id": "example-skill",
                "path": ".agents/skills/example-skill/SKILL.md",
                "sha256": hashlib.sha256(skill_path.read_bytes()).hexdigest(),
                "provenance": copy.deepcopy(manifest["skills"][0]["provenance"]),
            }
        ],
    }
    (root / ".agents/skills/manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    (root / ".agents/skills/manifest.schema.json").write_text(
        '{"$schema":"https://json-schema.org/draft/2020-12/schema"}\n', encoding="utf-8"
    )
    (root / "skills.lock.yaml").write_text(yaml.safe_dump(lock, sort_keys=False), encoding="utf-8")
    return manifest, lock


def _save(root: Path, manifest: dict, lock: dict) -> list[str]:
    (root / ".agents/skills/manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    (root / "skills.lock.yaml").write_text(yaml.safe_dump(lock, sort_keys=False), encoding="utf-8")
    return VALIDATOR.validate_skills(root)


def test_skills_catalog_accepts_complete_pinned_catalog(tmp_path):
    _write_catalog(tmp_path)
    assert VALIDATOR.validate_skills(tmp_path) == []


def test_skills_catalog_rejects_hash_mismatch(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    lock["skills"][0]["sha256"] = "0" * 64
    assert any("hash mismatch" in error for error in _save(tmp_path, manifest, lock))


def test_skills_catalog_rejects_mutable_external_revision(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    manifest["skills"][0]["provenance"]["sources"][0]["revision"] = "main"
    lock["skills"][0]["provenance"] = copy.deepcopy(manifest["skills"][0]["provenance"])
    assert any("immutable 40-character" in error for error in _save(tmp_path, manifest, lock))


def test_skills_catalog_rejects_orphan_skill(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    orphan = tmp_path / ".agents/skills/orphan/SKILL.md"
    orphan.parent.mkdir()
    orphan.write_text("---\nname: orphan\ndescription: Orphan.\n---\n# Orphan\n", encoding="utf-8")
    assert any("orphan skill" in error for error in _save(tmp_path, manifest, lock))


def test_skills_catalog_rejects_nested_orphan_skill(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    orphan = tmp_path / ".agents/skills/nested/escape/SKILL.md"
    orphan.parent.mkdir(parents=True)
    orphan.write_text("---\nname: escape\ndescription: Nested orphan.\n---\n# Escape\n", encoding="utf-8")
    assert any("orphan skill .agents/skills/nested/escape/SKILL.md" in error for error in _save(tmp_path, manifest, lock))


def test_skills_catalog_rejects_missing_manifest_declared_skill_file(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    (tmp_path / manifest["skills"][0]["path"]).unlink()
    assert any("missing skill file .agents/skills/example-skill/SKILL.md" in error for error in _save(tmp_path, manifest, lock))


def test_skills_catalog_rejects_lock_entry_missing_sha256(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    del lock["skills"][0]["sha256"]
    assert any("fields must exactly match the lock schema" in error for error in _save(tmp_path, manifest, lock))


def test_skills_catalog_rejects_missing_top_level_provenance_license(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    manifest["skills"][0]["provenance"]["license"] = ""
    lock["skills"][0]["provenance"] = copy.deepcopy(manifest["skills"][0]["provenance"])
    assert any("provenance license is required" in error for error in _save(tmp_path, manifest, lock))


def test_skills_catalog_rejects_missing_external_source_license(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    manifest["skills"][0]["provenance"]["sources"][0]["license"] = ""
    lock["skills"][0]["provenance"] = copy.deepcopy(manifest["skills"][0]["provenance"])
    assert any("sources[0]: license is required" in error for error in _save(tmp_path, manifest, lock))


def test_skills_catalog_rejects_missing_source_attestation(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    del manifest["skills"][0]["provenance"]["sources"][0]["license_sha256"]
    lock["skills"][0]["provenance"] = copy.deepcopy(manifest["skills"][0]["provenance"])

    errors = _save(tmp_path, manifest, lock)

    assert any("source-review attestation fields" in error for error in errors)


def test_skills_catalog_rejects_malformed_source_attestation(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    source = manifest["skills"][0]["provenance"]["sources"][0]
    source.update(
        {
            "license_path": "LICENSE",
            "license_sha256": "NOT-A-HASH",
            "verified_at": "yesterday",
            "verified_by": "controller-01",
        }
    )
    lock["skills"][0]["provenance"] = copy.deepcopy(manifest["skills"][0]["provenance"])

    errors = _save(tmp_path, manifest, lock)

    assert any("license_sha256 must be a lowercase 64-character digest" in error for error in errors)
    assert any("verified_at must be an ISO date or UTC datetime" in error for error in errors)
    assert any("verified_by must be an agent identity" in error for error in errors)


@pytest.mark.parametrize("license_path", ["../LICENSE", "/tmp/LICENSE", "licenses/../../LICENSE", "licenses\\LICENSE"])
def test_skills_catalog_rejects_escaping_or_noncanonical_license_path(tmp_path, license_path):
    manifest, lock = _write_catalog(tmp_path)
    source = manifest["skills"][0]["provenance"]["sources"][0]
    source.update(
        {
            "license_path": license_path,
            "license_sha256": "b" * 64,
            "verified_at": "2026-08-22",
            "verified_by": "agent:controller-01",
        }
    )
    lock["skills"][0]["provenance"] = copy.deepcopy(manifest["skills"][0]["provenance"])

    assert any("license_path must be a safe repository-relative path" in error for error in _save(tmp_path, manifest, lock))


def test_skills_catalog_rejects_duplicate_id_and_path(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    manifest["skills"].append(copy.deepcopy(manifest["skills"][0]))
    lock["skills"].append(copy.deepcopy(lock["skills"][0]))
    errors = _save(tmp_path, manifest, lock)
    assert any("duplicate skill id" in error for error in errors)
    assert any("duplicate skill path" in error for error in errors)


def test_skills_catalog_rejects_unknown_owner_and_lifecycle(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    manifest["skills"][0]["owning_agent"] = "invented-agent"
    manifest["skills"][0]["lifecycle_states"] = ["INVENTED_STATE"]
    errors = _save(tmp_path, manifest, lock)
    assert any("unknown owning_agent" in error for error in errors)
    assert any("unknown lifecycle state" in error for error in errors)


def test_skills_catalog_rejects_undeclared_dangerous_side_effects(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    manifest["skills"][0]["tools"] = ["read", "execute"]
    assert any("execute requires side effect execute_commands" in error for error in _save(tmp_path, manifest, lock))


def test_skills_catalog_rejects_unknown_tool(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    manifest["skills"][0]["tools"] = ["read", "shell"]

    assert any("unknown tool 'shell'" in error for error in _save(tmp_path, manifest, lock))


def test_skills_catalog_rejects_tool_not_owned_by_agent(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    manifest["skills"][0]["tools"] = ["read", "execute"]
    manifest["skills"][0]["side_effects"] = ["execute_commands"]

    assert any("owning_agent orchestrator does not allow tools ['execute']" in error for error in _save(tmp_path, manifest, lock))


def test_manifest_schema_agent_and_tool_enums_match_python_constants():
    schema_path = VALIDATOR_PATH.parents[1] / ".agents/skills/manifest.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    properties = schema["$defs"]["skill"]["properties"]

    assert set(properties["owning_agent"]["enum"]) == set(VALIDATOR.AGENT_TOOLS)
    assert set(properties["tools"]["items"]["enum"]) == VALIDATOR.SKILL_TOOLS


def test_current_catalog_tools_are_known_and_owned():
    manifest_path = VALIDATOR_PATH.parents[1] / ".agents/skills/manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

    assert len(manifest["skills"]) == 8
    for skill in manifest["skills"]:
        tools = set(skill["tools"])
        assert tools <= VALIDATOR.SKILL_TOOLS
        assert tools <= set(VALIDATOR.AGENT_TOOLS[skill["owning_agent"]])


def test_skills_catalog_rejects_path_escape_and_lock_disagreement(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    manifest["skills"][0]["path"] = "../SKILL.md"
    errors = _save(tmp_path, manifest, lock)
    assert any("path must equal .agents/skills/<id>/SKILL.md" in error for error in errors)
    assert any("lock/manifest disagreement" in error for error in errors)


def test_skills_catalog_rejects_absolute_manifest_path(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    manifest["skills"][0]["path"] = str((tmp_path / "outside/SKILL.md").resolve())
    errors = _save(tmp_path, manifest, lock)
    assert any("path must equal .agents/skills/<id>/SKILL.md" in error for error in errors)
    assert any("lock/manifest disagreement" in error for error in errors)


def test_skills_catalog_rejects_canonical_symlink_with_matching_hash(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    canonical = tmp_path / manifest["skills"][0]["path"]
    external = tmp_path.parent / f"{tmp_path.name}-external-SKILL.md"
    external.write_bytes(canonical.read_bytes())
    canonical.unlink()
    try:
        canonical.symlink_to(external)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks unavailable on this platform: {exc}")
    lock["skills"][0]["sha256"] = hashlib.sha256(external.read_bytes()).hexdigest()

    errors = _save(tmp_path, manifest, lock)

    assert any("symlink" in error for error in errors)


def test_skills_catalog_rejects_canonical_skill_directory_symlink_with_matching_hash(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    canonical = tmp_path / ".agents/skills/example-skill"
    external = tmp_path.parent / f"{tmp_path.name}-external-skill"
    external.mkdir()
    external_skill = external / "SKILL.md"
    external_skill.write_bytes((canonical / "SKILL.md").read_bytes())
    (canonical / "SKILL.md").unlink()
    canonical.rmdir()
    try:
        canonical.symlink_to(external, target_is_directory=True)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks unavailable on this platform: {exc}")
    lock["skills"][0]["sha256"] = hashlib.sha256(external_skill.read_bytes()).hexdigest()

    errors = _save(tmp_path, manifest, lock)

    assert any("symlink" in error and "example-skill" in error for error in errors)


def test_skills_catalog_rejects_orphan_skill_directory_symlink(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    external = tmp_path.parent / f"{tmp_path.name}-external-orphan"
    external.mkdir()
    (external / "SKILL.md").write_text(
        "---\nname: orphan\ndescription: External orphan.\n---\n# Orphan\n",
        encoding="utf-8",
    )
    orphan = tmp_path / ".agents/skills/orphan"
    try:
        orphan.symlink_to(external, target_is_directory=True)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks unavailable on this platform: {exc}")

    errors = _save(tmp_path, manifest, lock)

    assert any("symlinked skill directory .agents/skills/orphan" in error for error in errors)


def test_skills_catalog_discovery_rejects_broken_skill_symlink(tmp_path):
    manifest, lock = _write_catalog(tmp_path)
    broken = tmp_path / ".agents/skills/orphan/SKILL.md"
    broken.parent.mkdir()
    try:
        broken.symlink_to(tmp_path / "does-not-exist/SKILL.md")
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks unavailable on this platform: {exc}")

    assert any("symlinked skill .agents/skills/orphan/SKILL.md" in error for error in _save(tmp_path, manifest, lock))


@pytest.mark.parametrize(
    ("relative_path", "diagnostic"),
    [
        ("skills.lock.yaml", "skills.lock.yaml"),
        (".agents/skills/manifest.yaml", "manifest.yaml"),
        (".agents/skills/manifest.schema.json", "manifest.schema.json"),
    ],
)
def test_skills_catalog_rejects_symlinked_control_file_before_read(tmp_path, relative_path, diagnostic):
    _write_catalog(tmp_path)
    governed = tmp_path / relative_path
    external = tmp_path.parent / f"{tmp_path.name}-{governed.name}"
    external.write_bytes(governed.read_bytes())
    governed.unlink()
    try:
        governed.symlink_to(external)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks unavailable on this platform: {exc}")

    errors = VALIDATOR.validate_skills(tmp_path)

    assert any("symlink" in error and diagnostic in error for error in errors)


def test_skills_catalog_rejects_symlinked_catalog_root_before_read(tmp_path):
    _write_catalog(tmp_path)
    catalog = tmp_path / ".agents/skills"
    external = tmp_path.parent / f"{tmp_path.name}-skills"
    catalog.rename(external)
    try:
        catalog.symlink_to(external, target_is_directory=True)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks unavailable on this platform: {exc}")

    errors = VALIDATOR.validate_skills(tmp_path)

    assert any("symlink" in error and ".agents/skills" in error for error in errors)


def test_skills_catalog_rejects_symlinked_catalog_path_component(tmp_path):
    _write_catalog(tmp_path)
    agents = tmp_path / ".agents"
    external = tmp_path.parent / f"{tmp_path.name}-agents"
    agents.rename(external)
    try:
        agents.symlink_to(external, target_is_directory=True)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks unavailable on this platform: {exc}")

    errors = VALIDATOR.validate_skills(tmp_path)

    assert any("symlink" in error and ".agents" in error for error in errors)


def test_skills_catalog_rejects_non_regular_lock_node(tmp_path):
    _write_catalog(tmp_path)
    lock = tmp_path / "skills.lock.yaml"
    lock.unlink()
    lock.mkdir()

    assert any("regular non-symlink file" in error for error in VALIDATOR.validate_skills(tmp_path))


def test_public_text_scan_does_not_read_symlink_targets(tmp_path):
    external = tmp_path.parent / f"{tmp_path.name}-external.txt"
    external.write_text("external sentinel", encoding="utf-8")
    link = tmp_path / "linked.txt"
    try:
        link.symlink_to(external)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks unavailable on this platform: {exc}")

    assert VALIDATOR.collect_text_files(tmp_path) == []


def test_repository_symlink_scan_rejects_any_symlink(tmp_path):
    target = tmp_path / "target.txt"
    target.write_text("safe", encoding="utf-8")
    link = tmp_path / "link.txt"
    try:
        link.symlink_to(target)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks unavailable on this platform: {exc}")

    assert VALIDATOR.find_repository_symlinks(tmp_path) == [Path("link.txt")]
