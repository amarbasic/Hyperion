from src.db import db


class Customer(db.Model):
    """Customer model"""

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
