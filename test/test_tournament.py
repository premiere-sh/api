import pytest
import time
import json

from test.setup_client import client


sample_tournament = {
    'region': 'europe',
    'name': 'Warzone Play-Offs',
    'time': 1635353891,
    'prize': 0.03
}

sample_user = {
  'username': 'user2',
  'password': 'secret',
  'date_of_birth': 1635353891,
  'email': 'user2@gmail.com'
}

credentials = {
    'username': 'user2',
    'password': 'secret'
}


def test_create_tournament():
    client.post('/users/', json=sample_user)
    response = client.post('/token', data=credentials)
    auth = response.json()
    headers = {
        'Authorization': f'Bearer {auth["access_token"]}',
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = client.post(
        '/tournaments/', 
        json=sample_tournament,
        headers=headers
    )
    print(response.text)
    assert response.status_code == 200


def test_read_tournaments():
    response = client.get('/tournaments/')
    assert response.status_code == 200


def test_read_tournament():
    response = client.get('/tournaments/1')
    assert response.status_code == 200

