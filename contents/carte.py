import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_leaflet.express as dlx
import dash
from dash_extensions.javascript import Namespace, arrow_function
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from server import app
import json, pickle
import pandas as pd

url = "https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png"
attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '

ns = Namespace("dlx", "choropleth")


def get_info(feature=None):
    header = [html.H4("Vignoble Jacquesson")]
    if not feature:
        return header + ["Passer la souris sur une parcelle"]
    return header + [html.B(feature["properties"]["nom_parcelle"]) , html.Br(),
                     feature["properties"]["nom_proprietaire"]]

collapse = html.Div(
    [
        dbc.Button(
            id="creation-button",
            className="fas fa-plus"
        ),
        dbc.Tooltip("Définir une parcelle", target="creation-button", placement="right"),
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(html.H5("Nouvelle parcelle", className="card-subtitle"), justify='center'),
                        dbc.Input(id='nom_parcelle', placeholder='Nom parcelle', style={'height':'24px', 'margin-top':'10px'}, value=''),
                        dbc.Input(id='nom_proprietaire', placeholder='Nom propriétaire', style={'height':'24px', 'margin-top':'10px'}, value=''),
                        dbc.Row(dbc.Button(id='save', className="fas fa-save", style={'height':'28px', 'margin-top':'10px'}), justify='center'),
                        html.Div(id='confirm-save'),
                    ]
                )
            ),id="creation",
        )
    ], style={"position": "absolute", "top": "100px", "left": "104px", "z-index": "500"}
)

info = html.Div(
    children=get_info(),
    id="info",
    className="info",
    style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"},
)


tab1_content = []

tab2_content = []

tabs = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Consulter la carte", tab_id=1),
                    dbc.Tab(label="Modifier un élément", tab_id=2),
                ],
                id="tabs",
                card=True,
                active_tab=1,
                persistence=True,
                persistence_type="session",
            )
        ),
        dbc.Container(id="tab_content"),
    ]
)

content = html.Div(
    children=[
        dl.Map(
            children=[
                dl.TileLayer(
                    url=url,
                    attribution=attribution
                ),
                dl.GeoJSON(
                    options=dict(
                        style=dict(
                            weight=0.2,
                            opacity=1,
                            color="#FF4500",
                            dashArray="5",
                            fillOpacity=0.1,
                        )
                    ),
                    zoomToBounds=True,
                    # zoomToBoundsOnClick=True,
                    hoverStyle=arrow_function(
                        dict(weight=4, color="#ADFF2F", dashArray="", fillOpacity=0.2)
                    ),
                    id="geojson",
                ),
                dl.Polyline(id="polyline", positions=[[0, 0]]),
                dl.Polygon(id="polygone", positions=[[0, 0]]),
                info,
            ],
            style={
                "width": "100%",
                "height": "60vh",
                "margin": "auto",
                "display": "block",
            },
            id="map",
        ),
        collapse,
    ]
)

@app.callback(
    Output("polyline", "positions"),
    Output("polygone", "positions"),
    Input("map", "click_lat_lng"),
    Input('save', 'n_clicks'),
    State("creation", "is_open"),
    State("polyline", "positions"),
    State("polygone", "positions"),
    prevent_initial_callbacks=True,
)
def definition_parcelle(click_lat_lng, btn, is_open, positions, polygon_state):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    dummy_pos = [0, 0]
    dlatlon2 = 1e-8
    if is_open:
        if click_lat_lng is None or positions is None:
            return [dummy_pos], [dummy_pos]
        # Reset position arrays if polygon array not set to dummy_pos
        if polygon_state[0] != dummy_pos:
            return [dummy_pos], [dummy_pos]
        # On first click, reset the polyline.
        if len(positions) == 1 and positions[0] == dummy_pos:
            return [click_lat_lng], [dummy_pos]
        # If the click is close to the first point, close the polygon.
        dist2 = (positions[0][0] - click_lat_lng[0]) ** 2 + (
            positions[0][1] - click_lat_lng[1]
        ) ** 2
        if dist2 < dlatlon2:
            return [dummy_pos], positions

        if 'save' in changed_id :
            return [dummy_pos], positions
        # Otherwise, append the click position.
        positions.append(click_lat_lng)
        return positions, [dummy_pos]
    else:
        return [[0,0]], [[0,0]]

@app.callback(
    Output("creation", "is_open"),
    [Input("creation-button", "n_clicks"),
    Input('save', 'n_clicks')],
    [State("creation", "is_open"),
    State('nom_parcelle', 'value'),
    State('nom_proprietaire', 'value'),
    State("polygone", "positions")],
)
def toggle_collapse(n_clicks1, n_clicks2, is_open, nom_parcelle, nom_proprietaire, positions):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'creation-button' in changed_id:
        return not is_open
    if 'save' in changed_id:
        if nom_parcelle=='' or nom_proprietaire=='' or positions==[[0,0]]:
            raise PreventUpdate
        else:
            return False


@app.callback(
    Output("geojson", "data"),
    Output('nom_parcelle','value'),
    Output('nom_proprietaire','value'),
    Output('confirm-save', 'children'),
    Input("save", "n_clicks"),
    State('nom_parcelle', 'value'),
    State('nom_proprietaire', 'value'),
    State("polygone", "positions"),
)
def enregistrer_parcelle(n_clicks1, nom_parcelle, nom_proprietaire, positions):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    with open("data/test.json") as file:
        geojson = json.load(file)
    if 'save' in changed_id:
        if nom_parcelle!='' and nom_proprietaire!='':
            if positions!=[[0,0]]:
                coordinates = [[i[1], i[0]] for i in positions]
                polygon = {
                    "type": "Feature",
                    "geometry": {"type": "Polygon", "coordinates": [coordinates]},
                    "properties": {"nom_parcelle": nom_parcelle, "nom_proprietaire" : nom_proprietaire},
                }
                geojson["features"] += [polygon]
                with open("data/test.json", "w") as file:
                    json.dump(geojson, file)
                return geojson, '', '',''
            else:
                return geojson, '', '','*parcelle non conforme'
        else:
            return geojson, '', '','*champs manquants'
    else:
        return geojson, nom_parcelle, nom_proprietaire,''


@app.callback(
    Output("info", "children"),
    Input("geojson", "hover_feature")
)
def info_hover(feature):
    return get_info(feature)
