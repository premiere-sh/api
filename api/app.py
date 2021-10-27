from typing import List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from api.schemas import Tournament, User, UserCreate
from api.database import SessionLocal, engine, get_db
from api.models import Base
from api.crud import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_users,
    create_tournament,
    get_tournament_by_name,
    get_tournament_by_id,
    get_tournaments
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*']
)

Base.metadata.create_all(bind=engine)

@app.post('/users/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return create_user(db=db, user=user)


@app.post('/tournaments/', response_model=User)
def create_tournament(tournament: Tournament, db: Session = Depends(get_db)):
    db_tournament = get_tournament_by_name(db=db, name=tournament.name)
    if db_tournament:
        detail = 'Tournament already exists in the database'
        raise HTTPException(status_code=400, detail=detail)
    return create_tournament(db=db, tournament=tournament)


@app.get('/users/', response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db=db, skip=skip, limit=limit)
    return users


@app.get('/users/{user_id}', response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


# TODO the schema might differ from the actual model, check this
@app.get('/tournaments/', response_model=List[Tournament])
def read_tournaments(
    skip: int = 0,
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    tournaments = get_tournaments(db=db, skip=skip, limit=limit)
    return users


@app.get('/tournaments/{tournament_id}', response_model=Tournament)
def read_tournament(tournament_id: int, db: Session = Depends(get_db)):
    db_tournament = get_tournament_by_id(db=db, tournament_id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail='Tournament not found')
    return db_user

