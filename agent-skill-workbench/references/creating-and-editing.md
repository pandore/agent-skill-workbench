# Creating And Editing Skills

## Create

1. Confirm route, target agent/system, and whether the skill should be local-only, remote-only, or deployed from local to remote.
2. Research existing local skills and relevant external references before writing.
3. Choose a lowercase hyphenated name under 64 characters.
4. Write a trigger-focused description that starts with `Use when`.
5. Keep `SKILL.md` lean and move detailed procedures into one-level `references/`.
6. Add scripts only for deterministic repeated checks.
7. Update the local skill index if the repository uses one.
8. Validate locally and remotely when deployed.

## Edit

1. Read local and remote versions when the target is remote.
2. Classify drift before changing files.
3. Snapshot touched remote files before remote writes.
4. Patch surgically.
5. Preserve local business rules, approvals, and source-of-truth notes.
6. Validate and update index evidence when durable state changes.

## Remote Write Rule

Remote write is allowed only when the user explicitly requested it for a concrete target and preflight is clean. Otherwise prepare local changes, a proposal, or a reconcile report.
