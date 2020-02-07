"""Init views"""
from . import views
from .views import base
from . import exceptions


def init_views(app=None):
    """Initializes application views."""
    if app is None:
        raise ValueError("cannot init views without app object")

    # register defined views
    app.register_blueprint(views.customer_api)
    app.register_blueprint(views.healthcheck_api)

    # Handle HTTP errors
    register_error_handlers(app)


def register_error_handlers(app=None):
    """Register app error handlers.

    Raises error if app is not provided.
    """
    if app is None:
        raise ValueError("cannot register error handlers on an empty app")

    @app.errorhandler(exceptions.HyperionError)
    def handle_hyperion_error(error):
        return base.response(message=str(error), status=base.HTTP_400_BAD_REQUEST)

    @app.errorhandler(Exception)
    def handle_exception(error):
        return base.response(message=str(error), status=base.HTTP_500_SERVER_ERROR)
