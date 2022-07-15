from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from api import models, schemas
from api.database import get_db
from api.auth import pwd_context


router = APIRouter(tags=["users"])


@router.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
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
    return db_user.id


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/{user_id}/points/")
def update_user_points(
    user_id: int, points: schemas.Points, db: Session = Depends(get_db)
):
    if not points:
        raise HTTPException(status_code=422, detail="Points parameter required")
    # TODO for tournaments can do depends on if current user
    # is authenticated and is current user, see tiangolo
    # for user info can see if is active superuser
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    (db.query(models.User).filter(models.User.id == user_id).update(points.dict()))
    db.commit()
    return True
