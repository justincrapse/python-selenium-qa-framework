from .cart_page import CartPage
from beatport.bp_utilities import bp_conf as nc
from beatport.bp_pages import bp_pages


class CartPageSmall(CartPage):
    def __init__(self, tc):
        super().__init__(tc=tc)

    def navigate(self, nav_path=nc.CART_PAGE_VIA_NAV_BAR):
        if nav_path == nc.CART_PAGE_VIA_NAV_BAR:
            nav_bar = bp_pages.NavBar(self.tc)
            if not nav_bar.el_cart.is_clickable:
                bp_pages.HomePage(self.tc).navigate()
            # clear gritter notification if present
            nav_bar.el_cart.js_click()
        self.on_page()
        return self


class CartPageUsLargeStage(CartPage):
    def __init__(self, tc, page_url='/Product/Cart', page_id='Cart'):
        super().__init__(tc=tc, page_url=page_url, page_id=page_id)


class CartPageAuLarge(CartPage):
    def __init__(self, tc):
        super().__init__(tc=tc)


FACTORY_MAP = {
    'US_LARGE_STAGE': CartPageUsLargeStage,
    'SMALL': CartPageSmall,
    'AU_LARGE_TEST': CartPageAuLarge
}
