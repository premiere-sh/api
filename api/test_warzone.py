import pytest
from .setup_client import client


real_users=[("clutchbelk#3571595","acti"),("truegamedata#1375","battle"),("Bojo704","psn")]
sample_warzone_users = [{
    'username': uname,
    'platform': plat
} for (uname,plat) in real_users]

def test_get_stats():
    for user in sample_warzone_users:
        response = client.post('/warzone-stats/', json=user)
        assert response.status_code == 200

def test_invalid_platform():
    invalid_user={'username':real_users[0][0],
                  'platform':'not-a-valid-platform'}
    response = client.post('/warzone-stats/', json=invalid_user)
    assert response.status_code == 422

def test_invalid_user():
    invalid_user={'username':"not-a-real-user",
                  'platform':'acti'}
    response = client.post('/warzone-stats/', json=invalid_user)
    assert response.status_code == 404


def test_results_are_cached():
    pass