# sentiment_labeler.py

'''
Creates a dialog sentiment dictionary
Dictionary can be used to annotate script_data
'''

import json
from textblob import TextBlob as tb
from textblob.classifiers import NaiveBayesClassifier
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
import pprint
import nltk
import numpy as np
from tqdm import tqdm
pp = pprint.PrettyPrinter(indent=2)

def save(data_to_save, where):
    with open(where, 'w') as json_file_export:
        json.dump(data_to_save, json_file_export, indent=4)
        json_file_export.close()

# load train data
print("Loading traing sentiment data & dialog list data...")
with open('dataset/train_sentiment.json') as json_file:
    unformated_data = json.load(json_file)
    json_file.close()

# load dialog list
with open('dataset/dialog_data.json') as json_file:
    dialog_data = json.load(json_file)
    json_file.close()

# extract dictionary values from data
data = []
for label in unformated_data.values():
    data.append(tuple(label))

# init dialog variables
n_data = np.array(dialog_data)
dialog = []
dialog_dict = {}
length = len(n_data)

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


# split into train and test
print('Training model...')
train_manual = neg_m_data + pos_m_data

# create model
print('Annotating Dialog...')
cl = NaiveBayesClassifier(train_manual)

# classify dialog
blob = Blobber(classifier=cl)

for i in tqdm(range(length)):
    sentiment = np.array([])
    dialog_text = n_data[i]
    b = blob(n_data[i])
    for sentence in b.sentences:
        sentiment = np.append(sentiment, str(sentence.sentiment))
    dialog_dict[n_data[i]] = sentiment.tolist()

print("\nSaving EmotionPix custom classifier sentiment data to 'dialog_sentiment_custom.json'.")
save(dialog_dict, 'dataset/dialog_sentiment_custom.json')
print('Complete.')
