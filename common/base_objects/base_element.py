from time import sleep

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

from common.base_objects.base_page import BasePage
import common.utilities.element_selectors as es
import common.utilities.wait_times as waits

from bp_test_context import BPTestContext


class BaseElement:
    """ Currently diving into the 8th circle of decorator hell to use a better structural design for applying wait
    times to most of the interactive function. Will be updated soon. """
    def __init__(self, page, locator, locator_type=es.BY_XPATH):
        self.page = page  # type: BasePage
        self.driver = page.driver  # type: WebDriver
        self.tc = page.tc  # type: BPTestContext
        self.locator = locator
        self.locator_type = locator_type

    def get_href(self, wait_time=waits.DEFAULT):
        elem = self.locate_element(wait_time=wait_time)
        url = elem.get_attribute("href")
        return url

    def click(self, wait_time=waits.DEFAULT):
        web_element = self.locate_element(wait_time=wait_time)
        web_element.click()
        return self

    def element_on_page(self, wait_time=waits.DEFAULT):
        try:
            self.locate_element(wait_time=wait_time)
            return self.page
        except TimeoutException:
            raise TimeoutException(msg=f'Could not determine on page by page element locator: "{self.locator}"')

    def get_attribute_value(self, attribute, wait_time=waits.DEFAULT):
        web_el = self.locate_element(wait_time=wait_time)
        return web_el.get_attribute(attribute)

    def get_text(self, wait_time=waits.DEFAULT):
        web_el = self.locate_element(wait_time=wait_time)
        return web_el.text

    def get_value(self, wait_time=waits.DEFAULT):
        web_el = self.locate_element(wait_time=wait_time)
        return web_el.get_attribute('value')

    def hover_over_element(self, wait_time=waits.DEFAULT):
        web_el = self.locate_element(wait_time=wait_time)
        hover = ActionChains(self.driver).move_to_element(web_el)
        hover.perform()
        return self

    def hover_over_and_click(self, wait_time=waits.DEFAULT):
        web_el = self.locate_element(wait_time=wait_time)
        hover = ActionChains(self.driver).move_to_element(web_el).click()
        hover.perform()
        return self

    def hover_over_element_with_offset(self, x=1, y=1, wait_time=waits.DEFAULT):
        web_el = self.locate_element(wait_time=wait_time)
        ActionChains(self.driver).move_to_element_with_offset(web_el, x, y).perform()
        return self

    def insert_text(self, text, clear_text_first=True, wait_time=waits.DEFAULT):
        web_el = self.locate_element(wait_time=wait_time)
        if clear_text_first:
            web_el.clear()
        web_el.send_keys(text)
        return self

    def insert_text_and_hit_enter(self, text_string, clear_text_first=True, wait_time=waits.DEFAULT):
        web_el = self.locate_element(wait_time=wait_time)
        if clear_text_first:
            web_el.clear()
        web_el.send_keys(text_string)
        web_el.send_keys(Keys.ENTER)
        return self

    def insert_text_and_hit_tab(self, text_string, clear_text_first=True, wait_time=waits.DEFAULT):
        web_el = self.locate_element(wait_time=wait_time)
        if clear_text_first:
            web_el.clear()
        web_el.send_keys(text_string)
        web_el.send_keys(Keys.TAB)
        return self

    def implicit_wait(self, time=3):
        sleep(time)
        return self

    def is_present(self, wait_time=waits.DEFAULT):
        return self.locate_element(wait_time=wait_time, return_bool=True)

    def is_clickable(self, wait_time=waits.DEFAULT) -> bool:
        return self.wait_for_element_clickable(return_bool=True, wait_time=wait_time)

    def is_element_on_page(self, wait_time=waits.DEFAULT):
        return self.element_on_page(wait_time=wait_time)

    def is_stale(self, wait_time=waits.DEFAULT):
        return self.wait_for_staleness(wait_time=wait_time, return_bool=True)

    def is_visible(self, wait_time=waits.DEFAULT):
        return self.wait_for_element_visible(wait_time=wait_time, return_bool=True)

    def js_click(self, wait_time=waits.DEFAULT):
        self.wait_for_element_clickable(wait_time=wait_time)
        # web_element = self.tc.driver.find_element_by_xpath(self.locator)
        web_element = self.locate_element(wait_time=wait_time)
        try:
            self.tc.driver.execute_script("arguments[0].click();", web_element)
        except WebDriverException:
            raise
        return self

    def locate_element(self, wait_time=waits.DEFAULT, return_bool=False):
        self.wait_for_element_clickable(wait_time=wait_time)
        try:
            if self.locator_type == es.BY_XPATH:
                web_element = self.driver.find_element_by_xpath(self.locator)
            elif self.locator_type == es.BY_ID:
                web_element = self.driver.find_element_by_id(self.locator)
            elif self.locator_type == es.BY_CSS:
                web_element = self.driver.find_element_by_css_selector(self.locator)
            else:
                raise Exception("Need to define xpath, id, or css selector type for your element locator")
            if return_bool:
                return True
            return web_element
        except NoSuchElementException:
            if return_bool:
                return False
            raise NoSuchElementException(f'Element not found. Locator:{self.locator} Locator Type:{self.locator_type}')

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

    def scroll_to_element_and_return_location(self, wait_time=waits.DEFAULT):
        element = self.locate_element(wait_time=wait_time)
        location = element.location_once_scrolled_into_view
        return location

    def scroll_past_element(self, distance=100):
        """ positive numbers scroll down and negative numbers scroll up. """
        self.scroll_to_element_and_return_location()
        self.driver.execute_script(f'window.scrollBy(0, {distance})')
        return self

    def submit(self, wait_time=None):
        self.wait_for_element_visible()
        element = self.locate_element(wait_time=wait_time)
        element.submit()
        return self

    def sleep(self, time=3):
        sleep(time)
        return self

    def verify_string_in_text(self, string):
        text = self.get_text()
        if string in text:
            return True
        else:
            raise ValueError(f'String "{string}" was not found in text "{text}"')

    def wait_for_element_present(self, wait_time=None, return_bool=False, suppress=False):
        try:
            WebDriverWait(self.driver, wait_time).until(ec.presence_of_element_located((self.locator_type, self.locator)))
            if return_bool:
                return True
        except TimeoutException:
            if return_bool or suppress:
                return False
            raise TimeoutException(msg=f'Element not found. xpath: {self.locator}')

    def wait_for_staleness(self, wait_time=10, return_bool=False):
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

    def wait_for_element_visible(self, wait_time=None, return_bool=False):
        try:
            WebDriverWait(self.driver, wait_time).until(ec.visibility_of_element_located(
                (self.locator_type, self.locator)))
            if return_bool:
                return True
        except TimeoutException:
            if return_bool:
                return False
            raise TimeoutException(msg=f'Element not visible. xpath: {self.locator}')
        return self

    def wait_for_element_invisible(self, wait_time=None, return_bool=False):
        try:
            WebDriverWait(self.driver, wait_time).until(ec.invisibility_of_element_located(
                (self.locator_type, self.locator)))
            if return_bool:
                return True
        except TimeoutException:
            if return_bool:
                return False
            raise TimeoutException(msg=f'Element not invisible (still visible.) xpath: {self.locator}')

    def wait_for_element_clickable(self, wait_time=None, return_bool=False, suppress=False):
        if self.tc.browser == 'EDGE':
            return True
        try:
            WebDriverWait(self.driver, wait_time).until(ec.element_to_be_clickable((self.locator_type, self.locator)))
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
