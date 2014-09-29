import os

from flask import Flask

import configuration


app = Flask(__name__)


# Load default config and override config from an environment variable
# This is really the Flask configuration
app.config.update(dict(
    DATABASE='ahps_web.sqlite3',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

# This is the app-specific configuration
cfg = configuration.Configuration.load_configuration(app.root_path)

# Load randomly generated secret key from file
# Reference: http://flask.pocoo.org/snippets/104/
# Run make_secret_key to create a new key and save it in secret_key
app.config['SECRET_KEY'] = open('secret_key', 'r').read()

# All views must be imported after the app is defined
from views import views
from views import login_views
