"""Customers views"""
import logging

from flask import Blueprint, request

from hyperion.common.views import response, status
from . import usecases as customer_uc


customer_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customer_bp.route("/")
def get_customers():
    """Get list of customers"""
    logging.info("Get customers")
    customers = customer_uc.get_customer_list(request.args)

    return response(customers)


@customer_bp.route("/seed/")
def seed_customers():
    customer_uc.seed_customers(total_seed=10)
    return response(message="Seed done!")


@customer_bp.route("/", methods=["POST"])
def create_customer():
    """Create customer"""
    new_customer = customer_uc.create_customer(customer_data=request.get_json())

    return response(
        new_customer, "Customer successfully created.", status=status.HTTP_201_CREATED
    )
