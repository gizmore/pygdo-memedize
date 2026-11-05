from html import escape
from datetime import date
from pathlib import Path
from urllib.parse import quote

from gdo.base.Application import Application
from gdo.base.Method import Method
from gdo.base.util.href import href, url
from gdo.base.Trans import t
from gdo.core.GDT_Container import GDT_Container
from gdo.core.GDT_String import GDT_String
from gdo.message.GDT_HTML import GDT_HTML
from gdo.table.GDT_PageNum import GDT_PageNum
from gdo.ui.GDT_Panel import GDT_Panel


class overview(Method):
    PAGE_SIZE = 24

    def gdo_parameters(self):
        return [GDT_String('day').ascii().maxlen(10).tooltip('tt_memedize_day'),
                GDT_PageNum('page').initial('1').tooltip('tt_memedize_page')]

    def gdo_execute(self):
        if not self._env_mode.is_html():
            return GDT_HTML().text(url('memedize', 'overview'))

        folder = Path(__file__).resolve().parent.parent / 'memes'
        days = []
        if folder.is_dir():
            for entry in folder.iterdir():
                if entry.is_symlink() or not entry.is_dir():
                    continue
                try:
                    if date.fromisoformat(entry.name).isoformat() == entry.name:
                        days.append(entry.name)
                except ValueError:
                    continue
        days.sort(reverse=True)
        requested = self.param_val('day', throw=False)
        selected = requested if requested in days else (days[0] if days else None)
        base = Application.web_root().rstrip('/')
        nav = [f'<a href="{escape(base + "/gdo/memedize/memes/", quote=True)}">'
               f'{escape(t("memedize_browse_directory"))}</a>']
        if selected:
            index = days.index(selected)
            if index:
                nav.append(self.day_link(base, days[index - 1], t('memedize_newer')))
            nav.append(escape(selected))
            if index + 1 < len(days):
                nav.append(self.day_link(base, days[index + 1], t('memedize_older')))
        day_choices = [f'<strong aria-current="date">{escape(day)}</strong>' if day == selected
                       else self.day_link(base, day, day) for day in days]
        files = []
        if selected:
            for image in sorted((folder / selected).iterdir(), key=lambda p: (p.name.casefold(), p.name)):
                if image.is_symlink() or not image.is_file() or image.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.gif', '.webp'}:
                    continue
                files.append(image)
        page_count = max(1, (len(files) + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        page = min(self.param_value('page', throw=False) or 1, page_count)
        pages = []
        if selected and page_count > 1:
            if page > 1:
                pages.append(self.day_link(base, selected, t('memedize_previous_page'), page - 1))
            pages.append(escape(t('memedize_page', (page, page_count))))
            if page < page_count:
                pages.append(self.day_link(base, selected, t('memedize_next_page'), page + 1))
        images = []
        if selected:
            for image in files[(page - 1) * self.PAGE_SIZE:page * self.PAGE_SIZE]:
                relative = image.relative_to(folder)
                link = escape(base + '/gdo/memedize/memes/' + quote(relative.as_posix(), safe='/'), quote=True)
                name = escape(image.stem, quote=True)
                images.append(f'<a href="{link}"><img src="{link}" alt="{name}" loading="lazy"></a>')
        panel = GDT_Panel().title('module_memedize').text('memedize_info')
        pages_html = '<nav class="memedize-pages">' + ' | '.join(pages) + '</nav>' if pages else ''
        choices_html = '<nav class="memedize-day-choices">' + ' | '.join(day_choices) + '</nav>' if days else ''
        gallery = GDT_HTML().html('<nav class="memedize-days">' + ' | '.join(nav) + '</nav>' + choices_html + pages_html +
                                  '<div class="memedize-gallery">' + ''.join(images) + '</div>' + pages_html)
        return GDT_Container().vertical().add_fields(panel, gallery)

    @staticmethod
    def day_link(base, day, label, page=None):
        args = 'day=' + day + (f'&page={page}' if page is not None else '')
        target = base + href('memedize', 'overview', append=args)
        return f'<a href="{escape(target, quote=True)}">{escape(label)}</a>'
