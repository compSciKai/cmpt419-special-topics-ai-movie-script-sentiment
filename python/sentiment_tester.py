# sentiment_tester.py

import json
from textblob import TextBlob as tb
from textblob.classifiers import NaiveBayesClassifier
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
import pprint
import nltk
pp = pprint.PrettyPrinter(indent=2)

# lost test/train data
with open('dataset/train_sentiment.json') as json_file:
    unformated_data = json.load(json_file)
    json_file.close()

# extraxt dictionary values from data
data = []
for label in unformated_data.values():
    data.append(tuple(label))

# split into half positive half negative
pos_m_data = []
neg_m_data = []
for label in data:
    if label[1] == 'neg':
        neg_m_data.append(label)
    else:
        pos_m_data.append(label)

print('number of positive labels:', len(pos_m_data))    # 42
print('number of negative labels:', len(neg_m_data))    # 56

# extract movie_review data from:
# https://textblob.readthedocs.io/en/dev/_modules/textblob/en/sentiments.html#NaiveBayesAnalyzer
print('Training models...')
neg_ids = nltk.corpus.movie_reviews.fileids('neg')
pos_ids = nltk.corpus.movie_reviews.fileids('pos')
neg_feats = [(NaiveBayesAnalyzer().feature_extractor(
    nltk.corpus.movie_reviews.words(fileids=[f])), 'neg') for f in neg_ids]
pos_feats = [(NaiveBayesAnalyzer().feature_extractor(
    nltk.corpus.movie_reviews.words(fileids=[f])), 'pos') for f in pos_ids]

# split into train and test
#train_manual = data[:69]
train_manual = neg_m_data[105:] + pos_m_data[105:]
train_mrc = neg_feats + pos_feats #+ train_manual
#test_data  = data[69:]
test_data  = neg_m_data[:105] + pos_m_data[:105]

# create model
print('Testing models...')
cl = NaiveBayesClassifier(train_manual)
cl_2 = NaiveBayesClassifier(train_mrc)

# calculate score
score = round(cl.accuracy(test_data)*100, 3)
score_2 = round(cl_2.accuracy(test_data)*100, 3)
print('Classifier 1 (EmotionPix) is', str(score) + '% accurate.')
print('Informative Features:')
print(cl.show_informative_features(10))
print('Classifier 2 (NaiveBayes w/ movie review corpus) is', str(score_2) + '% accurate.')
print('Informative Features:')
print(cl_2.show_informative_features(10))
