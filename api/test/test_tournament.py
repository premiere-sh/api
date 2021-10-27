import pytest
import time
import json

from api.app import app
from fastapi.testclient import TestClient


client = TestClient(app)

sample_tournament = {
    'region': 'europe',
    'name': 'Warzone Play-Offs',
    'time': time.time(),
    'prize': 0.03
}

@pytest.fixture
def create_entries():
    assert 0


def test_create_tournament():
    tournament_json = json.dumps(sample_tournament)
    response = client.post('/tournaments', json=tournament_json)
    assert response.status_code == 200
    print(response.json())


def test_read_tournaments():
    response = client.get('/tournaments')
    assert response.status_code == 200
    print(response.json())


def test_read_tournament():
    response = client.get('/tournaments/1')
    assert response.status_code == 200
    print(response.json())

