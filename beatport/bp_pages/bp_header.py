from beatport.bp_base_objects.bp_base_page import BPBasePage
from bp_test_context import BPTestContext
from bp_base_objects.bp_element import BPElement
import utilities.element_selectors as by


class BPHeader(BPBasePage):
    def __init__(self, tc: BPTestContext):
        super().__init__(tc=tc)

        self.XP_HEADER = '//header[descendant::div[@class="nav-links"]]'
        self.XP_SEARCH = self.XP_HEADER + '//input[@placeholder="Search..."]'
        self.XP_LOGIN_ICON = self.XP_HEADER + '//div[@id="head-account-icon"]'
        self.XP_ACCOUNT_ICON = self.XP_HEADER + '//span[@class="head-account-user-image"]'
        self.search_field = BPElement(page=self, locator=self.XP_SEARCH)
        self.login_icon = BPElement(page=self, locator=self.XP_LOGIN_ICON)
        self.account_icon = BPElement(page=self, locator=self.XP_ACCOUNT_ICON)

        # login dropdown:
        self.XP_USERNAME_FLD = self.XP_HEADER + '//input[@name="username"]'
        self.XP_PASSWORD_FLD = self.XP_HEADER + '//input[@name="password"]'
        self.XP_LOG_IN_BTN = self.XP_HEADER + '//input[@value="Log In"]'
        self.username_fld = BPElement(page=self, locator=self.XP_USERNAME_FLD)
        self.password_fld = BPElement(page=self, locator=self.XP_PASSWORD_FLD)
        self.log_in_btn = BPElement(page=self, locator=self.XP_LOG_IN_BTN)

    # since this is just a component of every page, we handle on_page differently.
    def is_on_page(self):
        assert self.search_field.is_clickable()

    def log_in(self, username, password):
        self.login_icon.hover_over_element()
        self.username_fld.insert_text(username)
        self.password_fld.insert_text(password)
        self.log_in_btn.click()
