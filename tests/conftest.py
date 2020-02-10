"""Pytest conf"""
import pytest

from hyperion.app import create_app
from hyperion.config import TEST_CONFIG


@pytest.fixture(scope="module")
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
