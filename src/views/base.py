"""Base view functions"""
from flask import jsonify, Response

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
