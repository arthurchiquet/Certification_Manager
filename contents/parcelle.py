import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Output, Input, State

import pandas as pd

df = pd.read_csv('data/ParcellaireDetail_22_02_2021.csv', sep=';')

table_parcelles = dt.DataTable(
    id='table_parcelles',
    data=df.to_dict('records'),
    columns=[{"name": i, "id": i} for i in df.columns],
    style_table={'overflowX': 'auto'},
    style_cell={
        'height': 'auto',
        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
        'whiteSpace': 'normal'
    }
)

content=dbc.Container([
    dbc.Row(html.H2('Registre parcellaire'), justify='center'),
    html.Br(),
    table_parcelles])
