import requests
import logging
import time
import pickle
import json
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


def convert_to_qanda_pairs(response_payload):
    HOST = "B" # Lenny's podcast always starts with a guest snippet --> Host is speaker B not A
    GUEST = "A"
    qanda_pairs = []
    utterances = response_payload["utterances"]

    for i in range(len(utterances)):
        # identify pairs of host questions and guest answers. We employ a heuristic to filter for important questions by
        # length of the guest's answers (more than 20 words).
        if utterances[i]["speaker"] == HOST and "?" in utterances[i]["text"] and utterances[i+1]["speaker"] == GUEST\
                and len(utterances[i+1]["text"].split(" ")) > 20:
            qanda_pairs.append((utterances[i]["text"], utterances[i+1]["text"]))
    return qanda_pairs

def parse_podcast(
    audio_url: str,
    start_backoff_time: float = 10.0,
) -> str:
    json = {
        "audio_url": audio_url,
        "speaker_labels": True
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

    qanda_pairs = convert_to_qanda_pairs(payload)
    return qanda_pairs


if __name__ == "__main__":
    download_url = "https://api.substack.com/feed/podcast/89661224/f9e085cab47a18122dc0a7adc952c5c0.mp3"
    qanda_pairs = parse_podcast(download_url)
    with open(f'qanda_pairs_{download_url.split("/")[-1]}.pickle', 'wb') as f:
        pickle.dump(qanda_pairs, f)
