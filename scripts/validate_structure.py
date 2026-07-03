#!/usr/bin/env python3
"""Validate the structure of an Obsidian literature matrix package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REQUIRED_HEADINGS = [
    "## 0. 总览摘要",
    "## 1. 论文定位与核心痛点",
    "## 2. 核心思想与逻辑链",
    "## 3. 方法/模型/训练/推理拆解",
    "## 4. 数学公式、推导与算法映射",
    "## 5. 创新点与 baseline 本质差异",
    "## 6. 实验、消融、效率与可信度",
    "## 7. 优缺点、局限与过度宣传风险",
    "## 8. 复现路径与落地适用性",
    "## 9. 阅读建议与相关工作",
    "## 10. 最终总结",
]

BEGINNER_HEADING = "## 0. 总览摘要"
BEGINNER_LABELS = [
    "一句话总结",
    "三句话总结",
]
PLACEHOLDER_RE = re.compile(r"TODO|TBD|\?\?\?\?|主控|主 agent|这篇的用处是这篇的用处", re.IGNORECASE)
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WIKI_LINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
STUB_TYPES = {"paper-stub", "matrix-stub", "stub", "planning-stub"}
MIN_DEEP_CARD_CHARS = 2500
MIN_METHOD_CHARS = 600
MIN_EVIDENCE_CHARS = 450
STUB_SOURCE_RE = re.compile(r"source-level ready|prior survey|table-level pending", re.IGNORECASE)

SHALLOW_SOURCE_STATUS_RE = re.compile(
    r"metadata verified|metadata-only|abstract[- ]?only|abstract-level|full[- ]?text.*pending|table[- ]?level.*pending|source[- ]?level only|source-level ready|prior survey|not read|deep reading pending|pdf.*pending|metadata/abstract",
    re.IGNORECASE,
)
SHALLOW_BODY_RE = re.compile(
    r"without returning to the original PDF/HTML|full text was not read|not read the full text|metadata/abstract|metadata-only|abstract-only|没有读全文|只基于|仅基于|未读全文|未阅读全文",
    re.IGNORECASE,
)
NOVICE_CHECK_RE = re.compile(r"小白细节自检|Novice detail check", re.IGNORECASE)
NOVICE_FAIL_RE = re.compile(
    r"仍然不知道|无法复原|不能复原|细节不足|不足以复原|insufficient|not enough|cannot reconstruct|unable to reconstruct|details are insufficient|full text was not read|没有读全文|未读全文",
    re.IGNORECASE,
)
SOURCE_ANCHOR_RE = re.compile(
    r"https?://|arXiv|OpenReview|CVF|ACL|NeurIPS|ICML|ICLR|AAAI|EMNLP|PDF|HTML|Table\s+\d+|Figure\s+\d+|Fig\.|Sec\.|Section|source ledger|converted full text|manual correction|official",
    re.IGNORECASE,
)
NO_TABLE_UNREAD_RE = re.compile(
    r"no extractable result table.*(?:full text.*not read|without returning|pending)|未读全文.*无表|没读全文.*无表",
    re.IGNORECASE | re.DOTALL,
)
RESULT_INTERPRETATION_RE = re.compile(r"结果解析|Result interpretation", re.IGNORECASE)
NO_TABLE_RE = re.compile(r"no extractable result table|无可提取|没有可提取|无相关.*结果表|not applicable because", re.IGNORECASE)
EXAMPLE_RE = re.compile(r"例如|比如|像|Example|For example", re.IGNORECASE)
UNCLEAR_RE = re.compile(r"论文未明确说明|我无法从当前内容确认|not specified|cannot confirm", re.IGNORECASE)


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
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in ignored for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def resolve_markdown_link(base_file: Path, target: str, root: Path) -> bool:
    target = unquote(target.strip().strip("<>"))
    if not target or target.startswith("#"):
        return True
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return True
    target = target.split("#", 1)[0]
    if not target:
        return True
    candidate = (base_file.parent / target).resolve()
    if candidate.exists():
        return True
    if candidate.suffix == "":
        for suffix in (".md", ".canvas"):
            if candidate.with_suffix(suffix).exists():
                return True
    return False


def build_stem_index(files: list[Path]) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in files:
        index.setdefault(path.stem, []).append(path)
    return index


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


def inferred_paper_id(path: Path, fm: dict[str, str]) -> str:
    if fm.get("paper_id"):
        return fm["paper_id"]
    stem = path.stem
    match = re.match(r"(?:\d+_)?([A-Z]+[0-9]+)", stem)
    return match.group(1) if match else stem


def resolve_wikilink(raw: str, stem_index: dict[str, list[Path]]) -> bool:
    target = raw.split("|", 1)[0].split("#", 1)[0].strip()
    if not target:
        return True
    if "/" in target or "\\" in target:
        return Path(target).suffix in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".canvas"} or Path(target).stem in stem_index
    return target in stem_index


def extract_section(text: str, heading_prefix: str) -> str:
    pattern = re.compile(
        rf"(?ms)^##\s+{re.escape(heading_prefix)}.*?(?=^##\s+\d+\.|\Z)"
    )
    match = pattern.search(text)
    return match.group(0) if match else ""



def extract_novice_detail_check(text: str) -> str:
    match = NOVICE_CHECK_RE.search(text)
    if not match:
        return ""
    line_start = text.rfind("\n", 0, match.start())
    start = 0 if line_start == -1 else line_start + 1
    next_heading = re.search(r"(?m)^#{2,3}\s+", text[match.end():])
    end = len(text) if not next_heading else match.end() + next_heading.start()
    return text[start:end]


def has_any(text: str, terms: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def deep_card_issues(text: str, fm: dict[str, str]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    overview = extract_section(text, "0.")
    logic = extract_section(text, "2.")
    method = extract_section(text, "3.")
    formula = extract_section(text, "4.")
    innovation = extract_section(text, "5.")
    evidence = extract_section(text, "6.")
    reproduction = extract_section(text, "8.")
    final = extract_section(text, "10.")
    source_status = fm.get("source_status", "")

    novice_check = extract_novice_detail_check(text)

    if SHALLOW_SOURCE_STATUS_RE.search(source_status):
        issues.append({
            "severity": "critical",
            "issue": f"paper_card_has_shallow_or_pending_source_status:{source_status}",
        })
    if SHALLOW_BODY_RE.search(text):
        issues.append({"severity": "critical", "issue": "paper_card_contains_metadata_or_abstract_only_disclaimer"})
    if not SOURCE_ANCHOR_RE.search(text):
        issues.append({"severity": "major", "issue": "missing_source_anchor_for_formal_paper_card"})
    if not novice_check:
        issues.append({"severity": "critical", "issue": "missing_novice_detail_check"})
    elif NOVICE_FAIL_RE.search(novice_check):
        issues.append({"severity": "critical", "issue": "novice_detail_check_reports_insufficient_detail"})
    if NO_TABLE_UNREAD_RE.search(text):
        issues.append({"severity": "critical", "issue": "no_table_statement_based_on_unread_or_pending_full_text"})

    if len(text) < MIN_DEEP_CARD_CHARS:
        issues.append({
            "severity": "critical",
            "issue": f"paper_card_too_short_for_deep_card:{len(text)}<{MIN_DEEP_CARD_CHARS}",
        })
    if len(method) < MIN_METHOD_CHARS:
        issues.append({
            "severity": "critical",
            "issue": f"method_section_too_short_for_layered_reconstruction:{len(method)}<{MIN_METHOD_CHARS}",
        })
    if len(evidence) < MIN_EVIDENCE_CHARS:
        issues.append({
            "severity": "major",
            "issue": f"evidence_section_too_short_for_source_grounding:{len(evidence)}<{MIN_EVIDENCE_CHARS}",
        })
    if not (
        has_any(method, ("怎么做", "how", "pipeline", "流程"))
        and has_any(method, ("输入", "输出", "input", "output"))
        and has_any(method, ("训练", "推理", "training", "inference"))
    ):
        issues.append({"severity": "critical", "issue": "missing_method_model_training_inference_ladder"})
    if not has_any(logic, ("观察", "假设", "方法", "实验", "有效", "logic", "hypothesis")):
        issues.append({"severity": "major", "issue": "missing_core_logic_chain"})
    if not (
        has_any(formula, ("公式", "变量", "损失", "目标", "推导", "复杂度", "formula", "variable", "loss", "objective"))
        and has_any(formula, ("代码", "算法", "训练循环", "推理", "mapping", "implementation"))
    ) and not UNCLEAR_RE.search(formula):
        issues.append({"severity": "critical", "issue": "missing_formula_derivation_or_algorithm_mapping"})
    if not has_any(innovation, ("baseline", "本质区别", "创新", "工程", "替代", "改了")):
        issues.append({"severity": "major", "issue": "missing_innovation_and_baseline_difference"})
    if not has_any(reproduction, ("复现", "实现", "最小", "落地", "部署", "reproduce", "implementation")):
        issues.append({"severity": "major", "issue": "missing_reproduction_or_deployment_view"})
    if not (has_any(overview, ("一句话总结", "三句话总结")) and has_any(final, ("一句话总结", "三句话总结", "口语版总结"))):
        issues.append({"severity": "major", "issue": "missing_required_summary_blocks"})
    if STUB_SOURCE_RE.search(source_status):
        issues.append({"severity": "critical", "issue": f"paper_card_has_stub_source_status:{source_status}"})
    if not RESULT_INTERPRETATION_RE.search(text) and not NO_TABLE_RE.search(text):
        issues.append({"severity": "major", "issue": "missing_result_table_interpretation_or_explicit_no_table_statement"})
    if not EXAMPLE_RE.search(text):
        issues.append({"severity": "major", "issue": "missing_embedded_example_or_analogy"})
    return issues


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Obsidian package root")
    parser.add_argument("--require-beginner", action="store_true", help="Require beginner guide heading and labels on paper cards")
    args = parser.parse_args()

    root = args.root.resolve()
    files = markdown_files(root)
    stem_index = build_stem_index(files)
    paper_cards: list[Path] = []
    issues: list[dict[str, str]] = []
    seen_ids: dict[str, Path] = {}

    for path in files:
        text = read_text(path)
        fm = frontmatter(text)
        rel = str(path.relative_to(root))

        if PLACEHOLDER_RE.search(text):
            issues.append({"severity": "major", "path": rel, "issue": "placeholder_or_template_residue"})

        if looks_like_card(path, root, fm):
            paper_id = inferred_paper_id(path, fm)
            paper_cards.append(path)
            if paper_id in seen_ids:
                issues.append({"severity": "critical", "path": rel, "issue": f"duplicate_paper_id:{paper_id}", "other": str(seen_ids[paper_id].relative_to(root))})
            seen_ids[paper_id] = path
            if "paper_id" not in fm:
                issues.append({"severity": "minor", "path": rel, "issue": f"inferred_missing_frontmatter_paper_id:{paper_id}"})
            if "source_status" not in fm:
                issues.append({"severity": "major", "path": rel, "issue": "missing_source_status"})
            if "<!-- one_sentence_summary:start -->" not in text or "<!-- one_sentence_summary:end -->" not in text:
                issues.append({"severity": "major", "path": rel, "issue": "missing_one_sentence_summary_block"})
            for heading in REQUIRED_HEADINGS:
                if heading not in text:
                    issues.append({"severity": "major", "path": rel, "issue": f"missing_heading:{heading}"})
            if args.require_beginner:
                if BEGINNER_HEADING not in text:
                    issues.append({"severity": "major", "path": rel, "issue": "missing_beginner_heading"})
                for label in BEGINNER_LABELS:
                    if label not in text:
                        issues.append({"severity": "minor", "path": rel, "issue": f"missing_beginner_label:{label}"})
            for deep_issue in deep_card_issues(text, fm):
                deep_issue["path"] = rel
                issues.append(deep_issue)

        for target in MD_LINK_RE.findall(text):
            if not resolve_markdown_link(path, target, root):
                issues.append({"severity": "major", "path": rel, "issue": f"broken_markdown_link:{target}"})
        for target in WIKI_LINK_RE.findall(text):
            if not resolve_wikilink(target, stem_index):
                issues.append({"severity": "major", "path": rel, "issue": f"broken_wikilink:{target}"})

    report = {
        "root": str(root),
        "markdown_files": len(files),
        "paper_cards": len(paper_cards),
        "unique_paper_ids": len(seen_ids),
        "issues": issues,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
