import dash
import dash_bootstrap_components as dbc
from dash import dcc

dash.register_page(
    __name__,
    path="/process",
    name="Process",
    title="Process boundary",
    description="The release and runtime boundaries for this Dash reference application.",
    order=3,
)

layout = dbc.Card(
    dbc.CardBody(
        dcc.Markdown(
            """
            ## Process

            1. Change the page or application boundary.
            2. Regenerate and review the Linux dependency lock.
            3. Run request, layout, audit, and container gates.
            4. Publish and validate the exact pull-request head before merge.
            """
        )
    )
)
