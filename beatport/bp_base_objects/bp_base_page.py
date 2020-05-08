from common.base_objects.base_page import BasePage
import bp_utilities as bp


class BPBasePage(BasePage):
    def __init__(self, tc, page_url=None, page_id=None, by_xpath=False):
        super().__init__(tc=tc, page_url=page_url, page_id=page_id, by_xpath=by_xpath)


