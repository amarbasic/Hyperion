"""Customer queries"""
from hyperion.models import Customer


def get_customer_list(query_params):
    """Get customer list"""
    queryset = Customer.query

    if query_params and "name" in query_params:
        queryset = queryset.filter(Customer.name.contains(query_params["name"]))

    return [{"id": obj.id, "name": obj.name} for obj in queryset]
