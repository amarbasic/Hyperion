"""Customer services"""
from typing import List, Dict

from hyperion.db import db_session
from .models import Customer


def get(*, query_params: Dict = {}) -> List[Dict]:
    """Get customer list"""
    queryset = Customer.query

    if "name" in query_params:
        queryset = queryset.filter(Customer.name.contains(query_params["name"]))

    return queryset.all()


def seed(*, total_seed: int):
    """Seed"""
    for i in range(total_seed):
        db_session.add(Customer(name=f"Customer {i}"))

    db_session.commit()


def create(*, customer_data: Dict) -> Customer:
    """Create a customer"""
    customer_obj = Customer(**customer_data)
    db_session.add(customer_obj)
    db_session.commit()

    return customer_obj
