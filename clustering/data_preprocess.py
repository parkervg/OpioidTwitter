#!/usr/bin/python
# coding: utf-8
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import tensorflow as tf
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
from sklearn.feature_extraction import text
from tqdm import tqdm

import json

input_path = '../data/'
train_dataframe = pd.read_csv(input_path + 'opioid_tweets.csv')
my_stop_words = text.ENGLISH_STOP_WORDS.union(["codeine", "hydrocodone", "morphine", "oxycodone", "hydromorphone", "fentanyl", "oxycontin", "vicodin", "percocet","https", "ve"])
docs = train_dataframe.content.astype(str)

td_idf_vec = TfidfVectorizer(stop_words=my_stop_words, max_features = 20000)
X = td_idf_vec.fit_transform(docs)
X_norm = normalize(X)
X_arr = X_norm.toarray()

# PCA TRANSFORMATION, HOWEVER NOT GOOD FOR TEXT SINCE WE DON'T WANT TO CONVERT A SPARSE MATRIX TO A DENSE ONE
# data_pca = PCA(n_components = 2)
# response_skl = data_pca.fit_transform(X_arr)

# SVD IS PREFERRED HERE AND TRUNCATED SVD WORKS ON TERM COUNT/TF-IDF MATRICES AS RETURNED BY THE VECTORIZER, THIS IS LATENT SEMANTIC ANALYSIS
data_svd = TruncatedSVD(n_components = 250) #BEST VALUE FOR TIME-COMPLEXITY IS N=250
response_svd = data_svd.fit_transform(X_arr)
#var_explained = data_svd.explained_variance_ratio_.sum()

# TESTING FOR THE OPTIMAL NUMBER OF K CLUSTERS FOR THE KMEANS MODEL
# number_clusters = range(1, 20) # BEST ONE WAS 4-7
# max_iter_number = range(1, 1000, 100) # BEST ONE WAS 100
# kmeans = [KMeans(n_clusters=4, max_iter = i) for i in tqdm(max_iter_number)]
# score = [kmeans[i].fit(response_svd).score(response_svd) for i in tqdm(range(len(kmeans)))]
# PLOTTING ELBOW PLOT
# plt.plot(max_iter_number, score)
# plt.xlabel('Number of Clusters')
# plt.ylabel('Score')
# plt.title('Elbow Method')
# plt.show()

k_value = 4
kmeans = MiniBatchKMeans(n_clusters=k_value, batch_size = 100, init= 'k-means++', max_iter = 100, algorithm = 'auto')
fitted_values = kmeans.fit(response_svd)
predicted_values = kmeans.predict(response_svd)

def get_top_features_cluster(tf_idf_array, prediction, n_feats):
    labels = np.unique(prediction)
    dfs = []
    for label in labels:
        id_temp = np.where(prediction==label) # indices for each cluster
        x_means = np.mean(tf_idf_array[id_temp], axis = 0) # returns average score across cluster
        sorted_means = np.argsort(x_means)[::-1][:n_feats] # indices with top 20 scores
        features = td_idf_vec.get_feature_names()
        best_features = [(features[i], x_means[i]) for i in sorted_means]
        df = pd.DataFrame(best_features, columns = ['features', 'score'])
        dfs.append(df)
    return dfs
dfs = get_top_features_cluster(X_arr, predicted_values, 15)
print(dfs)
