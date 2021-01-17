"""
update.py

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

import json

from fastapi import APIRouter, BackgroundTasks, Response, Request

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.db.crud import crud_users as crud
from core.db.schemes import users as schemas

from core.db.database import SessionLocal
from core.auth.token import api_token_hash, generate_random_token

from config.settings import PATH_TO_API

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    f"{PATH_TO_API}" + "/update_uuids_by_fio/",
    response_model=schemas.User,
    tags=["User", ]
)
def update_uuids_by_fio(user: schemas.UserUpdateAll, db: Session = Depends(get_db)):
    db_user = crud.update_uuids_by_fio(db, user)
    return db_user


@router.post(
    f"{PATH_TO_API}" + "/update_uuid1_by_fio/",
    response_model=schemas.User,
    tags=["User", ]
)
def update_uuid1_by_fio(user: schemas.UserUpdate1, db: Session = Depends(get_db)):
    db_user = crud.update_uuid1_by_fio(db, user)
    return db_user


@router.post(
    f"{PATH_TO_API}" + "/update_uuid2_by_fio/",
    response_model=schemas.User,
    tags=["User", ]
)
def update_uuid2_by_fio(user: schemas.UserUpdate2, db: Session = Depends(get_db)):
    db_user = crud.update_uuid2_by_fio(db, user)
    return db_user


@router.post(
    f"{PATH_TO_API}" + "/update_cv_by_fio/",
    response_model=schemas.User,
    tags=["User", ]
)
def update_cv_by_fio(user: schemas.UserUpdateCV, db: Session = Depends(get_db)):
    db_user = crud.update_cv_by_fio(db, user)
    return db_user


@router.post(
    f"{PATH_TO_API}" + "/activate_by_fio/",
    response_model=schemas.User,
    tags=["User", ]
)
def activate_by_fio(user: schemas.UserUpdateActive, db: Session = Depends(get_db)):
    db_user = crud.activate_by_fio(db, user)
    return db_user


@router.post(
    f"{PATH_TO_API}" + "/deactivate_by_fio/",
    response_model=schemas.User,
    tags=["User", ]
)
def deactivate_by_fio(user: schemas.UserUpdateActive, db: Session = Depends(get_db)):
    db_user = crud.deactivate_by_fio(db, user)
    return db_user


@router.post(
    f"{PATH_TO_API}" + "/increase_cv_by_fio/",
    response_model=schemas.User,
    tags=["User", ]
)
def increase_cv_by_fio(user: schemas.UserUpdateCV, db: Session = Depends(get_db)):
    db_user = crud.increase_cv_by_fio(db, user)
    return db_user
