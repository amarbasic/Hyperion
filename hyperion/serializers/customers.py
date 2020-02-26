"""Customers serializers"""


def customer_list_serializer(queryset):
    """Serialize data as list

    :queryset: Customer queryset
    :returns: list of dict objects {id, name}
    """
    return [{"id": obj.id, "name": obj.name} for obj in queryset]
