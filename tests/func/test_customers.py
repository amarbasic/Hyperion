"""Functional tests for customers"""
from src.views import base as view_base
from src.db import db
from . import fixtures


def test_get_list_customers(client, make_customer_list):
    """Test should return list of customers"""
    # Arange
    customers = fixtures.make_customer_list(10)
    db.session.bulk_save_objects(customers)
    db.session.commit()

    # Act
    response = client.get("customers/")
    response_data = response.get_json()

    # Assert
    assert response.status_code == view_base.HTTP_200_OK
    assert len(response_data["data"]) == len(customers)
