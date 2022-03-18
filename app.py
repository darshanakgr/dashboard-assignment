from flask import Flask
from flask_cors import CORS

from api import api
from auth import auth
from dashboard import dashboard
from db import db_connection
from flask_session import Session

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
