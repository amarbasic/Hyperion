"""Base view functions"""
from functools import wraps

from flask import jsonify, Response, request
from cerberus import Validator

from hyperion.common import status
from hyperion import exceptions


def response(
    data: dict = {},
    message: str = None,
    errors: list = None,
    status: int = status.HTTP_200_OK,
) -> Response:
    """Create API JSON response

    :data: Data to return as dictionary
    :message: Message for notifications
    :errors: List of errors for details
    """
    return jsonify({"message": message, "data": data, "errors": errors}), status


def validate_request_body(schema):
    """Validate request body

    :schema: Cerberus schem object as dict
    """

    def _validate_body(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            v = Validator(schema)

            if not v.validate(request.get_json()):
                raise exceptions.HyperionError("Invalid input data.")

            return f(*args, **kwargs)

        return wrapper

    return _validate_body


def validate_query_params(schema):
    """Validate request query params

    :schema: Cerberus schem object as dict
    """

    def _validate_query_params(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            v = Validator(schema)

            if not v.validate(request.args):
                raise exceptions.HyperionError("Invalid query params.")

            return f(*args, **kwargs)

        return wrapper

    return _validate_query_params
