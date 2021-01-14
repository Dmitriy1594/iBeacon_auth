"""
users.py

created by dromakin as 14.01.2021
Project iBeacon_auth
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__copyright__ = "Cybertonica LLC, London, 2020"
__status__ = 'Development'
__version__ = '20210114'

from typing import List, Optional, Dict

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    surname: str
    last_name: str
    count_visitors: int = 0
    bluetooth_address_1: str
    bluetooth_address_2: str
    uuid_device_1: str
    uuid_device_2: str
    location: str


class UserCreate(UserBase):
    pass


class UserUpdateAll(BaseModel):
    name: str
    surname: str
    last_name: str
    bluetooth_address_1: str
    bluetooth_address_2: str
    uuid_device_1: str
    uuid_device_2: str


class UserUpdate1(BaseModel):
    name: str
    surname: str
    last_name: str
    bluetooth_address_1: str
    uuid_device_1: str


class UserUpdate2(BaseModel):
    name: str
    surname: str
    last_name: str
    bluetooth_address_2: str
    uuid_device_2: str


class UserFindByFIO(BaseModel):
    location: str
    active: Optional[bool] = False


class UserFindByLocation(BaseModel):
    name: str
    surname: str
    last_name: str
    active: Optional[bool] = False


class UserDelete(BaseModel):
    id: int


class User(UserBase):
    id: int
    active: bool = False

    class Config:
        orm_mode = True
