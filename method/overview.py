from html import escape
from pathlib import Path
from urllib.parse import quote

from gdo.base.Application import Application
from gdo.base.Method import Method
from gdo.base.util.href import url
from gdo.core.GDT_Container import GDT_Container
from gdo.message.GDT_HTML import GDT_HTML
from gdo.ui.GDT_Panel import GDT_Panel


class overview(Method):
    def gdo_execute(self):
        if not self._env_mode.is_html():
            return GDT_HTML().text(url('memedize', 'overview'))

        folder = Path(__file__).resolve().parent.parent / 'memes'
        images = []
        if folder.is_dir():
            for image in sorted(folder.iterdir(), key=lambda p: (p.name.casefold(), p.name)):
                if image.is_symlink() or not image.is_file() or image.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.gif', '.webp'}:
                    continue
                href = Application.web_root().rstrip('/') + '/gdo/memedize/memes/' + quote(image.name, safe='')
                link = escape(href, quote=True)
                name = escape(image.stem, quote=True)
                images.append(f'<a href="{link}"><img src="{link}" alt="{name}" loading="lazy"></a>')
        panel = GDT_Panel().title('module_memedize').text('memedize_info')
        gallery = GDT_HTML().html('<div class="memedize-gallery">' + ''.join(images) + '</div>')
        return GDT_Container().vertical().add_fields(panel, gallery)
