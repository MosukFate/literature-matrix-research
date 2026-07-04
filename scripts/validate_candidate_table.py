#!/usr/bin/env python3
"""Validate discovery candidate tables before matrix handoff."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Iterable

REQUIRED_FIELDS = [
    "id", "title", "year", "venue", "sources", "source_status", "layer",
    "overall_score", "relevance_score", "venue_score", "citation_score",
    "recency_score", "novelty_risk_score", "citation_count", "graph_relation",
    "doi", "arxiv_id", "openreview_id", "acl_id", "pmlr_url", "cvf_url",
    "semantic_scholar_id", "openalex_id", "official_url", "pdf_url",
    "code_url", "data_url", "why_relevant", "why_core", "query", "abstract",
]

VALID_LAYERS = {"core", "bridge", "supplemental", "matrix-only", "excluded"}


def as_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return -1.0


def first_identity(row: dict[str, str]) -> tuple[str, str]:
    for field in ["doi", "arxiv_id", "openreview_id", "acl_id", "pmlr_url", "cvf_url", "official_url"]:
        value = (row.get(field) or "").strip().lower().rstrip("/")
        if value:
            return field, value
    return "title", " ".join((row.get("title") or "").lower().split())


def validate_rows(rows: list[dict[str, str]], expected_fields: Iterable[str] = REQUIRED_FIELDS) -> list[str]:
    if not rows:
        return ["candidate_table_empty"]
    issues: list[str] = []
    fields = set(rows[0].keys())
    for field in expected_fields:
        if field not in fields:
            issues.append(f"missing_field:{field}")
    seen: set[tuple[str, str]] = set()
    for index, row in enumerate(rows, start=2):
        if not (row.get("title") or "").strip():
            issues.append(f"row_{index}:missing_title")
        if not (row.get("source_status") or "").strip():
            issues.append(f"row_{index}:missing_source_status")
        layer = (row.get("layer") or "").strip()
        if layer not in VALID_LAYERS:
            issues.append(f"row_{index}:invalid_layer:{layer}")
        for field in ["overall_score", "relevance_score", "venue_score", "citation_score", "recency_score", "novelty_risk_score"]:
            value = as_float(row.get(field, ""))
            if value < 0 or value > 1:
                issues.append(f"row_{index}:score_out_of_range:{field}")
        status = row.get("source_status", "")
        if status.startswith("official") and not (row.get("official_url") or row.get("pmlr_url") or row.get("cvf_url") or row.get("acl_id") or row.get("openreview_id")):
            issues.append(f"row_{index}:official_status_without_official_anchor")
        if "arxiv-only" in status and layer in {"core", "bridge"} and not (row.get("why_core") or "").strip():
            issues.append(f"row_{index}:arxiv_core_or_bridge_missing_why_core")
        if as_float(row.get("citation_score", "0")) > 0.9 and as_float(row.get("relevance_score", "0")) < 0.35 and layer == "core":
            issues.append(f"row_{index}:high_citation_low_relevance_core")
        identity = first_identity(row)
        if identity in seen:
            issues.append(f"row_{index}:duplicate_identity:{identity[0]}:{identity[1]}")
        seen.add(identity)
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate_table", type=Path)
    args = parser.parse_args(argv)
    with args.candidate_table.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    issues = validate_rows(rows)
    if issues:
        for issue in issues:
            print(issue)
        return 1
    print(f"validated={args.candidate_table} rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
