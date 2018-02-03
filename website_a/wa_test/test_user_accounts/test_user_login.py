import pytest

from website_a.wa_base_objects.wa_base_test_case import WaBaseTestCase
from website_a.wa_pages import wa_pages
from website_a.wa_utilities.log_handler import md_test_logger
from wa_test_context import WaTestContext


class TestLogin(WaBaseTestCase):
    @md_test_logger
    @pytest.mark.prod
    def test_login(self, tc):
        self.wa_login(tc)
        user_icon = wa_pages.NavBar(tc).el_user_icon
        home_page = wa_pages.HomePage(tc)
        assert home_page.is_logged_in(), f'User Icon is not locatable: {user_icon.locator}'

    @md_test_logger
    @pytest.mark.prod
    def test_logout(self, tc: WaTestContext):
        """ logging in, logging out, then waiting 2 seconds after home page is verified to see if user icon present"""
        self.wa_login(tc)
        self.wa_logout(tc)
        wa_pages.HomePage(tc).on_page()
        user_icon = wa_pages.NavBar(tc).el_user_icon
        assert not user_icon.is_present(wait_time=2), \
            f'el_user_icon still present after logout: {user_icon.locator}'
        tc.confirmation_msg = 'Logout successful as el_user_icon is no longer present'
