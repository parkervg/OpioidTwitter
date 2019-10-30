"""
Create, Drop and Modify tables.
"""
import psycopg2
conn = psycopg2.connect(dbname='opiods', user='parkerglenn', host='localhost')
c = conn.cursor()
c.execute("""DROP TABLE IF EXISTS Tweets CASCADE;""")
c.execute("""DROP TABLE IF EXISTS Users CASCADE;""")
c.execute("""
            CREATE TABLE IF NOT EXISTS Tweets (
                id SERIAL PRIMARY KEY,
                tweet_id bigint UNIQUE,
                content text,
                created_at date,
                fav_count int,
                url_present bool,
                user_name text,
                followers_count int,
                friends_count int,
                user_description text
                );""")

conn.commit()
conn.close()
