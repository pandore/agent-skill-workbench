# Deployment Validation

## Local Validation

Use the bundled read-only helpers when they match the repository layout:

```bash
python3 scripts/validate_skills.py --root skills
python3 scripts/check_skill_index.py --skills-root skills --index docs/skills/README.md
```

If the repository uses another skill root or index path, pass those paths explicitly.

## Remote Validation

After a remote write:

1. Confirm touched files exist and are readable.
2. Confirm the backup path exists.
3. Re-read touched skill frontmatter.
4. Confirm routing/reference docs remain readable.
5. Confirm service health did not regress when the target is live.
6. Run runtime-specific skill checks when available.
7. Run a no-delivery or realistic routing canary when the runtime supports it.

## Runtime Notes

- Prefer the runtime's native skill list/check command if available.
- If no native check exists, validate file structure and run a minimal dry-run prompt that does not mutate external systems.
- For remote live systems, use no-delivery canaries unless the user explicitly approves real delivery.
- For OpenClaw, Hermes, Claude Code, and Codex targets, read `runtime-adapters.md` before choosing validation commands.

## Failure Handling

If validation fails, report the exact failure and offer one of:

- restore the immediate backup;
- fix forward;
- leave the remote state as-is with a report.

Do not blindly restore over new remote edits made after the backup.
