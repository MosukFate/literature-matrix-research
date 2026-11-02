"""Offline official-index regression checks; network is replaced at http_text."""

import argparse
import pathlib
import sys
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import discover_candidates as discovery

PMLR = "https://proceedings.mlr.press/"
CVF = "https://openaccess.thecvf.com/menu"
PMLR_INDEX = '''<ul>
<li><a href="v306"><b>Volume 306</b></a> Proceedings of ICML 2026</li>
<li><a href="v300"><b>Volume 300</b></a> Proceedings of AISTATS 2026</li>
<li><a href="v267"><b>Volume 267</b></a> Proceedings of ICML 2025</li>
<li><a href="v318"><b>Volume 318</b></a> Proceedings of Canadian Conference on AI</li>
</ul>'''
CVF_INDEX = '''<dl><dd>CVPR 2026 [<a href="CVPR2026">Main Conference</a>]
[<a href="CVPR2026_workshops">Workshops</a>]</dd>
<dd>WACV 2026 [<a href="/WACV2026">Main Conference</a>]</dd>
<dd>ICCV 2025 [<a href="ICCV2025">Main Conference</a>]</dd></dl>'''
PMLR_PAPERS = '''<div class="paper"><p class="title">Causal &amp; Visual Evidence</p>
<p class="links">[<a href="https://proceedings.mlr.press/v306/example26.html">abs</a>]</p></div>'''
CVF_PAPERS = '''<dt class="ptitle"><br><a href="/content/CVPR2026/html/Example_Causal_Visual_Evidence_CVPR_2026_paper.html">Causal <em>Visual</em> Evidence</a></dt>'''


