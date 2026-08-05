"""Pure parsing coverage for the scraping helpers."""

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
