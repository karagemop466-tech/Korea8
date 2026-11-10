"""Regression tests for the public Pages artifact boundary."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('stage_pages', ROOT / 'scripts/stage_overflow_pages.py')
stage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage)

class PublicationTests(unittest.TestCase):
    def test_canonical_pages_staged_without_repository_internals(self):
        files = stage.public_files()
        for name in ('index.html', 'providers.html', 'decision-analysis.html', 'flagged-for-review.html', 'style.css'):
            self.assertIn(Path(name), files)
        self.assertIn(Path('audit/2026-11-10-b5ed3a43/REPORT.md'), files)
        self.assertIn(Path('audit/2026-11-10-5651e041/REPORT.md'), files)
        self.assertIn(Path('audit/2026-11-10-6f4c9f79/REPORT.md'), files)
        for path in files:
            self.assertNotIn(path.parts[0], {'.git', '.github', 'src', 'vendor', 'scripts', 'tests', 'data'})
        self.assertNotIn(Path('PROJECT_PROMPT.md'), files)
        self.assertNotIn(Path('COORDINATION.md'), files)

    def test_missing_target_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text('<a href="missing.html">Missing</a>')
            with self.assertRaises(ValueError):
                stage.public_files(root)

    def test_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text('<a href="../secret.md">Secret</a>')
            with self.assertRaises(ValueError):
                stage.public_files(root)

    def test_hidden_file_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text('<a href=".credentials.txt">Secret</a>')
            with self.assertRaises(ValueError):
                stage.public_files(root)

    def test_external_links_not_downloaded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text('<a href="https://example.org/x">External</a>')
            self.assertEqual(stage.public_files(root), {Path('index.html')})
