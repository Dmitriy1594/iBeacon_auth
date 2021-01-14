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

from fastapi import HTTPException

from sqlalchemy.orm import Session

from core.db import models
from core.db.schemes import pis as schemas

from core.auth.token import api_token_hash, generate_random_token


# Create
def create_pi(
        db: Session,
        pi: schemas.PICreate,
):
    name = pi.name
    count_visitors = pi.count_visitors
    address = pi.address
    uuid = pi.uuid
    locate_data = pi.locate_data
    active = False
    ip = pi.ip
    scanning_seconds = pi.scanning_seconds
    meters_detection = pi.meters_detection

    db_pi = models.Raspberry(
        name=name,
        count_visitors=count_visitors,
        address=address,
        uuid=uuid,
        locate_data=locate_data,
        active=active,
        ip=ip,
        scanning_seconds=scanning_seconds,
        meters_detection=meters_detection,
    )
    db.add(db_pi)
    db.commit()
    db.refresh(db_pi)
    return db_pi


# delete
def delete_pi_by_id(db: Session, id: int, ):
    # get deleted
    info = db.query(models.Raspberry).filter(
        models.Raspberry.id == id,
    ).first()
    # delete
    db.query(models.Raspberry).filter(
        models.Raspberry.id == id,
    ).delete()
    db.commit()
    return info


# Get
def get_pi_by_name(db: Session, name: str, active: bool = None):
    if active is not None:
        return db.query(models.Raspberry).filter(
            models.Raspberry.name == name,
            models.Raspberry.active == active
        ).first()
    else:
        return db.query(models.Raspberry).filter(
            models.Raspberry.name == name,
        ).first()


def get_pi(db: Session, id: int, active: bool):
    if active is None:
        return db.query(models.Raspberry).filter(
            models.Raspberry.id == id,
        ).first()
    else:
        return db.query(models.Raspberry).filter(
            models.Raspberry.id == id,
            models.Raspberry.active == active
        ).first()


def get_pi_by_uuid(db: Session, uuid: str):
    return db.query(models.Raspberry).filter(
        models.Raspberry.uuid == uuid,
    ).first()


def get_first_no_active_pi(db: Session):
    return db.query(models.Raspberry).filter(
        models.Raspberry.active == False,
    ).first()


def get_pis(db: Session, skip: int = 0, limit: int = 100, active: bool = True):
    return db.query(models.Raspberry).filter(
        models.Raspberry.active == active
    ).offset(skip).limit(limit).all()


def get_pi_by_address(
        db: Session,
        address: str,
):
    return db.query(models.Raspberry).filter(
        models.Raspberry.address == address,
    ).first()


# Update
def update_all(
        db: Session,
        name: str,
        count_visitors: int,
        uuid: str,
        locate_data: str,
        old_name: str,
        old_uuid: str,
):
    q = None
    if old_uuid is not None:
        q = db.query(models.Raspberry).filter(
            models.Raspberry.name == old_name,
            models.Raspberry.uuid == old_uuid,
        )
    else:
        q = db.query(models.Raspberry).filter(
            models.Raspberry.name == old_name,
        )

    q.update(
        {
            "name": name,
            "count_visitors": count_visitors,
            "uuid": uuid,
            "locate_data": locate_data,
        }
    )
    db.commit()
    return get_pi_by_name(db, name)


def update_pi_by_id(
        db: Session,
        name: str = None,
        pi_id: int = None,
        meters_detection: float = 1.0,
        scanning_seconds: float = 5.0,
):
    if name is not None:
        db.query(models.Raspberry).filter(
            models.Raspberry.id == pi_id,
        ).update(
            {
                "name": name,
                "meters_detection": meters_detection,
                "scanning_seconds": scanning_seconds,
            }
        )
    db.commit()
    return get_pi_by_name(db, name)


def update_pi_name_and_or_uuid(
        db: Session,
        name: str,
        uuid: str,
        old_name: str,
        old_uuid: str
):
    if old_name is not None or old_uuid is not None:
        if name is not None and uuid is not None:
            db.query(models.Raspberry).filter(
                models.Raspberry.name == old_name,
                models.Raspberry.uuid == old_uuid,
            ).update(
                {
                    "uuid": uuid,
                    "name": name
                }
            )
            db.commit()
            return get_pi_by_name(db, name)
        elif name is not None:
            db.query(models.Raspberry).filter(
                models.Raspberry.name == old_name,
            ).update(
                {
                    "name": name
                }
            )
            db.commit()
            return get_pi_by_name(db, name)
        elif uuid is not None:
            db.query(models.Raspberry).filter(
                models.Raspberry.uuid == old_uuid,
            ).update(
                {
                    "uuid": uuid
                }
            )
            db.commit()
            return get_pi_by_name(db, name)
        else:
            raise HTTPException(status_code=404,
                                detail="PI didn't update. Fields problem: uuid or name.")
    else:
        raise HTTPException(status_code=404,
                            detail="PI didn't update. Fields problem: old_name or old_uuid.")


def update_pi_locate_data(
        db: Session,
        name: str,
        locate_data: str
):
    db.query(models.Raspberry).filter(
        models.Raspberry.name == name,
    ).update(
        {
            "locate_data": locate_data,
        }
    )
    db.commit()
    db_pi = get_pi_by_name(db, name)
    return db_pi


def update_pi_active(
        db: Session,
        name: str,
        active: bool
):
    db.query(models.Raspberry).filter(
        models.Raspberry.name == name,
    ).update(
        {
            "active": active,
        }
    )
    db.commit()
    db_pi = get_pi_by_name(db, name)
    return db_pi


def update_count_visitors(db: Session, name: str, count_visitors: int):
    db.query(models.Raspberry).filter(
        models.Raspberry.name == name,
    ).update(
        {
            "count_visitors": count_visitors,
        }
    )
    db.commit()
    db_pi = get_pi_by_name(db, name)
    return db_pi
