"""Customer queries"""
from typing import List, Dict

from hyperion.db import db
from .models import Customer


def get(*, query_params: Dict = {}) -> List[Dict]:
    """Get customer list"""
    queryset = Customer.query

    if "name" in query_params:
        queryset = queryset.filter(Customer.name.contains(query_params["name"]))

    return [{"id": obj.name, "name": obj.name} for obj in queryset]


def seed(*, total_seed: int):
    """Seed"""
    db.create_all()
    for i in range(total_seed):
        db.session.add(Customer(name=f"Customer {i}"))

    db.session.commit()


def create(*, customer_data: Dict) -> int:
    """Create a customer"""
    customer_obj = Customer(**customer_data)
    db.session.add(customer_obj)
    db.session.commit()

    return customer_obj.id
