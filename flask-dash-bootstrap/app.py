from dash import Dash, html, page_container, page_registry
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.CERULEAN],
    title="Dash reference application",
    update_title="Loading Dash reference application…",
)
server = app.server


@server.get("/healthz")
def health_check():
    """Expose a dependency-free process-health boundary for containers."""

    return {"service": "flask-dash-bootstrap", "status": "ok"}


def build_navigation():
    """Build navigation from the same page registry that owns routing."""

    links = [
        dbc.NavLink(page["name"], href=page["relative_path"], active="exact")
        for page in page_registry.values()
        if page["module"] != "pages.not_found_404"
    ]
    return dbc.NavbarSimple(
        children=links,
        brand="Dash reference",
        brand_href="/",
        color="primary",
        dark=True,
        sticky="top",
    )


app.layout = html.Div(
    [
        build_navigation(),
        dbc.Container(page_container, class_name="py-4", fluid="lg"),
        html.Footer(
            dbc.Container(
                "A maintained Flask Apps reference boundary.",
                class_name="py-3 text-secondary border-top",
                fluid="lg",
            )
        ),
    ]
)


if __name__ == "__main__":
    app.run(debug=True)
