---
name: agent-skill-workbench
description: Use when creating, editing, researching, deploying, syncing, validating, indexing, or reconciling agent skills across local repositories and remote agent workspaces.
---

# Agent Skill Workbench

Safe, remote-aware workflow for the full lifecycle of Agent Skills.

## Scope

Use for skill and capability work that may touch local source, remote agent workspaces, or both:

- inspect existing skills;
- create or edit skills;
- research similar skills and authoring references;
- sync or reconcile local and remote drift;
- validate skill structure, indexes, deployment, and routing;
- improve one agent's skill/capability surface from observed work.

Remote workspaces are often live operational state. Treat them as authoritative until inspected.

## Hard Boundaries

- Verify live remote state before remote writes.
- Treat drift as valid until proven otherwise; humans, agents, automation, or DevOps processes may have changed remote skills.
- Do not delete skills, change model/runtime/auth settings, alter schedules, restart services, or rewrite broad workspaces without explicit approval.
- Do not print, copy, or commit secrets.
- Treat external skills as reference-only until manually reviewed.

## Route First

Classify the request before reading large references:

| Route | Use when | Read |
|---|---|---|
| `inspect` | Show local or remote skill state without changes. | `references/routing.md`, `references/remote-preflight.md` |
| `create` | Create a new local or remote skill. | `references/creating-and-editing.md`, `references/authoring-quality-bar.md` |
| `edit` | Improve an existing local or remote skill. | `references/creating-and-editing.md`, `references/sync-reconcile.md` |
| `research` | Find similar skills, docs, registries, or reusable patterns. | `references/researching.md`, `references/authoring-quality-bar.md` |
| `sync/reconcile` | Compare local and remote skill state before choosing a write direction. | `references/sync-reconcile.md`, `references/remote-preflight.md` |
| `validate` | Check skill structure, index coverage, remote deployment, or routing behavior. | `references/deployment-validation.md` |
| `index` | Create or update a skill inventory/index. | `references/indexing.md` |
| `enrich-agent` | Improve one agent's skill set from observed sessions or recurring work. | `references/agent-enrichment.md` |

## Runtime Profile First

For live or remote targets, identify the runtime profile before editing. Use `references/runtime-adapters.md` for the starter profiles:

- OpenClaw;
- Hermes;
- Claude Code;
- Codex.

If the target runtime is not covered, create a temporary target profile with source of truth, access method, artifact types, safe reads, backup method, validation method, and rollback method before writing.

## Default Protocol

1. Identify target agent/system, route, runtime profile, local source path, remote target path, and requested write direction.
2. Read local project instructions and the skill index/inventory if present.
3. Run remote preflight before any live-agent write.
4. Snapshot touched remote files before writing.
5. Detect drift and choose import, deploy, merge, or inspect-only.
6. Make the smallest coherent local or remote change.
7. Validate local files, remote touched files, service health, and routing behavior where available.
8. Update the local index/inventory with status, date, and evidence when durable state changes.

## Local Utilities

The bundled scripts are read-only helpers. Adapt paths to the current repository layout.

```bash
python3 scripts/validate_skills.py --root skills
python3 scripts/check_skill_index.py --skills-root skills --index docs/skills/README.md
```

## Output Contract

End with:

- what changed or what was inspected;
- validation evidence;
- backup paths for remote writes;
- unresolved drift or risks;
- next safe step.
