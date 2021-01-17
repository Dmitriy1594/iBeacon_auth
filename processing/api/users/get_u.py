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
    f"{PATH_TO_API}" + "/get_user_by_fio/",
    response_model=schemas.User,
    tags=["User", ]
)
def get_user_by_fio(user: schemas.UserFindByFIO, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_fio(db, f=user.surname, i=user.name, o=user.last_name,
                                   active=user.active)
    return db_user


@router.post(
    f"{PATH_TO_API}" + "/get_user/",
    response_model=schemas.User,
    tags=["User", ]
)
def get_user(id: int, active: bool, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, id=id, active=active)
    return db_user


@router.post(
    f"{PATH_TO_API}" + "/get_users/",
    response_model=List[schemas.User],
    tags=["User", ]
)
def get_users(skip: int = 0, limit: int = 100, active: bool = True, db: Session = Depends(get_db)):
    db_users = crud.get_users(db, skip=skip, limit=limit, active=active)
    return db_users


@router.post(
    f"{PATH_TO_API}" + "/get_users_by_location/",
    response_model=List[schemas.User],
    tags=["User", ]
)
def get_users_by_location(location: str = None, skip: int = 0, limit: int = 100, active: bool = True, db: Session = Depends(get_db)):
    db_users = crud.get_users_by_location(db, location=location, skip=skip, limit=limit, active=active)
    return db_users


@router.post(
    f"{PATH_TO_API}" + "/get_user_by_uuid/",
    response_model=schemas.User,
    tags=["User", ]
)
def get_user_by_uuid(user: schemas.UserFindByUUID, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_uuid(db, uuid=user.uuid)
    return db_user
