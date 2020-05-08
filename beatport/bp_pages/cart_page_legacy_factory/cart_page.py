from beatport.wa_base_elements.wa_button import WaButton
from beatport.wa_base_elements.wa_list import WaList
from beatport.wa_base_elements.wa_web_element import WaWebElement
from beatport.bp_base_objects.bp_base_page import BPBasePage
from beatport.bp_utilities import bp_conf as nc
from common.utilities import web_constants as wc
from beatport.bp_pages import bp_pages
from bp_test_context import BPTestContext


class CartPage(BPBasePage):
    def __new__(cls, *args, **kwargs):
        tc = kwargs['tc'] if kwargs else args[0]
        from .cart_page_factory import FACTORY_MAP
        return super().__new__(cls.return_subclass(cls, tc=tc, factory=FACTORY_MAP))

    def __init__(self, tc, page_url='/Product/Cart', page_id='Cart'):
        super().__init__(tc=tc, page_url=page_url, page_id=page_id)
        self.tc = tc  # type: BPTestContext
        self.btn_checkout = WaButton(
            page=self,
            name='btn_checkout',
            locator='some_xpath_locator',
            locator_type=wc.BY_XPATH)
        self.li_product_titles = WaList(
            page=self,
            name='li_product_titles',
            locator='some_xpath_locator',
            locator_type=wc.BY_XPATH)
        self.el_empty_cart_text = WaWebElement(
            page=self,
            name='el_empty_cart_text',
            locator='some_xpath_locator',
            locator_type=wc.BY_XPATH)

        self.btn_remove_first = WaButton(
            page=self,
            name='btn_remove_first',
            locator='some_xpath_locator',
            locator_type=wc.BY_XPATH)
        # Remove Item popup:
        self.btn_yes = WaButton(
            page=self,
            name='btn_yes',
            locator='some_xpath_locator',
            locator_type=wc.BY_XPATH)

        # Summary box on right:
        self.el_subtotal = WaWebElement(
            page=self,
            name='el_subtotal',
            locator='some_xpath_locator',
            locator_type=wc.BY_XPATH)

    def navigate(self, nav_path=nc.CART_PAGE_VIA_NAV_BAR):
        if nav_path == nc.CART_PAGE_VIA_NAV_BAR:
            nav_bar = bp_pages.NavBar(self.tc)
            if not nav_bar.is_on_page():
                nav_bar.navigate()
            nav_bar.el_cart.js_click()
        self.on_page()
        return self

    def clear_cart(self):
        cart_list = self.li_product_titles.get_list_text()
        del_first = self.btn_remove_first
        for item in range(len(cart_list)):
            del_first.js_click().sleep(.5)
            self.btn_yes.click().sleep(.5)
            self.btn_yes.wait_for_element_invisible()
        self.btn_remove_first.wait_for_element_invisible(wait_time=4)






