from pydantic import BaseModel
from api import models
from sqlalchemy.orm import Session
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


SECRET_KEY = '596b94d317a6acfb2ca9f0ef568dfa55d4f8d1065177d4bfdfe0573f671e5335'
ALGORITHM = 'HS256'
TOKEN_EXPIRY = 480

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(db: Session, username: str, password: str):
    db_user = (
        db.query(models.User)
            .filter(models.User.username == username)
            .first()
    )
    if not db_user:
        return False
    if not pwd_context.verify(password, db_user.hashed_password):
        return False
    return User


def create_access_token(
    data: dict, 
    expires_timedelta: Optional[timedelta] = None
):
    _data = data.copy()
    if expires_timedelta:
        expires = datetime.utcnow() + expires_timedelta
    else:
        expires = datetime.utcnow() + timedelta(minutes=30)
    _data.update({'expires': expires})
    jwt = jwt.encode(_data, SECRET_KEY, algorithm=ALGORITHM)
    return jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('username')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db_user = (
        db.query(models.User)
            .filter(models.User.username == username)
            .first()
    )
    if user is None:
        raise credentials_exception
    if user.disabled:
        raise HTTPException(status_code=400, detail='User inactive.')
    return user

# add Depends(get_current_user) in the api routes

