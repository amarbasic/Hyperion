"""Views package"""
from .customers import bp as customer_api
from .healthcheck import bp as healthcheck_api

__all__ = ["customer_api", "healthcheck_api"]
