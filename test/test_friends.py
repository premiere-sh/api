import pytest

from test.setup_client import client
from test.sample_user import get_sample_user


def test_send_invite():
    user1_id = (client.post('/users/', json=get_sample_user(1))).json()
    user2_id = (client.post('/users/', json=get_sample_user(2))).json()
    user1 = (client.get(f'/users/{user1_id}')).json()
    user2 = (client.get(f'/users/{user2_id}')).json()
    response = client.post('/token/', data={
        'username': get_sample_user(1)['username'],
        'password': get_sample_user(1)['password']
    })
    token = response.json()['access_token']
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    res = client.post(f'/users/{user2_id}/friends/invite/', headers=headers)
    friendship = res.json()
    assert friendship['inviting_friend'] == user1['username']
    assert friendship['accepting_friend'] == user2['username']


def test_accept_invite():
    pass


def test_only_authorized_can_send_request():
    """
    post request requiring auth to submit the request to friends table
    """
    pass


def test_only_invited_user_can_accept_request():
    """
    put request requiring auth to accept the friendship
    """
    pass


def test_get_friends():
    res = client.get('/users/1/friends/')
    assert res.status_code == 200


def test_remove_friend():
    pass
