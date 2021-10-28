import pytest
import time
import json

from api.test.setup_client import client


sample_tournament = {
    'region': 'europe',
    'name': 'Warzone Play-Offs',
    'time': 1635353891,
    'prize': 0.03
}


def test_create_tournament():
    response = client.post('/tournaments/', json=sample_tournament)
    print(response.text)
    assert response.status_code == 200


def test_read_tournaments():
    response = client.get('/tournaments/')
    assert response.status_code == 200


def test_read_tournament():
    response = client.get('/tournaments/1')
    assert response.status_code == 200

