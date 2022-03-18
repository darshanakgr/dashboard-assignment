from crypt import methods
from distutils.command.config import config
from tkinter import N
from flask import Flask, request, render_template, jsonify
from configs import colors, tile
from configs.tile import Config
from constraints_solver import TileCP, reoder_tiles
import sys
import copy
import numpy as np

app = Flask(__name__)

cfg = Config(n_tiles=len(tile.tiles))

@app.route('/')
def home():
    tiles_data = copy.deepcopy(tile.tiles)
    if cfg.get_mode() == Config.ALPHABETICAL:
        tiles_data.sort(key=lambda x: x["id"])
    else:
        tiles_data = reoder_tiles(tiles_data, cfg)
    return render_template("index.html", tiles=tiles_data, font_size=cfg.get_text_size(), icon_size=cfg.get_icon_size())

@app.route('/customize')
def customize():
    return render_template(
        "customize.html",
        primary_colors=colors.primary,
        secondary_colors=colors.secondary,
        tiles=tile.tiles
    )

@app.route('/tiles', methods=["GET"])
def get_tiles():
    return jsonify(tile.tiles)

@app.route('/tiles', methods=["POST"])
def customize_tiles():
    if request.is_json:
        d = request.get_json()
        cp = TileCP()
        cp.add_constraint(d['textSizeMin'], d['textSizeMax'], 'text_size')
        cp.add_constraint(d['iconSizeMin'], d['iconSizeMax'], 'icon_size')
        solutions = cp.get_solutions()
        return jsonify({"solutions": solutions})

    return {}

@app.route('/tiles/save', methods=["POST"])
def save_font():
    if request.is_json:
        d = request.get_json()
        print(f"Previous: {(cfg.get_text_size(), cfg.get_icon_size())}", file=sys.stderr)
        cfg.set_text_size(d['textSize'])
        cfg.set_icon_size(d['iconSize'])
        print(f"Current: {(cfg.get_text_size(), cfg.get_icon_size())}", file=sys.stderr)
        return "OK"
    return {}

@app.route('/api/frequencies', methods=["GET"])
def get_frequencies():
    return jsonify(cfg.get_frequencies().tolist())

@app.route('/api/preferences', methods=["GET"])
def get_preferences():
    return jsonify(cfg.get_preferences().tolist())

@app.route('/api/frequencies', methods=["POST"])
def randomize_frequencies():
    cfg.randomize_frequencies()
    return jsonify(cfg.get_frequencies().tolist())

@app.route('/api/preferences', methods=["POST"])
def set_preferences():
    if request.is_json:
        d = request.get_json()
        preferences = np.asarray(d).astype(np.int)
        cfg.set_preferences(preferences)
        return "OK"
    return "ERROR"

@app.route('/api/tiles', methods=["GET"])
def get_reodered_tiles():
    tiles_data = copy.deepcopy(tile.tiles)
    tiles_data = reoder_tiles(tiles_data, cfg)
    return jsonify(tiles_data)

@app.route('/api/order', methods=["POST"])
def set_mode():
    print("Function is called", file=sys.stdout)
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


@app.route('/api/order', methods=["GET"])
def get_mode():
    return jsonify(cfg.get_mode())


if __name__ == "__main__":
    app.run("0.0.0.0", port=80)