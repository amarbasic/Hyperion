"""Customers views"""
import logging

from flask import Blueprint, request

from hyperion import database
from hyperion.common import status
from hyperion.common.schema import validate_schema
from hyperion.common.utils import paginated_args, parse_bool
from .models import Customer
from .schemas import CustomerListDetailsSchema, CustomerCreateSchema


customer_bp = Blueprint("customers", __name__, url_prefix="/customers")


# @customer_bp.route("/")
# def get_customers():
#     """Get list of customers"""
#     logging.info("Get customers")
#     customers = customer_uc.get_customer_list(request.args)

#     return response(customers)


# @customer_bp.route("/seed/")
# def seed_customers():
#     customer_uc.seed_customers(total_seed=10)
#     return response(message="Seed done!")


@customer_bp.route("/", methods=["POST"])
@validate_schema(
    input_schema=CustomerCreateSchema, output_schema=CustomerListDetailsSchema
)
def create_customer(data):
    """Create customer"""
    return database.create(Customer(**data))


@customer_bp.route("/")
@validate_schema(output_schema=CustomerListDetailsSchema)
def get_customers():
    """Get list of customers"""
    query = database.session_query(Customer)
    filters = {
        "name": request.args.get("name", type=str),
        "is_active": parse_bool(request.args.get("isActive", type=int)),
    }

    filtered_query = database.filter(query, Customer, filters)
    customers = database.sort_and_page(
        filtered_query, Customer, paginated_args(request)
    )

    return customers


from flask.views import MethodView


class MyApi(MethodView):
    def dispatch_request(self, *args, **kwargs):
        print("Before request")
        response = super().dispatch_request(*args, **kwargs)
        print("After request: ", response)

        return response

    def get(self):
        return {"ok": "ok"}
