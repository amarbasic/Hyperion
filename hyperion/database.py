"""Database methods"""
from sqlalchemy import exc, func, distinct, Column
from sqlalchemy.orm import make_transient, lazyload
from sqlalchemy.sql import and_, or_

from hyperion.common.utils import underscore
from .extensions import db


def filter_none(kwargs):
    """
    Remove all `None` values froma  given dict. SQLAlchemy does not
    like to have values that are None passed to it.
    :param kwargs: Dict to filter
    :return: Dict without any 'None' values
    """
    n_kwargs = {}
    for k, v in kwargs.items():
        if v is not None:
            n_kwargs[k] = v
    return n_kwargs


def get_model_column(model, field):
    """Get model column

    :param model: database model
    :param field: field name
    :returns: Column object
    """
    if field in getattr(model, "sensitive_fields", ()):
        raise Exception(field)
    column = model.__table__.columns._data.get(field, None)
    if column is None:
        raise Exception(field)

    return column


def session_query(model):
    """
    Returns a SQLAlchemy query object for the specified `model`.
    If `model` has a ``query`` attribute already, that object will be returned.
    Otherwise a query will be created and returned based on `session`.
    :param model: sqlalchemy model
    :return: query object for model
    """
    return model.query if hasattr(model, "query") else db.session.query(model)


def create_query(model, kwargs):
    """
    Returns a SQLAlchemy query object for specified `model`.
    Model filtered by the kwargs passed.

    :param model:
    :param kwargs:
    :return:
    """
    s = session_query(model)
    return s.filter_by(**kwargs)


def commit():
    """
    Helper to commit the current session.
    """
    db.session.commit()


def add(model):
    """
    Helper to add a `model` to the current session.
    :param model:
    :return:
    """
    db.session.add(model)


def find_all(query, model, kwargs):
    """
    Returns a query object that ensures that all kwargs
    are present.
    :param query:
    :param model:
    :param kwargs:
    :return:
    """
    conditions = []
    kwargs = filter_none(kwargs)
    for attr, value in kwargs.items():
        if not isinstance(value, list):
            value = value.split(",")

        conditions.append(get_model_column(model, attr).in_(value))

    return query.filter(and_(*conditions))


def find_any(query, model, kwargs):
    """
    Returns a query object that allows any kwarg
    to be present.
    :param query:
    :param model:
    :param kwargs:
    :return:
    """
    or_args = []
    for attr, value in kwargs.items():
        or_args.append(or_(get_model_column(model, attr) == value))
    exprs = or_(*or_args)
    return query.filter(exprs)


def get(model, value, field="id"):
    """
    Returns one object filtered by the field and value.
    :param model:
    :param value:
    :param field:
    :return:
    """
    query = session_query(model)
    return query.filter(get_model_column(model, field) == value).scalar()


def get_all(model, value, field="id"):
    """
    Returns query object with the fields and value filtered.
    :param model:
    :param value:
    :param field:
    :return:
    """
    query = session_query(model)
    return query.filter(get_model_column(model, field) == value)


def create(model):
    """
    Helper that attempts to create a new instance of an object.
    :param model:
    :return: :raise IntegrityError:
    """
    try:
        db.session.add(model)
        commit()
    except exc.IntegrityError as e:
        raise Exception(e.orig.diag.message_detail)

    db.session.refresh(model)
    return model


def update(model):
    """
    Helper that attempts to update a model.
    :param model:
    :return:
    """
    commit()
    db.session.refresh(model)
    return model


def delete(model):
    """
    Helper that attempts to delete a model.
    :param model:
    """
    if model:
        db.session.delete(model)
        db.session.commit()


def filter(query, model, terms):
    """
    Helper that searched for 'like' strings in column values.
    :param query:
    :param model:
    :param terms:
    :return:
    """
    conditions = []
    kwargs = filter_none(terms)
    for attr, value in kwargs.items():
        # if not isinstance(value, list):
        #     value = value.split(",")

        column = get_model_column(model, underscore(attr))
        if isinstance(value, str):
            conditions.append(column.ilike("%{}%".format(value)))
        else:
            conditions.append(column == value)

    return query.filter(and_(*conditions))


def sort(query, model, field, direction):
    """
    Returns objects of the specified `model` in the field and direction
    given
    :param query:
    :param model:
    :param field:
    :param direction:
    """
    column = get_model_column(model, underscore(field))
    return query.order_by(column.desc() if direction == "desc" else column.asc())


def paginate(query, page, page_size):
    """
    Returns the items given the count and page specified
    :param query:
    :param page:
    :param page_size:
    """
    page -= 1
    items = query.offset(page_size * page).limit(page_size).all()
    total = get_count(query)

    return dict(items=items, total=total)


def update_list(model, model_attr, item_model, items):
    """
    Helper that correctly updates a models items
    depending on what has changed
    :param model_attr:
    :param item_model:
    :param items:
    :param model:
    :return:
    """
    ids = []

    for i in getattr(model, model_attr):
        if i.id not in ids:
            getattr(model, model_attr).remove(i)

    for i in items:
        for item in getattr(model, model_attr):
            if item.id == i["id"]:
                break
        else:
            getattr(model, model_attr).append(get(item_model, i["id"]))

    return model


def clone(model):
    """
    Clones the given model and removes it's primary key
    :param model:
    :return:
    """
    db.session.expunge(model)
    make_transient(model)
    model.id = None
    return model


def get_count(q):
    """Count rows"""
    return q.count()


def sort_and_page(query, model, args):
    """
    Helper that allows us to combine sorting and paging
    :param query:
    :param model:
    :param args:
    :return:
    """
    sort_by = args.get("sort_by")
    sort_order = args.get("sort_order")
    page = args.get("page")
    page_size = args.get("page_size")

    if sort_by and sort_order:
        query = sort(query, model, sort_by, sort_order)

    return paginate(query, page, page_size)