class ConferenceDiscoveryTests(unittest.TestCase):
    def run_search(self, pages=None, **overrides):
        args = argparse.Namespace(query="causal visual evidence", seed_title="", gap="",
                                  seed_url="", limit=8, sleep=0, year_from=2026,
                                  year_to=2026, proceedings_venue=[])
        for name, value in overrides.items():
            setattr(args, name, value)
        pages = {PMLR: PMLR_INDEX, CVF: CVF_INDEX, **(pages or {})}
        requested = []

        def offline_http(url, failed, adapter, timeout=20):
            requested.append(url)
            if url in pages:
                return pages[url]
            failed.append({"adapter": adapter, "url": url, "error": "offline missing fixture"})
            return ""

        with patch.object(discovery, "http_text", side_effect=offline_http):
            raw, log, failed = discovery.live_search(args)
        return raw, log, failed, requested

    def test_pmlr_new_year_resolves_volume_and_preserves_year(self):
        raw, log, failed, urls = self.run_search(
            {PMLR + "v306/": PMLR_PAPERS}, proceedings_venue=["ICML"])
        found = [row for row in raw if row["source"] == "pmlr"]
        self.assertEqual([row["title"] for row in found], ["Causal & Visual Evidence"])
        self.assertEqual(found[0]["year"], 2026)
        self.assertIn(PMLR + "v306/", urls)
        self.assertNotIn(PMLR + "v267/", urls)
        self.assertNotIn(PMLR + "v300/", urls)
        self.assertNotIn(PMLR + "v318/", urls)

    def test_cvf_new_year_resolves_main_conference_and_nested_title(self):
        raw, log, failed, urls = self.run_search(
            {"https://openaccess.thecvf.com/CVPR2026?day=all": CVF_PAPERS},
            proceedings_venue=["CVPR"])
        found = [row for row in raw if row["source"] == "cvf"]
        self.assertEqual([row["title"] for row in found], ["Causal Visual Evidence"])
        self.assertEqual(found[0]["year"], 2026)
        self.assertIn("https://openaccess.thecvf.com/CVPR2026?day=all", urls)
        self.assertEqual(found[0]["venue"], "CVPR")
        self.assertFalse(any("CVPR2026_workshops" in url or "ICCV2025?" in url for url in urls))

    def test_pmlr_preserves_workshop_and_main_event_labels_in_candidates(self):
        index = ('<li><a href="v251">Volume 251</a> Proceedings of GRaM at ICML 2024</li>'
                 '<li><a href="v235">Volume 235</a> Proceedings of ICML 2024</li>')
        paper = ('<div class="paper"><p class="title">Causal Visual Evidence {}</p>'
                 '<a href="example24.html">abs</a></div>')
        pages = {PMLR: index, PMLR + "v251/": paper.format("Workshop"),
                 PMLR + "v235/": paper.format("Main")}
        with patch.object(discovery, "http_text", side_effect=lambda url, *_args: pages.get(url, "")):
            rows = discovery.search_pmlr("causal visual evidence", 8, [], 2024, 2024, ["ICML"])
        self.assertEqual([row["venue"] for row in rows],
                         ["Proceedings of GRaM at ICML 2024", "Proceedings of ICML 2024"])

    def test_missing_requested_year_is_no_index_coverage(self):
        raw, log, failed, urls = self.run_search(year_from=2027, year_to=2027)
        coverage = log.get("source_coverage", [])
        self.assertEqual(len(coverage), 2)
        self.assertTrue(all(item["status"] == "no-index" for item in coverage))
        self.assertTrue(all(item["missing_indexes"] == [{"year": 2027, "venue": "*"}]
                            for item in coverage))
        self.assertFalse(any("?day=all" in url or "/v306/" in url for url in urls))

    def test_unknown_pmlr_year_is_reported_and_not_invented(self):
        raw, log, failed, urls = self.run_search()
        pmlr = next((row for row in log.get("source_coverage", []) if row["adapter"] == "pmlr"), {})
        self.assertEqual(pmlr.get("unknown_year_indexes"),
                         [{"url": PMLR + "v318/", "label": "Proceedings of Canadian Conference on AI"}])
        self.assertNotIn(PMLR + "v318/", urls)
        self.assertFalse(any(row.get("year") == 0 for row in raw if row["source"] == "pmlr"))

    def test_retrieved_index_and_failed_proceedings_are_distinct(self):
        raw, log, failed, urls = self.run_search(proceedings_venue=["ICML"])
        pmlr = next((row for row in log.get("source_coverage", []) if row["adapter"] == "pmlr"), {})
        self.assertEqual(pmlr.get("index_status"), "retrieved")
        self.assertEqual(pmlr.get("status"), "partial")
        self.assertEqual([row["status"] for row in pmlr.get("proceedings", [])], ["failed"])

    def test_result_limit_reports_unvisited_proceedings(self):
        raw, log, failed, urls = self.run_search({PMLR + "v306/": PMLR_PAPERS}, limit=1)
        pmlr = next((row for row in log.get("source_coverage", []) if row["adapter"] == "pmlr"), {})
        self.assertEqual(pmlr.get("status"), "truncated")
        self.assertEqual([row["status"] for row in pmlr.get("proceedings", [])],
                         ["retrieved", "not-fetched-limit"])
        self.assertNotIn(PMLR + "v300/", urls)

    def test_successful_title_search_reports_retrieved_without_completeness_claim(self):
        raw, log, failed, urls = self.run_search({"https://openaccess.thecvf.com/CVPR2026?day=all": CVF_PAPERS},
                                                proceedings_venue=["CVPR"])
        cvf = next((row for row in log.get("source_coverage", []) if row["adapter"] == "cvf"), {})
        self.assertEqual(cvf.get("status"), "retrieved")
        self.assertEqual(cvf.get("returned_records"), 1)
        self.assertEqual(cvf.get("search_scope"), "main-conference indexes; title matching only")

    def test_unbounded_calls_use_recent_years_and_keep_three_argument_adapter_api(self):
        fixed_now = datetime(2026, 11, 1, tzinfo=timezone.utc)
        pages = {PMLR: PMLR_INDEX, PMLR + "v306/": PMLR_PAPERS}
        with patch.object(discovery, "datetime") as clock, patch.object(
                discovery, "http_text", side_effect=lambda url, *args: pages.get(url, "")):
            clock.now.return_value = fixed_now
            found = discovery.search_pmlr("causal visual evidence", 1, [])
        self.assertEqual([row["year"] for row in found], [2026])
        self.assertEqual(discovery.conference_year_window(0, 2023), (2021, 2023))
        with patch.object(discovery, "datetime") as clock:
            clock.now.return_value = fixed_now
            self.assertEqual(discovery.conference_year_window(), (2024, 2026))

    def test_failed_root_index_is_not_no_index(self):
        raw, log, failed, urls = self.run_search({PMLR: ""})
        pmlr = next(row for row in log.get("source_coverage", []) if row["adapter"] == "pmlr")
        self.assertEqual(pmlr["status"], "failed")
        self.assertEqual(pmlr["index_status"], "failed")
        self.assertEqual(pmlr["missing_indexes"], [])

    def test_changed_markup_is_unparsed_instead_of_zero_papers(self):
        raw, log, failed, urls = self.run_search({PMLR + "v306/": "<html>unexpected markup</html>"},
                                                proceedings_venue=["ICML"])
        pmlr = next(row for row in log.get("source_coverage", []) if row["adapter"] == "pmlr")
        self.assertEqual(pmlr["status"], "partial")
        self.assertEqual(pmlr["proceedings"][0]["status"], "unparsed")

    def test_limit_inside_one_index_records_omitted_title_matches(self):
        second = CVF_PAPERS.replace("Example_", "Second_").replace("Causal <em>Visual</em> Evidence", "Second Causal Visual Evidence")
        raw, log, failed, urls = self.run_search({"https://openaccess.thecvf.com/CVPR2026?day=all": CVF_PAPERS + second},
                                                proceedings_venue=["CVPR"], limit=1)
        cvf = next(row for row in log.get("source_coverage", []) if row["adapter"] == "cvf")
        self.assertEqual(cvf["status"], "truncated")
        self.assertEqual(cvf["proceedings"][0]["title_matches"], 2)
        self.assertEqual(cvf["returned_records"], 1)

    def test_historical_cvf_index_preserves_official_py_link(self):
        raw, log, failed, urls = self.run_search(
            {CVF: '<a href="CVPR2020.py">CVPR 2020 Main Conference</a>',
             "https://openaccess.thecvf.com/CVPR2020.py?day=all": CVF_PAPERS.replace("2026", "2020")},
            year_from=2020, year_to=2020, proceedings_venue=["CVPR"])
        found = [row for row in raw if row["source"] == "cvf"]
        self.assertEqual([row["year"] for row in found], [2020])
        self.assertIn("https://openaccess.thecvf.com/CVPR2020.py?day=all", urls)

    def test_historical_pmlr_reissue_link_keeps_its_known_event_year(self):
        raw, log, failed, urls = self.run_search(
            {PMLR: '<li><a href="r16"><b>Volume R16</b></a> Proceedings of UAI 2018</li>',
             PMLR + "r16/": PMLR_PAPERS.replace("v306/example26", "r16/example18")},
            year_from=2018, year_to=2018, proceedings_venue=["UAI"])
        found = [row for row in raw if row["source"] == "pmlr"]
        self.assertEqual([row["year"] for row in found], [2018])
        self.assertIn(PMLR + "r16/", urls)


if __name__ == "__main__":
    unittest.main()
