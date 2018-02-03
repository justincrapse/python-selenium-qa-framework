from website_a.wa_base_elements.wa_base_element import WaBaseElement


class WaTextField(WaBaseElement):
    def __init__(self, page, name, locator, locator_type):
        super().__init__(page=page, name=name, locator=locator, locator_type=locator_type)
