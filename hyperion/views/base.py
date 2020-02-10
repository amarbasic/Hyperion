"""Base view functions"""
from flask import jsonify, Response, request

from hyperion import exceptions

HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400
HTTP_500_SERVER_ERROR = 500


def response(
    data: dict = {}, message: str = None, errors: list = None, status: int = HTTP_200_OK
) -> Response:
    """Create API JSON response

    :data: Data to return as dictionary
    :message: Message for notifications
    :errors: List of errors for details
    """
    return jsonify({"message": message, "data": data, "errors": errors}), status


def validate_request_body(schema):
    """Validate request body"""

    def _validate_body():
        v = Validator(schema)

        if not v.validate(request.get_json()):
            raise exceptions.HyperionError("Invalid input data.")

    return _validate_body


def validate_query_params(schema):
    """Validate request query params"""

    def _validate_query_params():
        v = Validator(schema)

        if not v.validate(request.args):
            raise exceptions.HyperionError("Invalid query params.")

    return _validate_query_params
