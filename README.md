# Agent Skill Workbench

A reusable Agent Skill for safely creating, editing, researching, validating, syncing, and deploying skills across local repositories and remote agent workspaces.

## What It Is

This package contains an installable skill folder:

```text
agent-skill-workbench/
  SKILL.md
  references/
  scripts/
```

Copy the inner `agent-skill-workbench/` folder into your agent's skills directory.

Common locations:

- Codex: `~/.codex/skills/agent-skill-workbench/` or project-local `.agents/skills/agent-skill-workbench/`
- Claude Code: `~/.claude/skills/agent-skill-workbench/`
- Other Agent Skills-compatible runtimes: use the runtime's documented skills directory.

## Use Cases

- Audit existing skills before editing them.
- Create new skills with trigger-focused descriptions.
- Reconcile local and remote skill drift.
- Back up remote files before changing live agent workspaces.
- Validate skill metadata, index coverage, and routing behavior.
- Research third-party skills without installing unreviewed code.
- Work across starter runtime profiles for OpenClaw, Hermes, Claude Code, and Codex.

## Safety Model

The skill assumes remote agent workspaces may be changed by humans, agents, automation, or DevOps processes. It therefore treats remote state as authoritative until inspected, requires backups before remote writes, and blocks broad runtime/auth/cron/service changes unless explicitly approved.

## Included Utilities

- `scripts/validate_skills.py` checks `SKILL.md` frontmatter (single-line and `>`/`|` block-scalar descriptions), naming, name/folder match, description length and trigger phrasing, draft markers, placeholder stubs (`<HOST>`-style), and common secret-shaped patterns. It uses `pyyaml` when available and falls back to a built-in parser, so it needs no dependencies. The secret and placeholder checks are heuristics, not guarantees.
- `scripts/check_skill_index.py` checks a Markdown skill index for required columns, known sync statuses, and rows for local skills.

Both scripts are read-only.

## Runtime Coverage

The first supported runtime profiles are OpenClaw, Hermes, Claude Code, and Codex. The skill treats those as adapters over the same safety loop: identify source of truth, inspect live state, back up touched files, edit surgically, validate with the runtime's own checks where possible, and record evidence.
