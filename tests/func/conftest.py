"""Functional fixtures"""
import pytest

from hyperion.customers import models as customer_models


@pytest.fixture
def make_customer_list(db_session):
    def _make_customer_list(count=0):
        customers = [
            customer_models.Customer(name=f"Customer {i}") for i in range(count)
        ]
        db_session.bulk_save_objects(customers)
        db_session.flush()

        return customers

    return _make_customer_list
