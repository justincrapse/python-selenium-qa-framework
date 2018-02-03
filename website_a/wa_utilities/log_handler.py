import functools
from time import time

from wa_test_context import WaTestContext
from website_a.wa_pages import wa_pages


def take_screen_shot(tc: WaTestContext, *args):
    """ You'll want to keep a similar format here to how it currently is as it can uniquely identify a screenshot if you
    run the same test multiple times. """
    driver = tc.driver
    path = tc.screen_shot_path
    counter = tc.get_screenshot_number()
    file_name = f'{path}/{tc.test_name}_{tc.screen_size}_{tc.browser}_' \
                f'{tc.session_id[-5:]}_{counter} {" ".join(args)}.png'
    driver.save_screenshot(filename=file_name)


def md_test_logger(func):
    """ Decorate every test function with this method to handle startup and teardown logging """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        test_name = func.__name__
        tc = kwargs['tc']  # type: WaTestContext
        tc.test_name = test_name
        tc.info_logger.info(f'\n{"/"*120}\nTest Start: {test_name}\n{"/"*120}')

        startup_message = '\n'.join([
            f'test: {test_name}',
            f'website: {tc.website}',
            f'browser: {tc.browser}',
            f'screensize: {tc.screen_size}',
            f'market: {tc.market_code}',
            f'environment: {tc.environment}',
            f'logging_level: {tc.logging_level}',
            f'computer_name: {tc.computer_Name}',
            f'session_id: {tc.session_id}',
            f'user_data: {tc.user}'
        ])

        tc.info_logger.info(startup_message)

        try:
            result = func(self, *args, **kwargs)
            if tc.confirmation_msg:
                tc.info_logger.info(tc.confirmation_msg)
            tc.info_logger.info(f'TEST_PASSED: {test_name}'.center(120, '/'))
            return result
        except Exception as e:
            tc.info_logger.info(f'Test Failed: {test_name}'.center(120, '/'))
            take_screen_shot(tc, 'TEST_FAILED')
            tc.syslog_logger.info(startup_message + '\n' + str(e))
            if wa_pages.LoginPage(tc).is_on_page():
                raise ValueError(f'{str(e)} unexpected fail or redirect at login screen')
            raise e
    return wrapper


def page_logger(func):
    """ page logger will log the page method being wrapped along with how long execution took. Only logs after the
     method is complete, so if a method inside that method is called, that inside method will be recorded first after it
     is finished, then the original method will be logged on the next line after it finishes. Spend some time reading
     the logs or pass in -s to suppress the capture of the realtime console log output to see the logs real time. """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        tc = self.tc  # type: WaTestContext
        tc.logger_depth += 1
        func_name = func.__name__
        class_name = self.__class__.__name__
        if tc.logger_depth == 1 and tc.logging_level == 'DEBUG':
            take_screen_shot(tc, class_name, func_name)
        t1 = time()
        try:
            result = func(self, *args, **kwargs)
            seconds = time() - t1

            msg = f'{tc.test_name}_{tc.session_id[-5:]} {class_name}: {func_name} [{seconds:.2f}s]'
            tc.info_logger.info(msg=msg)
            tc.logger_depth -= 1
            return result
        except Exception as e:
            seconds = time() - t1
            msg = f'{tc.test_name}_{tc.session_id[-5:]} {class_name}: {func_name} FAIL [{seconds:.2f}s]'
            tc.info_logger.info(msg=msg)
            take_screen_shot(tc, class_name, func_name, 'fail')
            raise e
    return wrapper


def element_logger(func):
    """ element logger will log the element method being wrapped along with how long execution took """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        tc = self.tc  # type: WaTestContext
        page_name = self.page.__class__.__name__
        func_name = func.__name__
        el_name = self.name
        tc.logger_depth += 1
        if tc.logger_depth == 1 and tc.logging_level == 'DEBUG':
            take_screen_shot(tc, page_name, el_name, func_name)
        t1 = time()
        try:
            result = func(self, *args, **kwargs)
            seconds = time() - t1
            msg = f'{tc.test_name}_{tc.session_id[-5:]} {page_name}: {func_name}: {el_name} [{seconds:.2f}s]'
            tc.info_logger.info(msg=msg)
            tc.logger_depth -= 1
            return result
        except Exception as e:
            seconds = time() - t1
            take_screen_shot(tc, page_name, el_name, func_name, 'fail')
            msg = f'{tc.test_name}_{tc.session_id[-5:]} {page_name}: {func_name}: {el_name} FIALED [{seconds:.2f}s]'
            tc.info_logger.info(msg=msg)
            raise e
    return wrapper
