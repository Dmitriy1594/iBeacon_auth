"""
get_pi.py

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

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

from core.db.database import SessionLocal
from core.auth.token import api_token_hash, generate_random_token

from config.settings import PATH_TO_API

router = APIRouter()
