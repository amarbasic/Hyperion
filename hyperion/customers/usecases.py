"""Customer usecases"""
from . import services as customer_services


def get_customer_list(*args, **kwargs):
    return customer_services.get(**kwargs)


def create_customer(*args, **kwargs):
    return customer_services.create(**kwargs)


def seed_customers(*, total_seed):
    customer_services.seed(total_seed=total_seed)
