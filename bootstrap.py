#!/usr/bin/env python3
"""Bootstrap an agent-ready repo by copying agent setup templates."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def prompt_yes_no(message: str, default: bool = False) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        reply = input(f"{message} {suffix} ").strip().lower()
        if not reply:
            return default
        if reply in {"y", "yes"}:
            return True
        if reply in {"n", "no"}:
            return False
        print("Please answer 'y' or 'n'.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clone a repo and add agent bootstrap files."
    )
    parser.add_argument(
        "repo",
        help="Git URL or 'owner/name' for the repo to clone.",
    )
    parser.add_argument(
        "--dest",
        help="Destination directory (default: derived from repo).",
    )
    return parser.parse_args()


def resolve_repo_dir(repo: str, dest: str | None) -> Path:
    if dest:
        return Path(dest).expanduser().resolve()

    repo_name = repo.rstrip("/").split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    return Path.cwd() / repo_name


def main() -> int:
    args = parse_args()

    repo_dir = resolve_repo_dir(args.repo, args.dest)

    if repo_dir.exists():
        print(f"Destination already exists: {repo_dir}")
        return 1

    print(f"Cloning {args.repo} into {repo_dir}...")
    run(["git", "clone", args.repo, str(repo_dir)])

    script_dir = Path(__file__).resolve().parent
    template_path = script_dir / "AGENTS_TEMPLATE.md"
    structure_path = script_dir / "AGENTS_STRUCTURE.md"

    if not template_path.exists() or not structure_path.exists():
        print("Missing AGENTS_TEMPLATE.md or AGENTS_STRUCTURE.md in this repo.")
        return 1

    agents_md = repo_dir / "AGENTS.md"
    print("Copying AGENTS_TEMPLATE.md -> AGENTS.md")
    shutil.copyfile(template_path, agents_md)

    print("Copying AGENTS_STRUCTURE.md -> AGENTS_STRUCTURE.md")
    shutil.copyfile(structure_path, repo_dir / "AGENTS_STRUCTURE.md")

    if prompt_yes_no("Create a new branch for these commits?"):
        branch_name = input("Branch name: ").strip()
        if not branch_name:
            print("Branch name is required. Aborting.")
            return 1
        run(["git", "checkout", "-b", branch_name], cwd=repo_dir)

    run(["git", "status", "--short"], cwd=repo_dir)

    if prompt_yes_no("Stage and commit the new files?"):
        run(["git", "add", "AGENTS.md", "AGENTS_STRUCTURE.md"], cwd=repo_dir)
        commit_message = input("Commit message: ").strip() or "Add agent bootstrap files"
        run(["git", "commit", "-m", commit_message], cwd=repo_dir)

        if prompt_yes_no("Push the commit now?"):
            # Use upstream if on a named branch created by this script
            try:
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=repo_dir,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                current_branch = result.stdout.strip()
            except subprocess.CalledProcessError:
                current_branch = ""

            if current_branch:
                run(["git", "push", "-u", "origin", current_branch], cwd=repo_dir)
            else:
                run(["git", "push"], cwd=repo_dir)
    else:
        print("Skipping commit and push.")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
