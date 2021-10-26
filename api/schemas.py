from pydantic import BaseModel
from typing import Optional, List


class Tournament(BaseModel):
    region: Optional[str]
    name: str
    description: Optional[str]
    time: int  # unix
    prize: float
    users: List[User] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    date_of_birth: str,
    email: str,
    hashed_password: str


class User(UserBase):
    _id: int,
    is_active: bool,
    tournaments: List[Tournament] = []

    class Config:
        orm_mode = True

