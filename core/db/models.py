"""
models.py

created by dromakin as 16.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__copyright__ = "Cybertonica LLC, London, 2020"
__status__ = 'Development'
__version__ = '20201116'

import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, JSON, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True,)
    surname = Column(String, index=True,)
    last_name = Column(String, index=True,)
    count_visitors = Column(Integer)
    bluetooth_address_1 = Column(String, index=True,)
    bluetooth_address_2 = Column(String, index=True,)
    uuid_device_1 = Column(String, index=True, unique=True)
    uuid_device_2 = Column(String, index=True, unique=True)
    location = Column(String, index=True,)
    active = Column(Boolean)


class Raspberry(Base):
    __tablename__ = "pi"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    count_visitors = Column(Integer)
    uuid = Column(String, index=True, unique=True)
    address = Column(String, index=True)
    ip = Column(String, index=True, unique=True)
    location = Column(String, index=True, )
    locate_data = Column(String) # the last customer
    active = Column(Boolean)
    scanning_seconds = Column(Float)
    ignore_seconds = Column(Float)
    meters_detection = Column(Float)


class Beacon(Base):
    __tablename__ = "beacon"

    id = Column(Integer, primary_key=True, index=True)
    # https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
    # date = Column(DateTime, default=datetime.datetime.timestamp) #utcnow
    date = Column(Float) #utcnow
    product_name = Column(String, index=True,)
    device_name = Column(String, index=True,)
    uuid = Column(String, index=True,)
    address = Column(String, index=True,)
    addressType = Column(String)
    txPower = Column(Integer)
    rssi = Column(Integer)
    meters = Column(Float)
