# Bootstrap

Bootstrap is a tiny CLI that installs agent templates into a target repo.

## Usage

python bootstrap.py <repo|path>

## Behavior

- Copies AGENTS_TEMPLATE.md to AGENTS.md.
- Copies AGENTS_STRUCTURE.md.
- Optionally creates a branch, then stages, commits, and pushes with confirmation.
