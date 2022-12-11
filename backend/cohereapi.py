import cohere
import logging
import pandas as pd
import pickle

from tqdm import tqdm
from typing import List, Tuple

logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
)

headline_prompt_stub = '''
"Amazing. And I think they're worth, I don't know, last valuation was like $10 billion. So there's been a quite the journey. Must have been quite the adventure being at Notion during this time. What's maybe the most, I don't know, tangible memory of working at Notion in the early days. What was it like?"
Headline: How was work at Notion in the early days?
"So speaking of community, you talked about just how important that was during this time, and then just in general, I was doing research on you and things that you've done over your career to prep for this podcast. And I found there's two areas that you've kind of led the charge on, and we're ahead of the curve on, and in part helped innovate. One is community led growth and two is content marketing in a big way. And so I wanted to focus a lot of our chat on these two areas. So community led growth, it feels like a very buzzy topic on Twitter. Everyone's always talking about how the future of growth is community. You got to build a community, you got to be community led and all these things. And so I want to try to make this concept concrete and help people understand. Should they invest in community? How can community help you? When does it make sense to when does it not make sense to invest? And so maybe just as a first question, just what is community like growth? What does that actually mean as a concept?"
Headline: What is community led growth?
"Note, and we were talking about stress working with you, and you talked about Notion at a different kind of stress. What's maybe the most stressful memory you have of working at Notion? Whatever you can share."
Headline: What is the most stressful memory of working at Notion?
"'''

summary_prompt_stub = '''
"Early day Notion, I think a lot about just what the environment felt like. This was the first very small start up that I had worked for when I left first round. I really wanted that experience. And the first office that I worked in was really just like a home. It literally had an apartment on top of this kind of loft space. And it just felt like we were a group of people who kind of lived there together during the day. But it had that kind of homes, fun, really warm quality. We all took our shoes off. There was like, beautiful furnishings and rugs, and we would all just sit around and drink tea and work together on these couches. So it really had that feeling to it. And then there were like, little quirks. I like to reminisce with my colleagues who were there at the time that we didn't have like, a great HVAC system. So during the summer it was really hot, and then in the winter, it was really cold and we would have these big industrial fans. And it was just at the time we were like, oh, this is really bizarre. But now it's like one of our favorite memories to talk about. Or for a while we didn't have overhead lighting, so me and my colleagues who were there working really late at night, it would just get darker and darker and darker. And one of my favorite folks there actually had a headlamp that she would switch on at a certain point, a great evening. So that's the stuff that really comes up for me. Like, we were all working really hard and in this thing together, but it's like that team sort of familial quality that stands out to me."
In summary: The office felt like a home and gave everybody the vibe of being a big family. It was common to take your shoes off. Some little quirks make the time even more memorable: There was no HVAC so it would get too hot in summer and too cold in winter. Also there was no overhead lighting so people would bring headlamps for when it got dark.

"Yeah, I think it has become quite buzzy and it's certainly aspirational for a lot of product led growth companies and even those that are maybe a little bit outside of the product Led growth orbit. And we're seeing all of these startups, I think, also come out that are about community and how to enhance that effect in terms of how I think about what it actually is. It's when your community helps you achieve such ubiquity and such name recognition that it actually allows you to start moving up market into the enterprise. And I know that might be very specific to enterprise oriented companies, but that's how we defined it. At notion was the fact that so many people were talking about this, sharing what they had built about it, honestly starting businesses of their own around it, to kind of formalize the relationship with teams. That I think it derisked notion as a choice for a lot of companies just because they had heard about it through so many channels. They had seen it on social media, they've heard about it on a podcast, their friend told them about it, they saw a billboard. All of that lended itself to larger and larger companies and teams buying more and more seats. So I think that's the power that the community had for us and I see that also being analogous to what companies like Figma have been able to achieve."
In summary:  Community led growth is a hot topic for product led growth companies. If executed correctly, your community helps you move up market and close enterprise customers. A strong community derisks your product as a choice for enterprises as they heard about it over so many channels.
""'''

API_KEY = "Pp0haiyiyMTfS4VHPCacV3W27tGF8tK7Bzmoz0dZ"
STOP_SEQ_TOKEN = '"'


def _clean_string(string: str) -> str:
    string = string.replace("\n", " ")
    string = string.replace("\\n", "")
    string = string.replace(STOP_SEQ_TOKEN, "")
    string = string.replace("\\", "")
    string = string.replace("/", " ")
    return string


def process_generation(generation, is_answer):
    gens = []
    likelihoods = []
    for gen in generation.generations:
        if (is_answer and len(gen.text.split(" ")) < 10) or (not is_answer and "?" not in gen.text):
            continue
        gens.append(gen.text)
        sum_likelihood = 0
        for t in gen.token_likelihoods:
            sum_likelihood += t.likelihood
        # Get sum of likelihoods
        likelihoods.append(sum_likelihood)

    pd.options.display.max_colwidth = 200
    # Create a dataframe for the generated sentences and their likelihood scores
    df = pd.DataFrame({'generation': gens, 'likelihood': likelihoods})
    # Drop duplicates
    df = df.drop_duplicates(subset=['generation'])
    # Sort by highest sum likelihood
    df = df.sort_values('likelihood', ascending=False, ignore_index=True)
    print(df)

    text = df.iloc[0]["generation"]
    print(text)
    return _clean_string(text)


def summarize(
    qanda_pairs: List[Tuple[str]],
) -> Tuple[List[str]]:
    headlines = []
    summaries = []
    for i in tqdm(range(len(qanda_pairs))):
        question, answer = qanda_pairs[i]
        headline_prompt = f'''{headline_prompt_stub}{question}"\nHeadline:{STOP_SEQ_TOKEN}'''
        summary_prompt = f'''{summary_prompt_stub}{answer}"\nIn summary:{STOP_SEQ_TOKEN}'''
        co = cohere.Client(API_KEY)
        try:
            headline_prediction = co.generate(
                model="xlarge",
                prompt=headline_prompt,
                max_tokens=50,
                return_likelihoods="GENERATION",
                temperature=0.8,
                stop_sequences=[STOP_SEQ_TOKEN],
                num_generations=5,
                k=0,  # beam search parameter
                p=0.75
            )
            summary_prediction = co.generate(
                model="xlarge",
                prompt=summary_prompt,
                max_tokens=200,
                return_likelihoods="GENERATION",
                temperature=0.8,
                stop_sequences=[STOP_SEQ_TOKEN],
                num_generations=5,
                k=0,  # beam search parameter
                p=0.75
            )
            headlines.append(process_generation(headline_prediction, is_answer=False))
            summaries.append(process_generation(summary_prediction, is_answer=True))
        except Exception as e:
            logging.info(f"{i}th grouped sentence failed due to the following issue")
            logging.info(str(e))
            logging.info(f"Grouped sentence text is {headline_prompt}, and {summary_prompt}.")
            continue
    return headlines, summaries


if __name__ == "__main__":
    file_name_qanda_pairs = "qanda_pairs_c942fd04195599fe23df3b093a8c62ee.mp3.pickle"
    with open(file_name_qanda_pairs, "rb") as f:
        qanda_pairs = pickle.load(f)

    print(qanda_pairs)
    headlines, summaries = summarize(qanda_pairs[1:])
    print(list(zip(headlines, summaries)))
    with open(f'headlines_summaries_{file_name_qanda_pairs.split("_")[-1]}', 'wb') as f:
        pickle.dump((headlines, summaries), f)
