"""Functional fixtures"""
import pytest

from hyperion.models import customers as customer_models


@pytest.fixture
def make_customer_list():
    def _make_customer_list(count=0):
        return [customer_models.Customer(name=f"Customer {i}") for i in range(count)]

    return _make_customer_list
