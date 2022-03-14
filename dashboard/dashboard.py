import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from db.db_connection import get_db
from configs import colors, tile
from configs.tile import cfg, Config
from constraints_solver import TileCP, reoder_tiles
from db import db_connection
from auth import auth
import sys
import copy
from auth.auth import login_required

bp = Blueprint('dashboard', __name__)


@bp.route('/')
@login_required
def home():
    tiles_data = copy.deepcopy(tile.tiles)
    if cfg.get_mode() == Config.ALPHABETICAL:
        tiles_data.sort(key=lambda x: x["id"])
    else:
        tiles_data = reoder_tiles(tiles_data, cfg)
    return render_template("index.html", tiles=tiles_data, font_size=cfg.get_text_size(), icon_size=cfg.get_icon_size())


# @bp.route('/customize')
# def customize():
#     return render_template(
#         "customize.html",
#         primary_colors=colors.primary,
#         secondary_colors=colors.secondary,
#         tiles=tile.tiles
#     )

@bp.route('/tiles', methods=["GET"])
def get_tiles():
    return jsonify(tile.tiles)


@bp.route('/tiles', methods=["POST"])
def customize_tiles():
    if request.is_json:
        d = request.get_json()
        cp = TileCP()
        cp.add_constraint(d['textSizeMin'], d['textSizeMax'], 'text_size')
        cp.add_constraint(d['iconSizeMin'], d['iconSizeMax'], 'icon_size')
        solutions = cp.get_solutions()
        return jsonify({"solutions": solutions})

    return {}


@bp.route('/tiles/save', methods=["POST"])
def save_font():
    if request.is_json:
        d = request.get_json()
        print(f"Previous: {(cfg.get_text_size(), cfg.get_icon_size())}", file=sys.stderr)
        cfg.set_text_size(d['textSize'])
        cfg.set_icon_size(d['iconSize'])
        print(f"Current: {(cfg.get_text_size(), cfg.get_icon_size())}", file=sys.stderr)
        return "OK"
    return {}
