from time import time
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from api import models, schemas
from api.database import get_db
from api.auth import get_current_user, verify_is_authorized

router = APIRouter(tags=['friends'])


def return_friend(friendship: models.Friendship, user: schemas.User):
    if friendship.inviting_friend == user.username:
        return friendship.accepting_friend
    else:
        return friendship.inviting_friend


@router.get('/users/{user_id}/friends/', response_model=List[schemas.User])
def get_friends(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db_friendships = (
        db.query(models.Friendship)
            .filter(
                or_(
                    models.Friendship.inviting_friend == user.username,
                    models.Friendship.accepting_friend == user.username
                )
            )
            .filter(models.Friendship.has_been_accepted)
            .all()
    )

    friend_usernames = [
        return_friend(friendship, user) 
        for friendship in db_friendships
    ]

    friends = [
        (db.query(models.User)
                .filter(models.User.username == username)
                .first()
        ) for username in friend_usernames
    ]

    return friends


@router.post('/users/{inviting_user_id}/friends/invite/{user_id}/', response_model=schemas.Friendship)
def send_invite(
    inviting_user_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    current_user_db = verify_is_authorized(db, inviting_user_id, current_user)
    accepting_user = (
        db.query(models.User)
            .filter(models.User.id == user_id)
            .first()
    )
    if not accepting_user:
        detail = f'User with id {user_id} does not exist'
        raise HTTPException(status_code=400, detail=detail)
    db_friendship = (
        db.query(models.Friendship)
            .filter( 
                models.Friendship.inviting_friend == current_user_db.username
                and
                models.Friendship.accepting_friend == accepting_user.username
            )
            .first()
    )
    if db_friendship:
        if db_friendship.has_been_accepted:
            detail = 'Friendship already exists'
            raise HTTPException(status_code=400, detail=detail)
        else:
            detail = 'Friendship invitation has been already sent'
            raise HTTPException(status_code=400, detail=detail)
    db_friendship = models.Friendship(
        inviting_friend=current_user_db.username,
        accepting_friend=accepting_user.username,
        has_been_accepted=False,
        friendship_start_date=0
    )
    db.add(db_friendship)
    db.commit()
    db.refresh(db_friendship)
    return db_friendship

    
@router.get(
    '/users/{user_id}/invites/', 
     response_model=List[schemas.Friendship]
)
def get_invites(
    user_id: int, 
    user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user_db = verify_is_authorized(db, user_id, user)
    db_friendships = (
        db.query(models.Friendship)
            .filter(
                models.Friendship.accepting_friend == current_user_db.username
            )
            .all()
    )
    db_friendships = [f for f in db_friendships if not f.has_been_accepted]
    return db_friendships


@router.put('/users/{user_id}/friends/invites/accept/')
def accept_invite(
    user_id: int,
    friendship: schemas.Friendship,
    user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user_db = (
        db.query(models.User)
            .filter(models.User.username == user.username)
            .first()
    )
    if user_id != current_user_db.id:
        raise HTTPException(status_code=403, detail='User unauthorized')
    if friendship.accepting_friend != current_user_db.username:
        raise HTTPException(status_code=403, detail='User unauthorized')
    db_query = (
        db.query(models.Friendship)
            .filter(
                (
                    models.Friendship.inviting_friend == friendship.inviting_friend
                    and 
                    models.Friendship.accepting_friend == user.username
                )
                and 
                not models.Friendship.has_been_accepted
            )
    )
    db_friendship = db_query.first()
    if not db_friendship:
        detail = 'No such invite, or invite has already been accepted'
        raise HTTPException(status_code=404, detail=detail)
    db_query.update(friendship.dict())
    db.commit()
    return True


@router.post('/users/{user_id}/friends/invites/delete/')
def accept_invite(
    user_id: int,
    friendship: schemas.Friendship,
    user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user_db = verify_is_authorized(db, user_id, user)
    if friendship.accepting_friend != current_user_db.username:
        raise HTTPException(status_code=403, detail='User unauthorized')
    db_query = (
        db.query(models.Friendship)
            .filter(
                (
                    models.Friendship.inviting_friend == friendship.inviting_friend
                    and 
                    models.Friendship.accepting_friend == current_user_db.username
                )
                and 
                not models.Friendship.has_been_accepted
            )
    )
    db_friendship = db_query.first()
    if not db_friendship:
        detail = 'No such invite or invite has already been accepted'
        raise HTTPException(status_code=404, detail=detail)
    db_query.delete()
    db.commit()
    return True


@router.post('/users/{user_id}/friends/{username}/delete/')
def unfriend(
    user_id: int,
    username: str,
    user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_is_authorized(db, user_id, user)
    db_query = (
        db.query(models.Friendship)
            .filter(
                (
                    models.Friendship.inviting_friend == user.username
                    or 
                    models.Friendship.accepting_friend == user.username
                )
                and models.Friendship.has_been_accepted
            )
    )
    friendship_db = db_query.first()
    if not friendship_db:
        raise HTTPException(status_code=400, detail='No such friendship')
    db_query.delete()
    db.commit()
    return True

