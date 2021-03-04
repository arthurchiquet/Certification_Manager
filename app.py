import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from server import app
# from flask_login import logout_user, current_user
from layouts import nav, connexion, deconnexion


app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content")
    ]
)

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/":
        return nav.layout
    elif pathname == "/nav":
        return nav.layout
    elif pathname == "/connexion":
        return connexion.layout
    elif pathname == "/deconnexion":
        return deconnexion.layout
    else:
        return "404"


# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/':
#         return connexion.layout
#     elif pathname == '/connexion':
#         return connexion.layout
#     elif pathname == '/nav':
#         if current_user.is_authenticated:
#             return nav.layout
#         else:
#             return deconnexion.layout
#     elif pathname == '/deconnexion':
#         if current_user.is_authenticated:
#             logout_user()
#             return deconnexion.layout
#         else:
#             return deconnexion.layout
#     else:
#         return '404'

if __name__ == "__main__":
    app.run_server(debug=True)
