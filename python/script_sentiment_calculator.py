# script_sentiment_calculator.py

# imports
import json
import pprint
from tqdm import tqdm
pp = pprint.PrettyPrinter(indent=2)

# functions

def save(data_to_save, where):
    with open(where, 'w') as json_file_export:
        json.dump(data_to_save, json_file_export, indent=4)
        json_file_export.close()

def extract(sentiment):
    sentiment_list = []
    sentiment_str = sentiment.replace('Sentiment', '').replace('polarity=', '')\
        .replace('subjectivity=', '').replace('(', '').replace(')', '')
    sentiment_tuple = tuple(map(float, sentiment_str.split(', ')))
    return round(sentiment_tuple[0], 3), round(sentiment_tuple[1], 3) # return polarity, subjectivity

# load sentiment dictionary & script data
print("Loading dialog & script data...")
with open('dataset/dialog_sentiment_custom.json') as json_file:
    sentiment_dict = json.load(json_file)
    json_file.close()

with open('dataset/script_data.json') as json_file:
    script_data = json.load(json_file)
    json_file.close()

# for each dialog: label sentiment polarity & subjectivitg
print('\nlabeling dialog sentiment polarity & subjectivity in scripts...')
for i in tqdm(range(len(script_data['scripts']))):
    script = script_data['scripts'][i]
    if script['scenes exist'] and script['characters exist']:
        for scene in script['scenes'].values():
            if scene['Context']:
                for context in scene['Context']:
                    dialog_text = " ".join(context['Text'])
                    # label sentiment
                    if dialog_text in sentiment_dict:
                        context['Sentence Sentiment'] = sentiment_dict[dialog_text]
                    else:
                        context['Sentence Sentiment'] = []

# for each scene: aggregate & average polarity & subjectivity
print('\nAggregating & averaging scene polarity & subjectivity in scripts...')
for i in tqdm(range(len(script_data['scripts']))):
    script = script_data['scripts'][i]
    if script['scenes exist'] and script['characters exist']:
        for scene in script['scenes'].values():
            # init vars
            sentiment_count = 0
            sentiment_sum = 0
            subjectivity_sum = 0
            if scene['Context']:
                for context in scene['Context']:
                    for sentiment in context['Sentence Sentiment']:
                        polarity, subjectivity = extract(sentiment)
                        if polarity != 0:
                            sentiment_count += 1
                            sentiment_sum += polarity
                            subjectivity_sum += subjectivity
            if sentiment_count != 0:
                scene['Scene Sentiment'] = { "polarity": round(sentiment_sum/sentiment_count, 3),
                        "subjectivity": round(subjectivity_sum/sentiment_count, 3) }
            else:
                scene['Scene Sentiment'] = { "polarity": 0.0,
                        "subjectivity": 0.0 }

# for each movie: aggregate & average polarity & subjectivity
print('\nAggregating & averaging Movie polarity & subjectivity in scripts...')
for i in tqdm(range(len(script_data['scripts']))):
    # init vars
    sentiment_count = 0
    sentiment_sum = 0
    subjectivity_sum = 0
    script = script_data['scripts'][i]
    if script['scenes exist'] and script['characters exist']:
        for scene in script['scenes'].values():
            if scene['Scene Sentiment']['polarity'] != 0:
                sentiment_count += 1
                sentiment_sum += scene['Scene Sentiment']['polarity']
                subjectivity_sum += scene['Scene Sentiment']['subjectivity']
    if sentiment_count != 0:
        script['Movie Sentiment'] = { "polarity": round(sentiment_sum/sentiment_count, 3),
                "subjectivity": round(subjectivity_sum/sentiment_count, 3) }
    else:
        script['Movie Sentiment'] = { "polarity": 0.0,
                "subjectivity": 0.0 }

# save new script dataset
print("\nSaving updated script dataset to 'script_sentiment_data'...")
save(script_data, 'dataset/script_sentiment_data.json')
