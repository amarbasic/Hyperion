"""Customer models"""
from sqlalchemy import Column, Integer, String
from hyperion.db import Base


class Customer(Base):
    """Customer model"""

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
