"""
crud_admins.py

created by dromakin as 14.01.2021
Project iBeacon_auth
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__copyright__ = "Cybertonica LLC, London, 2021"
__status__ = 'Development'
__version__ = '20210114'

from typing import List, Optional, Dict

from fastapi import HTTPException

from sqlalchemy.orm import Session

from core.db import models
from core.db.schemes import admins as schemas

from core.auth.token import api_token_hash, generate_random_token, is_api_token

from config.environment import DEBUG


# Auth
# sign on
def create_admin(db: Session, user: schemas.AdminCreate):
    hashed_password = api_token_hash(token=user.password)
    login = str(user.login).lower()
    db_user = models.Admin(login=login, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# sign in
def get_admin_by_login_password(db: Session, login: str, hashed_password: str):
    return db.query(models.Admin).filter(
        models.Admin.login == login,
        models.Admin.hashed_password == hashed_password,
    ).first()


# check login in base
def check_admin_by_login(db: Session, login: str, ):
    user = db.query(models.Admin).filter(
        models.Admin.login == login,
    ).first()
    if user is None:
        return False
    return True


# Change password
def update_password(db: Session, login: str, new_password: str, token_update: str):
    if is_api_token(token_update):
        hashed_password = api_token_hash(token=new_password)
        db.query(models.Admin).filter(
            models.Admin.login == login,
        ).update(
            {"hashed_password": hashed_password})
        db.commit()
        return check_admin_by_login(db, login)
    else:
        return False


# HELP & TEST
if DEBUG:
    def get_admin(db: Session, user_id: int):
        return db.query(models.Admin).filter(models.Admin.id == user_id).first()


    def get_admins(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Admin).offset(skip).limit(limit).all()
