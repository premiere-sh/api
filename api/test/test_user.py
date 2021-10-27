import pytest
import time
import json

from api.app import app
from fastapi.testclient import TestClient


client = TestClient(app)

sample_user = {
    'username': 'user1',
    'password': 'secret',
    'date_of_birth': time.time(),
    'email': 'user@gmail.com'
}

@pytest.fixture
def create_entries():
    assert 0


def test_create_user():
    user_json = json.dumps(sample_user)
    response = client.post('/users', json=user_json)
    assert response.status_code == 200
    print(response.json())


def test_read_users():
    response = client.get('/users')
    assert response.status_code == 200
    print(response.json())


def test_read_user():
    response = client.get('/users/1')
    assert response.status_code == 200
    print(response.json())

