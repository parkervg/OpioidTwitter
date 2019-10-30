import pandas as pd
import psycopg2
conn = psycopg2.connect(dbname='opiods', user='parkerglenn', host='localhost')

df = pd.read_sql("select * from Tweets", conn)
df.to_csv("opioid_tweets.csv", encoding = "utf-8")
