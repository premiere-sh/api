import pytest

from test.setup_client import client


def test_docs_redirect():
    response = client.get('/')
    assert response.status_code == 200

