from website_a.wa_base_objects.wa_base_page import WaBasePage
from website_a.wa_pages import wa_pages


class HomePage(WaBasePage):
    def __new__(cls, *args, **kwargs):
        tc = kwargs['tc'] if kwargs else args[0]
        from .home_page_factory import FACTORY_MAP
        return super().__new__(cls.return_subclass(cls, tc=tc, factory=FACTORY_MAP))

    def __init__(self, tc, page_url='', page_id='RedLineShoes'):
        super().__init__(tc=tc, page_url=page_url, page_id=page_id)

    def navigate(self, nav_path=None):
        if not nav_path:
            self._navigate()
            return self

    def is_logged_in(self):
        nav_bar = wa_pages.NavBar(self.tc)
        return nav_bar.el_user_icon.is_visible()
