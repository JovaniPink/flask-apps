"""Connexion application factory and runtime entry point."""

import connexion
from flask import render_template

from config import basedir, configure_app, db


def create_app(extra_config=None):
    """Create the Connexion application and its underlying Flask app."""
    connexion_app = connexion.FlaskApp(__name__, specification_dir=basedir)
    app = connexion_app.app
    configure_app(app, extra_config)
    connexion_app.add_api(
        "swagger.yml",
        strict_validation=True,
        validate_responses=True,
    )

    # Import model metadata before creating the sample application's tables.
    import models  # noqa: F401

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/people")
    @app.route("/people/<int:person_id>")
    def people_page(person_id=""):
        return render_template("people.html", person_id=person_id)

    @app.route("/people/<int:person_id>/notes")
    @app.route("/people/<int:person_id>/notes/<int:note_id>")
    def notes_page(person_id, note_id=""):
        return render_template("notes.html", person_id=person_id, note_id=note_id)

    return connexion_app


connex_app = create_app()
app = connex_app.app


if __name__ == "__main__":
    connex_app.run(port=5000)
