library(BTM)
# For this BTM package, we need the document ID in the column, and each row is a term
List <- strsplit(as.character(opi_inc_stemmed_data$V2), split = '\\s')
x_frame <- data.frame(doc_id=rep(opi_inc_stemmed_data$V1, sapply(List, length)), lemma=unlist(List))
# We apply the biterm topic model to our new dataframe
set.seed(321)
#this will take a while to perform gibbs sampling (warning_)
model <- BTM(x_frame, k = 20, beta = 0.01, iter = 1000, trace = 100)

model$phi
topicterms <- terms(model, top_n = 15)
topicterms
scores <- predict(model, x_frame, type = "sum_b")

opi_inc_stemmed_data$V2[scores[,15] > 0.50]
opioid_tweets