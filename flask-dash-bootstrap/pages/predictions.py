import dash
import dash_bootstrap_components as dbc
from dash import dcc

dash.register_page(
    __name__,
    path="/predictions",
    name="Predictions",
    title="Prediction boundary",
    description="A presentation-only prediction boundary with no hidden model or data service.",
    order=1,
)

layout = dbc.Row(
    dbc.Col(
        dbc.Card(
            dbc.CardBody(
                dcc.Markdown(
                    """
                    ## Predictions

                    This reference deliberately has no model, data source, or persistence layer.
                    Add those only with an explicit input schema, provenance contract, and tests.
                    """
                )
            )
        ),
        lg=8,
    ),
    justify="center",
)
