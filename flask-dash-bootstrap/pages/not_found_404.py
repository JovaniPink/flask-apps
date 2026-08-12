import dash
import dash_bootstrap_components as dbc
from dash import dcc

dash.register_page(
    __name__,
    title="Page not found",
    description="The requested Dash reference page does not exist.",
)

layout = dbc.Alert(
    [
        dcc.Markdown("## Page not found\n\nThe requested reference page does not exist."),
        dbc.Button("Return to overview", href="/", color="primary"),
    ],
    color="warning",
)
