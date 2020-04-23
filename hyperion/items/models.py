"""Item models"""
from sqlalchemy import Column, Integer, String

from hyperion.extensions import db


class Item(db.Model):
    """Item model"""

    __tablename__ = "items"

    item_id = Column(Integer(), primary_key=True)
    name = Column(String())
