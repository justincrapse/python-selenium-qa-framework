from base_objects.base_element import BaseElement
import common.utilities.element_selectors as es


class BPWebElement(BaseElement):
    def __init__(self, page, locator, locator_type=es.BY_XPATH):
        super().__init__(page=page, locator=locator, locator_type=locator_type)
