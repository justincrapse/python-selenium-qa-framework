from common.base_objects.base_page import BasePage


class BPBasePage(BasePage):
    """ Here you would code Base Page functionality unique to this website, extending the functionality of the common
    BasePage class. """
    def __init__(self, tc, page_url=None, page_id=None):
        super().__init__(tc=tc, page_url=page_url, page_id=page_id)


