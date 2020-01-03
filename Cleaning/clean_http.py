# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 23:25:50 2019

@author: JungleBook
"""
import requests as rq
import re
import pandas as pd 

df = pd.read_csv("data/opioid_tweets.csv")

pattern = re.compile(r"https?://t.co[\.A-Za-z0-9/]*\s*");
to_twitter = re.compile(r"https?://twitter.com[\.A-Za-z0-9/]*\s*")
# best to define this outside of the definition, saving time.

def url_present(text): 
    match = pattern.findall(text)
    if len(match) != 0:
        return True, match[0]
    else: 
        return False, False
       

def unshorten(url):
    try:
        if url != False:
            r = rq.get(url);# Should now be the "real" url
            if r.url == "www.newssummedup.com":
                return "Contains a virus"
            if int(r.status_code/100) ==  2: # int() will change any float that leads in 3 to an integer.
                if r.url == 'https://twitter.com/account/suspended':
                    return "Suspended"
                else:
                    return r.url
                    
            elif int(r.status_code/100) == (5 or 1):
                return "Redo"
            else: 
                return False
        else:
            return "N/A"
    except: 
        return "Redo"
#Had to use: try, except because the server times out giving me an error
# I cannot fix immediately 

def twitter(url):
    
    if type(url) != bool:
       if url == "Suspended":
           return True
       elif url == "N/A":
           return "N/A"
       elif url == "Redo":
           return "Redo"
       r = to_twitter.findall(url)
       if r != 0:        
           return( True)
       else:
           return False
    else:
         return False




# Need to keep all Trues and False
df = df[ (df['url_present'] == 'TRUE') | (df['url_present'] == 'FALSE') ]
df.reset_index(drop = True)
# In addition, we need to mark Suspended accounts. 
df.to_csv("data/opioid_tweets_corrected.csv")


# If it leads to a twitter URL, Mark it as false
has_url = []
shortened_url = []

for text in df['content']:
    present, url = url_present(text)
    has_url.append(present);
    shortened_url.append(url);
    
  

df['url_present'] = has_url #Should be correct now
df['short_url'] = shortened_url 



unshortened_url = [];
for text in df['short_url']:
    unshortened_url.append(unshorten(text))



unshortened_url = df['unshortened_url'] 
df['unshortened_url'] = unshortened_url
df.to_csv("data/opioid_tweets_new.csv")#Saving my work, just in case
df = df.drop(columns = 'unshortened_url')  

shortened_url = df['short_url'];
for i in range(len(unshortened_url)):
    if unshortened_url[i] == "Redo":
        unshortened_url[i] = unshorten(shortened_url[i])

for i in range(len(unshortened_url)):
    if unshortened_url[i] == "Redo":
        unshortened_url[i] = unshorten(shortened_url[i])


df['unshortened_url'] = unshortened_url
df['unshortened_url'] = df['unshortened_url'].fillna("N/A")

twitter_url = []
for text in unshortened_url:
    twitter_url.append(twitter(text))
    
df['twitter_url'] = twitter_url



df.to_csv("data/opioid_tweets_clean.csv")   
print("Done")