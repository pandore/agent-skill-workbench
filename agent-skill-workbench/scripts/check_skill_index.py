#!/usr/bin/env python3
"""Read-only coverage check for a Markdown skill index."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional


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


ALLOWED_STATUSES = {
    "local-only",
    "remote-only",
    "in-sync",
    "local-newer",
    "remote-newer",
    "diverged",
    "deployed-untracked",
    "deprecated",
}


def _split_row(line: str) -> list[str]:
    return [cell.strip().strip("`").strip() for cell in line.strip().strip("|").split("|")]


def _find_header_row(lines: list[str]) -> Optional[tuple[int, list[str]]]:
    for index, line in enumerate(lines):
        if "|" not in line:
            continue
        cells = [cell.lower() for cell in _split_row(line)]
        if "skill" in cells and "sync status" in cells:
            return index, _split_row(line)
    return None


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

    lines = index_path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []

    header = _find_header_row(lines)
    if header is None:
        print(f"ERROR: {index_path}: could not locate a skill-index table header row")
        return 1
    header_index, header_cells = header
    header_lower = {cell.lower() for cell in header_cells}
    for header in REQUIRED_HEADERS:
        if header.lower() not in header_lower:
            errors.append(f"{index_path}: missing required column {header!r}")

    status_column = next(
        (index for index, cell in enumerate(header_cells) if cell.lower() == "sync status"),
        None,
    )

    seen_skill_cells: set[str] = set()
    for line in lines[header_index + 1:]:
        if "|" not in line:
            continue
        if re.match(r"^\s*\|?\s*:?-{2,}", line):
            continue
        cells = _split_row(line)
        if len(cells) < 8:
            errors.append(f"{index_path}: malformed index row: {line.strip()}")
            continue
        seen_skill_cells.add(cells[0])
        if status_column is not None and status_column < len(cells):
            status = cells[status_column]
            if status and status not in ALLOWED_STATUSES:
                errors.append(
                    f"{index_path}: unsupported sync status {status!r} in row: {line.strip()}"
                )

    skill_names = sorted(path.parent.name for path in skills_root.glob("*/SKILL.md"))
    for skill_name in skill_names:
        if skill_name not in seen_skill_cells:
            errors.append(f"{index_path}: missing row for local skill {skill_name}")

    for error in errors:
        print(f"ERROR: {error}")

    print(f"Checked {len(skill_names)} skills against {index_path}: {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
