import pytest

from test.setup_client import client
from test.sample_user import get_sample_user


def get_auth_headers(client, sample_user_id):
    response = client.post('/token/', data={
        'username': get_sample_user(sample_user_id)['username'],
        'password': get_sample_user(sample_user_id)['password']
    })
    token = response.json()['access_token']
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    return headers


def test_send_invite():
    user1_id = (client.post('/users/', json=get_sample_user(1))).json()
    global user2_id
    user2_id = (client.post('/users/', json=get_sample_user(2))).json()
    user1 = (client.get(f'/users/{user1_id}')).json()
    user2 = (client.get(f'/users/{user2_id}')).json()
    headers = get_auth_headers(client=client, sample_user_id=1)
    slug = f'/users/{user2_id}/friends/invite/'
    response = client.post(slug, headers=headers)
    friendship = response.json()
    assert friendship['inviting_friend'] == user1['username']
    assert friendship['accepting_friend'] == user2['username']


def test_get_invites_requires_auth():
    response = client.get(f'/users/{user2_id}/invites/')
    assert response.status_code == 401


def test_user_can_only_see_their_own_invites():
    headers = get_auth_headers(client=client, sample_user_id=1)
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    assert response.status_code == 403


def test_get_invites():
    headers = get_auth_headers(client=client, sample_user_id=2)
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    assert response.status_code == 200


def test_accept_invite():
    return
    headers = get_auth_headers(client=client, sample_user_id=2)
    client.put(f'/users/{user2_id}/friends/invites/', {})

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
