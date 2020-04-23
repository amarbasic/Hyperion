"""Item services"""
from hyperion import repository
from .models import Item


def create(*, name: str) -> Item:
    """Create an item"""
    item_obj = Item(name=f"Item for {name}")
    repository.create(item_obj)
    repository.commit()

    return item_obj
