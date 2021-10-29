from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from api.database import Base


class Tournament(Base):
    __tablename__ = 'tournaments'

    _id = Column(Integer, primary_key=True)
    region = Column(String, default='international')
    name = Column(String, unique=True)
    description = Column(String)
    time = Column(Integer)
    game = Column(String)
    prize = Column(Float)
    users = Column(String, default='')  # comma separated


class User(Base):
    __tablename__ = 'users'

    _id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    date_of_birth = Column(Integer)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    tournaments = Column(String, default='')  # comma separated


class Friendship(Base):
    __tablename__ = 'friendships'

    _id = Column(Integer, primary_key=True)
    inviting_friend = Column(Integer, required=True)
    befriending_friend = Column(Integer, required=True)
    friendship_start_date = Column(Integer)  # unix

