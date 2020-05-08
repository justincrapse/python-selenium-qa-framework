import pytest

from beatport.bp_base_objects.wa_base_test_case import BPBaseTestCase
import bp_pages


class TestSamples(BPBaseTestCase):
    @pytest.mark.prod
    def test_home_page_nav(self, tc):
        home_page = bp_pages.HomePage(tc).navigate()
        assert home_page.on_page()
