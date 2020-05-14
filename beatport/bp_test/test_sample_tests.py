import pytest

from beatport.bp_base_objects.bp_base_test_case import BPBaseTestCase
import bp_pages


class TestSamples(BPBaseTestCase):
    def test_home_page_nav(self, tc):
        home_page = bp_pages.HomePage(tc).navigate()
        home_page.search_field.click(50)
        assert home_page.on_page()

    def test_track_search(self, tc):
        home_page = bp_pages.HomePage(tc)
