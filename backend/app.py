from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import pickle
from flask_cors import CORS
from .assemblyapi import parse_podcast
from .cohereapi import summarize as cohere_summarize
from typing import Dict

logging.basicConfig(
    encoding="utf-8",
    level=logging.DEBUG,
)

app = Flask(__name__)
CORS(app)
AUDIO_FORMAT = ".mp3"


@app.route("/", methods=["GET"])
def home() -> str:
    return "Backend server connected. Check API for possible routes."


def _text(uri: str) -> str:
    """Parse a uri that's been encoded by encodeURIComponent


    Example:
        start server wth:
            python -m flask run
        Then in a browser launch
            localhost:5000/podcast/?uri=https://d3ctxlq1ktw2nl.cloudfront.net/staging/2022-1-23/ebf1141e-02bb-7752-5e74-3aef1d03bbf9.mp3
    Args:
        uri: .
    Returns:
        Podcast as text.
    """
    assert AUDIO_FORMAT in uri, "Only mp3 is supported at this time."
    logging.info(f"Parsing mp3 uri found at {uri}")
    return parse_podcast(uri)


@app.route("/podcast/", methods=["GET", "POST"])
def text() -> str:
    # Assumes that the uri is found at /podcast/uri?=<uri>
    uri: str = request.args.get("uri")
    return _text(uri)


@app.route("/generateblog", methods=["GET"])
def summarize(use_cache: bool = True) -> Dict:
    """Parse an mp3 uri that's been encoded by encodeURIComponent


    Example:
        start server wth:
            python -m flask run
        Then in a browser launch
            localhost:5000/generateblog/?uri=https://d3ctxlq1ktw2nl.cloudfront.net/staging/2022-1-23/ebf1141e-02bb-7752-5e74-3aef1d03bbf9.mp3
    Args:
        use_cache: .
    Returns:
        Summary of podcast.

    """
    # Assumes that the uri is found at /generateblog/uri?=<uri>
    if not use_cache:
        uri: str = request.args.get("uri")
        podcast_text = _text(uri)
        summarized_text = cohere_summarize(podcast_text)[0]
        return summarized_text

    # Cache result for speed
    with open(
        "headlines_summaries_c942fd04195599fe23df3b093a8c62ee.mp3.pickle", "rb"
    ) as f:
        headlines_and_summaries = pickle.load(f)

    payload = jsonify(
        {
            "headlines": headlines_and_summaries[0],
            "summaries": headlines_and_summaries[1],
        }
    )
    logging.info(payload)
    return payload


if __name__ == "__main__":
    app.run(debug=True)
