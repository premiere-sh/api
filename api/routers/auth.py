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
    create_access_token
)


router = APIRouter(tags=['auth'])


@router.post('/token', response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise IncorrectCredentialsException
    access_token = create_access_token({'username': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}

