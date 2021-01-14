"""
token.py

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

import random
import datetime
import mmh3
from hashlib import sha256

import fastapi

from core.utils import to_epoch

random.seed("Salt_dfdf4395790sd__sdfgjopjrpg" + str(datetime.datetime.now()))


def is_api_token(token: str) -> bool:
    if not token.startswith('PI'):
        return False
    if not token.endswith('TOKEN'):
        return False
    return True


def generate_random_token(length=12 + 2) -> str:
    assert length > 8 + 2

    numbers = '0123456789'

    n0 = numbers[random.randint(0, len(numbers) - 1)]
    n1 = numbers[random.randint(0, len(numbers) - 1)]

    alphabet = numbers + 'aAbBcCdDEeFfGgHhGgKkLlMmNnPpQqRrSsTtXxYyZz'  # not OoIi

    sequence = ''.join(
        alphabet[random.randint(0, len(alphabet) - 1)]
        for i in range(length - 2)
    )

    token = f'PI{n0}{sequence}{n1}TOKEN'

    assert is_api_token(token)
    return token


def api_token_hash(token: str) -> str:
    _salt = 'sdfgj2235_sdnojhois'
    _salt2 = '354_498902sdfkjOLKg'

    hash_ = sha256((token + _salt).encode('utf-8')).hexdigest()
    hash_ = sha256((hash_ + _salt2).encode('utf-8')).hexdigest()

    return hash_.upper()


def get_hashed_password(password: str,):
    hashed_password = api_token_hash(token=password)
    answ = is_api_token(password)
    return answ, hashed_password

