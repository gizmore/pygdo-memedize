import json

from gdo.base.Application import Application
from gdo.base.Method import Method
from gdo.core.Connector import Connector
from gdo.core.GDT_RestOfText import GDT_RestOfText
from gdo.mira.util import send_to_mira


class create(Method):
    """Queue a meme request for Mira; credit charging is not implemented."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'memedize.create'

    def gdo_connectors(self) -> str:
        return Connector.text_connectors()

    def gdo_user_permission(self) -> str:
        # Temporary until fair, safe credit charging and rate limits exist.
        return 'staff'

    def gdo_parameters(self):
        return [GDT_RestOfText('idea').not_null()]

    def gdo_execute(self):
        if not Application.IS_DOG:
            return self.err('err_memedize_dog_only')
        idea = self.param_value('idea')
        if not isinstance(idea, str) or not idea.strip() or len(idea) > 1000:
            return self.err('err_memedize_idea')
        request = {
            'channel_id': self._env_channel.get_id() if self._env_channel else None,
            'user': self._env_user.get_name_sid(),
            'idea': idea,
        }
        send_to_mira('$meme ' + json.dumps(request, ensure_ascii=True), interrupt=False)
        return self.reply('msg_memedize_queued')
