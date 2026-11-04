import unittest
from unittest.mock import MagicMock, patch

from gdo.base.Application import Application
from gdo.memedize.method.abbo import abbo


class MemeSubscriptionTest(unittest.TestCase):
    def method(self, enabled):
        with patch.object(Application, 'get_mode', return_value=None):
            method = abbo()
        method._env_channel = MagicMock()
        method._env_channel.get_id.return_value = '42'
        method._env_user = MagicMock()
        method._env_user.get_id.return_value = '7'
        method.param_value = MagicMock(return_value=enabled)
        method.reply = MagicMock(side_effect=lambda key: key)
        return method

    @patch('gdo.memedize.method.abbo.GDO_MemeSubscription')
    def test_opt_in_is_scoped_to_channel_and_idempotent(self, table):
        method = self.method(True)
        table.table.return_value.get_by_vals.return_value = None
        self.assertEqual('msg_memedize_subscribed', method.gdo_execute())
        table.table.return_value.get_by_vals.assert_called_once_with({'ms_channel': '42'})
        table.blank.assert_called_once_with({'ms_channel': '42', 'ms_creator': '7'})
        table.blank.return_value.insert.assert_called_once()
        table.reset_mock()
        table.table.return_value.get_by_vals.return_value = MagicMock()
        method.gdo_execute()
        table.blank.assert_not_called()

    @patch('gdo.memedize.method.abbo.GDO_MemeSubscription')
    def test_opt_out_deletes_only_selected_subscription(self, table):
        method = self.method(False)
        row = table.table.return_value.get_by_vals.return_value
        self.assertEqual('msg_memedize_unsubscribed', method.gdo_execute())
        table.table.return_value.get_by_vals.assert_called_once_with({'ms_channel': '42'})
        row.delete.assert_called_once()

    def test_restricted_to_channel(self):
        self.assertFalse(self.method(True).gdo_in_private())
