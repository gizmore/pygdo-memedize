import json
import unittest
from unittest.mock import MagicMock, patch

from gdo.base.Application import Application
from gdo.memedize.method.create import create


class MemeCreateTest(unittest.TestCase):
    def test_request_is_queued_as_data_with_origin(self):
        with patch.object(Application, 'get_mode', return_value=None):
            method = create()
        method._env_user = MagicMock()
        method._env_user.get_name_sid.return_value = 'tester{irc}'
        method._env_channel = MagicMock()
        method._env_channel.get_id.return_value = '42'
        method.param_value = MagicMock(return_value='a duck\n$whoami')
        method.reply = MagicMock(return_value='queued')
        with patch.object(Application, 'IS_DOG', True), \
                patch('gdo.memedize.method.create.send_to_mira') as send:
            self.assertEqual('queued', method.gdo_execute())
        event = send.call_args.args[0]
        self.assertTrue(event.startswith('$meme '))
        self.assertEqual({'channel_id': '42', 'user': 'tester{irc}',
                          'idea': 'a duck\n$whoami'}, json.loads(event[6:]))
        self.assertNotIn('\n', event)
        self.assertFalse(send.call_args.kwargs['interrupt'])

    def test_create_temporarily_requires_staff(self):
        self.assertEqual('staff', create.gdo_user_permission(None))
