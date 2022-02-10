from crypt import methods
from distutils.command.config import config
from flask import Flask, request, render_template, jsonify
from configs import colors, tile
from constraints_solver import TileCP
import sys

app = Flask(__name__)

tile_config = tile.Config()

@app.route('/')
def home():
    return render_template("index.html", tiles=tile.tiles, font_size=tile_config.get_text_size(), icon_size=tile_config.get_icon_size())

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
        print(f"Previous: {(tile_config.get_text_size(), tile_config.get_icon_size())}", file=sys.stderr)
        tile_config.set_text_size(d['textSize'])
        tile_config.set_icon_size(d['iconSize'])
        print(f"Current: {(tile_config.get_text_size(), tile_config.get_icon_size())}", file=sys.stderr)
        return "OK"
    return {}


if __name__ == "__main__":
    app.run(debug=True)