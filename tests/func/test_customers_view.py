"""Functional tests for customers"""
import pytest

from hyperion.common import status
from hyperion.db import db_session
from .fixtures import *


def test_create_new_customer(client):
    """Test should create a new customer"""
    # Arrange
    customer_data = {"name": "Customer 1"}

    # Act
    response = client.post("customers/", json=customer_data)
    response_json = response.get_json()
    response_data = response_json["data"]

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response_data["name"] == customer_data["name"]


def test_get_list_customers_with_filters(client, make_customer_list):
    """Test should return list of customers"""
    # Arange
    customers = make_customer_list(10)

    # Act
    response = client.get("customers/?name=customer")
    response_json = response.get_json()
    response_data = response_json["data"]

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) == len(customers)


def test_get_customers_no_query_param_should_return_400(client, make_customer_list):
    """Test should return customers"""
    # Arange
    customers = make_customer_list(10)

    # Act
    response = client.get("customers/")
    response_json = response.get_json()
    response_data = response_json["data"]

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) == len(customers)
