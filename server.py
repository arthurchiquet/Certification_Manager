import dash
import dash_bootstrap_components as dbc
import os
from flask_login import LoginManager, UserMixin
from flask_caching import Cache

# from config_utilisateur import db, User as base

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME])

server = app.server
app.config.suppress_callback_exceptions = True

# db.init_app(server)

# # Setup the LoginManager for the server
# login_manager = LoginManager()
# login_manager.init_app(server)
# login_manager.login_view = "/"

# # Create User class with UserMixin
# class User(UserMixin, base):
#     pass

# # callback to reload the user object
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
