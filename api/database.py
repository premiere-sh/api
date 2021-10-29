from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = 'admin'
password = 'Borowki123'
host = 'premiere.c6mfxalyhupg.us-east-2.rds.amazonaws.com'
port = 3306
database_url = f'mariadb+pymysql://{username}:{password}@{host}/premiere'
database_url += '?charset=utf8mb4'
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

