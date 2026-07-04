import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from discover_candidates import Candidate, merge_candidates

fixture = json.loads((ROOT / "tests" / "fixtures" / "discovery_minimal.json").read_text(encoding="utf-8"))

def test_merges_same_arxiv_across_sources_and_preserves_ids():
    candidates = [Candidate.from_raw(row, gap=fixture["gap"]) for row in fixture["records"]]
    merged = merge_candidates(candidates)
    low_fact = [row for row in merged if row.arxiv_id == "2501.00001"]
    assert len(low_fact) == 1
    row = low_fact[0]
    assert row.semantic_scholar_id == "S2-LOWFACT"
    assert row.openalex_id == "W123"
    assert row.sources == ["arxiv", "semantic_scholar", "openalex"]


def test_prefers_official_url_over_arxiv_when_available():
    candidates = [Candidate.from_raw(row, gap=fixture["gap"]) for row in fixture["records"]]
    merged = merge_candidates(candidates)
    icml = next(row for row in merged if row.pmlr_url)
    assert icml.official_url == "https://proceedings.mlr.press/v235/fake.html"
    assert icml.source_status == "official:icml-pmlr"


if __name__ == "__main__":
    test_merges_same_arxiv_across_sources_and_preserves_ids()
    test_prefers_official_url_over_arxiv_when_available()
    print("test_candidate_normalization.py passed")
