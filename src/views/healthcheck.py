"""Customers views"""
from flask import Blueprint

from .base import response


bp = Blueprint("healthcheck", __name__, url_prefix="/healthcheck")


@bp.route("/")
def healthcheck():
    """Get list of customers"""
    return response(message="Healthy!")
