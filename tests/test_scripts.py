from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "agent-skill-workbench"
VALIDATOR = SKILL_DIR / "scripts" / "validate_skills.py"
INDEX_CHECKER = SKILL_DIR / "scripts" / "check_skill_index.py"


class ScriptTests(unittest.TestCase):
    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_validator_accepts_yaml_block_scalar_description(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            skill = root / "multiline-desc"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                """---
name: multiline-desc
description: >
  Use when the description is authored as a YAML block scalar
  spanning multiple lines, which real skills do.
---
# Body
""",
                encoding="utf-8",
            )

            result = self.run_script(VALIDATOR, "--root", str(root))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Checked 1 skills: 0 errors, 0 warnings", result.stdout)

    def test_validator_accepts_block_scalar_without_pyyaml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            skill = root / "multiline-desc"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                """---
name: multiline-desc
description: >
  Use when the description is authored as a YAML block scalar
  spanning multiple lines, which real skills do.
---
# Body
""",
                encoding="utf-8",
            )

            code = f"""
import builtins
import runpy
import sys

_import = builtins.__import__

def blocked(name, *args, **kwargs):
    if name == "yaml":
        raise ImportError()
    return _import(name, *args, **kwargs)

builtins.__import__ = blocked
sys.argv = ["validate_skills.py", "--root", {str(root)!r}]
runpy.run_path({str(VALIDATOR)!r}, run_name="__main__")
"""
            result = subprocess.run(
                [sys.executable, "-c", code],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Checked 1 skills: 0 errors, 0 warnings", result.stdout)

    def test_validator_placeholder_warning_ignores_generics_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            generics = root / "has-generics"
            stub = root / "has-stub"
            generics.mkdir(parents=True)
            stub.mkdir(parents=True)
            (generics / "SKILL.md").write_text(
                """---
name: has-generics
description: Use when working with List<String>.
---
Map<Key, Value> and <div>x</div>.
""",
                encoding="utf-8",
            )
            (stub / "SKILL.md").write_text(
                """---
name: has-stub
description: Use when connecting to a host.
---
ssh <HOST_ALIAS>; replace <...> first.
""",
                encoding="utf-8",
            )

            result = self.run_script(VALIDATOR, "--root", str(root))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("has-stub", result.stdout)
        self.assertNotIn("has-generics", result.stdout)
        self.assertIn("Checked 2 skills: 0 errors, 1 warnings", result.stdout)

    def test_index_checker_accepts_unquoted_skill_names_and_checks_status_column(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills = root / "skills"
            docs = root / "docs"
            (skills / "alpha").mkdir(parents=True)
            (skills / "beta").mkdir(parents=True)
            docs.mkdir()
            (skills / "alpha" / "SKILL.md").write_text(
                "---\nname: alpha\ndescription: Use when doing alpha.\n---\n",
                encoding="utf-8",
            )
            (skills / "beta" / "SKILL.md").write_text(
                "---\nname: beta\ndescription: Use when doing beta.\n---\n",
                encoding="utf-8",
            )
            index = docs / "index.md"
            index.write_text(
                """# Skill Index

| Skill | Purpose | Local source | Remote targets | Remote path | Sync status | Last verified | Evidence |
|---|---|---|---|---|---|---|---|
| alpha | does alpha | skills/alpha | none | - | in-sync | 2026-05-01 | report#1 |
| beta | does beta | skills/beta | prod | /x | bogus-status | 2026-05-02 | report#2 |
""",
                encoding="utf-8",
            )

            result = self.run_script(
                INDEX_CHECKER,
                "--skills-root",
                str(skills),
                "--index",
                str(index),
            )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stdout.count("ERROR:"), 1, result.stdout)
        self.assertIn("unsupported sync status 'bogus-status'", result.stdout)
        self.assertNotIn("missing row", result.stdout)

    def test_validator_self_check_remains_clean(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            root.mkdir()
            shutil.copytree(SKILL_DIR, root / "agent-skill-workbench")

            result = self.run_script(VALIDATOR, "--root", str(root))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Checked 1 skills: 0 errors, 0 warnings", result.stdout)


if __name__ == "__main__":
    unittest.main()
