import numpy as np
import pandas as pd
from os import path
from PIL import Image
from sklearn.feature_extraction import text
import matplotlib.pyplot as plt
import spacy
my_stop_words = ["n't", "adderall", "mathadone", "https", "actavis", "opana", "diluadid", "ritalin", "ecstasy", "codeine", "hydrocodone", "morphine", "oxycodone", "hydromorphone", "fentanyl", "oxycontin", "vicodin", "percocet", "xanax"]
my_stop_words = list(text.ENGLISH_STOP_WORDS.union(my_stop_words))
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
df = pd.read_csv("data/opioid_tweets.csv")
with open("bad_tweets.txt", "r") as f:
    bad_ids = [i.strip() for i in f.read().split("\n")]
nlp = spacy.load("en_core_web_sm")



bad_corpus = df["content"][df["id"].isin(bad_ids)].tolist()

clean_bad_docs = []
for doc in nlp.pipe(bad_corpus):
    add = ''
    for tok in doc:
        if tok.pos_ in ["VERB", "ADJ", "ADV", "NOUN"] and not tok.text.startswith("http"):
            add += " " + tok.text
    clean_bad_docs.append(add)


wordcloud = WordCloud(colormap = "RdYlBu",
                      stopwords=my_stop_words,
                      max_font_size=50,
                      max_words=100,
                      background_color="black").generate(" ".join([i for i in clean_bad_docs]))

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Illegal Pharmacies - Most Common Words")
plt.savefig("bad_tweets_wordcloud.png", dpi = 400, bbox_inches = "tight", pad_inches = .5)

good_corpus = df["content"][df["id"].isin(bad_ids) == False].tolist()
clean_good_docs = []
for doc in nlp.pipe(good_corpus):
    add = ''
    for tok in doc:
        if tok.pos_ in ["VERB", "ADJ", "ADV", "NOUN"] and not tok.text.startswith("http"):
            add += " " + tok.text
    clean_good_docs.append(add)

wordcloud = WordCloud(colormap = "RdBu",
                      stopwords=my_stop_words,
                      max_font_size=50,
                      max_words=100,
                      background_color="white").generate(" ".join([str(i) for i in clean_good_docs]))

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Innocent Opioid Tweets - Most Common Words")
plt.savefig("good_tweets_wordcloud.png", dpi = 400, bbox_inches = "tight", pad_inches = .5)
