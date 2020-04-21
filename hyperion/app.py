"""Application factory"""
from logging import StreamHandler

from flask import Flask

from hyperion.common import status
from hyperion.customers.views import customer_bp
from hyperion.customers.cli import customers_cli
from .config import configuration, DEV_CONFIG
from .extensions import db
from . import exceptions


def create_app(config: str = DEV_CONFIG):
    app = Flask(__name__)

    configure_app(app, config)
    configure_extensions(app)
    configure_blueprints(app)
    configure_logging(app)
    configure_cli(app)

    @app.teardown_appcontext
    def teardown(exception=None):
        if db.session:
            db.session.remove()

    return app


def configure_app(app: Flask, config: str):
    app.config.from_object(configuration[config])


def configure_extensions(app: Flask):
    db.init_app(app)


def configure_blueprints(app: Flask):
    app.register_blueprint(customer_bp, url_prefix="/api/customers")


def configure_error_handlers(app: Flask):
    @app.errorhandler(exceptions.HyperionError)
    def handle_hyperion_error(error):
        return str(error), status.HTTP_400_BAD_REQUEST

    @app.errorhandler(Exception)
    def handle_exception(error):
        message = str(error) if app.debug else "Something went wrong."

        return message, status.HTTP_500_SERVER_ERROR


def configure_logging(app: Flask):
    app.logger.setLevel(app.config.get("LOG_LEVEL", "DEBUG"))

    stream_handler = StreamHandler()
    stream_handler.setLevel(app.config.get("LOG_LEVEL", "DEBUG"))
    app.logger.addHandler(stream_handler)


def configure_cli(app: Flask):
    app.cli.add_command(customers_cli)
