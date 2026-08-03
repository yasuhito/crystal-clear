"""Discover, materialize, and hash complete Crystal Clear skill artifacts."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path
from typing import Callable


REPO_ROOT = Path(__file__).resolve().parent.parent
_ROOT_ARTIFACTS = ("SKILL.md", "language-guides.md", "elements-of-style.md")


def _git(command: list[str]) -> bytes:
    return subprocess.run(
        ["git", *command],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    ).stdout


def _directory_artifact_paths(directory: Path) -> tuple[str, ...]:
    paths = [name for name in _ROOT_ARTIFACTS if (directory / name).is_file()]
    references = directory / "references"
    if references.is_dir():
        paths.extend(
            path.relative_to(directory).as_posix()
            for path in references.rglob("*")
            if path.is_file()
        )
    return tuple(sorted(set(paths), key=lambda name: (name != "SKILL.md", name)))


def discover_skill_artifacts(ref: str) -> tuple[str, ...]:
    """Return artifact paths for a worktree or ref, including references recursively.

    Historical revisions may expose ``elements-of-style.md`` at the repository root;
    current revisions expose the recursively indexed ``references/`` tree.
    """
    if ref == "worktree":
        ordered = _directory_artifact_paths(REPO_ROOT)
    else:
        names = _git(
            [
                "ls-tree",
                "-r",
                "--name-only",
                ref,
                "--",
                *_ROOT_ARTIFACTS,
                "references",
            ]
        ).decode().splitlines()
        paths = [
            name
            for name in names
            if name in _ROOT_ARTIFACTS or name.startswith("references/")
        ]
        ordered = tuple(sorted(set(paths), key=lambda name: (name != "SKILL.md", name)))
    if "SKILL.md" not in ordered:
        raise FileNotFoundError(f"{ref!r} does not contain SKILL.md")
    return ordered


def read_skill_artifact(ref: str, name: str) -> bytes:
    if ref == "worktree":
        return (REPO_ROOT / name).read_bytes()
    return _git(["show", f"{ref}:{name}"])


def materialize_skill_artifacts(
    ref: str,
    destination: Path,
    *,
    transform: Callable[[str, bytes], bytes] | None = None,
) -> tuple[Path, dict[str, str]]:
    """Copy all discovered artifacts and return SKILL.md plus SHA-256 hashes."""
    destination.mkdir(parents=True, exist_ok=True)
    hashes: dict[str, str] = {}
    for name in discover_skill_artifacts(ref):
        content = read_skill_artifact(ref, name)
        if transform is not None:
            content = transform(name, content)
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        hashes[name] = hashlib.sha256(content).hexdigest()
    return destination / "SKILL.md", hashes


def materialized_skill_artifact_hashes(directory: Path) -> dict[str, str]:
    return {
        name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
        for name in _directory_artifact_paths(directory)
    }


def skill_artifact_hashes(ref: str) -> dict[str, str]:
    return {
        name: hashlib.sha256(read_skill_artifact(ref, name)).hexdigest()
        for name in discover_skill_artifacts(ref)
    }
