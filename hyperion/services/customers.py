"""Customer services"""
from hyperion.db import db
from hyperion.models import Customer


def seed_customers(total_seed):
    db.create_all()
    for i in range(total_seed):
        db.session.add(Customer(name=f"Customer {i}"))

    db.session.commit()


def create_customer(customer_data):
    """Create a customer"""
    customer_obj = Customer(**customer_data)
    db.session.add(customer_obj)
    db.session.commit()

    return {"id": customer_obj.id, "name": customer_obj.name}
