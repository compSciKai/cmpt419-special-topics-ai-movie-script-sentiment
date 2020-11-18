# sentiment_classifier.py
import json
import pprint
from textblob import TextBlob as tb
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Blobber
from tqdm import tqdm
import numpy as np
pp = pprint.PrettyPrinter(indent=4)

def save(data_to_save, where):
    with open(where, 'w') as json_file_export:
        json.dump(data_to_save, json_file_export, indent=4)
        json_file_export.close()

# load dialog data from list
print("Loading dialog list...")
with open('dataset/dialog_data.json') as json_file:
    data = json.load(json_file)
    json_file.close()

n_data = np.array(data)
dialog = []
dialog_dict = {}
#length = len(data[:3])
length = len(n_data)
#blob = tb(analyzer=NaiveBayesAnalyzer())
blob = Blobber(analyzer=NaiveBayesAnalyzer())
print("\nClassifying each dialog sentence with positive & negative sentiment")
print("using textblob's default NaiveBayesAnalyzer... (uses movie review corpus)")

for i in tqdm(range(length)):
    sentiment = np.array([])
    dialog_text = n_data[i]
    #blob = tb(n_data[i], analyzer=NaiveBayesAnalyzer())
    b = blob(n_data[i])
    for sentence in b.sentences:
        sentiment = np.append(sentiment, str(sentence.sentiment))
    #arr = np.array([n_data[i], sentiment])
    dialog_dict[n_data[i]] = sentiment.tolist()

#pp.pprint(dialog_dict)
print("\nSaving sentiment data to 'dialog_sentiment_nb.json'")
save(dialog_dict, 'dataset/dialog_sentiment_nb.json')

'''
for i in tqdm(range(len(data['scripts']))):
    script = data['scripts'][i]
    if script['scenes exist'] and script['characters exist']:
        for scene in script['scenes'].values():
            if scene['Context']:
                for context in scene['Context']:
                    dialog_text = " ".join(context['Text'])
                    dialog.append(dialog_text)
                    #blob = tb(dialog_text, analyzer=NaiveBayesAnalyzer())
                    blob_reg = tb(dialog_text)
                    sentiment = []
                    sentiment_reg = []
                    for sentence in blob.sentences:
                        sentiment.append(str(sentence.sentiment))
                    for sentence in blob_reg.sentences:
                        sentiment_reg.append(str(sentence.sentiment))
                    context['Text Sentiment (pa)'] = sentiment_reg
                    context['Text Sentiment (nb)'] = sentiment
                    if i%100 == 0 and i != 0:
                        save(dialog, 'dataset/dialog_data.json')
                        #save()
'''

'''
test_string = dialog[3400]
for sentence in blob.sentences:
    print('NaiveBayes:')
    print(sentence)
    print(sentence.sentiment)
print('--------------------------------------')
for sentence in blob_reg.sentences:
    print('PaternAnalyzer:')
    print(sentence)
    print(sentence.sentiment)
#for text in dialog:
'''



