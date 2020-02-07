"""Customer services"""
from src.db import db
from src.models import customers as customer_models


def get_customer_list():
    """Get customer list"""
    return [
        {"id": obj.id, "name": obj.name} for obj in customer_models.Customer.query.all()
    ]
    # or
    # from src.queries import customers as customer_queries
    # return customer_queries.write_complex_query_here()


def seed_customers(total_seed):
    for i in range(total_seed):
        db.session.add(customer_models.Customer(name=f"Customer {i}"))

    db.session.commit()


def create_customer(customer_data):
    """Create a customer"""
    customer_obj = customer_models.Customer(**customer_data)
    db.session.add(customer_obj)
    db.session.commit()

    return {"id": customer_obj.id, "name": customer_obj.name}
