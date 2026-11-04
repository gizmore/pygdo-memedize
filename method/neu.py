from pathlib import Path
from urllib.parse import quote

from gdo.base.Application import Application
from gdo.base.Method import Method
from gdo.core.Connector import Connector
from gdo.core.GDT_String import GDT_String
from gdo.memedize.GDO_MemeSubscription import GDO_MemeSubscription


class neu(Method):
    """Announce one local meme to opted-in channels, never arbitrary URLs."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'memedize.neu'

    def gdo_connectors(self) -> str:
        return Connector.text_connectors()

    def gdo_user_permission(self) -> str:
        return 'staff'

    def gdo_parameters(self):
        return [GDT_String('path').not_null().maxlen(240).positional()]

    @staticmethod
    def meme_url(root: Path, relative: str) -> str | None:
        part = Path(relative)
        if part.is_absolute() or not part.parts or any(p in ('.', '..') for p in part.parts):
            return None
        if part.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.gif', '.webp'}:
            return None
        current = root
        for component in part.parts:
            current = current / component
            if current.is_symlink():
                return None
        if not current.is_file():
            return None
        base = (Application.PROTOCOL + '://' + Application.domain()
                + Application.get_current_port(':') + Application.web_root().rstrip('/'))
        return base + '/gdo/memedize/memes/' + quote(part.as_posix(), safe='/')

    async def gdo_execute(self):
        root = Path(__file__).resolve().parent.parent / 'memes'
        url = self.meme_url(root, self.param_value('path'))
        if not url:
            return self.err('err_memedize_file')
        count = 0
        for subscription in GDO_MemeSubscription.table().select().exec().fetch_all():
            channel = subscription.gdo_value('ms_channel')
            if channel:
                await channel.send_text('msg_memedize_announcement', (url,))
                count += 1
        return self.reply('msg_memedize_announced', (count,))
