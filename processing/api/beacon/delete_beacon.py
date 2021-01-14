"""
delete_beacon.py

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
from core.db.schemes import beacons as schemas
from core.db.database import SessionLocal
from core.auth.token import api_token_hash, generate_random_token

from config.settings import PATH_TO_API, SERVER_URL, PI_SSH_CONNECTION_PROPERTIES, PORT

# router = APIRouter()
#
#
# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
from . import router, get_db


@router.post(
    f"{PATH_TO_API}" + "/delete_beacons_by_date_period/",
    response_model=schemas.Beacon,
    tags=["beacon"]
)
def delete_beacons_by_date_period(t1, t2, db: Session = Depends(get_db)):
    if t1 >= t2:
        return JSONResponse(content=jsonable_encoder({"error": "t1 >= t2"}))
    else:
        # t1 < t2
        beacons = crud.delete_beacons_by_date_period(db, t1, t2)
        return beacons


@router.post(
    f"{PATH_TO_API}" + "/delete_by_product_name/",
    response_model=schemas.Beacon,
    tags=["beacon"]
)
def delete_by_product_name(beacon: schemas.BeaconMultipleFind, db: Session = Depends(get_db)):
    beacons = crud.delete_by_product_name(db, product_name=beacon.product_name)
    return JSONResponse(content=jsonable_encoder(beacons))
