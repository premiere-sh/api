import pytest
import time
import json

from test.setup_client import client

sample_user = {
  'username': 'user3',
  'password': 'secret',
  'date_of_birth': 1635353891,
  'email': 'user3@gmail.com'
}

credentials = {
    'username': 'user3',
    'password': 'secret'
}


def test_create_account():
    response = client.post('/users/', json=sample_user)
    assert response.status_code == 200


def test_login():
    response = client.post('/token/', data=credentials)
    response = response.json()
    assert response['access_token'] is not None
    assert response['token_type'] == 'bearer'

