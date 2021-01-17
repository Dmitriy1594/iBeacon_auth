"""
routing.py

created by dromakin as 17.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__copyright__ = "Cybertonica LLC, London, 2020"
__status__ = 'Development'
__version__ = '20201117'

from typing import List
import requests
import json
from urllib.parse import unquote

import fastapi
from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import PlainTextResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from core.db import models
from core.db.crud import crud_pis
from core.db.crud import crud_users

from core.db import schemes

from core.auth.token import is_api_token

from core.db.database import SessionLocal, engine

from config.environment import DEBUG
from config.settings import PATH_TO_API

# security
from core.auth.basic_auth import get_current_username

from processing.api.imports import (
    auth,
    beacon,
    pi,
    users,
)

models.Base.metadata.create_all(bind=engine)

app = fastapi.FastAPI(
    debug=DEBUG,
    title='control-api',
    # description="**Tokens** in headers are provided on request.",
    openapi_url=f'{PATH_TO_API}',
    # openapi_tags=tags_metadata,
    docs_url=None,
    redoc_url=None
)

# http://localhost:40002/

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:40002",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:63342",
    "http://0.0.0.0:5002",
    "http://192.168.31.19:5002"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    beacon.cb.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    beacon.db.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    beacon.gb.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    beacon.ub.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    auth.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    pi.cpi.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    pi.dpi.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    pi.gpi.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    pi.mpi.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    pi.upi.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    users.cuser.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    users.duser.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    users.guser.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)

app.include_router(
    users.upuser.router,
    # dependencies=[fastapi.Depends(check_token_header)],
    responses={
        404: {"description": "Not found"},
    }
    #     422: {'description': 'Validation Error', 'model': ValidationErrorModelResponse}
    # },
)


# OPENAPI
@app.get(path=f'{PATH_TO_API}', tags=["secret"], include_in_schema=False)
async def get_open_api_endpoint():
    return JSONResponse(get_openapi(title="FastAPI", version="2.0.0", routes=app.routes))


# ADMIN PANEL
@app.get(path='/admin', tags=["secret"], include_in_schema=False)
async def get_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url=f'{PATH_TO_API}', title="docs")


# DOCS
@app.get(path='/docs', tags=["help"], include_in_schema=False)
async def get_documentation():
    return get_redoc_html(openapi_url=f'{PATH_TO_API}', title="docs")


@app.get(path='/', tags=["help"], include_in_schema=False)
async def root():
    return RedirectResponse("/auth")


# Rendering html
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")


@app.get(path='/auth', tags=["site", "pages"], include_in_schema=False, response_class=HTMLResponse)
async def auth(request: Request, ):
    # return templates.TemplateResponse("item.html", {"request": request})
    return templates.TemplateResponse("auth/sign-in.html", {"request": request})


@app.get(path='/register', tags=["site", "pages"], include_in_schema=False,
         response_class=HTMLResponse)
async def register(request: Request, ):
    # return templates.TemplateResponse("item.html", {"request": request})
    return templates.TemplateResponse("register/register_boxed.html", {"request": request})


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(path='/menu_pis', tags=["site", "pages"], include_in_schema=False, response_class=HTMLResponse)
async def menu_pis(
    request: Request,
    id: str = None,
    login: str = None,
    # token: str = None,
    db: Session = Depends(get_db)
):
    login_ = unquote(login)

    if id is None or login_ is None: # or token is None or is_api_token(token) == False or len(token) != 9:
        return RedirectResponse("/auth")

    pis_no_active = jsonable_encoder(crud_pis.get_pis(db, skip=0, limit=1000, active=False))
    pis_active = jsonable_encoder(crud_pis.get_pis(db, skip=0, limit=1000, active=True))

    return templates.TemplateResponse(
        "starter-template.html",
        {
            "request": request,
            "id": id,
            "login": login_,
            "pis_no_active": pis_no_active,
            "pis_active": pis_active
        }
    )


@app.get(path='/menu_users', tags=["site", "pages"], include_in_schema=False, response_class=HTMLResponse)
async def menu_users(
    request: Request,
    # site: schemes.site.MenuUsers,
    id_: str = None,
    login: str = None,
    location: str = None,
    # token: str = None,
    db: Session = Depends(get_db)
):
    # location = site.location
    # id_ = site.id
    # login = site.login
    location_ = unquote(location)

    if location is None or id is None or login is None: # or token is None or is_api_token(token) == False or len(token) != 16:
        return RedirectResponse("/auth")

    users_no_active = jsonable_encoder(crud_users.get_users_by_location(db, location=location_, skip=0, limit=1000, active=False))
    users_active = jsonable_encoder(crud_users.get_users_by_location(db, location=location_, skip=0, limit=1000, active=True))

    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "id": id_,
            "location": location_,
            "login": login,
            "users_no_active": users_no_active,
            "users_active": users_active
        }
    )

