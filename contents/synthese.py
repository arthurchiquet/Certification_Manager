import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State


content=dbc.Container(
    [
        dbc.Row(html.H2('Synthese'), justify='center'),
        html.Br(),
    ]
)
