# sentiment_sorter.py

# imports
import json
from tqdm import tqdm
import pprint
pp = pprint.PrettyPrinter(indent=2)

def save(data_to_save, where):
    with open(where, 'w') as json_file_export:
        json.dump(data_to_save, json_file_export, indent=2)
        json_file_export.close()

# load script data
print('Loading script sentiment data...')
with open('dataset/script_sentiment_data.json') as json_file:
    script_data = json.load(json_file)
    json_file.close()

# create list of movies w/ sentiment
print('\nExtracting sentiment values...')
mov_sentiment_vals = {}
for i in tqdm(range(len(script_data['scripts']))):
    script = script_data['scripts'][i]
    if script['manually remove'] == False and script['Movie Sentiment']['polarity'] != 0.0:
        mov_sentiment_vals[script['name']+' ('+script['year']+')'] = script['Movie Sentiment']['polarity']
    #mov_sentiment_vals[script['Movie Sentiment']['polarity']] = script['name']
print('\nRemoving movies without enough dialog data...')

# Sort
print('\nSorting sentiment values from most negative to most positive...')
sorted = {k: v for k, v in sorted(mov_sentiment_vals.items(), key=lambda item: item[1])}
#pp.pprint(sorted)
#print(sorted)

# Save
print('\nSaving list of movies sorted by sentiment to \'sorted_sentiment.json\'')
save(sorted, 'dataset/sorted_sentiment.json')
