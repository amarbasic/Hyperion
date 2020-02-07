"""Application factory"""
from flask import Flask

from .config import configuration


def create_app(config="dev"):
    app = Flask(__name__)
    app.config.from_object(configuration[config])

    # Models and database registration
    from src.db import db, init_db

    init_db(app, db)

    # Views registration
    from src.routes import init_views

    init_views(app)

    return app
