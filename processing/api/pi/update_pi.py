"""
update_pi.py

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

from core.db.crud import crud_pis as crud
from core.db.schemes import pis as schemas
from core.db.database import SessionLocal
from core.auth.token import api_token_hash, generate_random_token

from config.settings import PATH_TO_API, SERVER_URL, PI_SSH_CONNECTION_PROPERTIES, PORT

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    f"{PATH_TO_API}" + "/update_pi/",
    response_model=schemas.PI,
    tags=["PI", ]
)
def update_pi(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    count_visitors = pi.count_visitors
    uuid = pi.uuid
    locate_data = pi.locate_data
    # old
    old_name = pi.old_name
    old_uuid = pi.old_uuid

    # update all
    if name is not None and \
            count_visitors is not None and \
            uuid is not None and \
            locate_data is not None and \
            old_name is not None and \
            old_uuid is not None:

        pi_ = crud.update_all(
            db,
            name,
            count_visitors,
            uuid,
            locate_data,
            old_name,
            old_uuid
        )

        if pi_ is None:
            raise HTTPException(status_code=404, detail="PI didn't update. New PI didn't find.")
        return pi_
    else:
        raise HTTPException(status_code=404, detail="PI didn't update. Field problem.")


@router.post(
    f"{PATH_TO_API}" + "/update_by_id/",
    response_model=schemas.PI,
    tags=["PI", ]
)
def update_by_id(pi: schemas.PIUpdateByID, db: Session = Depends(get_db)):
    pi_id = pi.id
    name = pi.name
    meters_detection = pi.meters_detection
    ignore_seconds = pi.ignore_seconds
    scanning_seconds = pi.scanning_seconds
    return crud.update_pi_by_id(db, name, pi_id, meters_detection, ignore_seconds, scanning_seconds)


@router.post(
    f"{PATH_TO_API}" + "/update_name_and_uuid/",
    response_model=schemas.PI,
    tags=["PI", ]
)
def update_name_and_uuid(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    uuid = pi.uuid
    # old
    old_name = pi.old_name
    old_uuid = pi.old_uuid
    return crud.update_pi_name_and_or_uuid(db, name, uuid, old_name, old_uuid)


@router.post(
    f"{PATH_TO_API}" + "/increase_count_visitors/",
    response_model=schemas.PI,
    tags=["PI", ]
)
def increase_count_visitors(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    db_pi = crud.get_pi_by_name(db, name=name, )
    if db_pi is not None:
        count_visitors = db_pi.count_visitors + 1
        return crud.update_count_visitors(db, name, count_visitors)
    else:
        return JSONResponse(
            content=jsonable_encoder({"error": "Can't update count visitors. pi not found."}))


@router.post(
    f"{PATH_TO_API}" + "/set_null_count_visitors/",
    response_model=schemas.PI,
    tags=["PI", ]
)
def set_null_count_visitors(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    db_pi = crud.get_pi_by_name(db, name=name, )
    if db_pi is not None:
        count_visitors = 0
        return crud.update_count_visitors(db, name, count_visitors)
    else:
        return JSONResponse(
            content=jsonable_encoder({"error": "Can't update count visitors. pi not found."}))


@router.post(
    f"{PATH_TO_API}" + "/update_locate_data_by_name/",
    response_model=schemas.PI,
    tags=["PI", ]
)
def update_locate_data_by_name(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    locate_data_ = pi.locate_data
    locate_data = json.loads(locate_data_)
    # uuid_ = locate_data["uuid"]
    # uuid = None
    # if len(uuid_) > 0:
    #     uuid = uuid_[0]
    # db_pi = crud.get_pi_by_uuid(db, uuid)
    # if db_pi is not None:
    #     return JSONResponse(content=jsonable_encoder({"error": "This is a PI = )"}))

    db_pi = crud.get_pi_by_address(db, address=locate_data["address"])
    if db_pi is not None:
        return JSONResponse(content=jsonable_encoder({"error": "This is a PI = )"}))

    return crud.update_pi_locate_data(db, name, locate_data_)


@router.post(
    f"{PATH_TO_API}" + "/update_activate_by_name/",
    response_model=schemas.PI,
    tags=["PI", ]
)
def update_activate_by_name(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    name = pi.name
    active = pi.active
    return crud.update_pi_active(db, name, active)


@router.post(
    f"{PATH_TO_API}" + "/update_turn_by_pi/",
    # response_model=schemas.PIsettings,
    tags=["PI", ]
)
def update_turn_by_pi(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)
    active = pi_.active
    if active == False:
        info = {
            "info_output": "Program is running!"
        }

        # update in DB
        crud.update_pi_active(db, pi.name, True)

        # result
        return JSONResponse(content=jsonable_encoder(info))
    else:
        info = {
            "info_output": "This PI is active!",
        }
        return JSONResponse(content=jsonable_encoder(info))
