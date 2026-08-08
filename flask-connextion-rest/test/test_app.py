"""Runtime and CRUD smoke tests for the Connexion example."""

from pathlib import Path

import pytest
import yaml
from openapi_spec_validator import validate

from config import db
from server import create_app


APP_ROOT = Path(__file__).resolve().parents[1]


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


def test_openapi_document_is_valid():
    specification = yaml.safe_load((APP_ROOT / "swagger.yml").read_text())

    validate(specification)


@pytest.mark.parametrize(
    "payload",
    [
        {"fname": "Ada"},
        {"fname": "", "lname": "Lovelace"},
        {"fname": "Ada", "lname": "Lovelace", "role": "programmer"},
    ],
)
def test_people_create_contract_rejects_invalid_payloads(application, payload):
    response = application.test_client().post("/api/people", json=payload)

    assert response.status_code == 400


def test_write_contract_rejects_empty_updates(application):
    client = application.test_client()
    created_person = client.post(
        "/api/people",
        json={"fname": "Ada", "lname": "Lovelace"},
    )
    person_id = created_person.json()["person_id"]

    empty_person_update = client.put(f"/api/people/{person_id}", json={})
    missing_note_content = client.post(
        f"/api/people/{person_id}/notes",
        json={},
    )

    assert empty_person_update.status_code == 400
    assert missing_note_content.status_code == 400


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
    assert deleted_note.json() == {"message": f"Note {note_id} deleted"}

    updated_person = client.put(
        f"/api/people/{person_id}",
        json={"fname": "Augusta Ada", "lname": "Lovelace"},
    )
    assert updated_person.status_code == 200
    assert updated_person.json()["fname"] == "Augusta Ada"

    deleted_person = client.delete(f"/api/people/{person_id}")
    assert deleted_person.status_code == 200
    assert deleted_person.json() == {"message": f"Person {person_id} deleted"}
    assert client.get(f"/api/people/{person_id}").status_code == 404
