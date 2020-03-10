"""Customers views"""
import logging

from flask import Blueprint, request

from hyperion.common import status

# from . import dtos as customer_dtos
# from . import usecases as customer_uc


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


# @customer_bp.route("/", methods=["POST"])
# def create_customer():
#     """Create customer"""
#     customer_dto = customer_dtos.CreateCustomerDto(**request.get_json())
#     new_customer = customer_uc.create_customer(customer_data=customer_dto)

#     return response(
#         new_customer, "Customer successfully created.", status=status.HTTP_201_CREATED
#     )30


from hyperion.common.schema import validate_schema
from hyperion.common.utils import paginated_args, parse_bool
from .schemas import CustomerListDetailsSchema


@customer_bp.route("/")
@validate_schema(output_schema=CustomerListDetailsSchema)
def get_customers():
    """Get list of customers"""
    from hyperion import database
    from .models import Customer

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
