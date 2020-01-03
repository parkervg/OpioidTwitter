import pandas as pd

df = pd.read_csv("data/opioid_tweets.csv")

with open("bad_tweets.txt", "r") as f:
    ids = [i.strip() for i in f.read().split("\n")]

for item in df[df["id"].isin(ids)].iterrows():
    print()
    print("ID: {}".format(item[1]["id"]))
    print()
    print(item[1]["content"])
    print()
    print("User: {}".format(item[1]["user_name"]))
    print("_____________________________________________________________________________________________")
