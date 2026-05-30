# Sync And Reconcile

Remote drift is expected. Humans, agents, automation, and DevOps processes can all change remote workspaces.

## Drift Statuses

- `local-only`: local source exists; no recorded remote deployment.
- `remote-only`: remote skill exists; no local source.
- `in-sync`: local and remote content match for the target checked in this session.
- `local-newer`: local changed after last recorded remote sync.
- `remote-newer`: remote changed after last recorded local sync.
- `diverged`: both sides changed.
- `deployed-untracked`: remote deployment exists without tracked local source.
- `deprecated`: retained for history, not for new work.

## Reconcile Options

- `remote -> local`: import remote state into local source and update the index.
- `local -> remote`: deploy local source to the remote workspace after preflight and backup.
- `merge`: preserve both sides, make surgical edits, validate, and update index evidence.
- `inspect-only`: report drift without changing files.

## Conflict Rule

For `remote-newer` or `diverged`, do not overwrite automatically. Show the risk and choose import, merge, inspect-only, or explicit deploy based on the user's instruction.

## Evidence

After reconcile, record:

- target system and agent;
- local and remote paths;
- sync status;
- verification date;
- validation evidence;
- backup path when remote files were changed.
