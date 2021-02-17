import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash
from dash.dependencies import Input, Output
from server import app
import pandas as pd
from contents import carte, planning


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "5rem",
    "padding": "2rem 1rem",
    "background-color": "#222222",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "6rem",
    "margin-right": "1rem",
    "margin-top": "1rem",
    # "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.Button(className="fas fa-layer-group", style={'width':'50px'}, id='carte'),
                dbc.Tooltip(
                    'Carte',
                    target="carte",
                    placement='right'
                ),
                html.Br(),
                dbc.Button(id='parcelle', className="fas fa-vector-square"),
                dbc.Tooltip(
                    'Parcelles',
                    target="parcelle",
                    placement='right'
                ),
                html.Br(),
                dbc.Button(id='planning', className="far fa-calendar-alt"),
                dbc.Tooltip(
                    'Planning',
                    target="planning",
                    placement='right'
                ),
                html.Br(),
                dbc.Button(id='stocks', className="fas fa-box-open"),
                dbc.Tooltip(
                    'Gestion des stocks',
                    target="stocks",
                    placement='right'
                ),
                html.Br(),
                dbc.Button(id='ordre', className="fas fa-list-alt"),
                dbc.Tooltip(
                    'Ordre de travail',
                    target="ordre",
                    placement='right'
                ),
                html.Br(),
                dbc.Button(id='synthese', className="fas fa-chart-bar"),
                dbc.Tooltip(
                    'Synthèse',
                    target="synthese",
                    placement='right'
                ),
                html.Br(),
                dbc.Button(id='parametres', className="fas fa-sliders-h"),
                dbc.Tooltip(
                    'Paramètres généraux',
                    target="parametres",
                    placement='right'
                ),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                dbc.Button(id='aide', className="fas fa-question-circle"),
                dbc.Tooltip(
                    'Aide',
                    target="aide",
                    placement='right'
                ),
                html.Br(),
                dbc.Button(id='preferences', className="fas fa-user-cog"),
                dbc.Tooltip(
                    'Préfèrences',
                    target="preferences",
                    placement='right'
                ),
                html.Br(),
                dbc.Button(id='logout', className="fas fa-sign-out-alt"),
                dbc.Tooltip(
                    'Déconnexion',
                    target="logout",
                    placement='right'
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="content", style=CONTENT_STYLE)

layout = html.Div([sidebar, content])

@app.callback(
    Output('content', 'children'),
    Input('carte', 'n_clicks'),
    Input('parcelle', 'n_clicks'),
    Input('planning', 'n_clicks'),
    Input('stocks', 'n_clicks'),
    Input('ordre', 'n_clicks'),
    Input('synthese', 'n_clicks'),
    Input('parametres', 'n_clicks'))
def displayClick(btn1, btn2, btn3, btn4, btn5, btn6, btn7):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'carte' in changed_id:
        return carte.content
    elif 'planning' in changed_id:
        return planning.content
    elif 'actions' in changed_id:
        msg = 'Button 3 was most recently clicked'
        return html.Div(msg)
    elif 'stocks' in changed_id:
        msg = 'Button 4 was most recently clicked'
        return html.Div(msg)
    elif 'parametres' in changed_id:
        msg = 'Button 5 was most recently clicked'
        return html.Div(msg)
    else:
        return carte.content


