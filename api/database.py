from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = 'piotrostr'
password = 'password'
host = 'premiere-dev.c6mfxalyhupg.us-east-2.rds.amazonaws.com'
port = 5432
database_url = f'jdbc:postgresql://{username}:{password}@{host}:{port}/premiere-dev'
# database_url = 'sqlite:///./premiere.db'

engine = create_engine(
    database_url, 
    # connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

