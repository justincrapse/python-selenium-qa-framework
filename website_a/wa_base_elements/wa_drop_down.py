from website_a.wa_base_elements.wa_base_element import WaBaseElement
from selenium.webdriver.support.ui import Select


class WaDropDown(WaBaseElement):
    def __init__(self, page, name, locator, locator_type):
        super().__init__(page=page, name=name, locator=locator, locator_type=locator_type)

    def select_option_by_text(self, text):
        select_element = Select(self.locate_element(wait_for_present=False))
        select_element.select_by_visible_text(text)

    def select_option_by_index(self, index):
        self.scroll_past_element()
        select_element = Select(self.locate_element(wait_for_present=False))
        select_element.select_by_index(index)
