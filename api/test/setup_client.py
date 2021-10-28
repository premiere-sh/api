from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.app import app, get_db
from fastapi.testclient import TestClient
from api.database import Base


engine = create_engine(
    "sqlite:///./test.db", 
	connect_args={"check_same_thread": False}
)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(
	autocommit=False, 
	autoflush=False, 
	bind=engine
)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

