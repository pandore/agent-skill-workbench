# Skill Indexing

A skill index is optional but useful for teams that manage many local and remote skills.

## Recommended Columns

| Skill | Purpose | Local source | Remote targets | Remote path | Sync status | Last verified | Evidence |
|---|---|---|---|---|---|---|---|

## Update Triggers

Update the index when:

- a local skill is created, renamed, edited, or deprecated;
- a remote skill is imported;
- a local skill is deployed remotely;
- drift is detected;
- validation evidence changes durable state.

## Evidence Rules

Evidence should link to a report, system page, design/spec/plan, or commit. Do not use the index as a dump for logs, env files, secrets, or raw transcripts.

## Sync Status Values

Use these statuses unless the repository defines its own:

- `local-only`
- `remote-only`
- `in-sync`
- `local-newer`
- `remote-newer`
- `diverged`
- `deployed-untracked`
- `deprecated`
