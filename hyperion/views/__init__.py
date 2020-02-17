"""Views package"""
from .customers import bp as customer_api
from .healthcheck import bp as healthcheck_api
from .base import response

__all__ = [
    "response",
    "customer_api",
    "healthcheck_api",
]
