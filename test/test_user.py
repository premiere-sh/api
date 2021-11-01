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

sample_user_with_points = {
  'username': 'user1',
  'password': 'secret',
  'date_of_birth': 1635353891,
  'email': 'user1@gmail.com',
  'points': 30
}

sample_user_with_tournaments = {
  'username': 'user1',
  'password': 'secret',
  'date_of_birth': 1635353891,
  'email': 'user1@gmail.com',
  'points': 30,
  'tournaments': '3,5,7'
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
    sample_user_with_points['username'] = 'user124'
    in_db = (client.get('/users/1')).json()
    before = in_db['points']
    assert before == 0 
    print(in_db)
    was_updated = client.put('/users/1/points/', json=sample_user_with_points)
    print(was_updated.json())
    print(sample_user_with_points)
    assert was_updated.json()
    updated = (client.get('/users/1')).json()
    assert updated['points'] == sample_user_with_points['points']
    

def test_update_password():
    pass


def test_delete_user():
    pass

