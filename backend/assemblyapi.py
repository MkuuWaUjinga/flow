import requests
import logging
import time
from enum import Enum

logging.basicConfig(
    encoding="utf-8",
    level=logging.DEBUG,
)


class Status(Enum):
    QUEUED = "queued"
    COMPLETED = "completed"


STATUS_KEY = "status"
TEXT_KEY = "text"
BACKOFF_FACTOR = 2
API_KEY = "3d7fa80c0b1748eaaa5df94b65729cb4"
ENDPOINT = "https://api.assemblyai.com/v2/transcript"
HEADERS = {
    "authorization": API_KEY,
    "content-type": "application/json",
}


def parse_podcast(
    audio_url: str,
    start_backoff_time: float = 10.0,
) -> str:
    json = {
        "audio_url": audio_url,
    }

    post_response = requests.post(
        ENDPOINT,
        json=json,
        headers=HEADERS,
    )
    text_id = post_response.json()["id"]
    status = Status.QUEUED.value
    exponential_backoff = start_backoff_time
    while status != Status.COMPLETED.value:
        get_response = requests.get(
            ENDPOINT + f"/{text_id}",
            headers=HEADERS,
        )
        payload = get_response.json()
        status = payload[STATUS_KEY]
        logging.info(f"ASSEMBLY API STATUS IS: {status}")
        if status != Status.COMPLETED.value:
            logging.info(
                (
                    "Status not completed. "
                    f"Exponential backoff of {exponential_backoff}"
                )
            )
            time.sleep(exponential_backoff)
            exponential_backoff *= BACKOFF_FACTOR
    return payload[TEXT_KEY]


if __name__ == "__main__":
    text = parse_podcast(
        "https://d3ctxlq1ktw2nl.cloudfront.net/staging/2022-1-23/ebf1141e-02bb-7752-5e74-3aef1d03bbf9.mp3"  # David Sinclair podcast
    )
    logging.info(text)
