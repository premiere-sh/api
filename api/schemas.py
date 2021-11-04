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
    email: EmailStr


class UserCreate(UserBase):
    date_of_birth: int
    password: str


class User(UserBase):
    _id: int
    is_active: bool
    tournaments: str = ''
    points: int

    class Config:
        orm_mode = True


class Points(BaseModel):
    points: int


class Friendship(BaseModel):
    _id: int
    inviting_friend: str
    accepting_friend: str
    has_been_accepted: Optional[bool] = False
    friendship_start_date: Optional[int] = 0 # unix

    class Config:
        orm_mode = True

