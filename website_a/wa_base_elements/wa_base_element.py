from common.base_elements.base_element import BaseElement


class WaBaseElement(BaseElement):
    def __init__(self, page, name, locator, locator_type):
        super().__init__(page=page, name=name, locator=locator, locator_type=locator_type)