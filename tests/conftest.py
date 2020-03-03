"""Pytest conf"""
import pytest

from hyperion.app import create_app
from hyperion.db import db_session as _db_session, Base
from hyperion.config import TEST_CONFIG


@pytest.fixture(scope="session")
def client():
    flask_app = create_app(TEST_CONFIG)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope="function")
def db_session():
    """Clear database before and after test case."""
    engine = _db_session.get_bind()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield _db_session

    _db_session.rollback()
    Base.metadata.drop_all(bind=engine)
