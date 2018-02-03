import random

from website_a.wa_base_elements.wa_base_element import WaBaseElement
from website_a.wa_base_elements.wa_web_element import WaWebElement
from common.utilities import web_constants as wc


class WaList(WaBaseElement):
    """ All list elements will be set up with an xpath that matches all desired elements. All list elements will be
    wrapped up in parentheses with a [index] string appended at the end with an option for further appendages if needing
    to match deeper into the list after that. """
    def __init__(self, page, name, locator, locator_type):
        super().__init__(page=page, name=name, locator=locator, locator_type=locator_type)
        self.page = page
        self.driver = page.driver
        self.locator = locator

    def get_element_by_index(self, index, appendage=''):
        locator = f'(' + self.locator + f')[{index + 1}]{appendage}'
        web_element = WaWebElement(
            page=self.page,
            name='web_element',
            locator=locator,
            locator_type=wc.BY_XPATH)
        return web_element

    def get_random_list_index(self, cuttoff=0):
        self.wait_for_spinner()
        try:
            list_len = self.locate_elements()
            rand_int = random.randint(0, len(list_len) - 1 - cuttoff)
        except ValueError:
            try:
                self.implicit_wait(time=2)
                list_len = self.locate_elements()
                rand_int = random.randint(0, len(list_len) - 1 - cuttoff)
            except ValueError:
                raise ValueError(f'Could not locate list by xpath: {self.locator}')
        return rand_int

    def get_random_list_element(self, cuttoff=0, appendage=''):
        random_index = self.get_random_list_index(cuttoff=cuttoff)
        random_element = self.get_element_by_index(index=random_index, appendage=appendage)
        return random_element

    def is_text_in_list(self, string):
        list_elements = self.locate_elements()
        for element in list_elements:
            text = element.text
            if text == string:
                return True
        return False

    def is_substring_in_list(self, string, case_sensitive=False):
        self.wait_for_spinner()
        list_elements = self.locate_elements()
        for element in list_elements:
            text = element.text
            if case_sensitive:
                if string in text:
                    return True
            else:
                if string.lower() in text.lower():
                    return True
        return False

    def get_list_text(self):
        """ returns a list of text contained by elements in the list. """
        return [str(el.text) for el in self.locate_elements()]

    def click_list_item_by_text(self):
        pass


