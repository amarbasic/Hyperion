"""Customer models"""
from sqlalchemy import Column, Integer, String, Boolean

from hyperion.extensions import db


class Customer(db.Model):
    """Customer model"""

    __tablename__ = "customers"

    customer_id = Column(Integer(), primary_key=True)
    name = Column(String())
    is_active = Column(Boolean(), default=True)
