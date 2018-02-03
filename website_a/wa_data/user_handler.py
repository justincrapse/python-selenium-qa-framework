from copy import deepcopy
import importlib


JUSTIN_PC = 'JUSTIN_COMPUTER'
BRIAN_PC1 = 'BRIAN_COMPUTER1'
TEAMCITY1 = 'TEAMCITY1'
TEAMCITY2 = 'TEAMCITY2'


def update_dict(template, change_dict):
    new_dict = deepcopy(template)
    for key, value in change_dict.items():
        new_dict[key] = value
    return new_dict


def set_user(market_code, computer_name, user_type, env):
    market = market_code.lower()
    users = importlib.import_module(f'website_a.wa_data.user_data.{market}_users').USERS
    user_dict = users[computer_name][user_type]
    return user_dict
