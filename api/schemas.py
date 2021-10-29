from pydantic import BaseModel, EmailStr
from typing import Optional, List


class Tournament(BaseModel):
    region: Optional[str] = None
    name: str
    description: Optional[str] = None
    game: Optional[str] = 'cod'
    time: int  # unix
    prize: float
    users: str = ''

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    date_of_birth: int
    email: EmailStr
    password: str


class User(UserBase):
    _id: int
    is_active: bool
    tournaments: str = ''

    class Config:
        orm_mode = True


class Friendship(BaseModel):
    _id: int
    inviting_friend: int
    befriending_friend: int
    friendship_start_date: int  # unix

    class Config:
        orm_mode = True

