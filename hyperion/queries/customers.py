"""Customer queries"""
from hyperion.models import Customer
from hyperion.serializers import customers as customer_serializer


def get_customer_list(query_params={}):
    """Get customer list"""
    queryset = Customer.query

    if "name" in query_params:
        queryset = queryset.filter(Customer.name.contains(query_params["name"]))

    return customer_serializer.customer_list_serializer(queryset)
