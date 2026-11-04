import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from gdo.memedize.method.neu import neu


class MemeAnnouncementTest(unittest.TestCase):
    def test_only_real_images_in_meme_folder_are_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '2026-11').mkdir()
            (root / '2026-11' / 'meme test.png').touch()
            (root / 'link.png').symlink_to(root / '2026-11' / 'meme test.png')
            with patch('gdo.base.Application.Application.domain', return_value='example.test'), \
                    patch('gdo.base.Application.Application.get_current_port', return_value=''), \
                    patch('gdo.base.Application.Application.web_root', return_value='/site'):
                url = neu.meme_url(root, '2026-11/meme test.png')
                self.assertTrue(url.endswith('/site/gdo/memedize/memes/2026-11/meme%20test.png'))
                for path in ('../secret.png', '/etc/passwd', 'link.png', 'missing.png', 'a.txt'):
                    self.assertIsNone(neu.meme_url(root, path), path)

    def test_announcement_requires_staff(self):
        self.assertEqual('staff', neu.gdo_user_permission(None))


class MemeDeliveryTest(unittest.IsolatedAsyncioTestCase):
    async def test_only_subscribed_channels_receive_the_release(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            method = neu()
        method.param_value = MagicMock(return_value='2026-11/a.png')
        method.reply = MagicMock(return_value='queued')
        channel = MagicMock()
        channel.send_text = AsyncMock()
        subscription = MagicMock()
        subscription.gdo_value.return_value = channel
        with patch.object(neu, 'meme_url', return_value='https://example.test/a.png'), \
                patch('gdo.memedize.method.neu.GDO_MemeSubscription') as table:
            table.table.return_value.select.return_value.exec.return_value.fetch_all.return_value = [subscription]
            self.assertEqual('queued', await method.gdo_execute())
        channel.send_text.assert_awaited_once_with('msg_memedize_announcement', ('https://example.test/a.png',))
        method.reply.assert_called_once_with('msg_memedize_announced', (1,))
