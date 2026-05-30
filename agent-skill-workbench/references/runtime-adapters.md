# Runtime Adapters

Use this file after route selection when the target runtime is known or likely. These adapters are starter profiles, not exhaustive product documentation. Project-local instructions and live state override generic defaults.

## Universal Target Profile

Before writing to any runtime, fill in:

| Field | Meaning |
|---|---|
| Runtime | OpenClaw, Hermes, Claude Code, Codex, or other. |
| Source of truth | Local repo, remote workspace, cloud UI/API, or mixed. |
| Access method | Local filesystem, SSH, CLI, API, browser, or connector. |
| Artifact types | Skills, instructions, tools, memory, schedules, configs, references. |
| Safe reads | Commands or API calls that do not mutate state or print secrets. |
| Write method | Patch file, CLI command, API update, UI change, or manual proposal. |
| Backup method | Git commit, copied files, exported JSON, snapshot, or rollback branch. |
| Validation | Native check command, dry-run, canary, service health, or focused test. |
| Rollback | Restore backup, revert commit, redeploy prior config, or disable change. |

Stop before writing if any field is unknown and a wrong guess could touch production, credentials, schedules, billing, or irreversible state.

## OpenClaw

Use when the target is an OpenClaw-managed agent with workspace-backed instructions, skills, tools, sessions, or schedules.

Typical artifacts:

- workspace files such as `AGENTS.md`, persona/instruction files, `TOOLS.md`, `skills/`, `references/`, and scripts;
- runtime config and channel/provider settings;
- sessions, memory, generated reports, and scheduled jobs.

Default safety:

- Treat the remote workspace as source of truth until inspected.
- Do not change runtime config, auth, channel policy, models, schedules, or services during skill work unless explicitly requested.
- Keep generated reports, memory, backups, and scratch outputs out of commits unless they are intentional source artifacts.
- Back up touched files before remote writes.
- Prefer one agent at a time.

Useful validation choices:

- workspace git status and focused diff;
- skill structure validator for `skills/`;
- runtime-native skill check when available;
- gateway/service health when the target is live;
- no-delivery routing canary for behavior changes.

## Hermes

Use when the target is a Hermes-managed agent/profile or a host where Hermes coexists with another runtime.

Typical artifacts:

- profile instructions and persona files;
- gateway/service configuration;
- scheduler or delivery configuration;
- memory or knowledge files;
- rollback-preserved runtime state.

Default safety:

- First determine whether Hermes is active, inactive, or preserved only for rollback.
- Do not start, stop, enable, disable, or restart Hermes services unless the task explicitly asks for runtime operations.
- Do not assume Hermes and another runtime can run concurrently on the same agent identity.
- Treat profile migration and rollback files as durable state, not cleanup noise.

Useful validation choices:

- service status when service access exists;
- profile file diff and instruction syntax checks;
- no-delivery prompt/canary when supported;
- explicit confirmation that intended active/inactive service state did not change.

## Claude Code

Use when the target is Claude Code or a Claude-compatible local skill environment.

Typical artifacts:

- user skills under `~/.claude/skills/`;
- project or repository instruction files;
- `SKILL.md` plus optional `references/`, `scripts/`, and `assets/`;
- local tools or scripts called by the skill.

Default safety:

- Prefer project-local instructions over global defaults.
- Do not overwrite user-global skills without reading the existing skill and confirming write scope.
- Keep skill descriptions trigger-focused; do not put full workflows in frontmatter.
- Keep `SKILL.md` lean and move heavy material to one-level references.

Useful validation choices:

- frontmatter/name/folder validation;
- no unresolved placeholders or secret-shaped values;
- compile or smoke-test bundled scripts;
- focused task replay or dry-run prompt if available.

## Codex

Use when the target is Codex, Codex CLI, or a Codex-compatible local/project skill environment.

Typical artifacts:

- user skills under `~/.codex/skills/`;
- project skills under `.agents/skills/`;
- `AGENTS.md` or repository instructions;
- bundled references, scripts, and assets;
- local validators or task-specific checks.

Default safety:

- Check both user-global and project-local skill locations when resolving scope.
- Project instructions override generic skill guidance.
- Do not rely on remembered tool or runtime behavior; inspect available tools and local files.
- Keep generated caches, plugin downloads, and transient outputs out of commits.

Useful validation choices:

- frontmatter/name/folder validation;
- project skill index check when an index exists;
- script compile/smoke tests;
- current-session dry run or no-mutation task prompt when possible.

## Unsupported Or Mixed Runtimes

If the runtime is not one of the starter profiles:

1. Create a target profile using the universal table above.
2. Run inspect-only first.
3. Propose the write path before editing.
4. Validate through the runtime's own dry-run, health, or canary mechanism.
5. Add a new adapter only after the pattern is repeatable.
