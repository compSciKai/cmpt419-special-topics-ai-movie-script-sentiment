# create_dialog_list.py

import json
import pprint
from textblob import TextBlob as tb
from textblob.sentiments import NaiveBayesAnalyzer
pp = pprint.PrettyPrinter(indent=4)

with open('dataset/script_data.json') as json_file:
    data = json.load(json_file)

dialog = []

for script in data['scripts']:
    if script['scenes exist'] and script['characters exist']:
        for scene in script['scenes'].values():
            if scene['Context']:
                for context in scene['Context']:
                    dialog_text = " ".join(context['Text'])
                    dialog.append(dialog_text)

print(len(dialog), 'instances of character dialog')

# export
print("\nSaving dialog list to \'dialog_data.json\'")
with open('dataset/dialog_data.json', 'w') as json_file_export:
    json.dump(dialog, json_file_export, indent=4)


