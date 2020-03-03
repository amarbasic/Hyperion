import logging

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Session = sessionmaker(autocommit=False, autoflush=False)
db_session = scoped_session(Session)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db(app: Flask):
    """Init database"""
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

    Session.configure(bind=engine)
    Base.metadata.create_all(bind=engine)

    app.teardown_appcontext(teardown_session)


def teardown_session(exception=None):
    """Teardown database session"""
    logging.debug("Closing db session.")
    db_session.remove()
