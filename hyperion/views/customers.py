"""Customers views"""
from flask import Blueprint, request

from hyperion.views.base import response, validate_request_body, validate_query_params
from hyperion.validators import customers as customer_validators
from hyperion.services import customers as customer_services
from hyperion.exceptions import HyperionError


bp = Blueprint("customers", __name__, url_prefix="/customers")


@bp.route("/")
@validate_query_params(customer_validators.customer_query_schema)
def get_customers():
    """Get list of customers"""
    return response(customer_services.get_customer_list(request.args))


@bp.route("/", methods=["POST"])
@validate_request_body(customer_validators.create_customer_schema)
def create_customer():
    """Create customer"""
    return customer_services.create_customer(request.get_json())


@bp.route("/seed")
def seed():
    """Seed customers"""
    customer_services.seed_customers(10)
    return response(customer_services.get_customer_list(None))
