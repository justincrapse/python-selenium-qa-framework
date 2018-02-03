from website_a.wa_base_elements.wa_button import WaButton
from website_a.wa_pages.home_page.home_page import HomePage
from common.utilities import web_constants as wc
from website_a.wa_pages import wa_pages


class HomePageUsLargeStage(HomePage):
    def __init__(self, tc):
        super().__init__(tc=tc)


class HomePageUsLargeProd(HomePage):
    def __init__(self, tc, page_id='redlineshoes'):
        super().__init__(tc=tc, page_id=page_id)


class HomePageAuLargeStage(HomePage):
    def __init__(self, tc, page_id='RedlineFootwear'):
        super().__init__(tc=tc, page_url=page_id)


class HomePageJapan(HomePage):
    def __init__(self, tc):
        super().__init__(tc=tc)
        self.btn_exit_registration_success = WaButton(
            page=self,
            name='btn_exit_registration_success',
            locator='some_locator',
            locator_type=wc.BY_XPATH)


class HomePageJapanSmall(HomePageJapan):
    def __init__(self, tc):
        super().__init__(tc=tc)

    def is_logged_in(self):
        account_sub_nav = wa_pages.AccountSubNav(self.tc).navigate()
        return account_sub_nav.btn_log_out.is_visible()


FACTORY_MAP = {
    'US_LARGE_STAGE': HomePageUsLargeStage,
    'US_LARGE_PROD': HomePageUsLargeProd,
    'AU_LARGE_STAGE': HomePageAuLargeStage,
    'JP_LARGE_STAGE': HomePageJapan,
    'JP_LARGE_TEST': HomePageJapan,
    'JP_SMALL_STAGE': HomePageJapanSmall,
    'JP_SMALL_TEST': HomePageJapanSmall
}
