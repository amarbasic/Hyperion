"""Customer services"""
from typing import List, Dict

from hyperion import repository
from .models import Customer


def get(*, filters: Dict = {}, pagination: Dict = {}) -> List[Dict]:
    """Get customer list"""
    query = Customer.query

    filtered_query = repository.filter(query, Customer, filters)

    return repository.sort_and_page(filtered_query, Customer, pagination)


def create(*, name: str, is_active: bool) -> Customer:
    """Create a customer"""
    customer_obj = Customer(name=name, is_active=is_active)
    repository.create(customer_obj)
    repository.commit()

    return customer_obj
