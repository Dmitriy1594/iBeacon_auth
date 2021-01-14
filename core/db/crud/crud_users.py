"""
users.py

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

from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import or_

from core.db import models
from core.db.schemes import users as schemas

from core.auth.token import api_token_hash, generate_random_token


# Create
def create_user(
        db: Session,
        user: schemas.UserCreate,
):
    name = user.name
    surname = user.surname
    last_name = user.last_name
    count_visitors = user.count_visitors
    bluetooth_address_1 = user.bluetooth_address_1
    bluetooth_address_2 = user.bluetooth_address_2
    uuid_device_1 = user.uuid_device_1
    uuid_device_2 = user.uuid_device_2
    location = user.location
    active = False

    db_user = models.Users(
        name=name,
        surname=surname,
        last_name=last_name,
        count_visitors=count_visitors,
        bluetooth_address_1=bluetooth_address_1,
        bluetooth_address_2=bluetooth_address_2,
        uuid_device_1=uuid_device_1,
        uuid_device_2=uuid_device_2,
        active=active,
        location=location,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Delete
def delete_user_by_id(db: Session, id: int, ):
    # get deleted
    info = db.query(models.Users).filter(
        models.Users.id == id,
    ).first()
    # delete
    db.query(models.Users).filter(
        models.Users.id == id,
    ).delete()
    db.commit()
    return info


# Get
def get_user_by_fio(db: Session, f: str, i: str, o: str, active: bool = None):
    if active is not None:
        return db.query(models.Users).filter(
            models.Users.surname == f,
            models.Users.name == i,
            models.Users.last_name == o,
            models.Users.active == active
        ).first()
    else:
        return db.query(models.Users).filter(
            models.Users.surname == f,
            models.Users.name == i,
            models.Users.last_name == o,
        ).first()


def get_user(db: Session, id: int, active: bool = None):
    if active is None:
        return db.query(models.Users).filter(
            models.Users.id == id,
        ).first()
    else:
        return db.query(models.Users).filter(
            models.Users.id == id,
            models.Users.active == active
        ).first()


def get_users(db: Session, skip: int = 0, limit: int = 100, active: bool = True):
    return db.query(models.Users).filter(
        models.Users.active == active,
    ).offset(skip).limit(limit).all()


def get_users_by_location(db: Session, location: str = None, skip: int = 0, limit: int = 100, active: bool = True):
    return db.query(models.Users).filter(
        models.Users.active == active,
        models.Users.location == location,
    ).offset(skip).limit(limit).all()


def get_user_by_uuid(db: Session, uuid: str):
    return db.query(models.Users).filter(
        or_(models.Users.uuid_device_1 == uuid, models.Users.uuid_device_2 == uuid)
    ).first()


def get_first_no_active_user(db: Session):
    return db.query(models.Users).filter(
        models.Users.active == False,
    ).first()


# Update
def update_uuids_by_fio(db: Session, user: schemas.UserUpdateAll,):
    q = db.query(models.Users).filter(
        models.Users.surname == user.surname,
        models.Users.name == user.name,
        models.Users.last_name == user.last_name,
    ).first()
    q.update(
        {
            "bluetooth_address_1": user.bluetooth_address_1,
            "bluetooth_address_2": user.bluetooth_address_2,
            "uuid_device_1": user.uuid_device_1,
            "uuid_device_2": user.uuid_device_2,
        }
    )
    db.commit()
    return get_user_by_fio(db, f=user.surname, i=user.name, o=user.last_name)


def update_uuid1_by_fio(db: Session, user: schemas.UserUpdate1,):
    q = db.query(models.Users).filter(
        models.Users.surname == user.surname,
        models.Users.name == user.name,
        models.Users.last_name == user.last_name,
    ).first()
    q.update(
        {
            "bluetooth_address_1": user.bluetooth_address_1,
            "uuid_device_1": user.uuid_device_1,
        }
    )
    db.commit()
    return get_user_by_fio(db, f=user.surname, i=user.name, o=user.last_name)


def update_uuid2_by_fio(db: Session, user: schemas.UserUpdate2,):
    q = db.query(models.Users).filter(
        models.Users.surname == user.surname,
        models.Users.name == user.name,
        models.Users.last_name == user.last_name,
    ).first()
    q.update(
        {
            "bluetooth_address_1": user.bluetooth_address_2,
            "uuid_device_1": user.uuid_device_2,
        }
    )
    db.commit()
    return get_user_by_fio(db, f=user.surname, i=user.name, o=user.last_name)
