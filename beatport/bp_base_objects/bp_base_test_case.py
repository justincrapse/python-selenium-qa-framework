from common.base_objects.base_test_case import BaseTestCase
import bp_pages


class BPBaseTestCase(BaseTestCase):
    """ Shared functions across many pages can be written here for easy access from where the test method is written """
    @staticmethod
    def login(tc, username=None, password=None):
        username = username if username else tc.username
        password = password if password else tc.password
        bp_pages.BPHeader(tc).log_in(username=username, password=password)

    @staticmethod
    def logout(tc):
        pass

    @staticmethod
    def clear_cart(tc):
        pass
