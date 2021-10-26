from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Tournament(Base):
    __tablename__ = 'tournaments'

    _id = Column(Integer, primary_key=True)
    region = Column(String)
    name = Column(String, unique=True)
    description = Column(String)
    time = Column(Integer)
    prize = Column(Float)
    users = relationship('User', back_populates='tournaments')


class User(Base):
    __tablename__ = 'users'

    _id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    date_of_birth = Column(Integer)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    tournaments = relationship('Tournament', back_populates='users')

