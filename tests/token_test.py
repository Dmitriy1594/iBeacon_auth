"""
token_test.py

created by dromakin as 30.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201130'

import datetime

from core.auth.token import generate_random_token


def main():
    print(datetime.datetime.now())


if __name__ == "__main__":
    print(generate_random_token())
