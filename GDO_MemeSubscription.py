from gdo.base.GDO import GDO
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Channel import GDT_Channel
from gdo.core.GDT_Creator import GDT_Creator
from gdo.core.GDT_Unique import GDT_Unique
from gdo.date.GDT_Created import GDT_Created


class GDO_MemeSubscription(GDO):
    """An explicitly subscribed channel; no row means no announcements."""

    def gdo_columns(self):
        return [
            GDT_AutoInc('ms_id'),
            GDT_Channel('ms_channel').not_null().cascade_delete(),
            GDT_Creator('ms_creator').not_null(),
            GDT_Created('ms_created'),
            GDT_Unique('unique_meme_channel').unique_columns('ms_channel'),
        ]
