import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from db.db_connection import get_db
from configs import colors, tile
from configs.tile import Config, cfg
from constraints_solver import TileCP, reoder_tiles
from db import db_connection
from auth import auth
import sys
import copy
import random

bp = Blueprint('api', __name__, url_prefix="/api")


@bp.route('/preferences', methods=["GET", "POST"])
def preferences():
    if request.method == "POST":
        cfg.randomize_frequencies()

    return jsonify(cfg.get_frequencies().tolist())


@bp.route("/tiles", methods=["GET"])
def get_user_study_tiles():
    tiles_arr = copy.deepcopy(tile.tiles)
    tiles_arr = random.sample(tiles_arr, k=len(tiles_arr))
    return jsonify(tiles_arr)


#
# @app.route('/api/preferences', methods=["GET"])
# def get_preferences():
#     return jsonify(cfg.get_preferences().tolist())
#
# @app.route('/api/frequencies', methods=["POST"])
# def randomize_frequencies():
#     cfg.randomize_frequencies()
#     return jsonify(cfg.get_frequencies().tolist())
#
# @app.route('/api/preferences', methods=["POST"])
# def set_preferences():
#     if request.is_json:
#         d = request.get_json()
#         preferences = np.asarray(d).astype(np.int)
#         cfg.set_preferences(preferences)
#         return "OK"
#     return "ERROR"
#
#
# @bp.route('/preferences', methods=["POST"])
# def set_preferences():
#     if request.is_json:
#         d = request.get_json()
#         preferences = np.asarray(d).astype(np.int)
#         cfg.set_preferences(preferences)
#         return "OK"
#     return "ERROR"

@bp.route('/order', methods=["POST", "GET"])
def order():
    if request.method == 'POST':
        if request.is_json:
            d = request.get_json()
            mode = int(d["mode"])
            cfg.set_mode(mode)
            tiles_data = copy.deepcopy(tile.tiles)
            if cfg.get_mode() == Config.ALPHABETICAL:
                tiles_data.sort(key=lambda x: x["id"])
            else:
                tiles_data = reoder_tiles(tiles_data, cfg)
            return jsonify(tiles_data)
        return "ERROR"
    return jsonify(cfg.get_mode())
