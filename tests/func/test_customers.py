"""Functional tests for customers"""
from hyperion.views import base as view_base
from hyperion.db import db
from .fixtures import *


def test_get_list_customers(client, make_customer_list):
    """Test should return list of customers"""
    # Arange
    customers = make_customer_list(10)
    db.session.bulk_save_objects(customers)
    db.session.commit()

    # Act
    response = client.get("customers/?name=test")
    response_data = response.get_json()

    # Assert
    assert response.status_code == view_base.HTTP_200_OK
    assert len(response_data["data"]) == len(customers)


def test_get_customers_no_query_param_should_return_400(client, make_customer_list):
    """Test should return 400 when query param is missing"""
    # Arange
    customers = make_customer_list(10)
    db.session.bulk_save_objects(customers)
    db.session.commit()

    # Act
    response = client.get("customers/")
    response_data = response.get_json()

    # Assert
    assert response.status_code == view_base.HTTP_400_BAD_REQUEST
