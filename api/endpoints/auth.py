from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api import models, schemas
from api.database import get_db
from api.auth import (
    IncorrectCredentialsException,
    Token,
    authenticate_user,
    create_access_token,
    get_current_user
)


router = APIRouter(tags=['auth'])


@router.post('/token/', response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise IncorrectCredentialsException
    access_token = create_access_token({'username': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/is-authenticated/', response_model=schemas.User)
def get_current_user(
    current_user: schemas.User = Depends(get_current_user)
):
    return current_user

