from time import time
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import models, schemas
from api.database import get_db
from api.auth import get_current_user


router = APIRouter(tags=['friends'])


@router.get('/users/{user_id}/friends/', response_model=List[schemas.User])
def get_friends(user_id: int, db: Session = Depends(get_db)):
    db_friendships = (
        db.query(models.Friendship)
            .filter( 
                (
                    models.Friendship.inviting_friend == user_id
                    or 
                    models.Friendship.accepting_friend == user_id
                )
                and 
                (
                    models.Friendship.has_been_accepted
                )
            )
            .all()
    )

    def return_friend(friendship):
        if friendship.inviting_friend == user_id:
            return friendship.accepting_friend
        else:
            return friendship.inviting_friend

    friend_ids = [return_friend(friendship) for friendship in db_frienships]

    friends = [
        db.query(models.User).filter(models.User == friend_id).first()
        for friend_id in friends_ids
    ]

    return friends


@router.post('/users/{user_id}/invite/', response_model=[schemas.Friendship])
def send_invite(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_friendship = (
        db.query(models.Friendship)
            .filter( 
                models.Friendship.inviting_friend == current_user._id
                and 
                models.Friendship.accepting_friend == user_id
            )
            .first()
    )
    if db_friendship:
        if db_friendship.has_been_accepted:
            detail = 'Friendship already exists'
            return HTTPException(status_code=400, detail=detail)
        else:
            detail = 'Friendship invitation has been already sent'
            return HTTPException(status_code=400, detail=detail)
    db_friendship = models.Friendship(
        inviting_friend=current_user._id,
        accepting_friend=user_id,
        has_been_accepted=False,
        friendship_start_date=0
    )
    db.add(db_friendship)
    db.commit()
    db.refresh(db_friendship)
    return db_friendship
    

@router.get(
    '/users/{user_id}/invites/', 
    response_model=List[schemas.Friendship],
)
def get_invites(user_id: int, user: schemas.User = Depends(get_current_user)):
    if user_id != user._id:
        return HTTPException(status_code=403, 'User unauthorized')
    db_friendships = (
        db.query(models.Friendship)
            .filter(
                (
                    models.Friendship.inviting_friend != user_id
                    and 
                    models.Friendship.accepting_friend == user_id
                )
            )
            .all()
    )
    return db_friendships


@router.put('/users/{user_id}/invites/')
def accept_invite(
    user_id: int,
    friendship: schemas.Friendship,
    user: schemas.User = Depends(get_current_user)
):
    if user_id != user._id:
        return HTTPException(status_code=403, detail='User unauthorized')
    db_friendship = (
        db.query(models.Friendship)
            .filter(
                models.Friendship.inviting_friend == friendship.inviting_friend
                and 
                models.Friendship.accepting_friend == user_id
            )
            .first()
    )
    if not db_friendship:
        return HTTPException(status_code=404, detail='No such invite')
    (db.query(models.Friendship)
        .filter(models.Friendship._id == db_friendship._id)
        .update(friendship.dict(exclude_unset=True)))
    return True

