from pydantic import BaseModel, EmailStr
from typing import Optional, List


class Tournament(BaseModel):
    region: Optional[str] = 'international'
    name: str
    description: Optional[str] = None
    game: str = 'cod'
    time: int  # unix
    prize: float
    prize_currency: Optional[str]
    users: str = ''
    creator: str
    platform: Optional[str]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    date_of_birth: int
    password: str


class User(UserBase):
    id: int
    profile_pic: Optional[str]
    is_active: bool
    tournaments: str = ''
    points: int
    tag: Optional[str]
    platform: Optional[str]

    class Config:
        orm_mode = True


class Points(BaseModel):
    points: int


class Friendship(BaseModel):
    id: int
    inviting_friend: str
    accepting_friend: str
    has_been_accepted: Optional[bool] = False
    friendship_start_date: Optional[int] = 0  # unix

    class Config:
        orm_mode = True


class WarzoneUser(BaseModel):
    username: str
    platform: str


class WarzoneStats(BaseModel):
    username: str
    fetched_timestamp: int
    kdRatio: float
    kills: int
    deaths: int
    killsPerGame: float

    class Config:
        orm_mode = True
