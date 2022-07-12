import pytest

from .setup_client import client
sample_info=[("clutchbelk#3571595","acti"),("truegamedata#1375","battle"),("Bojo704","psn")]
#psn,steam,xbl,battle,uno(Activision ID),acti(Activision Tag)
sample_warzone_users = [{
    'username': uname,
    'platform': plat
} for uname,plat in sample_info]

def test_get_stats():
    for user in sample_warzone_users:
        response = client.post('/warzone-stats/', json=user)
        assert response.status_code == 200
        stats = response.json()