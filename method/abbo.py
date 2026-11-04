from gdo.base.Method import Method
from gdo.core.GDO_Permission import GDO_Permission
from gdo.core.GDT_Bool import GDT_Bool
from gdo.memedize.GDO_MemeSubscription import GDO_MemeSubscription


class abbo(Method):
    @classmethod
    def gdo_trigger(cls) -> str:
        return 'memedize.abbo'

    def gdo_in_private(self) -> bool:
        return False

    def gdo_user_permission(self) -> str:
        return GDO_Permission.VOICE

    def gdo_parameters(self):
        return [GDT_Bool('enabled').initial('1').positional()]

    def gdo_execute(self):
        channel_id = self._env_channel.get_id()
        subscription = GDO_MemeSubscription.table().get_by_vals({'ms_channel': channel_id})
        if self.param_value('enabled'):
            if not subscription:
                GDO_MemeSubscription.blank({
                    'ms_channel': channel_id,
                    'ms_creator': self._env_user.get_id(),
                }).insert()
            return self.reply('msg_memedize_subscribed')
        if subscription:
            subscription.delete()
        return self.reply('msg_memedize_unsubscribed')
