#!/usr/bin/env python3
"""Check local evidence links after export; this does not verify scientific claims."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


LINK_RE = re.compile(r'!?\[[^\]\n]*\]\(\s*(<[^>\n]*>|[^\s)\n]+)(?:\s+["\'][^\n]*?["\'])?\s*\)')
LEDGER_RE = re.compile(r"^\s*(?:asset_path|source_page_render):\s*(.+?)\s*$")
IGNORED = {".git", ".obsidian", "node_modules", "__pycache__"}


def scan_links(root: Path) -> dict:
    root = root.resolve()
    issues = []
    checked = 0
    files = sorted(path for path in root.rglob("*.md") if not any(part in IGNORED for part in path.parts))
    if not root.is_dir():
        issues.append({"path": str(root), "issue": "missing_package_root"})
    for path in files:
        fenced = False
        for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            targets = []
            ledger = LEDGER_RE.match(line)
            if ledger:
                target = ledger.group(1).strip().strip('"\'')
                if target.lower() not in {"unknown", "pending", "none"} and not target.lower().startswith("not applicable"):
                    targets.append(target)
            if line.lstrip().startswith(("```", "~~~")):
                fenced = not fenced
            elif not fenced:
                targets.extend(match.group(1).strip("<>") for match in LINK_RE.finditer(line))
            for target in targets:
                if target.startswith(("#", "//")) or urlsplit(target).scheme.lower() in {"http", "https", "mailto", "data"}:
                    continue
                local = unquote(target.split("#", 1)[0].split("?", 1)[0])
                if not local:
                    continue
                checked += 1
                resolved = (path.parent / local).resolve()
                issue = None
                if not resolved.is_relative_to(root):
                    issue = "target_outside_package"
                elif not resolved.exists():
                    issue = "missing_local_target"
                if issue:
                    issues.append({"path": path.relative_to(root).as_posix(), "line": number, "target": target, "issue": issue})
    return {
        "root": str(root),
        "markdown_files_scanned": len(files),
        "local_targets_checked": checked,
        "issues": issues,
        "scope": "Local packaging only; figure numbers, PDF pages, captions and scientific claims require source review.",
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Exported package root")
    report = scan_links(parser.parse_args().root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    sys.exit(main())
