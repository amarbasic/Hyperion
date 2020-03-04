"""Customer usecases"""
from . import services as customer_services
from . import dtos as customer_dtos


def get_customer_list(*args, **kwargs):
    customers_list = customer_services.get(**kwargs)

    return [{"id": obj.name, "name": obj.name} for obj in customers_list]


def create_customer(*, customer_data: customer_dtos.CreateCustomerDto):
    customer_obj = customer_services.create(customer_data=customer_data)

    return {"id": customer_obj.id, "name": customer_obj.name}


def seed_customers(*, total_seed):
    customer_services.seed(total_seed=total_seed)
