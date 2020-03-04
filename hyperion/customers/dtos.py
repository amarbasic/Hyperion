"""Customers DTOs"""
from pydantic import BaseModel, validator

from hyperion.exceptions import HyperionError


class CreateCustomerDto(BaseModel):
    """Create customer dto"""

    name: str

    @validator("name")
    def validate_name(cls, v):
        """Validate name field"""
        if not v:
            raise HyperionError("Name cannot be empty.")

        if len(v) > 10:
            raise HyperionError("Name cannot be longer than 10 characters.")

        return v
