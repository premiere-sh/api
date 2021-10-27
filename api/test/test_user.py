import pytest
import time
import json
import os

from api.app import app
from fastapi.testclient import TestClient


client = TestClient(app)

@pytest.fixture(scope='module')
def sample_user():
    return {
      'username': 'user1',
      'password': 'secret',
      'date_of_birth': 1635353891,
      'email': 'user@gmail.com'
    }


def test_create_user(sample_user):
    response = client.post('/users/', json=sample_user)
    print(response.text)
    assert response.status_code == 200


def test_read_users():
    response = client.get('/users/')
    assert response.status_code == 200


def test_read_user():
    response = client.get('/users/1')
    assert response.status_code == 200

