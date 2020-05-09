from common.base_objects.base_test_case import BaseTestCase


class BPBaseTestCase(BaseTestCase):
    """ Shared functions across many pages can be written here for easy access from where the test method is written """
    @staticmethod
    def bp_login(tc, username, password):
        pass

    @staticmethod
    def bp_logout(tc):
        pass

    @staticmethod
    def clear_cart(tc):
        pass
