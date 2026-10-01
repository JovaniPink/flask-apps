"""Pure parsing coverage for the scraping helpers."""

import pytest
import scraping
from scraping import create_browser, scrape_hemisphere


def test_container_browser_runtime():
    with create_browser() as browser:
        browser.visit("data:text/html,<title>browser-ready</title>")
        assert browser.title == "browser-ready"


def test_scrape_hemisphere_extracts_title_and_sample_url():
    parsed = scrape_hemisphere(
        '<h2 class="title">Valles Marineris</h2>'
        '<a href="https://example.test/mars.jpg">Sample</a>'
    )

    assert parsed == {
        "title": "Valles Marineris",
        "img_url": "https://example.test/mars.jpg",
    }


def test_scrape_hemisphere_handles_missing_markup():
    assert scrape_hemisphere("<main></main>") == {"title": None, "img_url": None}


def test_browser_uses_installed_native_binaries(monkeypatch):
    monkeypatch.setattr(scraping.shutil, "which", lambda name: "/usr/bin/" + name)
    captured = {}
    def browser(name, **kwargs):
        captured.update(name=name, **kwargs)
        return captured
    monkeypatch.setattr(scraping, "Browser", browser)
    result = create_browser()
    assert result["name"] == "chrome"
    assert result["options"].binary_location == "/usr/bin/chromium"
    assert result["service"].path == "/usr/bin/chromedriver"


def test_browser_fails_before_implicit_driver_download(monkeypatch):
    monkeypatch.setattr(scraping.shutil, "which", lambda name: None)
    monkeypatch.setattr(scraping, "Browser", lambda *args, **kwargs: pytest.fail("must not start browser"))
    with pytest.raises(RuntimeError, match="must be installed on PATH"):
        create_browser()
