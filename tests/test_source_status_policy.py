import csv
import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from discover_candidates import Candidate, CANDIDATE_FIELDS, merge_candidates, rank_candidates, write_outputs
from validate_candidate_table import validate_rows

fixture = json.loads((ROOT / "tests" / "fixtures" / "discovery_minimal.json").read_text(encoding="utf-8"))

def test_arxiv_only_core_keeps_arxiv_status_and_why_core():
    candidates = [Candidate.from_raw(row, gap=fixture["gap"]) for row in fixture["records"]]
    rows = rank_candidates(merge_candidates(candidates), gap=fixture["gap"], current_year=2026)
    arxiv_core = next(row for row in rows if row.arxiv_id == "2501.00001")
    assert "arxiv-only" in arxiv_core.source_status
    assert arxiv_core.layer in {"core", "bridge"}
    assert arxiv_core.why_core


def test_candidate_table_validator_requires_status_and_scores():
    candidates = [Candidate.from_raw(row, gap=fixture["gap"]) for row in fixture["records"]]
    rows = rank_candidates(merge_candidates(candidates), gap=fixture["gap"], current_year=2026)
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = pathlib.Path(tmp)
        write_outputs(rows, out_dir, search_log={"queries": []}, failed_queries=[])
        with (out_dir / "candidate_table.csv").open(newline="", encoding="utf-8") as fh:
            csv_rows = list(csv.DictReader(fh))
        issues = validate_rows(csv_rows, expected_fields=CANDIDATE_FIELDS)
    assert issues == []


if __name__ == "__main__":
    test_arxiv_only_core_keeps_arxiv_status_and_why_core()
    test_candidate_table_validator_requires_status_and_scores()
    print("test_source_status_policy.py passed")
