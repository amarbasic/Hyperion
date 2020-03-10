"""Application factory"""
from flask import Flask

from .config import configuration, DEV_CONFIG
from .extensions import db


def create_app(config=DEV_CONFIG):
    app = Flask(__name__)
    app.config.from_object(configuration[config])

    db.init_app(app)

    # Views registration
    from hyperion.routes import init_views

    init_views(app)

    @app.teardown_appcontext
    def teardown(exception=None):
        if db.session:
            db.session.remove()

    return app
