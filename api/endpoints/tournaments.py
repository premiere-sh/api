from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import models, schemas
from api.database import get_db
from api.auth import get_current_user


router = APIRouter(tags=['tournaments'])


@router.post( '/tournaments/', response_model=schemas.Tournament)
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


# TODO the schema might differ from the actual model, check this
@router.get('/tournaments/', response_model=List[schemas.Tournament])
def read_tournaments(
    skip: int = 0,
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    tournaments = db.query(models.Tournament).offset(skip).limit(limit).all()
    return tournaments


@router.get('/tournaments/{tournament_id}', response_model=schemas.Tournament)
def read_tournament(tournament_id: int, db: Session = Depends(get_db)):
    db_tournament = (
        db.query(models.Tournament)
            .filter(models.Tournament.id == tournament_id)
            .first()
    )
    if db_tournament is None:
        raise HTTPException(status_code=404, detail='Tournament not found')
    return db_tournament


@router.put('/tournaments/{tournament_id}')
def update_tournament(
    tournament_id: int,
    tournament: schemas.Tournament, 
    db: Session = Depends(get_db)
):
    db_tournament = (
        db.query(models.Tournament)
            .filter(models.Tournament.id == tournament_id)
            .first()
    )
    if db_tournament is None:
        raise HTTPException(status_code=404, detail='Tournament not found')
    (db.query(models.Tournament)
        .filter(models.Tournament.id == tournament_id)
        .update(tournament.dict(exclude_unset=True)))
    db.commit()
    return True

