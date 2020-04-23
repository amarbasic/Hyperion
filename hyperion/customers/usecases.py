"""Customer usecases"""
from hyperion.items import services as item_services
from . import services as customer_services
from .models import Customer


def create_customer(*, name: str, is_active: bool) -> Customer:
    customer = customer_services.create(name=name, is_active=is_active)
    item_services.create(name=customer.name)

    return customer
