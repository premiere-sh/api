from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from api.database import Base


class Tournament(Base):
    __tablename__ = 'tournaments'

    id = Column(Integer, primary_key=True)
    region = Column(String, default='international')
    name = Column(String, unique=True)
    description = Column(String, default=None)
    time = Column(Integer)
    game = Column(String)
    prize = Column(Float)
    prize_currency = Column(String, default='usd')
    users = Column(String, default='')  # comma separated
    creator = Column(String)
    platform = Column(String, default=None)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    profile_pic = Column(String)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    date_of_birth = Column(Integer)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    tournaments = Column(String, default='')  # comma separated
    points = Column(Integer, default=0)
    tag = Column(String, default=None)
    platform = Column(String, default=None)

class WarzoneStats(Base):
    __tablename__='warzoneStats'
    username = Column(String, ForeignKey(User.username), index=True)
    fetched_timestamp = Column(Integer)
    kdRatio = Column(Float)
    kills = Column(Integer)
    deaths = Column(Integer)
    killsPerGame = Column(Float)


class Friendship(Base):
    __tablename__ = 'friendships'

    id = Column(Integer, primary_key=True)
    inviting_friend = Column(String)
    accepting_friend = Column(String)
    has_been_accepted = Column(Boolean, default=False)
    friendship_start_date = Column(Integer, default=0)  # unix

