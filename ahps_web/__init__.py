import os
import Logging
import logging
from Version import GetVersion

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
    PASSWORD='default',
    SQLALCHEMY_DATABASE_URI='',  # Use Sqlite file db
    CSRF_ENABLED=True,
    USER_ENABLE_EMAIL=False                   # Disable emails for now

))

# This is the app-specific configuration
cfg = configuration.Configuration.load_configuration(app.root_path)

# Load randomly generated secret key from file
# Reference: http://flask.pocoo.org/snippets/104/
# Run make_secret_key to create a new key and save it in secret_key
key_file = configuration.Configuration.SecretKey()
app.config['SECRET_KEY'] = open(key_file, 'r').read()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{0}".format(configuration.Configuration.get_database_file_path('ahps_web.sqlite3'))

# Start logging
Logging.EnableServerLogging()

# All views must be imported after the app is defined
from views import views
from views import login_views

logger = logging.getLogger("app")

logger.info("################################################################################")
logger.info("Starting AHPS_Web version %s", GetVersion())
logger.info("Using configuration file %s", configuration.Configuration.get_configuration_file_path())
