# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 13:54:30 2019

@author: JungleBook
"""
import requests as rq
import re
import pandas as pd 

df = pd.read_csv("data/opioid_tweets_new.csv")

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

   

shortened_url = df['short_url'];
unshortened_url = df['unshortened_url'].fillna("N/A") 
#when importing the csv, some values of "N/A" change to nan. The above line corrects this
df['unshortened_url'] = unshortened_url



print("Starting the first url get")
j = 0
for i in range(len(unshortened_url)):
    if unshortened_url[i] == "Redo":
        j = j + 1
print("The total amount of redos is " + str(j) )


j = 0 
for i in range(len(unshortened_url)):
    if unshortened_url[i] == "Redo":
        j = j +1
        unshortened_url[i] = unshorten(shortened_url[i]) 
        print(str(j) + " " + str(i) )
        #Some times the script will stop in random places, I used the
        #above print to locate where it does stop.
        #Using this I was able to fix the nan errors
        
print("Starting the second url grab")
j = 0
for i in range(len(unshortened_url)):
    if unshortened_url[i] == "Redo":
        j = j + 1
        print(str(j) + " " + str(i) )
        

for i in range(len(unshortened_url)):
    if unshortened_url[i] == "Redo":
        unshortened_url[i] = unshorten(shortened_url[i])

df['unshortened_url'] = unshortened_url

twitter_url = []
print("Starting the twitter classification")
for text in unshortened_url:
       twitter_url.append(twitter(text))
       
df['twitter_url'] = twitter_url



df.to_csv("data/opioid_tweets_clean.csv")   
print("Done") 


 
