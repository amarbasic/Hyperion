"""Customers CLI"""
import click

from flask.cli import AppGroup

from hyperion import repository
from .models import Customer

customers_cli = AppGroup("customers")


@customers_cli.command("seed")
@click.argument("count", type=int)
def seed_customers(count: int):
    for i in range(count):
        repository.create(Customer(name=f"Customer {i}"))

    repository.commit()
