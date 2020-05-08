from beatport.bp_base_objects.bp_base_page import BPBasePage
import bp_utilities as bp


class HomePage(BPBasePage):
    def __init__(self, tc, page_url=bp.bp_conf.BASE_URL, page_id=bp.bp_page_id.HOME_PAGE):
        super().__init__(tc=tc, page_url=page_url, page_id=page_id)

    def navigate(self, nav_path=None):
        if not nav_path and not self.on_page():
            self._navigate()
            return self
        return self
