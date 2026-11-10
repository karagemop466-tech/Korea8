"""Regression tests for the publication-boundary guard."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('boundary', ROOT / 'scripts/check_publication_boundary.py')
boundary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(boundary)


class BoundaryClassificationTests(unittest.TestCase):
    def test_repository_internals_classified_internal(self):
        for relative in ('COORDINATION.md', 'PROJECT_PROMPT.md', 'AGENTS.md', 'pyproject.toml',
                         'vendor/README.md', 'scripts/build_overflow_site.py', 'src/korea8/features.py',
                         '.github/workflows/overflow-pages.yml',
                         'overflow-integration/data/providers.json', 'archive/superseded/x.py',
                         'audit/2026-11-10-independent-SECRET/REPORT.md'):
            self.assertTrue(boundary.is_internal(relative), relative)

    def test_hidden_directory_not_mangled_by_prefix_stripping(self):
        # Regression: str.lstrip('./') strips leading dots and would turn
        # '.github/...' into 'github/...', silently reclassifying hidden paths.
        self.assertTrue(boundary.is_internal('.github/workflows/overflow-pages.yml'))
        self.assertTrue(boundary.is_internal('./COORDINATION.md'))
        self.assertTrue(boundary.is_internal('/COORDINATION.md'))

    def test_linked_evidence_documents_are_publishable(self):
        # These are linked from the dashboard on purpose; the exception is by exact path.
        for relative in ('audit/2026-11-10-87e121e1/REPORT.md',
                         'audit/2026-11-10-660ab2dd.md',
                         'docs/index.html'):
            self.assertFalse(boundary.is_internal(relative), relative)

    def test_dashboard_pages_not_classified_internal(self):
        for relative in ('index.html', 'providers.html', 'decision-analysis.html', 'style.css',
                         'requirements.html', 'flagged-for-review.html', 'verification.html'):
            self.assertFalse(boundary.is_internal(relative), relative)


class StagedBoundaryTests(unittest.TestCase):
    def test_clean_staging_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text('<html></html>')
            (root / 'style.css').write_text('body{}')
            (root / '.nojekyll').write_text('')
            ok, offenders = boundary.check_staged(root)
            self.assertTrue(ok, offenders)
            self.assertEqual(offenders, [])

    def test_board_inside_staging_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text('<html></html>')
            (root / 'COORDINATION.md').write_text('# board')
            ok, offenders = boundary.check_staged(root)
            self.assertFalse(ok)
            self.assertEqual(offenders, ['COORDINATION.md'])

    def test_nested_internal_directory_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'vendor').mkdir()
            (root / 'vendor' / 'README.md').write_text('# vendored')
            ok, offenders = boundary.check_staged(root)
            self.assertFalse(ok)
            self.assertEqual(offenders, ['vendor/README.md'])

    def test_missing_staging_is_not_silently_ok(self):
        with tempfile.TemporaryDirectory() as tmp:
            ok, offenders = boundary.check_staged(Path(tmp) / 'absent')
            self.assertFalse(ok)
            self.assertTrue(offenders)


if __name__ == '__main__':
    unittest.main()
