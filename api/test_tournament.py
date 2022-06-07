import pytest
import time
import json

from test.setup_client import client


sample_tournament = {
    'region': 'europe',
    'name': 'Warzone Play-Offs',
    'game': 'warzone',
    'time': 1635353891,
    'prize': 0.03,
    'game': 'cod',
    'creator': 'username'
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

sample_tournament_with_users = {
    'region': 'europe',
    'name': 'Warzone Play-Offs',
    'game': 'cod',
    'time': 1635353891,
    'prize': 0.03,
    'users': '5,3',
    'creator': 'username'
}


def test_create_tournament():
    client.post('/users/', json=sample_user)
    response = client.post('/token/', data=credentials)
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
    assert response.status_code == 200


def test_read_tournaments():
    response = client.get('/tournaments/')
    assert response.status_code == 200


def test_read_tournament():
    response = client.get('/tournaments/1')
    assert response.status_code == 200


def test_get_upcoming_events():
    pass


def test_update_tournament_users():
    in_db = (client.get('/tournaments/1')).json()
    before = in_db['users']
    assert before == ''
    # the users like below should work for now, later create a table
    # for user_joined similarily as friendships
    was_updated = (client.put(
        '/tournaments/1', 
        json=sample_tournament_with_users
    )).json()
    assert was_updated
    updated = (client.get('/tournaments/1')).json()
    # TODO also update user tournaments when user joins
    assert updated['users'] == sample_tournament_with_users['users'] 


def test_delete_tournament():
    pass


def test_user_cannot_join_same_tournament_twice():
    pass


def test_user_tournaments_also_update_if_user_joins_tournament():
    pass


def test_get_ongoing():
    response = client.get('/tournaments/ongoing/')
    assert response.status_code == 200
    ongoing = response.json()
    assert 'cod' in ongoing
    assert 'rl' in ongoing
    assert 'minecraft' in ongoing
    assert 'dirt' in ongoing

