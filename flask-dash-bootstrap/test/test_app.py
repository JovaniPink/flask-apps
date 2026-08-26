from collections.abc import Iterator

import dash
from dash.development.base_component import Component

from app import app, build_navigation, server
from pages.index import figure as overview_figure
from pages.not_found_404 import layout as not_found_layout


def walk_components(component: Component) -> Iterator[Component]:
    """Yield every Dash component in a layout tree."""

    yield component
    children = getattr(component, "children", None)
    if isinstance(children, Component):
        yield from walk_components(children)
    elif isinstance(children, (list, tuple)):
        for child in children:
            if isinstance(child, Component):
                yield from walk_components(child)


def test_registered_page_contract():
    pages = {page["path"]: page for page in dash.page_registry.values()}

    assert set(pages) == {
        "/",
        "/insights",
        "/not-found-404",
        "/predictions",
        "/process",
    }
    assert pages["/"]["name"] == "Overview"
    assert all(page["title"] and page["description"] for page in pages.values())


def test_navigation_has_one_link_per_public_page():
    links = [
        component
        for component in walk_components(build_navigation())
        if component.__class__.__name__ == "NavLink"
    ]

    assert [link.href for link in links] == ["/", "/predictions", "/insights", "/process"]
    assert len({link.href for link in links}) == len(links)
    assert all(link.active == "exact" for link in links)


def test_application_routes_serve_the_dash_shell():
    client = server.test_client()

    for path in ("/", "/predictions", "/insights", "/process", "/missing"):
        response = client.get(path)
        assert response.status_code == 200
        assert b"Dash reference" in response.data


def test_custom_not_found_page_has_recovery_content():
    assert "Page not found" in str(not_found_layout)
    buttons = [
        component
        for component in walk_components(not_found_layout)
        if component.__class__.__name__ == "Button"
    ]
    assert [button.href for button in buttons] == ["/"]


def test_layout_and_dependency_endpoints_are_available():
    client = server.test_client()

    assert client.get("/_dash-layout").status_code == 200
    assert client.get("/_dash-dependencies").status_code == 200


def test_overview_figure_serializes_with_the_expected_plotly_contract():
    figure = overview_figure.to_plotly_json()

    assert len(figure["data"]) == 1
    assert figure["data"][0]["type"] == "scatter"
    assert figure["data"][0]["mode"] == "lines+markers"
    assert figure["data"][0]["x"] == [1, 2, 3, 4, 5]
    assert figure["data"][0]["y"] == [2, 5, 4, 8, 9]
    assert figure["layout"]["title"]["text"] == "A small, dependency-light Plotly figure"


def test_health_check_is_machine_readable():
    response = server.test_client().get("/healthz")

    assert response.status_code == 200
    assert response.get_json() == {"service": "flask-dash-bootstrap", "status": "ok"}
