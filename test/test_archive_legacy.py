import tempfile
import unittest
from pathlib import Path

from gdo.memedize.scripts.archive_legacy import archive, remove_legacy_links


class ArchiveLegacyTest(unittest.TestCase):
    def test_archive_moves_files_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            month = root / '2026-11'
            month.mkdir()
            (root / 'old.png').write_bytes(b'old')
            (month / 'recent.png').write_bytes(b'recent')
            self.assertEqual(archive(root), 2)
            self.assertEqual(archive(root, True), 2)
            self.assertFalse((root / 'old.png').exists())
            self.assertFalse((month / 'recent.png').exists())
            self.assertEqual((root / '2023-09-23' / 'old.png').read_bytes(), b'old')
            self.assertEqual((root / '2023-09-23' / 'recent.png').read_bytes(), b'recent')
            self.assertEqual(archive(root, True), 0)

    def test_cleanup_removes_only_matching_archive_aliases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive_dir = root / '2023-09-23'
            archive_dir.mkdir()
            (archive_dir / 'old.png').write_bytes(b'old')
            (root / 'old.png').symlink_to('2023-09-23/old.png')
            (root / 'other.png').symlink_to('missing.png')
            self.assertEqual(remove_legacy_links(root), 1)
            self.assertEqual(remove_legacy_links(root, True), 1)
            self.assertFalse((root / 'old.png').is_symlink())
            self.assertTrue((root / 'other.png').is_symlink())
            self.assertEqual((archive_dir / 'old.png').read_bytes(), b'old')

    def test_duplicate_names_abort_before_any_move(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            month = root / '2026-11'
            month.mkdir()
            (root / 'same.png').write_bytes(b'a')
            (month / 'same.png').write_bytes(b'b')
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                archive(root, True)
            self.assertFalse((root / 'same.png').is_symlink())
            self.assertFalse((root / '2023-09-23').exists())
