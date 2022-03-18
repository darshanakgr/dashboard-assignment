import copy

import click
from flask import Blueprint, request, session, jsonify

import utils.user as user_utils
import utils.vote as vote_utils
from auth.auth import login_required
from utils.constraints_solver import reorder_tiles
from utils.config import Config


bp = Blueprint('api', __name__, url_prefix="/api")


@bp.route('/preferences', methods=["GET", "POST"])
@login_required
def preferences():
    user = user_utils.load_user(user_id=session.get("user_id"))
    if request.method == "POST":
        user.generate_preferences()
        user_utils.save_user(user)

    return jsonify(user.get_preferences())


@bp.route('/frequencies', methods=["GET", "POST"])
@login_required
def frequencies():
    user = user_utils.load_user(user_id=session.get("user_id"))
    if request.method == "POST":
        user.generate_frequencies()
        user_utils.save_user(user)

    return jsonify(user.get_frequencies())


@bp.route('/vote', methods=["POST", "GET"])
@login_required
def vote():
    user = user_utils.load_user(user_id=session.get("user_id"))
    if request.method == 'POST':
        if request.is_json:
            d = request.get_json()
            vote = int(d["vote"])
            user.set_vote(vote)
            user_utils.save_user(user)
            return "OK"
        return "ERROR"

    return jsonify(user.get_vote())

@bp.route('/votes', methods=["GET"])
@login_required
def votes():
    return jsonify(vote_utils.count_votes())


@bp.route('/order', methods=["POST", "GET"])
@login_required
def order():
    user = user_utils.load_user(user_id=session.get("user_id"))
    if request.method == 'POST':
        if request.is_json:
            d = request.get_json()
            mode = int(d["mode"])
            user.set_mode(mode)
            user_utils.save_user(user)
            tiles_data = copy.deepcopy(Config.TILES)
            if mode == Config.ALPHABETICAL:
                tiles_data.sort(key=lambda x: x["id"])
            else:
                tiles_data = reorder_tiles(tiles_data, user)
            return jsonify(tiles_data)
        return "ERROR"
    return jsonify(user.get_mode())
