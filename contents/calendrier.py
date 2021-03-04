import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.express as px
import pandas as pd

df = pd.DataFrame([
    dict(Action="Phyto", Début='2020-01-01', Fin='2020-01-02', Parcelle="Léon"),
    dict(Action="Phyto", Début='2020-02-01', Fin='2020-02-02', Parcelle="Léon"),
    dict(Action="Engrais", Début='2020-03-01', Fin='2020-03-02', Parcelle="Léon"),
    dict(Action="Phyto", Début='2020-11-05', Fin='2020-11-06', Parcelle="CB"),
    dict(Action="Engrais", Début='2020-02-20', Fin='2020-02-24', Parcelle="VT")
])

fig = px.timeline(df, x_start="Début", x_end="Fin", y="Parcelle", color="Action")
fig.update_yaxes(autorange="reversed")
fig.update_traces(
    selector=dict(name="Phyto"), marker=dict(color='#FF7F50')
    )
fig.update_traces(
    selector=dict(name="Engrais"), marker=dict(color='#90EE90')
    )

content=dbc.Container(
    [
        dbc.Row(html.H2('Calendrier'), justify='center'),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='filtre-prop',
                        options=[],
                        placeholder="Propriétaire",
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='type-traitement',
                        options=[],
                        placeholder="Type de traitement",
                    ),
                )
            ], justify='center'
        ),
        dcc.Graph(id='planning', figure=fig)
    ]
)
