#!/usr/bin/env python3
"""Generate or verify the GitHub Copilot mirror of canonical Agent Skills."""
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".agents" / "skills"
TARGET = ROOT / ".github" / "skills"
README = """# Generated Copilot skill mirror\n\nThis directory is generated from [`../../.agents/skills/`](../../.agents/skills/).\nDo not edit it directly. Run `python scripts/sync_vendor_skills.py` after changing canonical skills.\n"""


def build(destination: Path) -> None:
    if not SOURCE.is_dir():
        raise RuntimeError(f"missing canonical source: {SOURCE.relative_to(ROOT)}")
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "README.md").write_text(README, encoding="utf-8")
    for skill_dir in sorted(path for path in SOURCE.iterdir() if path.is_dir()):
        if not (skill_dir / "SKILL.md").is_file():
            continue
        shutil.copytree(skill_dir, destination / skill_dir.name)


def same_tree(expected: Path, actual: Path) -> bool:
    expected_files = sorted(path.relative_to(expected) for path in expected.rglob("*") if path.is_file())
    actual_files = sorted(path.relative_to(actual) for path in actual.rglob("*") if path.is_file()) if actual.is_dir() else []
    if expected_files != actual_files:
        print("skill mirror file set differs", file=sys.stderr)
        return False
    for relative in expected_files:
        if not filecmp.cmp(expected / relative, actual / relative, shallow=False):
            print(f"skill mirror differs: {relative}", file=sys.stderr)
            return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when the generated mirror is stale")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="agent-skills-") as temp:
        expected = Path(temp) / "skills"
        build(expected)
        if args.check:
            return 0 if same_tree(expected, TARGET) else 1
        if TARGET.exists():
            shutil.rmtree(TARGET)
        shutil.copytree(expected, TARGET)
    print("Synced .github/skills from .agents/skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
