"""Flask and Celery integration tests that do not require external services."""

from unittest.mock import Mock

import app as application


def test_index_renders_without_triggering_a_scrape(monkeypatch):
    collection = Mock()
    collection.find_one.return_value = None
    monkeypatch.setattr(application.mongo.db, "mars_app", collection)

    response = application.app.test_client().get("/")

    assert response.status_code == 200
    assert "Mission to Mars" in response.text
    collection.find_one.assert_called_once_with()


def test_longtask_enqueues_scrape_and_returns_status_location(monkeypatch):
    queued = Mock(id="task-123")
    monkeypatch.setattr(application.scraping.scrape_all, "apply_async", Mock(return_value=queued))

    response = application.app.test_client().post("/longtask")

    assert response.status_code == 202
    assert response.json == {}
    assert response.headers["Location"].endswith("/status/task-123")


def test_task_status_contract(monkeypatch):
    monkeypatch.setattr(
        application.scraping.scrape_all,
        "AsyncResult",
        Mock(return_value=Mock(state="SUCCESS")),
    )

    response = application.app.test_client().get("/status/task-123")

    assert response.status_code == 200
    assert response.json == {"state": "SUCCESS"}


def test_404_page():
    response = application.app.test_client().get("/missing")

    assert response.status_code == 404
