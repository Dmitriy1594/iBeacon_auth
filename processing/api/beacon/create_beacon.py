"""
create_beacon.py

created by dromakin as 14.01.2021
Project iBeacon_auth
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__copyright__ = "Cybertonica LLC, London, 2021"
__status__ = 'Development'
__version__ = '20210114'

from typing import List
import datetime
import json
import random
import colorsys

from fabric import Connection

from fastapi import APIRouter, BackgroundTasks, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.db.crud import crud_beacons as crud
from core.db.crud import crud_pis
from core.db.schemes import beacons as schemas
from core.db.database import SessionLocal
from core.auth.token import api_token_hash, generate_random_token

from config.settings import PATH_TO_API, SERVER_URL, PI_SSH_CONNECTION_PROPERTIES, PORT


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Multi
@router.post(
    f"{PATH_TO_API}" + "/add_beacon/",
    response_model=schemas.Beacon,
    tags=["beacon"]
)
def add_beacon(beacon: schemas.BeaconCreate, db: Session = Depends(get_db)):
    address = beacon.address
    db_pi = crud_pis.get_pi_by_address(db, address=address)
    if db_pi is not None:
        return JSONResponse(content=jsonable_encoder({"error": "This is a PI = )"}))

    db_beacon = crud.get_beacon_by_device_name(db, beacon.device_name)
    if db_beacon is not None:
        raise HTTPException(status_code=404, detail="Device exist!")
    db_beacon = crud.create_beacon(db, pi_beacon=beacon)
    return db_beacon

