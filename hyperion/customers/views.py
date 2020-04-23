"""Customers views"""
import logging

from flask import Blueprint, request

from hyperion.common.schema import validate_schema
from hyperion.common.utils import parse_bool, paginated_args
from .schemas import CustomerListDetailsSchema, CustomerCreateSchema
from . import services as customer_services
from . import usecases as customer_uc


customer_bp = Blueprint("customers", __name__)


@customer_bp.route("/", methods=["POST"])
@validate_schema(
    input_schema=CustomerCreateSchema, output_schema=CustomerListDetailsSchema
)
def create_customer(data):
    logging.info(f"Create new customer: {data}")
    return (
        customer_uc.create_customer(name=data["name"], is_active=data["is_active"]),
        201,
    )


@customer_bp.route("/")
@validate_schema(output_schema=CustomerListDetailsSchema)
def get_customers():
    filters = {
        "name": request.args.get("name", type=str),
        "is_active": parse_bool(request.args.get("isActive", type=int)),
    }

    return customer_services.get(
        filters=filters, pagination=paginated_args(request.args)
    )
