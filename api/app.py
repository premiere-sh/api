from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from schemas import Tournament, User, UserCreate
from database import SessionLocal, engine, get_db
from models import Base
from crud import (
    get_user_by_email,
    get_users,
    get_user,
    get_tournament_by_name,
    create_user,
    create_tournament
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


@app.post('/users/', response_model=User)
def create_tournament(tournament: Tournament, db: Session = Depends(get_db)):
    db_tournament = get_tournament_by_name(db=db, name=tournament.name)
    if db_tournament:
        detail = 'Tournament already exists in the database.'
        raise HTTPException(status_code=400, detail=detail)
    return create_user(db=db, user=user)


@app.get('/users/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db=db, skip=skip, limit=limit)
    return users


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

