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

from fastapi import HTTPException

from sqlalchemy.orm import Session

from core.db import models
from core.db.schemes import beacons as schemas

from core.auth.token import api_token_hash, generate_random_token


# Create
def create_beacon(
        db: Session,
        pi_beacon: schemas.BeaconCreate,
):
    date = pi_beacon.date
    product_name = pi_beacon.product_name
    device_name = pi_beacon.device_name
    uuid = pi_beacon.uuid
    address = pi_beacon.address
    addressType = pi_beacon.addressType
    txPower = pi_beacon.txPower
    rssi = pi_beacon.rssi
    meters = pi_beacon.meters
    db_pi_beacon = models.Beacon(
        date=date,
        product_name=product_name,
        device_name=device_name,
        uuid=uuid,
        address=address,
        addressType=addressType,
        txPower=txPower,
        rssi=rssi,
        meters=meters,
    )
    db.add(db_pi_beacon)
    db.commit()
    db.refresh(db_pi_beacon)
    return db_pi_beacon


# Delete
def delete_pi_by_id(db: Session, id: int,):
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


def delete_beacons_by_date_period(
    db: Session,
    t1: float,
    t2: float,
):
    # get deleted beacons
    beacons = db.query(models.Beacon).filter(
        models.Beacon.date <= t2,
        models.Beacon.date >= t1,
    ).all()
    # delete
    db.query(models.Beacon).filter(
        models.Beacon.date <= t2,
        models.Beacon.date >= t1,
    ).delete()
    db.commit()
    return beacons


def delete_by_product_name(db: Session, product_name: str,):
    # get deleted beacons
    beacons = db.query(models.Beacon).filter(
        models.Beacon.product_name == product_name,
    ).all()
    # delete
    db.query(models.Beacon).filter(
        models.Beacon.product_name == product_name,
    ).delete()
    db.commit()
    return beacons


# Get
def get_beacon_by_device_name(
    db: Session,
    device_name: str,
):
    return db.query(models.Beacon).filter(
        models.Beacon.device_name == device_name,
    ).first()


def get_beacons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Beacon).offset(skip).limit(limit).all()


def get_beacons_by_product_name(db: Session, product_name: str, skip: int = 0, limit: int = 100):
    return db.query(models.Beacon).filter(
        models.Beacon.product_name == product_name,
    ).offset(skip).limit(limit).all()


def get_beacons_by_date_period(
    db: Session,
    t1: float,
    t2: float,
):
    return db.query(models.Beacon).filter(
        models.Beacon.date <= t2,
        models.Beacon.date >= t1,
    ).first()


def get_data_plot_by_product(db: Session, product_name: str,):
    return db.query(models.Beacon).filter(
        models.Beacon.product_name == product_name,
    ).all()

