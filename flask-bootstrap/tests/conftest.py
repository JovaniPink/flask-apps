"""Pytest fixtures for the Flask application."""

import pytest

from app import create_app, db as the_db
from app.commands.init_db import init_db


@pytest.fixture()
def app():
    application = create_app(
        {
            "SECRET_KEY": "isolated-test-secret",
            "SECURITY_PASSWORD_SALT": "isolated-test-salt",
            "TESTING": True,
            "MAIL_SUPPRESS_SEND": True,
            "SERVER_NAME": "localhost",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        }
    )
    with application.app_context():
        init_db()

    yield application

    with application.app_context():
        the_db.session.remove()
        the_db.drop_all()


@pytest.fixture()
def db():
    return the_db


@pytest.fixture()
def client(app):
    return app.test_client()
