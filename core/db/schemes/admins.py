"""
admins.py

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


class AdminBase(BaseModel):
    login: str


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(AdminBase):
    token_update: str
    new_password: str


class Admin(AdminBase):
    id: int

    class Config:
        orm_mode = True
