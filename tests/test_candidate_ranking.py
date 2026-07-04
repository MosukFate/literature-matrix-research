import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from discover_candidates import Candidate, merge_candidates, rank_candidates

fixture = json.loads((ROOT / "tests" / "fixtures" / "discovery_minimal.json").read_text(encoding="utf-8"))

def ranked_rows():
    candidates = [Candidate.from_raw(row, gap=fixture["gap"]) for row in fixture["records"]]
    return rank_candidates(merge_candidates(candidates), gap=fixture["gap"], current_year=2026)


def test_core_requires_direct_gap_value_not_raw_citations():
    rows = ranked_rows()
    survey = next(row for row in rows if row.title == "A Highly Cited Survey of Generic Neural Networks")
    assert survey.citation_score > 0.9
    assert survey.layer != "core"
    assert survey.relevance_score < 0.35


def test_direct_mechanism_or_benchmark_work_can_be_core_or_bridge():
    rows = ranked_rows()
    low_fact = next(row for row in rows if row.arxiv_id == "2501.00001")
    assert low_fact.layer in {"core", "bridge"}
    assert low_fact.why_core
    acl = next(row for row in rows if row.acl_id)
    assert acl.layer in {"core", "bridge", "supplemental"}
    assert acl.relevance_score >= 0.35


if __name__ == "__main__":
    test_core_requires_direct_gap_value_not_raw_citations()
    test_direct_mechanism_or_benchmark_work_can_be_core_or_bridge()
    print("test_candidate_ranking.py passed")
