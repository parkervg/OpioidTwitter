# OpioidTwitter
## Tasks:
https://docs.google.com/document/d/1AHY9714oP3lTTIEBICok4gSd_j3d00SYlW8ARfqc2q8/edit?usp=sharing

# Abstract

# Motivation
“The United States is in the midst of a drug crisis with fatal consequences. Drug overdoses have become the leading cause of injury death and have more than tripled between 1999 and 2017. There were more than 70,000 confirmed drug overdose deaths in 2017, and of those, more than 47,000 involved an opioid.1”. There are many mediums through which drugs are acquired, and online pharmacies are one. In 2015 alone, the World Health organization estimates, “50% of the drugs for sale on the internet are fake… did not comply with NABP patient safety and pharmacy practice standards or US state and federal laws.2 ” These pharmacies take to social media, advertising to teens drugs that can potentially lead to death. With so much at risk there has been a question of how to stop the selling of illicit drugs on media platforms and one we aim to solve. Using methods from data science we aim to observe tweets that are selling drugs and build a model that will detect them, flagging them for removal. 
# Discussion:

## Methodology - Data Cleaning

Data was scraped using the Twitter API. Keywords from a list of 9 prevalent opioids (codeine, hydrocodone, morphine, oxycodone, hydromorphone, fentanyl, oxycontin, vicodin, and percocet) were entered in Twitter’s search endpoint, and the tweet content and metadata was scraped and stored in a Postgresql database (insert table of data).
|    |          |                                                                                                                                                |            |           |             |             |                 |               | 
|----|----------|------------------------------------------------------------------------------------------------------------------------------------------------|------------|-----------|-------------|-------------|-----------------|---------------| 
| id | tweet_id | content                                                                                                                                        | created_at | fav_count | url_present | user_name   | followers_count | friends_count | 
| 3  | 1.18E+18 | Three #Chinese nationals were charged with importing and distributing #Fentanyl as part of an international drug op‚Ä¶ https://t.co/pF6AlZf2wW | 10/10/19   | 164       | TRUE        | EpochTimes  | 134594          | 102           | 
| 4  | 1.18E+18 | Boston is using a chemical warfare device to help fight fentanyl https://t.co/gqJURUHwnH via @commonhealth                                     | 10/11/19   | 0         | TRUE        | BUSPH       | 27642           | 2202          | 
| 5  | 1.18E+18 | Dana Point Rehab Campus CEO Michael Castanon Discusses the Fentanyl Crisis on CBS-LA https://t.co/tYigh2TJOG                                   | 10/11/19   | 0         | TRUE        | feed_stocks | 357             | 103           | 
| 9  | 1.18E+18 | @Praying_Medic China has to put an end to the manufacturing of illicit fentanyl or NO DEAL!!                                                   | 10/11/19   | 0         | FALSE       | MesiaArte   | 1286            | 1080          | 

Data sets are often “unclean” or could be expanded upon. Our data set was the same, within our data every tweet contains an abbreviated twitter link. To make a more robust dataset, we decided to expand these local URLs to global URLs. Using the “requests” library we were able to expand the URLs of over 40,000 tweets. There were many difficulties when doing this, for instance twitter servers deny requests when attempting to access so many of them, and the “get” function is slow. With no way around this, we had to use a virtual machine to free up our PCs’.  
    GCP - Compute engine: Google Cloud Platform offers many services that are beneficial to data enthusiasts. Using Compute Engine we were able to: push and pull to github, and run scripts on this virtual machine. It is with this we ran the code to extend the URLS and then classify them as going to twitter, or to and outside source. 


## NLP Tasks
#### Text Pre-Processing
With help from Parker, we were pointed in the direction of using a TFIDF matrix to create quantitative data from text.To do so we used methods from Brandon Rose. Using lemmatization to change words from third person to first. Stemming to take the roots of each word and changing past tense to present tense. In Tokenization we discard punctuation and break down our stings. Lastly we preprocess the data, getting rid of hashtags, words that are less than two letters and anything we did not want in each string. With all of this we could now use SKlearn’s “tfidfvectorizer” to show how important each word is to our documents and move into other methods such as clustering or topic modeling. 

#### Clustering 
K-means is a very popular way of exploring data. In our project we decided to use K Means Clustering to see some differences in our data. As you probably know, K-means looks for groups in data and tries to minimize the euclidean distance of each centroid. Unfortunately it is not easy to pick the amount of centroids we want, and the traditional elbow method would not work for our data. So we used two other methods, Brendan used the “Scoring” method and Branden used the “BIC” method…. Insert brief explanations and how we attained these methods and what they do. 

#### LDA

#### BTM
All the above tasks are traditional statistical methods for discovering patterns in text. However, they only have power when the number of words is large. In the case of tweets, the number of words per tweet is heavily outweighed by the number of words in the dictionary. The fundamental reason lies in that conventional topic models implicitly capture the document-level word co-occurrence patterns to reveal topics,and thus suffer from the severe data sparsity in short documents. One can circumvent the data sparsity problem by aggregating all the short texts into one long text before training LDA. However, this method is extremely data dependent and may vary heavily from one collection of data to the next. This method also suffers from the fact that the body of text will be imbalanced from those users with many tweets and those with just one or two. Bi-term topic modeling is, as described in the original paper: “[...] [BTM] learns topics over short texts by directly modeling the generation of biterms in the whole corpus. Here, a biterm is an unordered word-pair co-occurred in a short context” (Yan 2013). This model is effective because it models biterm co-occurrence patterns in the entire corpus, rather than patterns within the document.

## Classification Tasks

#### Random Forest
After exploring the data, we aimed to build a model that would detect the tweets that were selling drugs, we first decided to use a random forest because it does well with imbalanced data sets. A random forest is a decision tree that looks at the most important predictors, and attempts to lead us to the correct response. Using only the tf-idf matrix, we attempted to create a model but ran into an issue it was too precise. It classified most things as not selling illicit drugs and since most of the data was not selling illicit drugs, it achieved a high score. In order to combat this we attempted upsampling, downsampling, synthetic sampling, and we even added an extra attribute to our matrix. Nothing worked well due to the how imbalanced the data set was so we decided to use a model that is more suited for anomaly detection, the Variational autoencoder. 

#### Variational Autoencoder (VAE)
Autoencoders are a type of neural network often used for compression. The inputs the network is trained on is a subset of the domain that the autoencoder should be able to compress and the expected output is the same as the input. The key to an autoencoder is that the hidden layers get progressively smaller and then progressively bigger. This means that the network has to learn a representation of the data that will preserve all the information(so that it can be decompressed in the following layers and give the correct output), but takes up less space than the actual input. We used restoration loss for our autoencoder. Autoencoders work well for anomaly detection. A well trained autoencoder that is unable to reproduce the input data in the output layers indicates that the data was not something the network encountered when it was trained and was thus one for which it was unable to learn a limited representation. We trained the network on more than 10000 inputs/tweets. Each of which had information regarding the number of followers the person tweeting had, number of people the person tweeting follows, whether the tweet leads to an outside url, and of course, all the values of the TF-IDF matrix of the tweet.
(include picture of autoencoder)

