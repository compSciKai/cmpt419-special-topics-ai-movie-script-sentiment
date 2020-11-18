# script_clip_matcher.py

# imports
import os
import json
from tqdm import tqdm

def save(data_to_save, where):
    with open(where, 'w') as json_file_export:
        json.dump(data_to_save, json_file_export, indent=2)
        json_file_export.close()

# load script data & sentiment labels
print('Loading script & sortend sentiment data...')
with open('dataset/script_sentiment_data.json') as json_file:
    script_data = json.load(json_file)
    json_file.close()
with open('dataset/sorted_sentiment.json') as json_file:
    sentiment_labels = json.load(json_file)
    json_file.close()

# Get list of movies with clips
print('\nGetting movie clip names...')
path = './dataset/movie_clips'
movies = []
for r, d, f in os.walk(path):
    for dir in d:
        movies.append(dir)

# Find Movies that have extracted script dialog and have movie clips
selected_movies = []
print('\nMatching movie clips & scripts')
for i in tqdm(range(len(script_data['scripts']))):
    script = script_data['scripts'][i]
    key = script['name'] + '_' + script['year']
    key_clip = key.replace(' ', '_')
    key_sentiment = script['name']+' ('+script['year']+')'
    if key_clip in movies and key_sentiment in sentiment_labels:
        selected_movies.append(script)

print('\n' + str(len(selected_movies)) + ' Movies with scripts and clips.')

# save data
print('\nSaving filtered script data...')
data = { "movies": selected_movies }
save(data, 'dataset/filtered_script_data.json')
