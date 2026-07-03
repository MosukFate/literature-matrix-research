#!/usr/bin/env python3
"""Package this skill into a portable ZIP file."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path


EXCLUDE_PARTS = {"__pycache__", ".git"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}


def should_include(path: Path) -> bool:
    if any(part in EXCLUDE_PARTS for part in path.parts):
        return False
    if path.suffix in EXCLUDE_SUFFIXES:
        return False
    return True


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path, help="Path to literature-matrix-research")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output zip path")
    args = parser.parse_args()

    skill_dir = args.skill_dir.resolve()
    if not (skill_dir / "SKILL.md").exists():
        raise SystemExit(f"SKILL.md not found in {skill_dir}")
    output = args.output or skill_dir.with_suffix(".zip")
    output = output.resolve()
    if output.exists():
        output.unlink()

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(skill_dir.rglob("*")):
            if not path.is_file() or not should_include(path):
                continue
            arcname = Path(skill_dir.name) / path.relative_to(skill_dir)
            zf.write(path, arcname.as_posix())

    print(f"created={output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
