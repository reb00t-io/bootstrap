#!/usr/bin/env python3
"""Update AGENTS.md using Claude Code or Codex CLI."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


DEFAULT_PROMPT = """
Update AGENTS.md so it conforms to AGENTS_STRUCTURE.md.
- Only edit AGENTS.md (do not touch other files).
- Replace outdated content and add new information as needed.
- Keep it concise and bullet-based. If needed, make it more concise.
""".strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update AGENTS.md via Claude Code or Codex CLI."
    )
    parser.add_argument(
        "tool",
        choices=["claude", "codex"],
        help="Which CLI to use.",
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Target repo path (default: current directory).",
    )
    parser.add_argument(
        "--prompt-file",
        default=".automation/update-agents.prompt.txt",
        help="Path to prompt file (optional).",
    )

    codex = parser.add_argument_group("codex")
    codex.add_argument(
        "--output-last-message",
        default=None,
        help="Optional path for Codex last message output.",
    )
    codex.add_argument(
        "--full-auto",
        action="store_true",
        help="Enable Codex full-auto preset.",
    )

    claude = parser.add_argument_group("claude")
    claude.add_argument(
        "--append-system-prompt-file",
        default=".automation/claude-system.txt",
        help="System prompt additions file (optional).",
    )
    claude.add_argument(
        "--allowed-tools",
        default="Read,Edit,Bash",
        help="Allowed tools for headless mode.",
    )
    claude.add_argument(
        "--no-allowed-tools",
        action="store_true",
        help="Disable --allowedTools flag.",
    )

    return parser.parse_args()


def load_prompt(prompt_file: Path) -> str:
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8").strip()
    return DEFAULT_PROMPT


def run_codex(args: argparse.Namespace, repo_dir: Path, prompt: str) -> None:
    cmd = ["codex", "exec", "-C", str(repo_dir), "-"]
    if args.output_last_message:
        cmd.extend(["--output-last-message", args.output_last_message])
    if args.full_auto:
        cmd.append("--full-auto")
    subprocess.run(cmd, input=prompt, text=True, check=True)


def run_claude(args: argparse.Namespace, repo_dir: Path, prompt: str) -> None:
    cmd = ["claude", "-p"]

    system_path = Path(args.append_system_prompt_file).expanduser().resolve()
    if system_path.exists():
        cmd.extend(["--append-system-prompt-file", str(system_path)])

    if not args.no_allowed_tools:
        cmd.extend(["--allowedTools", args.allowed_tools])

    cmd.append(prompt)

    subprocess.run(cmd, cwd=repo_dir, check=True)


def main() -> int:
    args = parse_args()

    repo_dir = Path(args.repo).expanduser().resolve()
    prompt_path = Path(args.prompt_file).expanduser().resolve()
    prompt = load_prompt(prompt_path)

    if args.tool == "codex":
        run_codex(args, repo_dir, prompt)
    else:
        run_claude(args, repo_dir, prompt)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
