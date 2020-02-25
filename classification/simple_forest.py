import pandas as pd
import sklearn
import os
from sklearn.ensemble import RandomForestClassifier

"""
Look into auto-encoder model for anomaly detection.
"""

df = pd.read_csv("data/opioid_tweets.csv")
with open("bad_tweets.txt", "r") as f:
    bad_ids = [i.strip() for i in f.read().split("\n")]

def success(*kwargs):
    for column in kwargs:
        print("Scores for model", column)
        print("Classification accuracy:", sklearn.metrics.accuracy_score(output.Actual, output[column]))
        print("F1 score:", sklearn.metrics.f1_score(output.Actual, output[column], average = "micro"))
        print("Precision:", sklearn.metrics.precision_score(output.Actual, output[column], average = "micro"))
        print("Matthews coefficient:", sklearn.metrics.matthews_corrcoef(output.Actual, output[column]))
        print()
def success2(*kwargs):
    for column in kwargs:
        print("Scores for model", column)
        print("Classification accuracy:", sklearn.metrics.accuracy_score(output2.Actual, output2[column]))
        print("F1 score:", sklearn.metrics.f1_score(output2.Actual, output2[column], average = "micro"))
        print("Precision:", sklearn.metrics.precision_score(output2.Actual, output2[column], average = "micro"))
        print("Matthews coefficient:", sklearn.metrics.matthews_corrcoef(output2.Actual, output2[column]))
        print()

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import sklearn.pipeline

def is_bad(id):
    if id in bad_ids:
        return True
    else:
        return False

df = df.fillna("")
df["is_bad"] = df["id"].apply(lambda x: is_bad(x))
train, test = sklearn.model_selection.train_test_split(df)
output = pd.DataFrame(
    {
        "Content": test.content,
        "Actual": test.is_bad
    })

vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(stop_words = "english")
clf = RandomForestClassifier(n_estimators=80)
default_pipeline = sklearn.pipeline.make_pipeline(
    vectorizer,
    clf,
)
default_pipeline.fit(train.content,train.is_bad)
output["default_RF"] = default_pipeline.predict(test.content)

success("default_RF")

output[output["default_RF"] == True]
output[(output["default_RF"] == False) & (output["Actual"] == True)]
