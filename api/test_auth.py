from .setup_client import client
from .sample_user import get_sample_user


def get_auth_headers(client, sample_user_id):
    response = client.post(
        "/token/",
        data={
            "username": get_sample_user(sample_user_id)["username"],
            "password": get_sample_user(sample_user_id)["password"],
        },
    )
    token = response.json()["access_token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    return headers


def test_create_account():
    response = client.post("/users/", json=get_sample_user(3))
    assert response.status_code == 200


def test_login():
    user = get_sample_user(3)
    response = client.post(
        "/token/", data={"username": user["username"], "password": user["password"]}
    )
    response = response.json()
    assert response["access_token"] is not None
    assert response["token_type"] == "bearer"


def test_is_authenticated():
    headers = get_auth_headers(client, sample_user_id=3)
    response = client.get("/is-authenticated/", headers=headers)
    assert response.json()


def test_is_not_authenticated():
    response = client.get("/is-authenticated/")
    assert response.status_code == 401
