"""
beacons.py

created by dromakin as 14.01.2021
Project iBeacon_auth
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__copyright__ = "Cybertonica LLC, London, 2021"
__status__ = 'Development'
__version__ = '20210114'

from typing import List, Optional, Dict

from pydantic import BaseModel


# Beacon
class BeaconBase(BaseModel):
    date: float
    product_name: str
    device_name: str
    uuid: str = "No data"
    address: str
    addressType: str
    txPower: int = -69
    rssi: int
    meters: float

    class Config:
        schema_extra = {
            "example": {
                "date": 1609967007.7562,
                "device_name": "fenix 5x",
                "uuid": [
                    "6a4e3e10-667b-11e3-949a-0800200c9a66"
                ],
                "address": "D0:72:10:EC:BE:64",
                "addressType": "random",
                "txPower": 12,
                "rssi": -66,
                "meters": 0.7405684692262438,
                "product_name": "Product Name"
            }
        }


class Beacon(BeaconBase):
    id: int

    class Config:
        orm_mode = True


class BeaconCreate(BeaconBase):
    pass


class BeaconMultipleFind(BaseModel):
    product_name: Optional[str]
    device_name: Optional[str]
    txPower: Optional[int]
    rssi: Optional[int]
    meters: Optional[float]


#  check beacon in PI db
class BeaconFind(BaseModel):
    date: Optional[float]
    product_name: Optional[str]
    device_name: Optional[str]
    address: Optional[str]
    addressType: Optional[str]
    txPower: Optional[int]
    rssi: Optional[int]
    meters: Optional[float]
