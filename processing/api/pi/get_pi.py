"""
get_pi.py

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
from core.db.crud import crud as crud_multi
from core.db.schemes import pis as schemas
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
    f"{PATH_TO_API}" + "/get_pi_by_name/",
    response_model=schemas.PI,
    tags=["PI",]
)
def get_pi_by_name(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    db_pi = crud.get_pi_by_name(db, name=pi.name,)
    return db_pi


@router.post(
    f"{PATH_TO_API}" + "/get_count_visitors_by_name/",
    response_model=schemas.PI,
    tags=["PI",]
)
def get_count_visitors_by_name(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    db_pi = crud_multi.get_count_visitors_by_name(db, name=pi.name,)
    return db_pi


@router.get(
    f"{PATH_TO_API}" + "/get_pis/",
    response_model=List[schemas.PI],
    tags=["PI",]
)
def get_pis(skip: int = 0, limit: int = 100, active: bool = True, db: Session = Depends(get_db)):
    pis = crud.get_pis(db, skip=skip, limit=limit, active=active)
    return pis


@router.get(
    f"{PATH_TO_API}" + "/get_pis/{pi_id}",
    response_model=schemas.PI,
    tags=["PI",]
)
def get_pi(pi_id: int, active: bool = None, db: Session = Depends(get_db)):
    pi = None
    if active is None:
        pi = crud.get_pi(db, id=pi_id, active = None)
    else:
        pi = crud.get_pi(db, id=pi_id, active=active)
    if pi is None:
        raise HTTPException(status_code=404, detail="PI not found")
    return pi


@router.post(
    f"{PATH_TO_API}" + "/get_pi_data/",
    response_model=schemas.PI,
    tags=["PI",]
)
def get_pi_data(find_scheme: schemas.PIFindBase, db: Session = Depends(get_db)):
    name = find_scheme.name
    uuid = find_scheme.uuid
    active = find_scheme.active
    pi = crud.get_pi_by_name(db, name=name, active=active)
    if pi is None:
        raise HTTPException(status_code=404, detail="PI not found")
    return pi


@router.post(
    f"{PATH_TO_API}" + "/get_locate_data_by_name/",
    response_model=schemas.PI,
    tags=["PI",]
)
def get_locate_data_by_name(pi: schemas.PIUpdate, db: Session = Depends(get_db)):
    name = pi.name
    db_pi = crud.get_pi_by_name(db, name=name,)
    data = db_pi.locate_data
    if data == "json_data":
        return JSONResponse(content=jsonable_encoder({"error": "locate_data has not been updated!"}))
    else:
        locate_data = json.loads(data)
        return JSONResponse(content=jsonable_encoder(locate_data))
