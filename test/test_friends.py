import pytest

from test.setup_client import client


def test_add_friend():
    res = client.post('/friends/')


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
    return
    res = client.get('/friends/')
    assert res.status_code == 200
    friends = res.json()
    print(friends)
    assert 0


def test_remove_friend():
    pass

