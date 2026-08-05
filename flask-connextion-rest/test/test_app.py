"""Runtime and CRUD smoke tests for the Connexion example."""

import pytest

from config import db
from server import create_app


@pytest.fixture()
def application():
    connexion_app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    with connexion_app.app.app_context():
        db.create_all()
        yield connexion_app
        db.session.remove()
        db.drop_all()


def test_landing_page_renders(application):
    response = application.test_client().get("/")

    assert response.status_code == 200
    assert "People" in response.text


def test_people_and_notes_crud_contract(application):
    client = application.test_client()

    created_person = client.post(
        "/api/people",
        json={"fname": "Ada", "lname": "Lovelace"},
    )
    assert created_person.status_code == 201
    person_id = created_person.json()["person_id"]

    created_note = client.post(
        f"/api/people/{person_id}/notes",
        json={"content": "First programmer"},
    )
    assert created_note.status_code == 201
    note_id = created_note.json()["note_id"]

    note = client.get(f"/api/people/{person_id}/notes/{note_id}")
    assert note.status_code == 200
    assert note.json()["content"] == "First programmer"

    people = client.get("/api/people")
    assert people.status_code == 200
    assert people.json()[0]["notes"][0]["content"] == "First programmer"

    updated_note = client.put(
        f"/api/people/{person_id}/notes/{note_id}",
        json={"content": "Analytical Engine pioneer"},
    )
    assert updated_note.status_code == 200
    assert updated_note.json()["content"] == "Analytical Engine pioneer"

    deleted_note = client.delete(f"/api/people/{person_id}/notes/{note_id}")
    assert deleted_note.status_code == 200

    updated_person = client.put(
        f"/api/people/{person_id}",
        json={"fname": "Augusta Ada", "lname": "Lovelace"},
    )
    assert updated_person.status_code == 200
    assert updated_person.json()["fname"] == "Augusta Ada"

    deleted_person = client.delete(f"/api/people/{person_id}")
    assert deleted_person.status_code == 200
    assert client.get(f"/api/people/{person_id}").status_code == 404
