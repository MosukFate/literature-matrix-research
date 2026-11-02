#!/usr/bin/env python3
"""Scan paper cards for content-risk cues that need human/source review."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


STRONG_RE = re.compile(r"证明|直接证明|必须|一定|完全|唯一|SOTA|state-of-the-art|best", re.IGNORECASE)
NEGATED_STRONG_PREFIX_RE = re.compile(
    r"(?:尚未|并未|没有|未|不能|无法|不足以|不|并非|不是)"
    r"(?:直接|被|充分|严格|完全|能|意味着|代表|视为|认定为|称为|认为|普遍|全局|是|证明|\s){0,4}$"
    r"|(?:not|cannot|can't|doesn't|do not|no)\s+"
    r"(?:(?:necessarily|fully|directly|a|the|be|considered|universally)\s+){0,4}$",
    re.IGNORECASE,
)
NUMBER_RE = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?\s*(?:%|K|k|M|B|篇|张|个|次|分|points?|samples?|models?)?")
FORMULA_RE = re.compile(r"\$\$.*?\$\$|\$[^$\n]+\$", re.DOTALL)
ANCHOR_HINT_RE = re.compile(r"ledger|Evidence|Anchor|PDF|Table|Figure|Fig\.|Sec\.|Section|OpenReview|arXiv|CVF|ACL|NeurIPS|ICML|ICLR|AAAI|EMNLP|official|source_status|核验|表|图|节", re.IGNORECASE)
SHALLOW_SOURCE_STATUS_RE = re.compile(
    r"metadata verified|metadata-only|abstract[- ]?only|abstract-level|full[- ]?text.*pending|table[- ]?level.*pending|source[- ]?level only|source-level ready|prior survey|not read|deep reading pending|metadata/abstract",
    re.IGNORECASE,
)
NOVICE_CHECK_RE = re.compile(r"小白细节自检|Novice detail check", re.IGNORECASE)
NOVICE_FAIL_RE = re.compile(
    r"仍然不知道|无法复原|不能复原|细节不足|不足以复原|insufficient|not enough|cannot reconstruct|unable to reconstruct|details are insufficient|full text was not read|没有读全文|未读全文",
    re.IGNORECASE,
)
EXPLANATION_RE = re.compile(r"符号解释|公式解释|其中|变量|含义|表示|是指|这里|目标|动机|训练|推理|代码|算法映射|自然语言|阈值|解释规则|概率.{0,12}倍")
FORMULA_SECTION_RE = re.compile(r"(?ms)^##\s+4\.\s+.*?(?=^##\s+\d+\.|\Z)")
BASELINE_SECTION_RE = re.compile(r"(?ms)^##\s+5\.\s+.*?(?=^##\s+\d+\.|\Z)")
REPRO_SECTION_RE = re.compile(r"(?ms)^##\s+8\.\s+.*?(?=^##\s+\d+\.|\Z)")
BASELINE_DETAIL_RE = re.compile(r"baseline|本质区别|相比|替代|多做|少做|改了|目标函数|训练|推理|数据构造", re.IGNORECASE)
REPRO_DETAIL_RE = re.compile(r"复现|实现|最小|先实现|简化|超参数|训练 trick|评估协议|落地|部署", re.IGNORECASE)
MAPPING_DETAIL_RE = re.compile(r"代码|训练循环|推理阶段|显式计算|隐式学习|算法映射|implementation|mapping", re.IGNORECASE)
STUB_TYPES = {"paper-stub", "matrix-stub", "stub", "planning-stub"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for raw in text[4:end].splitlines():
        if ":" not in raw or raw.startswith(" "):
            continue
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def markdown_files(root: Path) -> list[Path]:
    ignored = {".git", ".obsidian", "node_modules", "__pycache__"}
    return sorted(path for path in root.rglob("*.md") if not any(part in ignored for part in path.parts))


def looks_like_card(path: Path, root: Path, fm: dict[str, str]) -> bool:
    if path.name.lower() == "index.md":
        return False
    note_type = fm.get("type", "").strip().lower()
    if note_type in STUB_TYPES:
        return False
    if note_type == "paper-card":
        return True
    if fm.get("paper_id"):
        return True
    if path.name.startswith("00_"):
        return False
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        return False
    return bool(rel_parts and re.match(r"0[1-7]_", rel_parts[0]))


def context_lines(lines: list[str], index: int, radius: int = 3) -> str:
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)
    return "\n".join(lines[start:end])


def has_positive_strong_claim(line: str) -> bool:
    # Match each occurrence separately: a negated claim must not hide a later one.
    return any(not NEGATED_STRONG_PREFIX_RE.search(line[:match.start()]) for match in STRONG_RE.finditer(line))


def table_anchor_context(lines: list[str], index: int) -> str:
    if not lines[index].lstrip().startswith("|"):
        return context_lines(lines, index, 2)
    start = index
    while start > 0 and lines[start - 1].lstrip().startswith("|"):
        start -= 1
    context = lines[start:min(start + 2, index + 1)] + [lines[index]]
    previous = start - 1
    # Only the immediately preceding paragraph belongs to this table.
    while previous >= 0 and not lines[previous].strip() and start - previous <= 2:
        previous -= 1
    for _ in range(4):
        if previous < 0 or not lines[previous].strip() or lines[previous].strip() == "---" or lines[previous].lstrip().startswith(("|", "#")):
            break
        context.append(lines[previous])
        previous -= 1
    return "\n".join(context)


def extract_section(pattern: re.Pattern[str], text: str) -> str:
    match = pattern.search(text)
    return match.group(0) if match else ""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Obsidian package root")
    args = parser.parse_args()

    root = args.root.resolve()
    issues: list[dict[str, str]] = []
    cards = 0

    for path in markdown_files(root):
        text = read_text(path)
        fm = frontmatter(text)
        if not looks_like_card(path, root, fm):
            continue
        cards += 1
        rel = str(path.relative_to(root))
        lines = text.splitlines()
        source_status = fm.get("source_status", "")

        if not source_status:
            issues.append({"severity": "major", "path": rel, "issue": "missing_source_status"})
        if "pending" in source_status.lower() or "arxiv-only" in source_status.lower():
            issues.append({"severity": "minor", "path": rel, "issue": f"weak_or_pending_source_status:{source_status}"})

        if source_status and SHALLOW_SOURCE_STATUS_RE.search(source_status):
            issues.append({"severity": "major", "path": rel, "issue": f"formal_card_shallow_or_pending_source_status:{source_status}"})
        if fm.get("type", "").strip().lower() == "paper-card":
            if not NOVICE_CHECK_RE.search(text):
                issues.append({"severity": "major", "path": rel, "issue": "missing_novice_detail_check"})
            elif NOVICE_FAIL_RE.search(text):
                issues.append({"severity": "major", "path": rel, "issue": "novice_detail_check_reports_insufficient_detail"})

        for idx, line in enumerate(lines, start=1):
            if has_positive_strong_claim(line):
                issues.append({"severity": "review", "path": rel, "line": idx, "issue": "strong_claim_word", "text": line.strip()[:240]})
            if "未核验数字" in line and "无" not in line:
                issues.append({"severity": "major", "path": rel, "line": idx, "issue": "unverified_number_marker", "text": line.strip()[:240]})
            if NUMBER_RE.search(line) and "|" in line and not ANCHOR_HINT_RE.search(table_anchor_context(lines, idx - 1)):
                issues.append({"severity": "review", "path": rel, "line": idx, "issue": "numeric_table_line_without_obvious_anchor", "text": line.strip()[:240]})

        formula_section = extract_section(FORMULA_SECTION_RE, text)
        baseline_section = extract_section(BASELINE_SECTION_RE, text)
        reproduction_section = extract_section(REPRO_SECTION_RE, text)

        if "$" in formula_section and not MAPPING_DETAIL_RE.search(formula_section):
            issues.append({"severity": "major", "path": rel, "issue": "formula_section_missing_algorithm_mapping"})
        if baseline_section and not BASELINE_DETAIL_RE.search(baseline_section):
            issues.append({"severity": "major", "path": rel, "issue": "baseline_section_missing_concrete_difference"})
        if reproduction_section and not REPRO_DETAIL_RE.search(reproduction_section):
            issues.append({"severity": "major", "path": rel, "issue": "reproduction_section_missing_implementation_details"})

        for match in FORMULA_RE.finditer(text):
            line_no = text[: match.start()].count("\n") + 1
            line_index = line_no - 1
            ctx = context_lines(lines, line_index, 5)
            if not EXPLANATION_RE.search(ctx):
                issues.append({"severity": "major", "path": rel, "line": line_no, "issue": "formula_without_nearby_symbol_explanation"})

    report = {
        "root": str(root),
        "paper_cards_scanned": cards,
        "issues": issues,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if any(issue["severity"] in {"critical", "major"} for issue in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
