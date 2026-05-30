# Remote Preflight

Run remote preflight before any live-agent write.

## Required Checks

1. Confirm the user explicitly requested deploy, update, sync, or edit for a concrete remote target.
2. Confirm access works.
3. Confirm the target workspace and skill path exist, or confirm the request is to create them.
4. Check service/gateway/worker health when the target is live.
5. Read touched remote files without printing secrets.
6. Check dirty state when the remote workspace is version-controlled.
7. Create a timestamped backup of touched remote files before writing.

## Safe Read Examples

Adapt commands to the target environment:

```bash
ssh HOST_ALIAS 'pwd; hostname'
ssh HOST_ALIAS 'find ~/agent-workspaces -maxdepth 3 -type d -name skills 2>/dev/null | sort'
ssh HOST_ALIAS 'git -C WORKSPACE_PATH status --short'
```

Replace placeholders with verified values. Do not run commands that print secrets.

## Backup Rule

Back up only touched files. Prefer a timestamped path near the target workspace, for example:

```text
WORKSPACE_PATH/.skill-backups/YYYYMMDD-HHMMSS/skill-name/
```

Record backup paths in the final report and index evidence when deployment is durable.

## Stop Conditions

Stop before writing if:

- access fails;
- service state is unknown;
- remote file changed unexpectedly;
- target path is ambiguous;
- command would print secrets;
- change scope includes runtime, auth, schedules, or unrelated service changes;
- drift is `remote-newer` or `diverged` and the user did not ask to merge.
