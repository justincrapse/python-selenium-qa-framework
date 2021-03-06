from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

from bp_test_context import BPTestContext
from common.utilities import wait_times as waits


class BasePage(object):
    """
    All page objects inherit from this class
    """
    def __init__(self, tc, page_url='', page_id=None):
        self.page_url = page_url
        self.page_id = page_id
        self.wait_time = waits.MEDIUM
        self.spinner_wait_time = waits.SPINNER
        self.tc = tc  # type: BPTestContext  # easier autofill for tc.
        self.driver = tc.driver  # type: WebDriver
        self.base_url = tc.base_url

    def wait_for_spinner(self, wait_time=None, wait_delay=None):
        """ wait for the spinner, if present, to go away """
        pass

    def is_on_page(self):
        return self.on_page(return_bool=True)

    def on_page(self, page_id_override=None, wait_time=None, return_bool=False):
        """ checks the page ID to confirm if you are on the page. This checks the page_id text is in the title tag or
        will check that an page_id xpath has a match on the page. Make sure to pass in by_xpath=True to check xpath """
        wait_time = wait_time if wait_time else self.wait_time
        page_id = page_id_override if page_id_override else self.page_id
        xpath = f'//title[text() = "{page_id}"]'
        try:
            WebDriverWait(driver=self.driver,
                          timeout=wait_time).until(ec.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            if return_bool:
                return False
            raise TimeoutException(msg=f'Could not find page id by xpath: "{xpath}"')
        if return_bool:
            return True
        return self

    def _navigate_url(self, appendage=None):
        if appendage:
            self.driver.get(self.base_url + appendage)
        else:
            self.driver.get(self.base_url + self.page_url)
        return self

    def refresh_page_until_element_present(self, element, interval_time=10, interval_count=5, fail_msg=None):
        """ Note that this returns the element it is looking for so you can chain it in-line in your code """

        for i in range(interval_count):
            self._navigate_url()
            self.on_page(wait_time=waits.PAGE_LOAD_DEFAULT)
            if element.is_present(wait_time=5):
                return element
            else:
                sleep(interval_time)
        exc_message = f'{fail_msg}: {element.name} not found on page ({self.__class__.__name__}) after refreshing' \
                      f' {interval_count} times and waiting for {interval_time} seconds each time'
        raise NoSuchElementException(exc_message)
