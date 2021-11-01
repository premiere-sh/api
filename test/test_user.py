import pytest
import time
import json
import os

from test.setup_client import client


sample_user = {
  'username': 'user1',
  'password': 'secret',
  'date_of_birth': 1635353891,
  'email': 'user1@gmail.com'
}


def test_create_user():
    response = client.post('/users/', json=sample_user)
    assert response.status_code == 200


def test_read_users():
    response = client.get('/users/')
    assert response.status_code == 200


def test_read_user():
    response = client.get('/users/1')
    assert response.status_code == 200


def test_update_user_points():
    pass


def test_update_password():
    pass


def test_delete_user():
    pass

