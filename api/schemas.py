from pydantic import BaseModel
from typing import Optional, List


class Tournament(BaseModel):
    region: Optional[str] = None
    name: str
    description: Optional[str] = None
    time: int  # unix
    prize: float
    users: List[int] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    date_of_birth: str
    email: str
    password: str


class User(UserBase):
    _id: int
    is_active: bool
    tournaments: List[int] = []

    class Config:
        orm_mode = True

