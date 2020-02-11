"""Pytest conf"""
import pytest

from hyperion.app import create_app
from hyperion.db import db as _db
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


@pytest.fixture(scope="session")
def db(client):
    """Session-wide test database."""
    _db.app = client
    _db.drop_all()
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope="function")
def db_session(db):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()
