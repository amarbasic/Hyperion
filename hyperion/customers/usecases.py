"""Customer usecases"""
from . import services as customer_services


def get_customer_list(*args, **kwargs):
    return customer_services.get(**kwargs)


def create_customer(*args, **kwargs):
    return customer_services.create(**kwargs)
