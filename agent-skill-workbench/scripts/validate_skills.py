#!/usr/bin/env python3
"""Read-only validator for Agent Skill folders."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{30,}"),
    re.compile(r"[0-9]{8,}:[A-Za-z0-9_-]{25,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]
DRAFT_WORDS = ["TO" + "DO", "TB" + "D", "FIX" + "ME", "PLACE" + "HOLDER"]


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []
    if not lines or lines[0].strip() != "---":
        return {}, [f"{path}: missing opening YAML frontmatter delimiter"]
    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break
    if end is None:
        return {}, [f"{path}: missing closing YAML frontmatter delimiter"]
    data: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"{path}: unsupported frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, errors


def validate_skill(skill_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    data, frontmatter_errors = parse_frontmatter(skill_file)
    errors.extend(frontmatter_errors)

    name = data.get("name", "")
    description = data.get("description", "")

    if not name:
        errors.append(f"{skill_file}: missing required name")
    elif not NAME_RE.match(name):
        errors.append(f"{skill_file}: invalid name {name!r}")
    elif name != skill_dir.name:
        errors.append(f"{skill_file}: name {name!r} does not match folder {skill_dir.name!r}")

    if not description:
        errors.append(f"{skill_file}: missing required description")
    else:
        if len(description) > 1024:
            errors.append(f"{skill_file}: description is longer than 1024 characters")
        if "Use when" not in description:
            warnings.append(f"{skill_file}: description should include a concrete 'Use when' trigger")
        elif not description.startswith("Use when"):
            warnings.append(f"{skill_file}: prefer starting description with 'Use when'")

    text = skill_file.read_text(encoding="utf-8")
    for word in DRAFT_WORDS:
        if re.search(rf"\b{word}\b", text, re.IGNORECASE):
            warnings.append(f"{skill_file}: contains unresolved draft marker {word}")
    if re.search(chr(60) + r"[^>\n]+" + chr(62), text):
        warnings.append(f"{skill_file}: contains angle-bracket placeholder-style text")

    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"{skill_file}: possible secret pattern matched {pattern.pattern}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="skills", help="directory containing skill folders")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"ERROR: skills root does not exist: {root}")
        return 1

    skill_dirs = sorted(path.parent for path in root.glob("*/SKILL.md"))
    errors: list[str] = []
    warnings: list[str] = []

    for skill_dir in skill_dirs:
        skill_errors, skill_warnings = validate_skill(skill_dir)
        errors.extend(skill_errors)
        warnings.extend(skill_warnings)

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    print(f"Checked {len(skill_dirs)} skills: {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
