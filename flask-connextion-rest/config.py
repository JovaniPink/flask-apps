"""Shared configuration and Flask extension ownership."""

import os

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
ma = Marshmallow()


def configure_app(app, extra_config=None):
    """Configure one Flask application instance."""
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'people.db')}"
        ),
        SQLALCHEMY_ECHO=False,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    app.config.update(extra_config or {})

    db.init_app(app)
    ma.init_app(app)
