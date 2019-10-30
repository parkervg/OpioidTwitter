"""
TODO:
    Scrape twitter api search for opiods
        Use geocode in search param to pinpoint popular opiod area?
    Cluster together for topics
    Get top terms for each cluster
    illicit pharmacy cluster?

"""
import os
import twitter
import regex as re
import datetime
import uuid
import nltk
from fuzzywuzzy import fuzz
import psycopg2
import time
os.chdir("/Users/parkerglenn/Credentials")
from twitter_api import *
fmt = "%a %b %d %H:%M:%S %Y"
opiods = ["codeine", "hydrocodone", "morphine", "oxycodone", "hydromorphone", "fentanyl", "oxycontin", "vicodin", "percocet"]

Twitter = twitter.Api(consumer_key = consumer_key,
                      consumer_secret = consumer_secret,
                      access_token_key = access_token_key,
                      access_token_secret = access_token_secret,
                      sleep_on_rate_limit = True)



def SearchTwitter(drug, max_id = None):
    # Connection to DB
    conn = psycopg2.connect(dbname= "opiods", user='parkerglenn', host='localhost')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM Tweets;")
    starting_length = c.fetchall()[0][0]

    results = Twitter.GetSearch(drug, count = 200, lang ="en", max_id = max_id)

    Tweet_IDs = []
    for info in results:
        if not info.retweeted: # Not taking retweets. This makes the corpus messy
            dt_string = re.sub(r"(.*?)(\+\d+ )(\d\d\d\d$)", r"\1\3", info.created_at)
            dt = datetime.datetime.strptime(dt_string, fmt)
            created_at = datetime.datetime.strftime(dt, "%Y/%m/%d")
            user_name = info.user.screen_name
            followers_count = info.user.followers_count
            friends_count = info.user.friends_count
            user_description = info.user.description
            content = info.text
            tweet_id = info.id
            fav_count = info.favorite_count
            url_present = len(info.urls) != 0
            try:
                c.execute("INSERT INTO Tweets(tweet_id, content, created_at, fav_count, url_present, user_name, followers_count, friends_count, user_description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", [tweet_id, content, created_at, fav_count, url_present, user_name, followers_count, friends_count, user_description])
                conn.commit()
                Tweet_IDs.append(tweet_id)
            except:
                # The tweet has already been added. A unique constraint is thrown
                conn.rollback()

    c.execute("SELECT COUNT(*) FROM Tweets;")
    ending_length = c.fetchall()[0][0]
    conn.close()
    print("Added {} tweets pertaining to search {}".format(ending_length - starting_length, drug))
    try:
        return min(Tweet_IDs) - 1
    except ValueError:
        return None


for drug in opiods:
    max_id = SearchTwitter(drug)
    try:
        for i in range(50):
            max_id = SearchTwitter(drug, max_id = max_id)
    except ValueError:
        pass
