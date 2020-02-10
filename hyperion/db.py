from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# our global DB object (imported by models & views & everything else)
db = SQLAlchemy()
# support importing a functioning session query
query = db.session.query


def init_db(app=None, db=None):
    """Initializes the global database object used by the app."""
    if isinstance(app, Flask) and isinstance(db, SQLAlchemy):
        db.init_app(app)
        db.create_all(app=app)
    else:
        raise ValueError("Cannot init DB without db and app objects.")
