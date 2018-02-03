from website_a.wa_data.credit_cards import CREDIT_CARDS
from website_a.wa_data.user_handler import JUSTIN_PC, TEAMCITY1, TEAMCITY2
from website_a.wa_data.user_handler import update_dict

current_password = 'SuperSonic1234'

justin = {
            'FIRST_NAME': 'Justin',
            'LAST_NAME': 'Time',
            'USER_NAME': 'justintime',
            'EMAIL': 'justintime1@krk.com',
            'PASSWORD': current_password,
            'PHONE': '9999999999',
            'DOB': '1999-9-9',
            'REFERRAL_CODE': 'ASH',
            'ADDRESS1': '8810 Ida Lane',
            'ADDRESS2': '',
            'CITY': 'Sandy',
            'STATE': 'Utah',
            'ZIP': '84093',
            'SSN': '382938473',
            'CC1': CREDIT_CARDS['BILL'],
            'CC2': CREDIT_CARDS['SLIM']
}

USERS = {
    JUSTIN_PC: {
        'MC': justin,
    },
    TEAMCITY1: {
        'MC': update_dict(justin, {
            'FIRST_NAME': 'Jet',
            'LAST_NAME': 'Brains',
            'EMAIL': 'teamcity1@jetbrains.com'}),
        'EXTRA': update_dict(justin, {
            'FIRST_NAME': 'Extra Jet',
            'LAST_NAME': 'Extra Brains',
            'EMAIL': 'teamcity_extra1@jetbrains.com'}),
    },
    TEAMCITY2: {
        'MC': update_dict(justin, {
            'FIRST_NAME': 'Jet2',
            'LAST_NAME': 'Brains2',
            'EMAIL': 'teamcity22@jetbrains.com'}),
        'EXTRA': update_dict(justin, {
            'FIRST_NAME': 'Extra Jet2',
            'LAST_NAME': 'Extra Brains2',
            'EMAIL': 'teamcity_extra22@jetbrains.com'}),
    }
}
