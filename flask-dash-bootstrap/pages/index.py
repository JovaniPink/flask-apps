import dash
import dash_bootstrap_components as dbc
from dash import dcc
import plotly.graph_objects as go

dash.register_page(
    __name__,
    path="/",
    name="Overview",
    title="Dash reference overview",
    description="A maintained multipage Dash and Bootstrap reference application.",
    order=0,
)

figure = go.Figure(
    data=go.Scatter(
        x=[1, 2, 3, 4, 5],
        y=[2, 5, 4, 8, 9],
        mode="lines+markers",
        name="Example series",
        hovertemplate="Step %{x}<br>Value %{y}<extra></extra>",
    )
)
figure.update_layout(
    title="A small, dependency-light Plotly figure",
    xaxis_title="Step",
    yaxis_title="Value",
    margin={"l": 48, "r": 24, "t": 64, "b": 48},
)

layout = dbc.Row(
    [
        dbc.Col(
            [
                dcc.Markdown(
                    """
                    ## A current multipage Dash reference

                    This sample demonstrates one routing registry, responsive Bootstrap
                    composition, a production WSGI boundary, and a container health contract.
                    """
                ),
                dbc.Button("See the prediction boundary", href="/predictions", color="primary"),
            ],
            lg=4,
        ),
        dbc.Col(dcc.Graph(figure=figure, responsive=True), lg=8),
    ],
    class_name="g-4 align-items-center",
)
