"""
basic_auth.py

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from core.db.crud import crud_admins

from sqlalchemy.orm import Session
from core.db.database import SessionLocal

from core.auth.token import api_token_hash


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security),
                        db: Session = Depends(get_db)):
    # if not crud_admins.check_admin_by_login(db=db, login=credentials.username.lower()):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect login or password",
    #         headers={"WWW-Authenticate": "Basic"},
    #     )
    # else:
    hashed_password = api_token_hash(credentials.password)
    admin = crud_admins.get_admin_by_login_password(db=db, login=credentials.username,
                                                    hashed_password=hashed_password)
    if admin is not None:
        return credentials.username
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Basic"},
        )
