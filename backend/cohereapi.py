import cohere
import logging
from tqdm import tqdm

logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
)


API_KEY = "Pp0haiyiyMTfS4VHPCacV3W27tGF8tK7Bzmoz0dZ"
STOP_SEQ_TOKEN = "<STOP>"
TEMPERATURE = 0.3  # lower = more predictable, higher = more creative
MAX_TOKEN_SIZE = 2048  # so about 2048//3 words


def _clean_string(string: str) -> str:
    string = string.replace("\n", " ")
    string = string.replace("\\n", "")
    string = string.replace(STOP_SEQ_TOKEN, "")
    string = string.replace("\\", "")
    string = string.replace("/", " ")
    return string


def summarize(
    text: str,
    max_word_length: int = 10,
    grouped_size: int = 20,
) -> list[str]:

    sentences = text.split(".")
    summaries = []
    for i in tqdm(
        range(0, len(sentences), grouped_size), total=len(sentences) // grouped_size
    ):
        grouped_sentences = sentences[i : i + grouped_size]
        subtext = ".".join(grouped_sentences)
        co = cohere.Client(API_KEY)
        subtext = subtext + STOP_SEQ_TOKEN
        try:
            response = co.generate(
                model="xlarge",
                prompt=subtext,
                max_tokens=max_word_length * 3,
                temperature=TEMPERATURE,
                stop_sequences=[STOP_SEQ_TOKEN],
                k=5,  # beam search parameter
                frequency_penalty=0.4,
                presence_penalty=0.7,
            )
            summaries.extend([_clean_string(g.text) for g in response.generations])
        except Exception as e:
            logging.info(f"{i}th grouped sentence failed due to the following issue")
            logging.info(str(e))
            logging.info(f"Grouped sentence text is {grouped_sentences}.")
            continue

    grouped_summaries = ".".join(summaries)

    return [grouped_summaries]


if __name__ == "__main__":
    with open("./podcast_text.txt", "r") as f:
        text = f.readlines()[0]
    logging.info(summarize(text))
