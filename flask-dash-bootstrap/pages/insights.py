import dash
import dash_bootstrap_components as dbc
from dash import dcc

dash.register_page(
    __name__,
    path="/insights",
    name="Insights",
    title="Insight boundary",
    description="Guidance for adding evidence-backed analytical insights.",
    order=2,
)

layout = dbc.Alert(
    dcc.Markdown(
        """
        ## Insights

        Analytical claims belong here only after their source, observation time,
        transformation, and uncertainty are visible to the reader.
        """
    ),
    color="info",
)
