"""
display.py

created by dromakin as 01.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201101'

import datetime
import sys
import os
import requests
import time
import json
import asyncio

from PIL import Image, ImageDraw, ImageFont
from lib.waveshare_epd import epd2in7

# Beacon
from beacon_module import beacon
from settings import get_settings

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
settingsDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings')

SETTINGS = get_settings()
SERVER_URL = SETTINGS["server_url"]


class DisplayManager:

    def __init__(self, ) -> None:
        # 264×176
        self.epd = epd2in7.EPD()  # get the display object and assing to epd
        self.epd.init()  # initialize the display
        self.epd.Clear(0xFF)

        self.location = SETTINGS['location']
        super().__init__()

    def clear_display(self):
        self.epd.init()
        self.epd.Clear(0xFF)

    @staticmethod
    def deactivate_by_fio(f, i, o):
        url_method = "/v1/deactivate_by_fio"

        payload = json.dumps(
            {
                "name": i,
                "surname": f,
                "last_name": o,
            }
        )
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST",
            "http://" + SERVER_URL + url_method,
            headers=headers,
            data=payload
        )

        if response.status_code == 200:
            res_json = response.json()
            return res_json

        return None

    @staticmethod
    def activate_by_fio(f, i, o):
        url_method = "/v1/activate_by_fio"

        payload = json.dumps(
            {
                "name": i,
                "surname": f,
                "last_name": o,
            }
        )
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST",
            "http://" + SERVER_URL + url_method,
            headers=headers,
            data=payload
        )

        if response.status_code == 200:
            res_json = response.json()
            return res_json

        return None

    @staticmethod
    def increase_cv_by_fio(f, i, o):
        url_method = "/v1/increase_cv_by_fio"

        payload = json.dumps(
            {
                "name": i,
                "surname": f,
                "last_name": o,
            }
        )
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST",
            "http://" + SERVER_URL + url_method,
            headers=headers,
            data=payload
        )

        if response.status_code == 200:
            res_json = response.json()
            return res_json

        return None

    def update_on_start(self):
        url_method = "/v1/update_turn_by_pi"

        payload = json.dumps({"name": SETTINGS['name']})
        headers = {
            'Content-Type': 'application/json'
        }

        requests.request("POST", "http://" + SERVER_URL + url_method, headers=headers, data=payload)
        # response = requests.request("POST", "http://" + SERVER_URL + url_method, headers=headers, data=payload)
        # print(response.text)

    @staticmethod
    def check_user_by_uuid(uuid: str = None):
        if uuid is None or uuid == 'No data':
            return None
        elif uuid != 'No data':
            url_method = "/v1/get_user_by_uuid"

            payload = json.dumps({"uuid": uuid})
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request(
                "POST",
                "http://" + SERVER_URL + url_method,
                headers=headers,
                data=payload
            )

            if response.status_code == 200:
                res_json = response.json()
                return res_json

            return None

    def printToDisplay(self, msg: str = "Authorized!", fio: str = str()):
        image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        # font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

        # print product and price
        draw.text((72, 45), msg, font=font, fill=0)
        draw.line((0, 88, 264, 88), fill=0)
        draw.text((50, 120), fio, font=font, fill=0)

        self.epd.display(self.epd.getbuffer(image))


def test():
    d = DisplayManager()
    # d.update_on_start()
    d.printToDisplay(fio="Иванов И. В.")


def find_device_asyncio(dispay_manager: DisplayManager) -> bool:
    loop = asyncio.get_event_loop()
    visitors, find_flag = loop.run_until_complete(beacon.find_device())

    for visitor in visitors:
        user = dispay_manager.check_user_by_uuid(visitor.get("uuid"))
        if user is not None:
            fio = f"{user['surname']} {user['name'][0]}.{user['last_name'][0]}."
            # pi dashboard
            beacon.increase_count_visitors()
            # user cv update
            dispay_manager.increase_cv_by_fio(
                i=user['name'],
                f=user['surname'],
                o=user['last_name'],
            )
            # update site
            if user.get("active") == True:
                dispay_manager.printToDisplay(msg="Bye!", fio=fio)
                time.sleep(SETTINGS["ignore_seconds"])
                dispay_manager.clear_display()

                dispay_manager.deactivate_by_fio(
                    i=user['name'],
                    f=user['surname'],
                    o=user['last_name'],
                )
            else:
                dispay_manager.printToDisplay(msg="Hello!", fio=fio)
                time.sleep(SETTINGS["ignore_seconds"])
                dispay_manager.clear_display()

                dispay_manager.activate_by_fio(
                    i=user['name'],
                    f=user['surname'],
                    o=user['last_name'],
                )

        else:
            continue

    return find_flag


def main():
    d = DisplayManager()
    d.update_on_start()

    while find_device_asyncio(dispay_manager=d):
        pass


if __name__ == '__main__':
    # test()
    main()
