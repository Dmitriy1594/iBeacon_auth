"""
pis.py

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


class PIBase(BaseModel):
    name: str
    count_visitors: int = 0
    address: str
    uuid: str
    ip: str
    locate_data: str
    scanning_seconds: float = 5.0
    meters_detection: float = 1.0

    class Config:
        schema_extra = {
            "example": {
                "name": "Product Name",
                "count_visitors": 0,
                "address": "address",
                "uuid": "string",
                "ip": "192.168.31.97",
                "locate_data": "json_data",
                "scanning_seconds": 5.0,
                "meters_detection": 1.0
            }
        }


class PIFindBase(BaseModel):
    name: Optional[str] = "name"
    address: Optional[str] = "address"
    uuid: Optional[str] = "uuid"
    active: Optional[bool] = False
    ip: Optional[str]


class PIUpdate(BaseModel):
    name: Optional[str] = None
    count_visitors: Optional[int] = None
    locate_data: Optional[str] = None
    active: Optional[bool] = False
    # old
    old_name: Optional[str] = None
    old_uuid: Optional[str] = None


class PIUpdateByID(BaseModel):
    id: int
    name: Optional[str] = None
    meters_detection: Optional[float] = 1.0
    scanning_seconds: Optional[float] = 5.0


class PICreate(PIBase):
    pass


class PI(PIBase):
    id: int
    active: bool = False

    class Config:
        orm_mode = True
