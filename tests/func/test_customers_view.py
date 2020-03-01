"""Functional tests for customers"""
import pytest

from hyperion.common import status
from hyperion.db import db
from .fixtures import *


def test_get_list_customers_with_filters(client, db_session, make_customer_list):
    """Test should return list of customers"""
    # Arange
    customers = make_customer_list(10)

    # Act
    response = client.get("customers/?name=customer")
    response_data = response.get_json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data["data"]) == len(customers)


@pytest.mark.skip(reason="Not implemented")
def test_get_customers_no_query_param_should_return_400(
    client, db_session, make_customer_list
):
    """Test should return customers"""
    # Arange
    customers = make_customer_list(10)

    # Act
    response = client.get("customers/")
    response_data = response.get_json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data["data"]) == len(customers)
