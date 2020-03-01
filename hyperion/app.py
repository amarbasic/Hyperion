"""Application factory"""
from flask import Flask

from .config import configuration


def create_app(config="dev"):
    app = Flask(__name__)
    app.config.from_object(configuration[config])

    # Models and database registration
    from hyperion.db import init_db

    init_db(app)

    # Views registration
    from hyperion.routes import init_views

    init_views(app)

    return app
