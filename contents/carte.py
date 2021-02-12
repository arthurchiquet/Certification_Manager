import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import Namespace, arrow_function
from dash.dependencies import Output, Input
from server import app
import json, pickle
import pandas as pd

with open('data/lieux_dits.json') as file:
    geojson=json.load(file)

# with open("data/parcelles_J.txt", "rb") as fp:
#         filter_list = pickle.load(fp)

# features = geojson['features']
# filtered_features = []

# for feature in features:
#     if feature['id'] in filter_list:
#         filtered_features.append(feature)
#     else:
#         pass

# geojson_v2={'type':'FeatureCollection','features':filtered_features}


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

url = 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png'
attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '

ns = Namespace("dlx", "choropleth")


content = html.Div(
    children=
        [
            dl.Map(
                children=
                    [
                        dl.TileLayer(url=url, attribution=attribution),
                        dl.GeoJSON(
                            data=geojson,
                            options=dict(style = dict(weight=1, opacity=1, color='#FF4500', dashArray='5', fillOpacity=0.1)),
                            zoomToBounds=True,
                            # zoomToBoundsOnClick=True,
                            hoverStyle=arrow_function(dict(weight=4, color='#ADFF2F', dashArray='', fillOpacity=0.2)),
                            id="geojson"
                        ),
                        dl.MeasureControl(position="topleft", primaryLengthUnit="meters", primaryAreaUnit="hectares",
                              activeColor="#214097", completedColor="#972158"),
                        info,
                    ]
                , style={'width': '100%', 'height': '60vh', 'margin': "auto", "display": "block"},
                id="map"
            )
        ]
    )

@app.callback(
    Output("info", "children"),
    [Input("geojson", "hover_feature")]
)
def info_hover(feature):
    return get_info(feature)
