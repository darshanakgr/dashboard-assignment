import copy
import sys

from flask import Blueprint, render_template, session, jsonify

import utils.user_utils as user_utils
from auth.auth import login_required
from utils.config import Config
from constraints_solver import reorder_tiles

bp = Blueprint('dashboard', __name__)


@bp.route('/')
@login_required
def home():
    user = user_utils.load_user(user_id=session.get("user_id"))
    tiles_data = copy.deepcopy(Config.TILES)
    print("user mode:", user.get_mode(), file=sys.stdout)
    if user.get_mode() == Config.ALPHABETICAL:
        tiles_data.sort(key=lambda x: x["id"])
    else:
        tiles_data = reorder_tiles(tiles_data, user)
    return render_template("index.html", tiles=tiles_data, font_size=20, icon_size=40)


@bp.route('/tiles', methods=["GET"])
def get_tiles():
    return jsonify(Config.TILES)
