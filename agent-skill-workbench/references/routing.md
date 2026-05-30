# Routing And Target Resolution

## Route Selection

- `inspect`: read-only inventory, state summary, or drift report.
- `create`: new skill folder, new remote skill, or reusable skill template.
- `edit`: change existing local or remote skill content.
- `research`: find similar skills, official docs, reusable examples, or authoring guidance.
- `sync/reconcile`: compare local and remote state before choosing a direction.
- `validate`: run structure, index, remote, or routing checks.
- `index`: update a skill inventory.
- `enrich-agent`: improve one agent's skill set from observed work.

Read `runtime-adapters.md` whenever the target is live, remote, or runtime-specific.

## Target Resolution

Before changing anything, identify:

- local project instructions and approval rules;
- access method for the remote environment, if any;
- runtime family or agent framework;
- agent id/name;
- runtime adapter or target profile;
- remote workspace path;
- remote skill path;
- local source path, when present;
- skill index or inventory path, when present;
- requested write direction: local-only, remote-only, local-to-remote, remote-to-local, merge, or inspect-only.

If target identity is ambiguous and a wrong choice could touch production or overwrite remote state, ask for clarification before writing.

## Local Context To Read

Prefer project-local docs over assumptions:

- agent/project instruction files;
- system or deployment inventory;
- skill inventory/index;
- recent evidence reports;
- current git status for the relevant workspace.
