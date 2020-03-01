"""Init views"""
from hyperion.common import status, views
from hyperion.customers.views import customer_bp
from . import exceptions


def init_views(app=None):
    """Initializes application views."""
    if app is None:
        raise ValueError("cannot init views without app object")

    # register defined views
    app.register_blueprint(customer_bp)

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
        return views.response(message=str(error), status=status.HTTP_400_BAD_REQUEST)

    @app.errorhandler(Exception)
    def handle_exception(error):
        message = str(error) if app.debug else "Something went wrong."

        return views.response(message=message, status=status.HTTP_500_SERVER_ERROR)
