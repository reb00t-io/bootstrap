#!/usr/bin/env python3
"""Bootstrap an agent-ready repo by copying agent setup templates."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


TEMPLATE_REPO = "git@github.com:reb00t-io/bootstrap-template.git"


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
        help="Git URL, 'owner/name', or a path to an existing checkout.",
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


def resolve_existing_repo(repo: str) -> Path | None:
    repo_path = Path(repo).expanduser()
    if repo_path.exists() and repo_path.is_dir():
        return repo_path.resolve()
    return None


def prepare_repo(repo: str, dest: str | None) -> Path:
    existing_repo_dir = resolve_existing_repo(repo)
    if existing_repo_dir:
        if dest:
            raise ValueError("--dest cannot be used when repo is an existing directory.")
        repo_dir = existing_repo_dir
        try:
            run(["git", "rev-parse", "--show-toplevel"], cwd=repo_dir)
        except subprocess.CalledProcessError as exc:
            raise ValueError(f"Not a git repository: {repo_dir}") from exc
        print(f"Using existing checkout: {repo_dir}")
        return repo_dir

    repo_dir = resolve_repo_dir(repo, dest)
    if repo_dir.exists():
        raise ValueError(f"Destination already exists: {repo_dir}")

    print(f"Cloning {repo} into {repo_dir}...")
    try:
        run(["git", "clone", repo, str(repo_dir)])
    except subprocess.CalledProcessError:
        raise SystemExit(f"Error: failed to clone {repo}")
    return repo_dir


def clone_template_repo(tmp_dir: Path) -> None:
    print(f"Cloning {TEMPLATE_REPO} into {tmp_dir}...")
    try:
        run(["git", "clone", TEMPLATE_REPO, str(tmp_dir)])
    except subprocess.CalledProcessError:
        raise SystemExit(f"Error: failed to clone template repo {TEMPLATE_REPO}")

    git_dir = tmp_dir / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)


def copy_tree_contents(source_dir: Path, target_dir: Path) -> None:
    for source_item in source_dir.iterdir():
        target_item = target_dir / source_item.name

        if source_item.is_dir():
            if target_item.exists() and not target_item.is_dir():
                target_item.unlink()
            shutil.copytree(source_item, target_item, dirs_exist_ok=True)
            continue

        if target_item.exists():
            if target_item.is_dir():
                shutil.rmtree(target_item)
            else:
                target_item.unlink()
        shutil.copy2(source_item, target_item)


def main() -> int:
    args = parse_args()
    try:
        repo_dir = prepare_repo(args.repo, args.dest)
    except ValueError as exc:
        print(exc)
        return 1

    with tempfile.TemporaryDirectory() as tmp_dir:
        template_dir = Path(tmp_dir) / "template"
        clone_template_repo(template_dir)
        copy_tree_contents(template_dir, repo_dir)

    init_script = repo_dir / "scripts" / "init.sh"
    if init_script.exists():
        print(f"Running {init_script}...")
        run(["bash", str(init_script)], cwd=repo_dir)
    else:
        print(f"Warning: {init_script} not found, skipping.")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
