import schemas
import models

from sqlalchemy.orm import Session


def get_tournament(db: Session, tournament_id: int):
    return (
        db.query(models.Tournament)
            .filter(models.Tournament.id == tournament_id)
            .first()
    )


def create_tournament(db: Session, tournament: schemas.Tournament):
    db_tournament = models.Tournament(
        region=tournament.region,
        name=tournament.name,
        time=tournament.time,
        prize=tournament.prize
    )
    # todo check how optional works in situation like below
    if tournament.description:
        db_tournament.description = tournament.description
    if tournament.region:
        db_tournament.region = tournament.region
    else:
        db_tournament.region = 'international'
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


def add_tournament_user(db: Session, tournament_id: int):
    pass


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

