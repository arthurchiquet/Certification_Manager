import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from server import app
import pandas as pd
import json
import pickle
import plotly.express as px

mapbox_token = 'pk.eyJ1IjoiYXJ0aHVyY2hpcXVldCIsImEiOiJja2E1bDc3cjYwMTh5M2V0ZzdvbmF5NXB5In0.ETylJ3ztuDA-S3tQmNGpPQ'


colors = {
    'background': '#222222',
    'text': 'white'
}

def empty_figure():
    fig = {
        'data': [],
        'layout': {
        'plot_bgcolor': colors['background'],
        'paper_bgcolor': colors['background'],
        'font': {
            'color': colors['text']}
        }
    }
    return fig

def create_figure(df, geojson):
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations='id',
        zoom=13,
        center = {"lat": 49.0686, "lon":3.9695},
        color='commune',
        opacity=1,
        hover_name='numero',
        color_discrete_map={
            '51210':'#7FFFD4',
            '51287':'#FF7F50',
            '51119':'#6495ED',
            '51030':'#FF1493'
        },
        hover_data={
            'contenance':True,
            'commune':True
        }
    )
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        showlegend=False,
        height=690,
        clickmode='event+select',
        mapbox_style="dark",
        mapbox_accesstoken=mapbox_token,
        margin=dict(l=10, r=10, t=25, b=0))

    fig.update_traces(marker=dict(line=dict(color='grey')))

    return fig

app.layout=html.Div(
    [
        html.Div(id="page-content"),
        dcc.Graph(
            id='map',
            figure=empty_figure()
            ),
        html.Br(),
        dbc.Row(html.H3(id='surface'), justify='center'),
        # html.Pre(id='test'),
    ]
)


@app.callback(
    Output('map', 'figure'),
    Input('page-content', 'children'))
def display_map(page_content):
    with open('data/data.json') as file:
        geojson=json.load(file)

    with open("data/parcelles_J.txt", "rb") as fp:
        filter_list = pickle.load(fp)

    df=pd.read_csv('data/df.csv')
    df=df[df.id.isin(filter_list)]
    df.commune=df.commune.astype('str')
    features = geojson['features']
    filtered_features = []

    for feature in features:
        if feature['id'] in filter_list:
            filtered_features.append(feature)
        else:
            pass

    geojson_v2={'type':'FeatureCollection','features':filtered_features}

    return create_figure(df, geojson_v2)

@app.callback(
    Output('surface', 'children'),
    Input('map','selectedData'))
def return_surface(selectedData):
    try:
        surface=0
        for i in selectedData['points']:
            surface+=i['customdata'][0]
        return f'{round(surface/10000, 3)} ha'
    except:
        return ''


# @app.callback(
#     Output('test', 'children'),
#     Input('map','selectedData'))
# def save_list(selectedData):
#     return json.dumps(selectedData, indent=2)

if __name__ == "__main__":
    app.run_server(debug=True)
