"""
delete_pi.py

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

from core.db.crud import crud_pis as crud
from core.db.schemes import pis as schemas

from core.db.database import SessionLocal
from core.auth.token import api_token_hash, generate_random_token

from config.settings import PATH_TO_API

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
    f"{PATH_TO_API}" + "/delete_pi/",
    response_model=schemas.PI,
    tags=["PI",]
)
def delete_pi(pi: schemas.PIUpdateByID, db: Session = Depends(get_db)):
    pi_id = pi.id
    return crud.delete_pi_by_id(db, id=pi_id)
