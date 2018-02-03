import logging
from logging.handlers import SysLogHandler
from common.utilities.context_filter import ContextFilter


class WaTestContext(object):
    def __init__(self, website, market_code, screen_size, environment, browser, base_url, user, class_suffix, screen_shot_path,
                 logging_level, computer_name):
        self.website = website
        self.market_code = market_code
        self.screen_size = screen_size
        self.environment = environment
        self.browser = browser
        self.base_url = base_url
        self.user = user
        self.class_suffix = class_suffix
        self.screen_shot_path = screen_shot_path
        self.logging_level = logging_level
        self.computer_Name = computer_name

        # These are set after the driver is instantiated and depend on what driver was instantiated
        self.session_id = None
        self.driver = None
        self.test_name = None
        self.confirmation_msg = None
        self.logger_depth = 0

        self.screen_shot_counter = 0

        # set up info log
        self.info_logger = logging.getLogger('info_logger')
        if logging_level == 'INFO':
            self.info_logger.setLevel(level=logging.INFO)
        elif logging_level == 'DEBUG':
            self.info_logger.setLevel(level=logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        file_handler = logging.FileHandler('../../build_artifacts/logs/test_log.log')
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        """ need to see if handler already added or not or else it will add another and duplicate the output when
         running multiple tests """
        if not len(self.info_logger.handlers):
            self.info_logger.addHandler(stream_handler)
            self.info_logger.addHandler(file_handler)

        # set up on_fail file logger:
        self.fail_logger = logging.getLogger('fail_logger')
        if logging_level == 'INFO':
            self.info_logger.setLevel(level=logging.INFO)
        elif logging_level == 'DEBUG':
            self.info_logger.setLevel(level=logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        file_handler = logging.FileHandler('../../build_artifacts/logs/fail_logs.log')
        file_handler.setFormatter(formatter)
        if not len(self.fail_logger.handlers):
            self.fail_logger.addHandler(file_handler)

        # set up syslog logger
        self.syslog_logger = logging.getLogger('syslog_logger')
        self.syslog_logger.setLevel(level=logging.INFO)
        f = ContextFilter()
        self.syslog_logger.addFilter(f)
        syslog = SysLogHandler(address=('syslog-a.logdna.com', 'your id number here for logdna'))
        formatter = logging.Formatter('%(asctime)s %(hostname)s %(message)s', datefmt='%b %d %H:%M:%S')
        syslog.setFormatter(formatter)
        if not len(self.syslog_logger.handlers):
            self.syslog_logger.addHandler(syslog)

    def get_screenshot_number(self):
        if self.screen_shot_counter < 10:
            return_string = '0' + str(self.screen_shot_counter)
            self.screen_shot_counter += 1
            return return_string
        else:
            return_string = str(self.screen_shot_counter)
            self.screen_shot_counter += 1
            return return_string
