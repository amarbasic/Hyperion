"""Customers views"""
import logging

from flask import Blueprint, request

from hyperion.views.base import response, validate_request_body, validate_query_params
from hyperion.validators import customers as customer_validators
from hyperion.services import customers as customer_services
from hyperion.queries import customers as customer_queries
from hyperion.exceptions import HyperionError


customer_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customer_bp.route("/")
@validate_query_params(customer_validators.customer_query_schema)
def get_customers():
    """Get list of customers"""
    logging.info("Get customers")
    customers = customer_queries.get_customer_list(request.args)

    return response(customers)


@customer_bp.route("/", methods=["POST"])
@validate_request_body(customer_validators.create_customer_schema)
def create_customer():
    """Create customer"""
    new_customer = customer_services.create_customer(request.get_json())

    return response(new_customer, "Customer successfully created.")
