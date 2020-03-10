"""Pytest conf"""
import pytest

from hyperion.app import create_app
from hyperion.extensions import db
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
    db.create_all()

    yield db.session

    db.drop_all()
