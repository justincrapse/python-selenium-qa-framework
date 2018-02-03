import random
from common.base_objects.base_test_case import BaseTestCase
from website_a.wa_pages import wa_pages
from wa_test_context import WaTestContext


class WaBaseTestCase(BaseTestCase):
    @staticmethod
    def wa_login(tc: WaTestContext, with_unique_email=False, password_override=None, email_override=None):
        if with_unique_email:
            new_email = WaBaseTestCase.generate_unique_email(tc)
            __class__.set_unique_email(tc, unique_email=new_email)
        login_page = wa_pages.LoginPage(tc).navigate()
        login_page.log_in(
            with_unique_email=with_unique_email,
            password_override=password_override,
            email_override=email_override)

    @staticmethod
    def wa_logout(tc):
        account_menu = wa_pages.AccountSubNav(tc).navigate()
        account_menu.btn_log_out.click()

    @staticmethod
    def generate_unique_email(tc: WaTestContext, suffix_length=6, from_session_id=True):
        """ appends your email name with the last characters of the driver session id (suffix_length) Example:
        justinc@monkeyman.com becomes justinc_f9607@monkeyman.com """
        name, domain = tc.user['EMAIL'].split('@')
        if from_session_id:
            new_email = name + '_' + tc.session_id[-suffix_length:] + '@' + domain
        else:
            new_email = name + ''.join([chr(i) for i in random.sample(range(ord('a'), ord('z')), 4)]) + '@' + domain
        return new_email

    @staticmethod
    def set_unique_email(tc: WaTestContext, unique_email):
        tc.user['UNIQUE_EMAIL'] = unique_email

    @staticmethod
    def clear_cart(tc):
        nav_bar = wa_pages.NavBar(tc).navigate()
        cart_page = wa_pages.CartPage(tc)
        if nav_bar.el_cart_count.is_present(wait_time=2):
            cart_page.navigate()
            cart_page.clear_cart()
            if not cart_page.el_empty_cart_text.is_present():
                raise ValueError('Hey, your cart did not clean up')
