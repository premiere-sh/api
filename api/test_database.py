from .database import get_db


def test_get_db():
    assert get_db() is not None


# TODO test for database closing
