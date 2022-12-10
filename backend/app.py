from flask import Flask, request
import logging
import numpy as np
from PIL import Image
from .assemblyapi import parse_podcast
from .cohereapi import summarize as cohere_summarize
from .openaiapi import make_image

logging.basicConfig(
    encoding="utf-8",
    level=logging.DEBUG,
)

app = Flask(__name__)
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
def summarize() -> str:
    """Parse an mp3 uri that's been encoded by encodeURIComponent


    Example:
        start server wth:
            python -m flask run
        Then in a browser launch
            localhost:5000/generateblog/?uri=https://d3ctxlq1ktw2nl.cloudfront.net/staging/2022-1-23/ebf1141e-02bb-7752-5e74-3aef1d03bbf9.mp3
    Args:
        uri: .
    Returns:
        Summary of podcast.

    """
    # Assumes that the uri is found at /generateblog/uri?=<uri>
    uri: str = request.args.get("uri")
    podcast_text = _text(uri)
    summarized_text = cohere_summarize(podcast_text)[0]
    return summarized_text


@app.route("/hallucinate_podcast", methods=["GET"])
def hallucinate_podcast() -> np.ndarray:
    """Parse an mp3 uri that's been encoded by encodeURIComponent into an image.


    Example:
        start server wth:
            python -m flask run
        Then in a browser launch
            localhost:5000/hallucinate/?uri=https://d3ctxlq1ktw2nl.cloudfront.net/staging/2022-1-23/ebf1141e-02bb-7752-5e74-3aef1d03bbf9.mp3
    Args:
        uri: .
    Returns:
        Image of podcast.
    """
    uri: str = request.args.get("uri")
    podcast_text = _text(uri)
    summarized_text = cohere_summarize(podcast_text)[0]
    image: np.ndarray = make_image(summarized_text)
    Image.fromarray(image).save("./hallucinate.png")
    return np.ndarray


if __name__ == "__main__":
    app.run(debug=True)
