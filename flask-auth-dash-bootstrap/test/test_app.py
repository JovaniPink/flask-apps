"""Authentication and Dash integration smoke tests."""

import pytest

from app import create_app
from app.extensions import db


def test_runtime_requires_a_secret_key():
    with pytest.raises(RuntimeError, match="SECRET_KEY must be set"):
        create_app({"SECRET_KEY": None})


@pytest.fixture()
def application():
    app = create_app(
        {
            "SECRET_KEY": "isolated-test-secret",
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        }
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_landing_page_and_dashboard_auth_gate(application):
    client = application.test_client()

    assert client.get("/").status_code == 200

    protected = client.get("/dashboard/")
    assert protected.status_code == 302
    assert "/login/" in protected.headers["Location"]


def test_registration_login_and_dashboard_access(application):
    client = application.test_client()

    registered = client.post(
        "/register/",
        data={"username": "ada", "password": "analytical-engine"},
    )
    assert registered.status_code == 302
    assert registered.headers["Location"].endswith("/login/")

    logged_in = client.post(
        "/login/?next=/dashboard/",
        data={"username": "ada", "password": "analytical-engine"},
    )
    assert logged_in.status_code == 302
    assert logged_in.headers["Location"].endswith("/dashboard/")

    dashboard = client.get("/dashboard/")
    assert dashboard.status_code == 200
    assert "Dashapp 1" in dashboard.text
