import sys
from configparser import ConfigParser
from logging import config


config_parser = ConfigParser()
config_parser.read('config_active.ini')

class Constants:
    def __init__(self) -> None:
        pass

_const = Constants()

_const.telegram_token = config_parser.get('Telegram', 'acces_token')
_const.google_key = config_parser.get('Google', 'dev_key')


sys.modules[__name__] = _const
