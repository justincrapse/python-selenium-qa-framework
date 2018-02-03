from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

from common.base_objects.base_page import BasePage
from common.utilities import web_constants as wc
from website_a.wa_utilities.log_handler import element_logger, page_logger
from wa_test_context import WaTestContext


class BaseElement:
    def __init__(self, page, name, locator, locator_type):
        self.page = page  # type: BasePage
        self.name = name
        self.driver = page.driver  # type: WebDriver
        self.tc = page.tc  # type: WaTestContext
        self.locator = locator
        self.locator_type = locator_type
        self.wait_time = 15
        self.spinner_wait_time = 65

    def get_href(self):
        self.wait_for_spinner()
        elem = self.locate_element()
        url = elem.get_attribute("href")
        return url

    @element_logger
    def click(self, wait_time=None, return_bool=False, suppress=False, wait_delay=None):
        wait_time = wait_time if wait_time else self.wait_time
        self.wait_for_spinner(wait_delay=wait_delay)
        self.wait_for_element_clickable(wait_time=wait_time, return_bool=return_bool, suppress=suppress)
        web_element = self.locate_element(wait_time=wait_time, return_bool=return_bool, suppress=suppress)
        web_element.click()
        return self

    @page_logger
    def click_if_present(self, suppress=True, wait_time=None):
        wait_time = wait_time if wait_time else self.page.wait_time
        self.click(suppress=suppress, wait_time=wait_time)

    @page_logger
    def element_on_page(self, wait_time=None, return_bool=False):
        """ determine if on_page by element and return the page object this elements belongs to """
        wait_time = wait_time if wait_time else self.page.wait_time
        self.wait_for_spinner(wait_delay=0.5)
        try:
            self.locate_element(wait_time=wait_time)
            if return_bool:
                return True
            return self.page
        except TimeoutException:
            if return_bool:
                return False
            raise TimeoutException(msg=f'Could not determine on page by page element locator: "{self.locator}"')

    @element_logger
    def get_attribute_value(self, attribute, wait_time=None):
        self.wait_for_spinner()
        web_el = self.locate_element(wait_time=wait_time)
        return web_el.get_attribute(attribute)

    @element_logger
    def get_text(self):
        self.wait_for_spinner()
        web_el = self.locate_element()
        return web_el.text

    @element_logger
    def get_value(self, wait_time=None):
        self.wait_for_spinner()
        web_el = self.locate_element(wait_time=wait_time)
        return web_el.get_attribute('value')

    @element_logger
    def hover_over_element(self):
        self.wait_for_spinner()
        web_el = self.locate_element()
        hover = ActionChains(self.driver).move_to_element(web_el)
        hover.perform()
        return self

    @element_logger
    def hover_over_and_click(self):
        self.wait_for_spinner()
        web_el = self.locate_element()
        hover = ActionChains(self.driver).move_to_element(web_el).click()
        hover.perform()
        return self

    @element_logger
    def hover_over_element_with_offset(self, x=1, y=1):
        self.wait_for_spinner()
        web_el = self.locate_element()
        ActionChains(self.driver).move_to_element_with_offset(web_el, x, y).perform()
        return self

    @element_logger
    def insert_text(self, text, clear_text_first=True):
        self.wait_for_spinner()
        web_el = self.locate_element()
        if clear_text_first:
            web_el.clear()
        web_el.send_keys(text)
        return self

    @element_logger
    def insert_text_and_hit_enter(self, text_string, clear_text_first=True):
        self.wait_for_spinner()
        web_el = self.locate_element()
        if clear_text_first:
            web_el.clear()
        web_el.send_keys(text_string)
        web_el.send_keys(Keys.ENTER)
        return self

    @element_logger
    def insert_text_and_hit_tab(self, text_string, clear_text_first=True):
        self.wait_for_spinner()
        web_el = self.locate_element()
        if clear_text_first:
            web_el.clear()
        web_el.send_keys(text_string)
        web_el.send_keys(Keys.TAB)
        return self

    @element_logger
    def implicit_wait(self, time=3):
        sleep(time)
        return self

    @element_logger
    def is_present(self, wait_for_present=True, wait_time=None):
        self.wait_for_spinner()
        wait_time = wait_time if wait_time else self.wait_time
        return self.locate_element(wait_for_present=wait_for_present, wait_time=wait_time, return_bool=True)

    @element_logger
    def is_clickable(self, wait_time=None):
        self.wait_for_spinner()
        wait_time = wait_time if wait_time else self.wait_time
        return self.wait_for_element_clickable(return_bool=True, wait_time=wait_time)

    @element_logger
    def is_element_on_page(self, wait_time=None):
        self.wait_for_spinner()
        wait_time = wait_time if wait_time else self.wait_time
        return self.element_on_page(return_bool=True, wait_time=wait_time)

    @element_logger
    def is_stale(self, wait_time=None):
        self.wait_for_spinner()
        wait_time = wait_time if wait_time else self.wait_time
        return self.wait_for_staleness(wait_time=wait_time, return_bool=True)

    @element_logger
    def is_visible(self, wait_time=None, spinner=True):
        if spinner:
            self.wait_for_spinner()
        wait_time = wait_time if wait_time else self.wait_time
        return self.wait_for_element_visible(wait_time=wait_time, return_bool=True)

    @element_logger
    def js_click(self, wait_time=None):
        wait_time = wait_time if wait_time else self.wait_time
        self.wait_for_spinner()
        self.wait_for_element_clickable(wait_time=wait_time)
        # web_element = self.tc.driver.find_element_by_xpath(self.locator)
        web_element = self.locate_element(wait_time=wait_time)
        try:
            self.tc.driver.execute_script("arguments[0].click();", web_element)
        except WebDriverException:
            raise
        return self

    @element_logger
    def locate_element(self, wait_for_present=True, wait_time=None, return_bool=False, suppress=False):
        wait_time = wait_time if wait_time else self.wait_time
        if wait_for_present:
            self.wait_for_element_present(wait_time=wait_time, return_bool=return_bool, suppress=suppress)
        try:
            if self.locator_type == 'xpath':
                web_element = self.driver.find_element_by_xpath(self.locator)
            elif self.locator_type == 'id':
                web_element = self.driver.find_element_by_id(self.locator)
            elif self.locator_type == 'css':
                web_element = self.driver.find_element_by_css_selector(self.locator)
            else:
                raise Exception("Need to define xpath, id, or css selector type for your element locator")
            if return_bool:
                return True
            return web_element
        except NoSuchElementException:
            if return_bool or suppress:
                return False
            raise NoSuchElementException("Element not found. Locator: {} Locator Type: {} ".format(self.locator,
                                                                                                   self.locator_type))

    @element_logger
    def locate_elements(self, wait_for_element_present=True):
        if wait_for_element_present:
            self.wait_for_element_present()
        try:
            if self.locator_type == 'xpath':
                web_elements = self.driver.find_elements_by_xpath(self.locator)
            elif self.locator_type == 'id':
                web_elements = self.driver.find_elements_by_id(self.locator)
            elif self.locator_type == 'css':
                web_elements = self.driver.find_elements_by_css_selector(self.locator)
            else:
                raise Exception("Need to define xpath, id, or css selector type for your elements locator")
        except NoSuchElementException:
            raise NoSuchElementException("Elements not found. Locator: {} Locator Type: {} ".format(self.locator,
                                                                                                    self.locator_type))
        return web_elements

    @element_logger
    def scroll_to_element_and_return_location(self):
        self.wait_for_spinner()
        element = self.locate_element()
        location = element.location_once_scrolled_into_view
        return location

    @element_logger
    def scroll_past_element(self, distance=100):
        """ positive numbers scroll down and negative numbers scroll up. """
        self.scroll_to_element_and_return_location()
        self.driver.execute_script(f'window.scrollBy(0, {distance})')
        return self

    @element_logger
    def submit(self, wait_time=None):
        wait_time = wait_time if wait_time else self.wait_time
        self.wait_for_spinner()
        self.wait_for_element_visible()
        element = self.locate_element(wait_time=wait_time)
        element.submit()
        return self

    @element_logger
    def sleep(self, time=3):
        sleep(time)
        return self

    @element_logger
    def verify_string_in_text(self, string):
        text = self.get_text()
        if string in text:
            return True
        else:
            raise ValueError(f'String "{string}" was not found in text "{text}"')

    @element_logger
    def wait_for_element_present(self, wait_time=None, return_bool=False, suppress=False):
        wait_time = wait_time if wait_time else self.wait_time
        try:
            if self.locator_type == wc.BY_XPATH:
                WebDriverWait(self.driver, wait_time).until(ec.presence_of_element_located((By.XPATH, self.locator)))
            elif self.locator_type == wc.BY_ID:
                WebDriverWait(self.driver, wait_time).until(ec.presence_of_element_located((By.ID, self.locator)))
            elif self.locator_type == wc.BY_CSS:
                WebDriverWait(self.driver, wait_time).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, self.locator)))
            if return_bool:
                return True
        except TimeoutException:
            if return_bool or suppress:
                return False
            raise TimeoutException(msg=f'Element not found. xpath: {self.locator}')

    @element_logger
    def wait_for_staleness(self, wait_time=10, return_bool=False):
        wait_time = wait_time if wait_time else self.wait_time
        if self.is_present(wait_time=2):
            try:
                element = self.locate_element(wait_time=2)
            except (NoSuchElementException, TimeoutException):
                return True
            try:
                WebDriverWait(self.driver, wait_time).until(ec.staleness_of(element))
                if return_bool:
                    return True
            except TimeoutException:
                if return_bool:
                    return False
                raise TimeoutException(msg=f'Element not stale and still found in the DOM. xpath: {self.locator}')
        else:
            if return_bool:
                return False

    @element_logger
    def wait_for_element_visible(self, wait_time=None, return_bool=False):
        wait_time = wait_time if wait_time else self.wait_time
        try:
            if self.locator_type == wc.BY_XPATH:
                WebDriverWait(self.driver, wait_time).until(ec.visibility_of_element_located((By.XPATH, self.locator)))
            elif self.locator_type == wc.BY_ID:
                WebDriverWait(self.driver, wait_time).until(ec.visibility_of_element_located((By.ID, self.locator)))
            elif self.locator_type == wc.BY_CSS:
                WebDriverWait(self.driver, wait_time).until(ec.visibility_of_element_located(
                    (By.CSS_SELECTOR, self.locator)))
            if return_bool:
                return True
        except TimeoutException:
            if return_bool:
                return False
            raise TimeoutException(msg=f'Element not visible. xpath: {self.locator}')
        return self

    @element_logger
    def wait_for_element_invisible(self, wait_time=None, return_bool=False):
        wait_time = wait_time if wait_time else self.wait_time
        try:
            if self.locator_type == wc.BY_XPATH:
                WebDriverWait(self.driver, wait_time).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                                self.locator)))
            elif self.locator_type == wc.BY_ID:
                WebDriverWait(self.driver, wait_time).until(ec.invisibility_of_element_located((By.ID, self.locator)))
            elif self.locator_type == wc.BY_CSS:
                WebDriverWait(self.driver, wait_time).until(ec.invisibility_of_element_located(
                    (By.CSS_SELECTOR, self.locator)))
            if return_bool:
                return True
        except TimeoutException:
            if return_bool:
                return False
            raise TimeoutException(msg=f'Element not invisible (still visible.) xpath: {self.locator}')

    @element_logger
    def wait_for_element_clickable(self, wait_time=None, return_bool=False, suppress=False):
        wait_time = wait_time if wait_time else self.wait_time
        if self.tc.browser == 'EDGE':
            return True
        try:
            if self.locator_type == wc.BY_XPATH:
                WebDriverWait(self.driver, wait_time).until(ec.element_to_be_clickable((By.XPATH, self.locator)))
            elif self.locator_type == wc.BY_ID:
                WebDriverWait(self.driver, wait_time).until(ec.element_to_be_clickable((By.ID, self.locator)))
            elif self.locator_type == wc.BY_CSS:
                WebDriverWait(self.driver, wait_time).until(ec.element_to_be_clickable((By.CSS_SELECTOR, self.locator)))
            if return_bool:
                return True
            return self
        except TimeoutException:
            if return_bool or suppress:
                return False
            raise TimeoutException(msg=f'Element not found clickable. xpath: {self.locator}')
        except AttributeError:
            if return_bool or suppress:
                return False
            raise AttributeError(f'Element not found clickable. xpath: {self.locator}')

    @element_logger
    def wait_for_spinner(self, wait_time=None, wait_delay=None):
        """ wait for the spinner, if present, to go away """
        pass
