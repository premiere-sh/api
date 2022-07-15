import pytest
from .setup_client import client
from .sample_warzone_users import *


def test_get_stats():
    for user in get_users_list():
        response = client.post("/warzone-stats/", json=user)
        assert response.status_code == 200


def test_invalid_platform():

    invalid_user = get_a_user()
    invalid_user["platform"] = "not-a-valid-platform"
    response = client.post("/warzone-stats/", json=invalid_user)
    assert response.status_code == 422


def test_invalid_user():
    invalid_user = get_a_user()
    invalid_user["username"] = "not-a-real-user"
    response = client.post("/warzone-stats/", json=invalid_user)
    assert response.status_code == 404


def test_results_are_cached():
    pass
