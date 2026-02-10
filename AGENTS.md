# AGENTS.md

## 1. Mission & Priorities
- Maintain a small, reliable bootstrap CLI and agent template set.
- Decision priority: correctness > maintainability > security > speed.
- Keep changes minimal, repo-scoped, and easy to review.

## 2. Executable Commands (Ground Truth)
- Setup (editable install): `python -m pip install -e .`
- Run CLI directly: `python bootstrap.py <repo|path>`
- Run installed entrypoint: `bootstrap <repo|path>`
- Development server: not applicable (CLI-only repo).
- Help/smoke check: `python bootstrap.py --help`
- Linting: not configured in this repo.
- Formatting: not configured in this repo.
- Type checking: not configured in this repo.
- Unit tests: not configured in this repo.
- Integration/e2e tests: not configured in this repo.

## 3. Repository Map
- `bootstrap.py`: main CLI entrypoint; cloning/pulling, copying artifacts, commit flow.
- `AGENTS_TEMPLATE.md`: source template copied to target repo as `AGENTS.md`.
- `AGENTS_STRUCTURE.md`: structure guide copied to target repo.
- `agent_scripts/`: helper scripts copied into target repo.
- `README.md`: usage and behavior summary.
- `pyproject.toml`: package metadata, Python requirement, `bootstrap` console script.

## 4. Definition of Done
- Implement requested behavior with minimal diff.
- Keep copy behavior for `AGENTS.md`, `AGENTS_STRUCTURE.md`, and `agent_scripts/` correct.
- Run at least one local confidence command when code changes (`python bootstrap.py --help` minimum).
- Update docs/templates when behavior or copied artifacts change.
- Final summary includes changed files and checks run.

## 5. Code Style & Conventions (Repo-Specific)
- Python 3.12+ only (`requires-python = ">=3.12"`).
- Prefer standard library; keep dependencies minimal.
- Keep CLI output explicit and prompts clear.
- Preserve current copy semantics and git workflow shape unless explicitly requested.

## 6. Boundaries & Guardrails
- Do not modify target repos beyond `AGENTS.md`, `AGENTS_STRUCTURE.md`, and `agent_scripts/` unless asked.
- Do not add dependencies unless explicitly requested.
- Do not make unrelated refactors.
- Do not bypass git safety checks or suppress command failures.
- Do not break public CLI behavior without coordinated doc updates.

## 7. Security & Privacy Constraints
- Never commit credentials, tokens, SSH keys, or local secrets.
- Treat target repo paths/URLs as untrusted input; keep path handling conservative.
- Keep subprocess safety checks (`check=True`) unless explicitly justified.

## 8. Common Pitfalls & Couplings
- If copied artifact names/paths change, update both copy logic and `git add` paths in `bootstrap.py`.
- If CLI args or behavior change, update `README.md` and template docs in the same change.
- Keep `AGENTS_TEMPLATE.md` and `AGENTS_STRUCTURE.md` aligned when changing guidance intent.

## 9. Examples & Canonical Patterns (Optional)
- Change touching copy behavior: update `bootstrap.py`, verify copied paths, run `python bootstrap.py --help`, then update related docs/templates.

## 10. Branches and PRs
- Branch naming: no enforced convention in this repo.
- PRs: include concise summary, touched files, and validation commands; open a PR for user-visible behavior/template changes.
