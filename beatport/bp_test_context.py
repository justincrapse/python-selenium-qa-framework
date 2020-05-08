class BPTestContext(object):
    def __init__(self, environment, browser, base_url, user):
        self.environment = environment
        self.browser = browser
        self.base_url = base_url
        self.user = user

        self.driver = driver = None
