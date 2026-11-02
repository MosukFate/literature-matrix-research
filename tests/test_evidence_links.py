import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_evidence_links.py"
TEST_TEMP = Path(os.environ.get("MATRIX_TEST_TMP", tempfile.gettempdir()))


class EvidenceLinksTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), "Missing delivery link checker; old skill cannot detect copied render pointers")
        spec = importlib.util.spec_from_file_location("validate_evidence_links", SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        TEST_TEMP.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=TEST_TEMP)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def write(self, name, content=""):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def scan(self):
        return self.module.scan_links(self.root)

    def test_existing_relative_links_images_and_external_sources_pass(self):
        self.write("figures/my image.png")
        self.write("paper.pdf")
        self.write("note.md", "[PDF](paper.pdf#page=6)\n![figure](figures/my%20image.png)\n[full](<figures/my image.png>)\n[official](https://example.org/paper.pdf#page=6)\n[section](#method)")
        self.assertEqual(self.scan()["issues"], [])

    def test_missing_image_and_ledger_render_are_reported_with_line_numbers(self):
        self.write("note.md", "![Figure 1](figures/missing.png)\n```yaml\nsource_page_render: evidence/missing-page.png\nasset_path: unknown\n```\n")
        issues = self.scan()["issues"]
        self.assertEqual([(i["line"], i["issue"]) for i in issues], [(1, "missing_local_target"), (3, "missing_local_target")])

    def test_existing_target_outside_bundle_is_not_portable(self):
        self.write("outside.png")
        self.write("bundle/note.md", "[outside](../outside.png)")
        issues = self.module.scan_links(self.root / "bundle")["issues"]
        self.assertEqual([i["issue"] for i in issues], ["target_outside_package"])

    def test_copy_rechecks_previously_valid_bundle_relative_pointer(self):
        self.write("evidence/page.png")
        original = self.write("original/note.md", "source_page_render: ../evidence/page.png\n")
        self.assertEqual(self.scan()["issues"], [])
        destination = self.root / "export"
        destination.mkdir()
        shutil.copy2(original, destination / "note.md")
        issues = self.module.scan_links(destination)["issues"]
        self.assertEqual([i["issue"] for i in issues], ["target_outside_package"])

    def test_unknown_and_external_ledger_fields_do_not_become_local_files(self):
        self.write("note.md", "asset_path: 'unknown'\nsource_page_render: not applicable (HTML-only)\nsource_page_render: https://example.org/paper.pdf#page=3\n")
        self.assertEqual(self.scan()["issues"], [])

    def test_placeholder_prefix_is_still_a_real_filename(self):
        self.write("note.md", "asset_path: unknown-figure.png\n")
        self.assertEqual([i["issue"] for i in self.scan()["issues"]], ["missing_local_target"])

    def test_unclosed_or_malformed_markdown_is_not_a_parser_error(self):
        self.write("note.md", "[unfinished](\nordinary prose\n")
        self.assertEqual(self.scan()["issues"], [])


if __name__ == "__main__":
    unittest.main()
