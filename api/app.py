from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from api import models, schemas
from api.database import SessionLocal, engine, get_db
from api.auth import (
    IncorrectCredentialsException,
    Token,
    authenticate_user,
    create_access_token,
    get_current_user,
    pwd_context
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*']
)

models.Base.metadata.create_all(bind=engine)


@app.get('/')
def docs_redirect():
    return RedirectResponse(url='/docs')


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = (
        db.query(models.User)
            .filter(models.User.email == user.email)
            .first()
    )
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        date_of_birth=user.date_of_birth,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post('/token', response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise IncorrectCredentialsException
    access_token = create_access_token({'username': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.post('/tournaments/', response_model=schemas.Tournament)
def create_tournament(
    tournament: schemas.Tournament, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_tournament = (
        db.query(models.Tournament)
            .filter(models.Tournament.name == tournament.name)
            .first()
    )
    if db_tournament:
        detail = 'Tournament already exists in the database'
        raise HTTPException(status_code=400, detail=detail)
    db_tournament = models.Tournament(
        region=tournament.region,
        name=tournament.name,
        description=tournament.description,
        time=tournament.time,
        prize=tournament.prize,
    )
    # TODO check how optional works in situation like below
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


@app.get('/users/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User._id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


# TODO the schema might differ from the actual model, check this
@app.get('/tournaments/', response_model=List[schemas.Tournament])
def read_tournaments(
    skip: int = 0,
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    tournaments = db.query(models.Tournament).offset(skip).limit(limit).all()
    return tournaments


@app.get('/tournaments/{tournament_id}', response_model=schemas.Tournament)
def read_tournament(tournament_id: int, db: Session = Depends(get_db)):
    db_tournament = (
        db.query(models.Tournament)
            .filter(models.Tournament._id == tournament_id)
            .first()
    )
    if db_tournament is None:
        raise HTTPException(status_code=404, detail='Tournament not found')
    return db_tournament

