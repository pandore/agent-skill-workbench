# Authoring Quality Bar

## Core Rules

- Create a skill only for a repeatable workflow, domain procedure, standard, or reusable tool pattern.
- One skill should have one clear trigger and one output contract.
- Split separate triggers or outputs into separate skills.
- The `description` should tell the agent when to activate the skill, not replace the workflow.
- Keep `SKILL.md` lean: routing, hard rules, core protocol, and deliverables.
- Put detailed policies, schemas, examples, and longer checklists in `references/`.
- Put deterministic fragile operations in `scripts/`.
- Put reusable static templates in `assets/` when needed.

## Required Checks

- YAML frontmatter is valid.
- Folder name matches `name`.
- Description is concrete and trigger-focused.
- No unresolved draft markers or placeholder labels remain.
- No obvious secret patterns are present.
- Local index row exists when the repository has an index.
- Remote deployment has preflight, backup, and validation evidence.

## External Best-Practice References

- Agent Skills specification: https://agentskills.io/specification
- Anthropic Agent Skills: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- OpenAI Academy: https://openai.com/academy/skills/
- OpenAI Help: https://help.openai.com/en/articles/20001066-skills-in-chatgpt
