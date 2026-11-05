import os
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

from gdo.memedize.scripts.move_today import move_today


class MoveTodayTest(unittest.TestCase):
    def test_moves_only_today_images_and_preserves_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = root / '2023-09-23'
            old.mkdir()
            today = date(2026, 11, 5)
            newest = old / 'today.png'
            newest.write_bytes(b'today')
            earlier = old / 'yesterday.png'
            earlier.write_bytes(b'earlier')
            archive = old / 'sessions.zip'
            archive.write_bytes(b'zip')
            today_ts = datetime(2026, 11, 5, 12).timestamp()
            old_ts = datetime(2026, 11, 4, 12).timestamp()
            os.utime(newest, (today_ts, today_ts))
            os.utime(earlier, (old_ts, old_ts))
            os.utime(archive, (today_ts, today_ts))
            self.assertEqual(move_today(root, today), 1)
            self.assertEqual(move_today(root, today, True), 1)
            self.assertEqual((root / '2026-11-05' / 'today.png').read_bytes(), b'today')
            self.assertFalse(newest.exists())
            self.assertTrue(earlier.exists())
            self.assertTrue(archive.exists())
            self.assertEqual(move_today(root, today, True), 0)
