import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import Namespace, arrow_function
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from server import app
import json, pickle
import pandas as pd

url = 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png'
attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '

ns = Namespace("dlx", "choropleth")

def get_info(feature=None):
    header = [html.H4("Vignoble Jacquesson")]
    if not feature:
        return header + ["Passer la souris sur une parcelle"]
    return header + [html.B(feature['properties']["nom"]), html.Br(),]
                     # "{:.3f} ha".format(feature["properties"]["contenance"]/10000), html.Sup("2")]

info = html.Div(
    children=get_info(),
    id="info",
    className="info",
    style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"}
    )

dummy_pos = [0, 0]
dlatlon2 = 1e-8

tab1_content=[]
tab2_content=[]

tabs = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label='Consulter la carte', tab_id=1),
                    dbc.Tab(label="Modifier un élément", tab_id=2),
                ],
                id="tabs",
                card=True,
                active_tab=1,
                persistence=True,
                persistence_type="session",
            )
        ),
        dbc.Container(id='tab_content', children=dbc.Label('test'))
    ]
)


content = html.Div(
    children=
        [
            dl.Map(
                children=
                    [
                        dl.TileLayer(url=url, attribution=attribution),
                        dl.GeoJSON(
                            options=dict(style = dict(weight=0.2, opacity=1, color='#FF4500', dashArray='5', fillOpacity=0.1)),
                            zoomToBounds=True,
                            # zoomToBoundsOnClick=True,
                            hoverStyle=arrow_function(dict(weight=4, color='#ADFF2F', dashArray='', fillOpacity=0.2)),
                            id="geojson"
                        ),
                        dl.Polyline(id='polyline', positions=[dummy_pos]),
                        dl.Polygon(id='polygone', positions=[dummy_pos]),
                        info,
                    ]
                , style={'width': '100%', 'height': '60vh', 'margin': "auto", "display": "block"},
                id="map"
            ),
            html.Div(id='test'),
            dbc.Button(id='save', href='/'),
            html.Div(id='success'),
            html.Div(id='reload'),
            tabs
        ]
    )



@app.callback(
    [Output('polyline', "positions"),
    Output('polygone', "positions")],
    Input('map', "click_lat_lng"),
    State('polyline', "positions"),
    State('polygone', "positions"),
    prevent_initial_callbacks=True)
def update_polyline_and_polygon(click_lat_lng, positions, polygon_state):
    if click_lat_lng is None or positions is None:
        raise PreventUpdate()
    # Reset position arrays if polygon array not set to dummy_pos
    if polygon_state[0] != dummy_pos:
        return [dummy_pos], [dummy_pos]
    # On first click, reset the polyline.
    if len(positions) == 1 and positions[0] == dummy_pos:
        return [click_lat_lng], [dummy_pos]
    # If the click is close to the first point, close the polygon.
    dist2 = (positions[0][0] - click_lat_lng[0]) ** 2 + (positions[0][1] - click_lat_lng[1]) ** 2
    if dist2 < dlatlon2:
        return [dummy_pos], positions
    # Otherwise, append the click position.
    positions.append(click_lat_lng)
    return positions, [dummy_pos]


@app.callback(
    Output('success', "children"),
    Output('geojson', "data"),
    Input("save", 'n_clicks'),
    State('polygone', "positions"))
def save(n_clicks, positions):
    if n_clicks:
        coordinates=[[i[1],i[0]] for i in positions]
        polygon = {'type': 'Feature',
           'geometry': {'type': 'Polygon',
            'coordinates': [coordinates]},
           'properties': {'nom': 'Maison de arthur'}}
        with open('data/test.json') as file:
            geojson=json.load(file)
        geojson['features'] += [polygon]
        with open('data/test.json','w') as file:
            json.dump(geojson, file)
        return 'success', geojson
    else:
        with open('data/test.json') as file:
            geojson=json.load(file)
        return '', geojson

@app.callback(
    Output("info", "children"),
    [Input("geojson", "hover_feature")]
)
def info_hover(feature):
    return get_info(feature)
