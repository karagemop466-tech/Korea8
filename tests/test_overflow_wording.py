"""Wording rule: every tracked text file is written in neutral repair-scope language."""
import importlib.util
import io
import contextlib
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('wording_guard', ROOT / 'scripts/wording_guard.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

SAMPLE = 'purple elephant parade'  # synthetic wording used only to exercise the matcher


class WordingTests(unittest.TestCase):
    def test_tracked_files_follow_the_wording_rule(self):
        hits = guard.scan_repo(ROOT)
        self.assertEqual(hits, [], '\n' + guard.format_hits(hits))

    def test_entries_are_digests(self):
        self.assertTrue(guard.ENTRIES)
        for item in guard.ENTRIES:
            self.assertRegex(item, r'^[1-9]\d*:[0-9a-f]{8}:[0-9a-f]{16}$')
        self.assertEqual(len(set(guard.ENTRIES)), len(guard.ENTRIES))

    def test_matcher_ignores_case_punctuation_and_line_breaks(self):
        table = guard.build_table([guard.entry(SAMPLE)])
        text = b'first line\nA Purple-ELEPHANT\n   parade, at noon.\n'
        self.assertEqual([line for line, _ in guard.scan_bytes(text, table)], [2])
        self.assertEqual(guard.scan_bytes(b'purple elephants parade', table), [])
        self.assertEqual(guard.scan_bytes(b'', table), [])

    def test_matcher_reports_each_line_once(self):
        table = guard.build_table([guard.entry(SAMPLE), guard.entry('elephant parade')])
        hits = guard.scan_bytes(b'purple elephant parade\nok\nELEPHANT PARADE\n', table)
        self.assertEqual(sorted({line for line, _ in hits}), [1, 3])
        self.assertEqual(len(hits), 3)

    def test_file_scan_reports_path_and_line_and_skips_binary(self):
        table = guard.build_table([guard.entry(SAMPLE)])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'note.md').write_text('clean line\n' + SAMPLE + '\n')
            (root / 'blob.bin').write_bytes(b'\0\1\2' + SAMPLE.encode())
            paths = [root / 'note.md', root / 'blob.bin', root / 'absent.txt']
            hits = guard.scan_paths(paths, root, table)
            self.assertEqual([(name, line) for name, line, _ in hits], [('note.md', 2)])
            self.assertIn('note.md:2:', guard.format_hits(hits))
            self.assertEqual(guard.scan_paths(paths, root), [])

    def test_command_line_exit_codes(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(guard.main(['--digest', SAMPLE]), 0)
        self.assertIn(guard.entry(SAMPLE), out.getvalue())
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(guard.main(['--digest']), 2)
            self.assertEqual(guard.main(['--unknown']), 2)
            self.assertEqual(guard.main([str(ROOT / 'scripts/wording_guard.py')]), 0)


if __name__ == '__main__':
    unittest.main()
