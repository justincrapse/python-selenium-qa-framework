from datetime import datetime
import time

import pytest

from website_a.wa_base_objects.wa_base_test_case import WaBaseTestCase
from website_a.wa_pages import wa_pages
from website_a.wa_utilities.log_handler import md_test_logger
from wa_test_context import WaTestContext


class TestSignup(WaBaseTestCase):
    @md_test_logger
    @pytest.mark.countdown
    def test_signup(self, tc: WaTestContext):
        # with unique email will create a new account
        unique_email = self.generate_unique_email(tc)
        register_page = wa_pages.RegisterPage(tc)._navigate()
        register_page.fill_out_and_submit(email_override=unique_email)
        home_page = wa_pages.HomePage(tc)

        assert home_page.is_logged_in(), f'Could not determine if the user was successfully logged in'
        tc.confirmation_msg = f'SUCCESS: Created new user: {unique_email}'

    @md_test_logger
    def test_signup_no_referral_code(self, tc: WaTestContext):
        unique_email = self.generate_unique_email(tc)
        register_page = wa_pages.RegisterPage(tc).navigate()
        register_page.fill_out_and_submit(referral_code=False, email_override=unique_email)
        user_icon = wa_pages.NavBar(tc).el_user_icon

        assert user_icon.is_present(), f'User Icon is not locatable: {user_icon.locator}'
        tc.confirmation_msg = f'SUCCESS: Created new user without referral code: {unique_email}'

    @md_test_logger
    @pytest.mark.genesis
    @pytest.mark.sql_test
    def test_sql_signup(self, tc: WaTestContext):
        unique_email = self.generate_unique_email(tc)
        register_page = wa_pages.RegisterPage(tc).navigate()
        register_page.fill_out_and_submit(email_override=unique_email)

        conn = self.sql_server_con()
        cursor = conn.cursor()
        sql = "SELECT firstname, lastname, phone, birthdate, customertypeid " \
              "FROM customers " \
              f"WHERE email = '{unique_email}'"
        result = None
        counter = 0
        wait_time = 10
        while not result:
            cursor.execute(sql)
            result = cursor.fetchone()
            time.sleep(wait_time)
            if counter >= 5:
                raise ValueError(f'New customer with ({unique_email}) was not found in the database after waiting'
                                 f'for {wait_time * counter} seconds')
        firstname, lastname, phone, birthday, customer_type = result
        cursor.close()

        dob_datetime = datetime.strptime(tc.user['DOB'], '%Y-%m-%d')
        result_set = [firstname, lastname, phone, birthday, customer_type]
        expected_set = [tc.user['FIRST_NAME'], tc.user['LAST_NAME'], tc.user['PHONE'], dob_datetime, 1]
        assert result_set == expected_set, \
            f'result set ({result_set}) does not match expected user data: {expected_set}'
        tc.confirmation_msg = f'SUCCESS: result set ({result_set}) matches expected user data: {expected_set}'
