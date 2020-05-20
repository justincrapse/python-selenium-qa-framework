from beatport.bp_base_objects.bp_base_page import BPBasePage
from bp_utilities import bp_conf, bp_page_id
from bp_base_objects.bp_element import BPElement


class HomePage(BPBasePage):
    def __init__(self, tc, page_url=bp_conf.BASE_URL, page_id=bp_page_id.HOME_PAGE):
        super().__init__(tc=tc, page_url=page_url, page_id=page_id)

        self.search_field = BPElement(page=self, locator='//input[@placeholder="Search..."]')

    def navigate(self, nav_path=None):
        if not nav_path and not self.on_page():
            self._navigate()
            return self
        return self
