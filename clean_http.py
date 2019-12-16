# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 23:25:50 2019

@author: JungleBook
"""
import requests as rq
import re
import pandas as pd
import time
total_time = time.time() 

df = pd.read_csv("data/opioid_tweets.csv")

pattern = re.compile(r"https?://t.co[\.A-Za-z0-9/]*\s*");
# best to define this outside of the definition, saving time.

def url_present(url):
    url = url 
    match = pattern.findall(url)
    if len(match) != 0:
        return "True", match[0]
    else: 
        return "False", "False"
       

def unshorten(url):
    url = url 
    try:
        r = rq.get(url);
        if int(r.status_code/100) ==  3: # int() will change any float that leads in 3 to an integer.
            if r.url != 'https://twitter.com/account/suspended':
                return r.url
            else:
                return "N/A"
                
        elif int(r.status_code/100) == 4:
            return "N/A"
        elif int(r.status_code/100) == 5:
            return "N/A"
        elif int(r.status_code/100) == 1:
            return "Redo"
            
        else:
            if r.url != 'https://twitter.com/account/suspended':
                return r.url
            else:
                return "N/A"
    except: 
        return "Redo"
#Had to use: try, except because the server times out giving me an error
# I cannot fix immediately 


df = df[ df['url_present'] == 'TRUE'] # pulls items in the df only if the condition for column url_present is met
 
df = df.drop(columns = 'url_present' )
df = df.reset_index(drop = True)

has_url = []
shortened_url = []

for text in df['content']:
    present, url = url_present(text)
    has_url.append(present);
    shortened_url.append(url);
    
    
df['url_present'] = has_url
df['short_url'] = shortened_url 
print(df.head())

df = df[ df['url_present'] == 'True'] 
df = df.drop(columns = 'url_present' )
df = df.reset_index(drop = True)



unshortened_url = []
for text in df['short_url']:
    unshortened_url.append(unshorten(text))

df['unshortened_url'] = unshortened_url
 
df = df[ df['unshortened_url'] != 'N/A']
df = df.reset_index(drop = True)
df.to_csv("data/opioid_tweets_new.csv")#Saving my work, just in case

unshortened_url = df['unshortened_url']

i= 0
for text in df['unshortened_url']:
    if text == "Redo":
        unshortened_url[i] = unshorten(text)
    i = i + 1 
    
# After this the same exact, "Redo"s where giving me error, and very long
    #errors if I followed it in my browser
#Finna Drop them
#Only dropping like 10 items 
df['unshortened_url'] = unshortened_url
df = df[ df['unshortened_url'] != 'Redo']
df = df.reset_index(drop = True) 

df.to_csv("data/opioid_tweets_clean.csv")   
print("Total time is" + str(total_time) )
#Took me 4 hours from start of epoch