import pytest
import time
import json

from api.app import app
from fastapi.testclient import TestClient


client = TestClient(app)

@pytest.fixture(scope='module')
def user_json():
    with open('sample_user.json', 'r') as f:
        user_json = f.read()
    return user_json


def test_create_user(user_json):
    response = client.post('/users', json=user_json)
    assert response.status_code == 200


def test_read_users():
    response = client.get('/users/')
    assert response.status_code == 200


def test_read_user():
    response = client.get('/users/1')
    assert response.status_code == 200

