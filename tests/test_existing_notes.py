import copy
import os
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from existing_notes import match_existing_notes

TEST_TEMP = pathlib.Path(os.environ.get("MATRIX_TEST_TMP", tempfile.gettempdir()))


class ExistingNotesTests(unittest.TestCase):
    def setUp(self):
        TEST_TEMP.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=TEST_TEMP)
        self.addCleanup(temporary.cleanup)
        self.notes_root = pathlib.Path(temporary.name)

    def note(self, relative_path, metadata, body=""):
        path = self.notes_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\n{metadata}\n---\n{body}", encoding="utf-8")
        return str(path.resolve())

    def matches(self, candidates):
        return match_existing_notes(candidates, self.notes_root)

    def test_doi_url_prefix_and_case_match_a_stub_without_promoting_it(self):
        path = self.note("stub.md", 'type: paper-stub\ntitle: "Earlier title"\ndoi: "https://doi.org/10.1234/AbC"')
        row = self.matches([{"id": "C0001", "title": "Published title", "doi": "DOI:10.1234/abc"}])[0]
        self.assertEqual(row, {
            "candidate_id": "C0001", "title": "Published title", "status": "matched",
            "match_reason": "doi", "existing_note_path": path, "existing_note_type": "paper-stub",
        })

    def test_versioned_arxiv_urls_and_the_local_arxiv_alias_share_identity(self):
        modern = self.note("nested/modern.md", 'title: "Old title"\narxiv: "2501.12345v1"')
        legacy = self.note("legacy.md", 'title: "Legacy"\narxiv_id: "https://arxiv.org/abs/hep-th/9901001v2"')
        rows = self.matches([
            {"id": "C1", "title": "Renamed", "pdf_url": "https://arxiv.org/pdf/2501.12345v4.pdf?download=1"},
            {"id": "C2", "title": "Other", "arxiv_id": "arXiv:hep-th/9901001v5"},
        ])
        self.assertEqual([row["existing_note_path"] for row in rows], [modern, legacy])
        self.assertEqual([row["match_reason"] for row in rows], ["arxiv_id", "arxiv_id"])

    def test_openreview_url_matches_case_sensitive_primary_id(self):
        path = self.note("openreview.md", 'title: "Original"\nopenreview_id: "AbC_12-X"')
        rows = self.matches([
            {"id": "C1", "title": "Renamed", "official_url": "https://openreview.net/forum?id=AbC_12-X"},
            {"id": "C2", "title": "Different", "openreview_id": "abc_12-x"},
        ])
        self.assertEqual(rows[0]["existing_note_path"], path)
        self.assertEqual(rows[0]["match_reason"], "openreview_id")
        self.assertEqual(rows[1]["status"], "no_match")

    def test_normalized_exact_title_preserves_unicode_identity(self):
        path = self.note("unicode.md", 'title: "模型甲： Café — Αλφα"')
        rows = self.matches([
            {"candidate_id": "C1", "title": "模型甲 cafe\u0301 ΑΛΦΑ"},
            {"candidate_id": "C2", "title": "模型乙: Café — Αλφα"},
        ])
        self.assertEqual(rows[0]["existing_note_path"], path)
        self.assertEqual(rows[0]["match_reason"], "title")
        self.assertEqual(rows[1]["status"], "no_match")
        self.assertEqual(rows[1]["candidate_id"], "C2")

    def test_exact_identifier_takes_priority_over_another_note_title(self):
        path = self.note("identity.md", 'title: "Earlier title"\ndoi: "10.1000/right"')
        self.note("title.md", 'title: "New title"')
        row = self.matches([{"id": "C1", "title": "New title", "doi": "10.1000/right"}])[0]
        self.assertEqual(row["status"], "matched")
        self.assertEqual(row["existing_note_path"], path)
        self.assertEqual(row["match_reason"], "doi")

    def test_conflicting_identifiers_block_a_same_title_match(self):
        self.note("collision.md", 'title: "Same title"\ndoi: "10.1000/wrong"')
        row = self.matches([{"id": "C1", "title": "Same title", "doi": "10.1000/right"}])[0]
        self.assertEqual(row["status"], "no_match")
        self.assertEqual(row["match_reason"], "conflicting_identifiers")
        self.assertNotIn("existing_note_path", row)

    def test_conflicting_secondary_identity_blocks_a_partial_id_match(self):
        self.note("collision.md", 'title: "Same"\ndoi: "10.1000/shared"\narxiv_id: "2501.00002"')
        row = self.matches([{"title": "Same", "doi": "10.1000/shared", "arxiv_id": "2501.00001"}])[0]
        self.assertEqual(row["status"], "no_match")
        self.assertEqual(row["match_reason"], "conflicting_identifiers")

    def test_conflicting_primary_id_and_url_cannot_hide_behind_an_intersection(self):
        self.note("collision.md", 'title: "Same"\narxiv_id: "2501.00002"\n' +
                  'official_url: "https://arxiv.org/abs/2501.00001"')
        row = self.matches([{"title": "Same", "arxiv_id": "2501.00001"}])[0]
        self.assertEqual(row["status"], "no_match")
        self.assertEqual(row["match_reason"], "conflicting_identifiers")

    def test_ambiguous_exact_titles_expose_every_path(self):
        first = self.note("a/card.md", 'type: paper-card\ntitle: "Shared title"')
        second = self.note("b/stub.md", 'type: matrix-stub\ntitle: "Shared title"')
        row = self.matches([{"id": "C1", "title": "Shared title"}])[0]
        self.assertEqual(row["status"], "ambiguous")
        self.assertEqual(row["match_reason"], "title")
        self.assertEqual(row["existing_note_paths"], [first, second])
        self.assertEqual(row["existing_note_types"], ["paper-card", "matrix-stub"])
        self.assertNotIn("existing_note_path", row)

    def test_duplicate_versioned_ids_are_ambiguous_even_with_different_titles(self):
        first = self.note("a.md", 'title: "First"\narxiv_id: "2501.12345v1"')
        second = self.note("b.md", 'title: "Second"\narxiv_id: "2501.12345v3"')
        row = self.matches([{"title": "Current", "arxiv_id": "2501.12345v5"}])[0]
        self.assertEqual(row["status"], "ambiguous")
        self.assertEqual(row["existing_note_paths"], [first, second])

    def test_body_citations_nested_metadata_and_aliases_do_not_define_identity(self):
        self.note("other.md", 'title: "Other paper"\naliases: ["Target"]\ncitations:\n  doi: "10.1000/target"',
                  '# Target\n- DOI: 10.1000/target\nhttps://arxiv.org/abs/2501.00001\n')
        row = self.matches([{"title": "Target", "doi": "10.1000/target", "arxiv_id": "2501.00001"}])[0]
        self.assertEqual(row["status"], "no_match")
        self.assertEqual(row["match_reason"], "no_exact_match")

    def test_primary_urls_and_yaml_scalar_styles_are_supported(self):
        path = self.note("scalar.md", "title: 'A researcher''s paper' # comment\n" +
                         "doi: https://dx.doi.org/10.1234/ABCD # identity\n" +
                         "paper_type: paper-stub\nofficial_url: https://openreview.net/pdf?id=CaseID")
        rows = self.matches([
            {"title": "A researcher's paper"},
            {"title": "Different", "doi": "https://doi.org/10.1234/abcd"},
            {"title": "Different", "openreview_id": "https://openreview.net/forum?id=CaseID"},
        ])
        self.assertEqual([row["existing_note_path"] for row in rows], [path, path, path])
        self.assertTrue(all(row["existing_note_type"] == "paper-stub" for row in rows))

    def test_no_fuzzy_matching_or_empty_title_collisions(self):
        self.note("nearby.md", 'title: "An exact paper title"')
        self.note("empty.md", 'title: ""\narxiv_id: null')
        rows = self.matches([{"title": "An exact paper title extended"}, {"title": ""}])
        self.assertEqual([row["status"] for row in rows], ["no_match", "no_match"])

    def test_recursive_lookup_preserves_note_asset_and_candidate_bytes(self):
        path = pathlib.Path(self.note("lane/cards/deep.md", 'type: paper-stub\ntitle: "Target"',
                                      '<!-- personal annotation -->\n![[image.png]]\n'))
        image = path.parent / "image.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\nuser-image")
        before = {item: item.read_bytes() for item in self.notes_root.rglob("*") if item.is_file()}
        candidates = [{"id": "C1", "title": "Target", "source_status": "metadata-only"}]
        original = copy.deepcopy(candidates)
        row = self.matches(candidates)[0]
        after = {item: item.read_bytes() for item in self.notes_root.rglob("*") if item.is_file()}
        self.assertEqual(row["existing_note_path"], str(path))
        self.assertEqual(after, before)
        self.assertEqual(candidates, original)
        self.assertNotIn("source_status", row)


if __name__ == "__main__":
    unittest.main()
