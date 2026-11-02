import contextlib
import csv
import io
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import discover_candidates as discovery
from validate_candidate_table import validate_rows


class DiscoveryNoteReuseTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = pathlib.Path(temporary.name)
        self.notes = self.root / "notes"
        self.notes.mkdir()
        self.output = self.root / "output"
        self.arguments = ["--fixture", str(ROOT / "tests/fixtures/discovery_minimal.json"),
                          "--out-dir", str(self.output)]

    def run_discovery(self, arguments):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                return discovery.main(arguments)
            except SystemExit as error:
                return error.code

    def test_cli_reuses_versioned_arxiv_stub_without_writing_notes_or_changing_csv(self):
        note = self.notes / "existing.md"
        note.write_text('---\ntitle: "Earlier title"\npaper_id: OLD\ntype: paper-stub\n'
                        'arxiv_id: "2501.00001v2"\n---\nMy handwritten question.\n', encoding="utf-8")
        image = self.notes / "original.png"
        image.write_bytes(b"user image asset")
        before = {p.name: p.read_bytes() for p in self.notes.iterdir()}
        self.assertEqual(self.run_discovery([*self.arguments, "--notes-root", str(self.notes)]), 0)
        matches = [json.loads(line) for line in (self.output / "existing_note_matches.jsonl").read_text(encoding="utf-8").splitlines()]
        matched = next(row for row in matches if row["status"] == "matched")
        self.assertEqual(matched["existing_note_path"], str(note.resolve()))
        self.assertEqual(matched["existing_note_type"], "paper-stub")
        with (self.output / "candidate_table.csv").open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            self.assertEqual(reader.fieldnames, discovery.CANDIDATE_FIELDS)
            rows = list(reader)
        self.assertEqual(validate_rows(rows), [])
        self.assertIn(matched["candidate_id"], [row["id"] for row in rows])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.notes.iterdir()})

    def test_missing_notes_root_is_reported_before_discovery_outputs(self):
        self.assertEqual(self.run_discovery([*self.arguments, "--notes-root", str(self.root / "missing")]), 2)
        self.assertFalse(self.output.exists())

    def test_legacy_fixture_run_has_no_note_reuse_sidecar(self):
        self.assertEqual(self.run_discovery(self.arguments), 0)
        self.assertTrue((self.output / "candidate_table.csv").is_file())
        self.assertFalse((self.output / "existing_note_matches.jsonl").exists())

    def test_rerun_without_notes_root_does_not_retain_old_match_decisions(self):
        self.assertEqual(self.run_discovery([*self.arguments, "--notes-root", str(self.notes)]), 0)
        self.assertTrue((self.output / "existing_note_matches.jsonl").is_file())
        self.assertEqual(self.run_discovery(self.arguments), 0)
        self.assertFalse((self.output / "existing_note_matches.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
