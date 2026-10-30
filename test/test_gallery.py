import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gdo.base.Render import Mode
from gdo.memedize.method.overview import overview


class GalleryTest(unittest.TestCase):
    def test_text_modes_return_the_absolute_overview_link(self):
        for mode in (Mode.render_cli, Mode.render_irc, Mode.render_telegram):
            with self.subTest(mode=mode), patch('gdo.base.Application.Application.get_mode', return_value=mode), \
                    patch('gdo.memedize.method.overview.url', return_value='https://example.test/memedize.overview.html'):
                result = overview().gdo_execute()
                self.assertEqual('https://example.test/memedize.overview.html', result.render_txt())

    def test_html_lists_only_safe_images_with_escaped_clickable_urls(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'method').mkdir()
            memes = root / 'memes'
            memes.mkdir()
            (memes / 'A & "B".PNG').touch()
            (memes / 'z.jpg').touch()
            (memes / 'sessions.zip').touch()
            (memes / 'secret.svg').touch()
            (memes / 'linked.png').symlink_to(memes / 'z.jpg')
            with patch('gdo.base.Application.Application.get_mode', return_value=Mode.render_html), \
                    patch('gdo.base.Application.Application.web_root', return_value='/site/'), \
                    patch('gdo.memedize.method.overview.__file__', str(root / 'method' / 'overview.py')):
                result = overview().gdo_execute()
            panel, gallery = result.get_fields()
            self.assertEqual('memedize_info', panel._text_key)
            html = gallery.render_html()
            self.assertIn('href="/site/gdo/memedize/memes/A%20%26%20%22B%22.PNG"', html)
            self.assertIn('alt="A &amp; &quot;B&quot;"', html)
            self.assertIn('href="/site/gdo/memedize/memes/z.jpg"', html)
            self.assertNotIn('sessions.zip', html)
            self.assertNotIn('secret.svg', html)
            self.assertNotIn('linked.png', html)
