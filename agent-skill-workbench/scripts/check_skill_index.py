#!/usr/bin/env python3
"""Read-only coverage check for a Markdown skill index."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_HEADERS = [
    "Skill",
    "Purpose",
    "Local source",
    "Remote targets",
    "Remote path",
    "Sync status",
    "Last verified",
    "Evidence",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", default="skills")
    parser.add_argument("--index", default="docs/skills/README.md")
    args = parser.parse_args()

    skills_root = Path(args.skills_root)
    index_path = Path(args.index)
    if not index_path.exists():
        print(f"ERROR: missing skill index: {index_path}")
        return 1

    text = index_path.read_text(encoding="utf-8")
    errors: list[str] = []

    for header in REQUIRED_HEADERS:
        if header not in text:
            errors.append(f"{index_path}: missing required column {header!r}")

    skill_names = sorted(path.parent.name for path in skills_root.glob("*/SKILL.md"))
    for skill_name in skill_names:
        if f"`{skill_name}`" not in text:
            errors.append(f"{index_path}: missing row for local skill {skill_name}")

    allowed_statuses = {
        "local-only",
        "remote-only",
        "in-sync",
        "local-newer",
        "remote-newer",
        "diverged",
        "deployed-untracked",
        "deprecated",
    }
    for line in text.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if len(cells) < 8:
            errors.append(f"{index_path}: malformed index row: {line}")
            continue
        status = cells[5]
        if status not in allowed_statuses:
            errors.append(f"{index_path}: unsupported sync status {status!r} in row: {line}")

    for error in errors:
        print(f"ERROR: {error}")

    print(f"Checked {len(skill_names)} skills against {index_path}: {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
