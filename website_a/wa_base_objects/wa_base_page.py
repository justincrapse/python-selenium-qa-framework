from common.base_objects.base_page import BasePage
from wa_test_context import WaTestContext


class WaBasePage(BasePage):
    def __init__(self, tc, page_url=None, page_id=None, by_xpath=False):
        super().__init__(tc=tc, page_url=page_url, page_id=page_id, by_xpath=by_xpath)

    @staticmethod
    def return_subclass(self, tc, factory):
        """ returns the appropriate subclass from the subclass factory dictionary """
        try:
            subclass = factory[tc.class_suffix]
        except KeyError:
            return self
        return subclass
