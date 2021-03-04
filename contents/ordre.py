import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import dash_table as dt

from datetime import date


ot_nouveau = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                dcc.Dropdown(
                    id='type_travail',
                    options=[
                        dict(label = 'Manuel', value = 0),
                        dict(label = 'Mécanique', value = 1),
                        dict(label = 'Traitement' , value = 2),
                    ],
                    placeholder="Type de travail",
                    style=dict(width='300px')
                ), justify='center'
            ),
            html.Br(),
            dbc.Row(
                dcc.Dropdown(
                    id='action',
                    options=[],
                    placeholder="Action",
                    style=dict(width='300px')
                ), justify='center'
            ),
            html.Br(),
            dbc.Row(
                dcc.Dropdown(
                    id='parcelles',
                    options=[],
                    placeholder="Parcelles",
                    style=dict(width='300px'),
                    multi=True
                ), justify='center'
            ),
            html.Br(),
            dbc.Row(
                dcc.Dropdown(
                    id='operateur',
                    options=[],
                    placeholder="Opérateur",
                    style=dict(width='300px')
                ), justify='center'
            ),
            html.Br(),
            dbc.Row(
                dcc.Dropdown(
                    id='materiel',
                    options=[],
                    placeholder="Matériel",
                    style=dict(width='300px')
                ), justify='center'
            ),
            html.Br(),
            dbc.Row(
                dcc.Dropdown(
                    id='produit',
                    options=[],
                    placeholder="Produit",
                    style=dict(width='300px')
                ), justify='center'
            ),
            html.Br(),
            dbc.Row(
                dcc.Dropdown(
                    id='dose',
                    options=[],
                    placeholder="Dose",
                    style=dict(width='300px')
                ), justify='center'
            ),

            html.Br(),
            dbc.Row(
                dcc.DatePickerRange(
                    id='periode_ot',
                    initial_visible_month=date.today(),
                    start_date_placeholder_text='Debut',
                    end_date_placeholder_text='Fin',
                ), justify='center'
            ),

            html.Br(),
            dbc.Row(dbc.Button('Créer', disabled=True), justify='center')

        ]
    ),
    className="mt-3"
)

ot_en_cours = dbc.Card(
    dbc.CardBody(
        [
            html.P("Statut : En cours", className="card-text"),
            html.Br(),
            dt.DataTable(
                id='list_ot_en_cours',
                data=[],
                columns=[],
                style_table={'overflowX': 'auto'},
                style_cell={
                    'height': 'auto',
                    'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                    'whiteSpace': 'normal'
                }
            ),
            html.Br(),
            dbc.Row(dbc.Button('Valider'), justify='center')

        ]
    ),
    className="mt-3",
)

ot_archive = dbc.Card(
    dbc.CardBody(
        [
            html.P("Statut : Terminé", className="card-text"),
            html.Br(),
            dt.DataTable(
                id='list_ot_termine',
                data=[],
                columns=[],
                style_table={'overflowX': 'auto'},
                style_cell={
                    'height': 'auto',
                    'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                    'whiteSpace': 'normal'
                }
            )
        ]
    ),
    className="mt-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(ot_en_cours, label="En cours"),
        dbc.Tab(ot_nouveau, label="Nouveau"),
        dbc.Tab(ot_archive, label="Terminé"),
    ]
)

content=dbc.Container(
    [
        dbc.Row(html.H3('Ordres de travail'), justify='center'),
        html.Br(),
        tabs
    ]
)
