from dtw import dtw
from utils.config import Config
import numpy as np


def encode(text: str):
    return np.array([ord(t) for t in text.strip("\"").lower()])


def match(query):
    encoded_query = encode(query)
    best_match = None
    best_dtw = 1e3
    for tile in Config.TILES:
        alignment = dtw(encoded_query, encode(tile["name"]), keep_internals=True)
        if alignment.normalizedDistance < 1.0 and best_dtw > alignment.normalizedDistance:
            best_match = tile["id"]
            best_dtw = alignment.normalizedDistance

    if best_match:
        return best_match
    return None
