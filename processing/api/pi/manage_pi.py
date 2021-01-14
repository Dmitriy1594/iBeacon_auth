"""
manage_pi.py

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


# settings.json
@router.post(
    f"{PATH_TO_API}" + "/get_settings_pi/",
    response_model=schemas.PIsettings,
    tags=["PI", "manage"]
)
def get_settings_pi(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)
    default_buttons_currency = pi_.currencies
    default_currency = default_buttons_currency[0]
    scanning_seconds = pi_.scanning_seconds
    meters_detection = pi_.meters_detection
    version = str(datetime.datetime.now().timestamp())

    settings_json = {
        "server_url": SERVER_URL + ":" + str(PORT),
        "default_currency": default_currency,
        "default_buttons_currency": default_buttons_currency,
        "scanning_seconds": scanning_seconds,
        "meters_detection": meters_detection,
        "version": version
    }

    return JSONResponse(content=jsonable_encoder(settings_json))


@router.post(
    f"{PATH_TO_API}" + "/deploy_settings_json/",
    response_model=schemas.PIsettings,
    tags=["PI", "manage"]
)
def deploy_settings_json(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)
    default_buttons_currency = pi_.currencies
    default_currency = default_buttons_currency[0]
    scanning_seconds = pi_.scanning_seconds
    meters_detection = pi_.meters_detection
    version = str(datetime.datetime.now().timestamp())

    settings_json = {
        "server_url": SERVER_URL + ":" + str(PORT),
        "default_currency": default_currency,
        "default_buttons_currency": default_buttons_currency,
        "scanning_seconds": scanning_seconds,
        "meters_detection": meters_detection,
        "version": version
    }

    connection_settings = PI_SSH_CONNECTION_PROPERTIES
    connection_settings["host"] = pi_.ip

    # ssh connect to PI
    c = Connection(**connection_settings)

    # deploy settings.json
    command = f"cd ~/Documents/display/settings &&\
                 >settings.json && \
                 echo '{json.dumps(settings_json)}' >settings.json"
    out_str = c.run(command, hide=True).stdout.strip()
    if out_str == "":
        com = "cd ~/Documents/display/settings && cat settings.json"
        out_str = c.run(com, hide=True).stdout.strip()

    info = {
        "data": settings_json,
        "remote_out_str": out_str
    }

    return JSONResponse(content=jsonable_encoder(info))


# turn on program
@router.post(
    f"{PATH_TO_API}" + "/turn_on/",
    response_model=schemas.PIsettings,
    tags=["PI", "manage"]
)
def turn_on(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)

    connection_settings = PI_SSH_CONNECTION_PROPERTIES
    connection_settings["host"] = pi_.ip

    active = pi_.active
    if active == False:
        # ssh connect to PI
        # c = Connection(**connection_settings)
        command = "sudo systemctl start display.service"
        # # remote run program
        # c.run(command, hide=True)

        with Connection(**connection_settings) as c:
            c.run(command)

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


@router.post(
    f"{PATH_TO_API}" + "/update_turn_by_pi/",
    response_model=schemas.PIsettings,
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


# turn off program
@router.post(
    f"{PATH_TO_API}" + "/turn_off/",
    response_model=schemas.PIsettings,
    tags=["PI", "manage"]
)
def turn_off(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)

    connection_settings = PI_SSH_CONNECTION_PROPERTIES
    connection_settings["host"] = pi_.ip

    active = pi_.active
    if active == True:
        # ssh connect to PI
        # c = Connection(**connection_settings)
        # command = "ps aux | grep display.py | awk '{print $2}' | xargs kill -9"
        command = "sudo systemctl stop display.service"
        # out_str = str()
        # remote stop program
        # out_str = c.run(command, hide=True).stdout.strip()

        with Connection(**connection_settings) as c:
            c.run(command)

        info = {
            "info_output": "PI is no active more!"
        }

        # update in DB
        crud.update_pi_active(db, pi.name, False)

        # result
        return JSONResponse(content=jsonable_encoder(info))
    else:
        info = {
            "info_output": "This PI is non-active!",
        }
        return JSONResponse(content=jsonable_encoder(info))


# status
@router.post(
    f"{PATH_TO_API}" + "/status_pi/",
    response_model=schemas.PIFindBase,
    tags=["PI", "manage"]
)
def status_pi(pi: schemas.PIFindBase, db: Session = Depends(get_db)):
    pi_ = crud.get_pi_by_name(db, name=pi.name)

    connection_settings = PI_SSH_CONNECTION_PROPERTIES
    connection_settings["host"] = pi_.ip

    # ssh connect to PI
    # c = Connection(**connection_settings)
    command = "sudo systemctl status display.service"
    out_str = str()
    # remote get status program
    # out_str = c.run(command, hide=True).stdout.strip()

    with Connection(**connection_settings) as c:
        out_str = c.run(command, hide=True).stdout.strip()

    info = {
        "info_output": out_str
    }

    # result
    return JSONResponse(content=jsonable_encoder(info))

