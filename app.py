from flask import *
from flask_session import Session
from flask_cors import CORS
from configs import colors, tile
from configs.tile import Config
from constraints_solver import TileCP, reoder_tiles
from db import db_connection
from auth import auth
from dashboard import dashboard
from api import api
import sys
import copy
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

db_connection.init_app(app)
app.secret_key = 'cs702_assignment'
app.config['SESSION_TYPE'] = 'filesystem'
app.register_blueprint(auth.bp)
app.register_blueprint(api.bp)

app.register_blueprint(dashboard.bp)
app.add_url_rule("/", endpoint='index')

if __name__ == "__main__":
    sess = Session()
    sess.init_app(app)
    app.run("0.0.0.0", port=80)
