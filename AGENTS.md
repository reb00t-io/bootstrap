# AGENTS.md

## Mission & Priorities
- Maintain a small, reliable bootstrap script and templates for agent setup.
- Priority order: correctness > maintainability > security > speed.

## Repo Map
- bootstrap.py — CLI that clones or targets a repo and adds agent files.
- AGENTS_TEMPLATE.md — template copied to AGENTS.md in target repos.
- AGENTS_STRUCTURE.md — structure guide copied to target repos.
- README.md — repo overview.
- pyproject.toml — project metadata.

## Commands (Ground Truth)
- Run: python bootstrap.py <repo|path>
- Tests: N/A (none configured).

## Boundaries
- Do not add dependencies or frameworks unless explicitly requested.
- Do not modify target repos beyond adding AGENTS.md and AGENTS_STRUCTURE.md unless asked.
