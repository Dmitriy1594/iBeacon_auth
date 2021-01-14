"""
auth.py

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

from typing import List

from fastapi import APIRouter, BackgroundTasks, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.db.crud import crud_admins as crud
from core.db.schemes import admins as schemas

from core.db.database import SessionLocal
from core.auth.token import api_token_hash, generate_random_token, is_api_token

from config.settings import PATH_TO_API
from config.environment import DEBUG

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Sign
# Sign on
@router.post(
    f"{PATH_TO_API}" + "/sign_on/",
    response_model=schemas.Admin,
    tags=["admin", ]
)
def sign_on(user: schemas.AdminCreate, db: Session = Depends(get_db)):
    if crud.check_admin_by_login(db, login=user.login):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_admin(db=db, user=user, )


# Sign in
@router.post(
    f"{PATH_TO_API}" + "/sign_in/",
    response_model=schemas.Admin,
    tags=["admin", ]
)
def sign_in(auth_model: schemas.AdminCreate, db: Session = Depends(get_db)):
    login = auth_model.login
    password = auth_model.password
    hash_password = api_token_hash(password)

    db_user = crud.get_admin_by_login_password(db, login=login, hashed_password=hash_password)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Please sign up!")

    return db_user


# Forget password
@router.post(
    f"{PATH_TO_API}" + "/change_password/",
    response_model=schemas.Admin,
    tags=["admin", ]
)
def change_password(auth_model: schemas.AdminUpdate, db: Session = Depends(get_db)):
    login = auth_model.login
    if crud.check_admin_by_login(db, login):
        token_update = auth_model.token_update
        if len(token_update) != 20:
            raise HTTPException(status_code=400, detail="Please token_update!")

        new_password = auth_model.new_password
        if crud.update_password(db, login=login, new_password=new_password, token_update=token_update):
            return JSONResponse(content=jsonable_encoder({"info": "password updated!"}))
        else:
            return JSONResponse(
                content=jsonable_encoder({"info": "Change token_update!"}))
    else:
        raise HTTPException(status_code=400, detail="Please change login!")


# Token create
@router.get(
    f"{PATH_TO_API}" + "/get_example_password/",
    tags=["admin"]
)
def get_example_password(length: int):
    data = {
        "example_password": generate_random_token(length=length)
    }
    return JSONResponse(content=jsonable_encoder(data))


# HELP & TEST
if DEBUG:

    @router.get(
        f"{PATH_TO_API}" + "/admins/",
        response_model=List[schemas.Admin],
        tags=["help", "test"]
    )
    def read_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        users = crud.get_admins(db, skip=skip, limit=limit)
        return users


    @router.get(
        f"{PATH_TO_API}" + "/admins/{admin_id}",
        response_model=schemas.Admin,
        tags=["help", "test"]
    )
    def read_admin(user_id: int, db: Session = Depends(get_db)):
        db_user = crud.get_admin(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="Admin not found")
        return db_user
