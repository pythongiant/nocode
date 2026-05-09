# diff.py
# Workspace snapshotting and per-file change summaries.

from __future__ import annotations

import difflib
from pathlib import Path
from typing import Iterable

# Directories we never walk into when snapshotting.
IGNORE_DIRS = frozenset({
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "__pycache__",
    "env",
    "venv",
    ".venv",
    ".tox",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    ".next",
    ".cache",
})

# Files larger than this are not loaded into the snapshot
# (they are still tracked for create/delete, but no diff is computed).
MAX_BYTES = 512 * 1024


def _is_ignored(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return True
    return any(part in IGNORE_DIRS for part in rel.parts)


def snapshot(root: Path) -> dict[str, bytes | None]:
    """Map relpath -> bytes (or None when file is over the size limit)."""
    snap: dict[str, bytes | None] = {}
    if not root.is_dir():
        return snap
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if _is_ignored(path, root):
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        rel = str(path.relative_to(root))
        if size > MAX_BYTES:
            snap[rel] = None
            continue
        try:
            snap[rel] = path.read_bytes()
        except OSError:
            continue
    return snap


def _line_counts(a: bytes | None, b: bytes | None) -> tuple[int, int]:
    """Return (added, removed) line counts for a→b."""
    if a is None and b is None:
        return (0, 0)
    a_lines = (a or b"").decode("utf-8", errors="replace").splitlines()
    b_lines = (b or b"").decode("utf-8", errors="replace").splitlines()
    if a is None:
        return (len(b_lines), 0)
    if b is None:
        return (0, len(a_lines))
    added = removed = 0
    for line in difflib.unified_diff(a_lines, b_lines, n=0, lineterm=""):
        if line.startswith(("+++", "---", "@@")):
            continue
        if line.startswith("+"):
            added += 1
        elif line.startswith("-"):
            removed += 1
    return (added, removed)


def compute_changes(
    before: dict[str, bytes | None],
    after: dict[str, bytes | None],
) -> list[dict]:
    """Diff two snapshots; return one dict per changed file."""
    changes: list[dict] = []
    for path in sorted(set(before) | set(after)):
        a = before.get(path, None) if path in before else None
        b = after.get(path, None) if path in after else None
        in_before = path in before
        in_after = path in after
        if in_before and in_after and a == b:
            continue
        if in_before and not in_after:
            status = "deleted"
        elif in_after and not in_before:
            status = "created"
        else:
            status = "modified"
        added, removed = _line_counts(a, b)
        changes.append({
            "path": path,
            "added": added,
            "removed": removed,
            "status": status,
        })
    return changes


def format_changes_text(changes: Iterable[dict]) -> str:
    """Plain-text rendering of changes, included in the model-visible result."""
    lines = ["FILE CHANGES:"]
    for c in changes:
        suffix = "" if c["status"] == "modified" else f"  ({c['status']})"
        lines.append(
            f"  {c['path']}  +{c['added']} -{c['removed']}{suffix}"
        )
    return "\n".join(lines)
