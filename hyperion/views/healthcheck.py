"""Customers views"""
from flask import Blueprint

from .base import response


healthcheck_bp = Blueprint("healthcheck", __name__, url_prefix="/healthcheck")


@healthcheck_bp.route("/")
def healthcheck():
    """Get list of customers"""
    return response(message="Healthy!")
