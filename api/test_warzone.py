import pytest

from .setup_client import client


warzone_user = {
    'username': '',
    'platform': ''
}


def test_get_stats():
    response = client.post('/warzone-stats/', json=warzone_user)
    assert response.status_code == 200
    stats = response.json()
    # assert stats

