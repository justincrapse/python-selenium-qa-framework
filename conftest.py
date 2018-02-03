"""
Site codes:
MD: Modere
NG: Ngage
SR: Shifting Retail
ST: Stockist
GS: Global Shop
"""

import os
import platform
import importlib

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from website_a.wa_data.user_handler import set_user
from wa_test_context import WaTestContext

SCREEN_SHOT_PATH = '/some_path'

def pytest_addoption(parser):
    parser.addoption('--site', action='store', default='MD', help='select which website to test (MD, NG, SR, ST, GS')
    parser.addoption('--brow', action='store', default='FIREFOX', help='select browser driver')
    parser.addoption('--size', action='store', default='LARGE', help='select screen size (SMALL, MEDIUM, LARGE)')
    parser.addoption('--market', action='store', default='US', help='select market')
    parser.addoption('--env', action='store', default='TEST', help='select test environment (DEV, TEST, STAGE, PROD')
    parser.addoption('--user', action='store', default='MC', help='Select user type')
    parser.addoption('--headless', action='store', default='False', help='run headless browser')
    parser.addoption('--level', action='store', default='INFO', help='selects the logging level (INFO OR DEBUG)')


@pytest.fixture
def env_config(request):
    website = request.config.getoption('--site')
    market_code = request.config.getoption('--market')
    screen_size = request.config.getoption('--size')
    environment = request.config.getoption('--env')
    browser = request.config.getoption('--brow')
    logging_level = request.config.getoption('--level')
    user_type = request.config.getoption('--user')
    markets = importlib.import_module(f'website_a.wa_data.{website.lower()}_markets').MARKETS
    base_url = markets[market_code][environment]
    class_suffix = f'{market_code}_{screen_size}_{environment}'
    screen_shot_path = SCREEN_SHOT_PATH
    computer_name = platform.node()
    user = set_user(market_code=market_code, computer_name=computer_name, user_type=user_type, env=environment)

    test_context = WaTestContext(
        website=website,
        market_code=market_code,
        screen_size=screen_size,
        environment=environment,
        browser=browser,
        base_url=base_url,
        user=user,
        class_suffix=class_suffix,
        screen_shot_path=screen_shot_path,
        logging_level=logging_level,
        computer_name=computer_name)
    return test_context


@pytest.fixture
def driver(request, env_config):
    test_context = env_config
    browser = test_context.browser
    size = test_context.screen_size
    headless = request.config.getoption('--headless')
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

    # set the window size
    if size == 'LARGE':
        web_driver.set_window_size(1920, 1080)
        web_driver.set_window_position(0, 0)
    elif size == 'SMALL':
        web_driver.set_window_size(375, 667)

    # go to base url as default for all tests after setting up the driver:
    web_driver.get(test_context.base_url)

    yield web_driver
    # everything after yield will run after the tests run. This is pytest's version of teardown.
    web_driver.quit()


@pytest.fixture
def tc(driver, env_config):
    test_context = env_config
    # add session ID for easy access for logging:
    test_context.session_id = driver.session_id
    test_context.driver = driver  # type: webdriver
    return test_context
