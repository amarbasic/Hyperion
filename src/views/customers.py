"""Customers views"""
from flask import Blueprint, request
from cerberus import Validator

from .base import response
from src.validators import customers as customer_validators
from src.services import customers as customer_services
from src.exceptions import HyperionError


bp = Blueprint("customers", __name__, url_prefix="/customers")


@bp.route("/")
def get_customers():
    """Get list of customers"""
    return response(customer_services.get_customer_list())


@bp.route("/", methods=["POST"])
def create_customer():
    """Create customer"""
    v = Validator(customer_validators.create_customer_schema)
    if v.validate(request.get_json()):
        return response(customer_services.create_customer(request.get_json()))

    raise HyperionError("Invalid data")


@bp.route("/seed")
def seed():
    """Seed customers"""
    customer_services.seed_customers(10)
    return response(customer_services.get_customer_list())
