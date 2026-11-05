import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gdo.base.Render import Mode
from gdo.memedize.method.overview import overview


class GalleryTest(unittest.TestCase):
    def test_large_day_has_separate_pages_and_keeps_day_in_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'method').mkdir()
            day = root / 'memes' / '2023-09-23'
            day.mkdir(parents=True)
            for i in range(26):
                (day / f'meme-{i:02}.png').touch()
            with patch('gdo.base.Application.Application.get_mode', return_value=Mode.render_html), \
                    patch('gdo.base.Application.Application.web_root', return_value='/site/'), \
                    patch('gdo.base.Application.Application.get_lang_iso', return_value='en'), \
                    patch('gdo.memedize.method.overview.t', side_effect=lambda key, *args: key), \
                    patch('gdo.memedize.method.overview.__file__', str(root / 'method' / 'overview.py')), \
                    patch.object(overview, 'param_val', return_value='2023-09-23'):
                with patch.object(overview, 'param_value', return_value=1):
                    first = overview().gdo_execute().get_fields()[1].render_html()
                with patch.object(overview, 'param_value', return_value=2):
                    second = overview().gdo_execute().get_fields()[1].render_html()
                self.assertEqual(first.count('<img '), 24)
                self.assertEqual(second.count('<img '), 2)
                self.assertIn('meme-00.png', first)
                self.assertNotIn('meme-24.png', first)
                self.assertIn('meme-24.png', second)
                self.assertIn('day.2023-09-23.page.2', first)
                self.assertIn('day.2023-09-23.page.1', second)

    def test_text_modes_return_the_absolute_overview_link(self):
        for mode in (Mode.render_cli, Mode.render_irc, Mode.render_telegram):
            with self.subTest(mode=mode), patch('gdo.base.Application.Application.get_mode', return_value=mode), \
                    patch('gdo.memedize.method.overview.url', return_value='https://example.test/memedize.overview.html'):
                self.assertEqual('https://example.test/memedize.overview.html', overview().gdo_execute().render_txt())

    def test_gallery_pages_by_day_and_excludes_nonimages_and_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'method').mkdir()
            memes = root / 'memes'
            old = memes / '2023-09-23'
            new = memes / '2026-11-05'
            old.mkdir(parents=True)
            new.mkdir()
            (old / 'old.png').touch()
            (new / 'A & "B".PNG').touch()
            (new / 'sessions.zip').touch()
            (new / 'linked.png').symlink_to(old / 'old.png')
            (memes / '2026-11-06').symlink_to(new, target_is_directory=True)
            with patch('gdo.base.Application.Application.get_mode', return_value=Mode.render_html), \
                    patch('gdo.base.Application.Application.web_root', return_value='/site/'), \
                    patch('gdo.base.Application.Application.get_lang_iso', return_value='en'), \
                    patch('gdo.memedize.method.overview.t', side_effect=lambda key: key), \
                    patch('gdo.memedize.method.overview.__file__', str(root / 'method' / 'overview.py')):
                for requested, shown, hidden in [(None, 'A%20%26%20%22B%22.PNG', 'old.png'),
                                                  ('2023-09-23', 'old.png', 'A%20%26%20%22B%22.PNG')]:
                    with self.subTest(day=requested), patch.object(overview, 'param_val', return_value=requested):
                        panel, gallery = overview().gdo_execute().get_fields()
                        html = gallery.render_html()
                        self.assertEqual('memedize_info', panel._text_key)
                        self.assertIn(shown, html)
                        self.assertNotIn(hidden, html)
                        self.assertIn('/site/gdo/memedize/memes/', html)
                        self.assertIn('memedize.overview.day.', html)
                        self.assertLess(html.index('2026-11-05'), html.rindex('2023-09-23'))
                        self.assertNotIn('linked.png', html)
                        self.assertNotIn('sessions.zip', html)
                        self.assertNotIn('2026-11-06', html)
