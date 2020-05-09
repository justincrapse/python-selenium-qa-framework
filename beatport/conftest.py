import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bp_test_context import BPTestContext
import bp_utilities as bp_util


def pytest_addoption(parser):
    parser.addoption('--brow', action='store', default='CHROME', help='select browser driver')
    parser.addoption('--env', action='store', default='TEST', help='select test environment (DEV, TEST, STAGE, PROD')
    parser.addoption('--user', action='store', default='TEST_USER', help='Select user type')


@pytest.fixture
def env_config(request):
    environment = request.config.getoption('--env')
    browser = request.config.getoption('--brow')
    user_type = request.config.getoption('--user')

    test_context = BPTestContext(
        environment=environment,
        browser=browser,
        base_url=bp_util.bp_conf.BASE_URL,
        user=user_type)
    return test_context


@pytest.fixture
def driver(request, env_config):
    test_context = env_config
    browser = test_context.browser
    headless = False
    headless = True if headless == 'True' else False

    if browser == 'FIREFOX':
        if headless:
            os.environ['MOZ_HEADLESS'] = '1'
        web_driver = webdriver.Firefox()

    elif browser == 'CHROME':
        if headless:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            web_driver = webdriver.Chrome(chrome_options=chrome_options)
        else:
            web_driver = webdriver.Chrome()
    elif browser == 'EDGE':
        web_driver = webdriver.Edge()
    elif browser == 'SAFARI':
        web_driver = webdriver.Safari()
    else:
        web_driver = None

    # go to base url as default for all tests after setting up the driver:
    web_driver.get(test_context.base_url)

    failed = request.session.testsfailed  # this value is not quite reliable, so we check for a difference to be sure.
    yield web_driver
    # everything after yield will run after the tests run. This is pytest's version of teardown.
    if request.session.testsfailed != failed:  # as long as it is not the same as initial value.
        web_driver.save_screenshot(f'{bp_util.bp_conf.SCREENSHOT_DIR}\\my_screenshot.jpg')
    web_driver.quit()


@pytest.fixture
def tc(driver, env_config):
    test_context = env_config
    # add session ID for easy access for logging:
    test_context.session_id = driver.session_id
    test_context.driver = driver  # type: webdriver
    return test_context
