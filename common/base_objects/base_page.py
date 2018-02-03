from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

from website_a.wa_utilities.log_handler import page_logger, take_screen_shot
from wa_test_context import WaTestContext


class BasePage(object):
    """
    All page objects inherit from this class
    """
    def __init__(self, tc, page_url='', page_id=None, by_xpath=False):
        self.page_url = page_url
        self.page_id = page_id
        self.by_xpath = by_xpath
        self.wait_time = 30
        self.spinner_wait_time = 45

        self.tc = tc  # type: WaTestContext
        self.driver = tc.driver  # type: WebDriver
        self.base_url = tc.base_url

    @page_logger
    def wait_for_spinner(self, wait_time=None, wait_delay=None):
        """ wait for the spinner, if present, to go away """
        pass

    @page_logger
    def sleep(self, wait_time=3):
        sleep(wait_time)
        return self

    @page_logger
    def is_on_page(self, wait_time=0.1):
        """ checks to see if you are on a page. Low default wait time as most of the time this will be used for simply
        checking weather you are already on a page or not """
        self.wait_for_spinner()
        return self.on_page(wait_time=wait_time, return_bool=True)

    @page_logger
    def on_page(self, page_id_override=None, wait_time=None, return_bool=False):
        """ checks the page ID to confirm if you are on the page. This checks the page_id text is in the title tag or
        will check that an page_id xpath has a match on the page. Make sure to pass in by_xpath=True to check xpath """
        wait_time = wait_time if wait_time else self.wait_time
        self.wait_for_spinner()
        page_id = page_id_override if page_id_override else self.page_id
        xpath = page_id if self.by_xpath else f'//title[contains(text(), "{page_id}")]'
        try:
            WebDriverWait(
                driver=self.driver,
                timeout=wait_time).until(ec.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            if return_bool:
                return False
            raise TimeoutException(msg=f'Could not find page id by xpath: "{xpath}"')
        if return_bool:
            return True
        return self

    @page_logger
    def _navigate(self, appendage=None):
        """
        When you call a page's _navigate function, it simply navigates to its URL (base url + page_url)
        """
        if appendage:
            self.driver.get(self.base_url + appendage)
        else:
            self.driver.get(self.base_url + self.page_url)
        return self

    @page_logger
    def _navigate_to_url(self, url):
        """
        explicitly define the url you want to navigate to for this page if base_url is different than what you need
        """
        self.driver.get(url)
        return self

    @page_logger
    def refresh_page_until_element_present(self, element, interval_time=10, interval_count=5, fail_msg=None):
        """ Note that this returns the element it is looking for so you can chain it in-line in your code """
        if self.tc.logging_level == 'DEBUG':
            take_screen_shot(self.tc, 'REFRESHING_PAGE_FOR_ELEMENT_SEARCH')
        for i in range(interval_count):
            self._navigate()
            self.on_page()
            if element.is_present(wait_time=5):
                return element
            else:
                sleep(interval_time)
        take_screen_shot(self.tc, 'ELEMENT_NOT_FOUND_ON_PAGE_AFTER_REFRESH')
        raise NoSuchElementException(f'{fail_msg}: {element.name} not found on page ({self.__class__.__name__}) after'
                                     f' refreshing {interval_count} times and waiting for {interval_time} seconds each '
                                     f'time')
