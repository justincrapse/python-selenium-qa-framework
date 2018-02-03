from itertools import zip_longest

import pytest

from website_a.wa_base_objects.wa_base_test_case import WaBaseTestCase
from website_a.wa_pages import wa_pages
from website_a.wa_utilities.log_handler import md_test_logger, take_screen_shot
from wa_test_context import WaTestContext
from website_a.wa_utilities import wa_nav_constants as nc


class TestCartPage(WaBaseTestCase):
    @md_test_logger
    @pytest.mark.prod
    def test_add_to_cart(self, tc):
        """ this test makes sure that exactly only the products added to the cart are found in the cart """
        self.wa_login(tc)
        self.clear_cart(tc)

        # add a bunch of products to the cart:
        shop_all = wa_pages.ShopAllPage.ListView(tc).navigate()
        products = shop_all.add_onetime_products(products_quantity=3)
        products = sorted(list(set(products)))

        # validate that the products were added to the cart
        cart_page = wa_pages.CartPage(tc).navigate()
        products_in_cart = cart_page.li_product_titles.get_list_text()
        cart_prods = sorted(list(set(products_in_cart)))
        try:
            assert cart_page.added_to_cart_matches_cart(added_to_cart=products, in_cart=cart_prods), \
                f'Products added: {products} do not match products in cart: {cart_prods}'
        except Exception as e:
            take_screen_shot(self.tc, 'Cart_products_mismatch')
            raise e
        finally:
            self.clear_cart(tc)

    @md_test_logger
    @pytest.mark.prod
    @pytest.mark.countdown
    def test_add_to_cart_no_login(self, tc: WaTestContext):
        # add a bunch of products to the cart:
        shop_all = wa_pages.ShopAllPage.ListView(tc).navigate()
        products = shop_all.add_onetime_products(products_quantity=3)
        products = sorted(list(set(products)))

        # validate that the products were added to the cart
        cart_page = wa_pages.CartPage(tc).navigate()
        products_in_cart = cart_page.li_product_titles.get_list_text()
        cart_prods = sorted(list(set(products_in_cart)))
        mismatch = False
        for p1, p2 in zip_longest(products, cart_prods):
            if p1 not in p2:
                mismatch = True
                break
        try:
            assert not mismatch, f'Products added: {products} do not match products in cart: {cart_prods}'
        finally:
            self.clear_cart(tc)

    @md_test_logger
    @pytest.mark.prod
    @pytest.mark.countdown
    def test_update_cart_quantity(self, tc: WaTestContext):
        quantity = 17
        # add a bunch of products to the cart:
        product_page = wa_pages.ProductPage(tc).navigate(nc.PRODUCT_PAGE_RANDOM_VIA_SHOP_ALL)
        product_title = product_page.el_product_title.get_attribute_value(attribute='content')
        product_page.radio_onetime_purchase.click()
        product_page.btn_add_to_cart.click()
        cart_page = wa_pages.CartPage(tc).navigate()
        cart_page.set_quantity_by_product_title(product_title=product_title, quantity=quantity)
        cart_page.el_subtotal.click()
        updated_quantity = cart_page.get_quantity_by_product_name(product_name=product_title)
        assert updated_quantity == str(quantity), f'product quantity ({updated_quantity}) ' \
                                                  f'does not match entered quantity ({quantity})'

    @md_test_logger
    @pytest.mark.prod
    @pytest.mark.genesis
    def test_cart_dropdown_quantity_no_login(self, tc: WaTestContext):
        if tc.screen_size == 'SMALL':
            pass
        else:
            shop_all = wa_pages.ShopAllPage.ListView(tc).navigate()
            product_count = 3
            product_quantity_each = 3
            total_count = product_count * product_quantity_each
            shop_all.add_onetime_products(products_quantity=product_count, quantity_each=product_quantity_each)
            nav_bar = wa_pages.NavBar(tc).navigate()
            nav_bar.el_cart.hover_over_element().sleep(1)
            cart_quantity = int(nav_bar.el_cart_dropdown_quantity.get_text())
            assert cart_quantity == total_count, \
                f'Cart dropdown quantity: {cart_quantity} does not match expected: {total_count}'
            tc.confirmation_msg = f'SUCCESS: Cart dropdown quantity: {cart_quantity} matches expected: {total_count}'
