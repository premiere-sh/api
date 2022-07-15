from .setup_client import client
from .sample_user import (
    sample_user,
    sample_user_with_points,
)
from .setup_client import Base, engine


def test_create_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.post("/users/", json=sample_user)
    assert response.status_code == 200


def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200


def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200


def test_update_user_points():
    sample_user_with_points["username"] = "user124"
    in_db = (client.get("/users/1")).json()
    before = in_db["points"]
    assert before == 0
    was_updated = client.put("/users/1/points/", json=sample_user_with_points)
    assert was_updated.json()
    updated = (client.get("/users/1")).json()
    assert updated["points"] == sample_user_with_points["points"]


def test_update_password():
    pass


def test_delete_user():
    pass
