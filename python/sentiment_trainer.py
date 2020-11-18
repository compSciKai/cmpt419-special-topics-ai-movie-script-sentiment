# sentiment_trainer.py

import random
import json
import keyboard
import time
from textblob import TextBlob as tb
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Blobber
import pprint
pp = pprint.PrettyPrinter(indent=4)

with open('dataset/dialog_data.json') as json_file:
    dialog_data = json.load(json_file)
    json_file.close()

with open('dataset/train_sentiment.json') as json_file:
    labels = json.load(json_file)
    json_file.close()

with open('dataset/untrainable_sentiment.json') as json_file:
    cant_label = json.load(json_file)
    json_file.close()

blob = Blobber(analyzer=NaiveBayesAnalyzer())
not_finished = True


while not_finished:
    # randomly select dialog and choose which sentence to label
    not_new = True
    while not_new:
        r_dialog = random.choice(dialog_data)
        if r_dialog in labels or r_dialog in cant_label or r_dialog == "":
            continue
        else: not_new = False

    b = blob(r_dialog)
    length = len(b.sentences)
    chosen_sentence = ''
    q = False
    n = False
    sent_selected = False
    one_sentence = False
    ind = -1

    # If dialog has one sentence
    if length == 1:
        one_sentence = True
        chosen_sentence = b.sentences[0]

    # otherwise select a sentence
    else:
        print('\n--------------------------------------\nPlease choose a sentence to classifiy:\n--------------------------------------\n')
        for i in range(length):
            print('[' + str(i+1) + ']: ' + str(b.sentences[i]))

        print('\n - Press the sentence number to label\n - Or \'n\' key to move to next dialog\n - Or \'q\' key to save and quit for now.')

        # wait for key input
        print('')
        while n != True:
            dialog_input = input()
            # if quiting
            if dialog_input == 'q':
                print('\nSaving and quiting...')
                q = True
                break
            # if dialog not labelable
            if dialog_input == 'n':
                print('\nMoving to next label...')
                n = True
                break
                # if key selected
            if dialog_input == '1' and length >= 1:
                ind = 1-1
                sent_selected = True
                break
            if dialog_input == '2' and length >= 2:
                ind = 2-1
                sent_selected = True
                break
            if dialog_input == '3' and length >= 3:
                ind = 3-1
                sent_selected = True
                break
            if dialog_input == '4' and length >= 4:
                ind = 4-1
                sent_selected = True
                break
            if dialog_input == '5' and length >= 5:
                ind = 5-1
                sent_selected = True
                break
            if dialog_input == '6' and length >= 6:
                ind = 6-1
                sent_selected = True
                break
            if dialog_input == '7' and length >= 7:
                ind = 7-1
                sent_selected = True
                break
            if dialog_input == '8' and length >= 8:
                ind = 8-1
                sent_selected = True
                break
            if dialog_input == '9' and length >= 9:
                ind = 9-1
                sent_selected = True
                break
            if dialog_input == '10' and length >= 10:
                ind = 10-1
                sent_selected = True
                break
            if dialog_input == '11' and length >= 11:
                ind = 11-1
                sent_selected = True
                break
            if dialog_input == '12' and length >= 12:
                ind = 12-1
                sent_selected = True
                break
            if dialog_input == '13' and length >= 13:
                ind = 13-1
                sent_selected = True
                break
        if n:
            cant_label.append(r_dialog)
            continue
        elif q: break

    # Functions based on input
    if one_sentence:
        print('\n--------------------------------------\n' + str(chosen_sentence))
        print('--------------------------------------\n')
        print('\n - Press \'1\' to tag as a positive sentence\n - Press \'2\' to tag as a negative sentence\n - Press \'n\' key to skip\n - Press \'q\' to quit')
    elif sent_selected:
        chosen_sentence = str(b.sentences[ind])
        print('\n--------------------------------------\n' + str(chosen_sentence))
        print('--------------------------------------\n')
        print('\n - Press \'1\' to tag as a positive sentence\n - Press \'2\' to tag as a negative sentence\n - Press \'n\' key to skip\n - Press \'q\' to quit')
    elif n:
        cant_label.append(r_dialog)
        #TODO go through loop again

    # Do somthing with selected text
    print('')
    pos = False
    neg = False
    while True and q != True:
        sentence_input = input()
        # if quiting
        if sentence_input == 'q':
            not_finished = False
            break
        # if skipping
        if sentence_input == 'n':
            cant_label.append(r_dialog)
            print('\nMoving to next label...\n')
            n = True
            break
        # if labeled positive
        if sentence_input == '1':
            print('\nLabeling sentence as positive...')
            pos = True
            break
        # if labeled positive
        if sentence_input == '2':
            print('\nLabeling sentence as negative...')
            neg = True
            break

    if pos:
        if type(chosen_sentence) == str:
            labels[r_dialog] = (chosen_sentence, 'pos')
        else:
            labels[r_dialog] = (chosen_sentence.dict['raw'], 'pos')
    elif neg:
        if type(chosen_sentence) == str:
            labels[r_dialog] = (chosen_sentence, 'neg')
        else:
            labels[r_dialog] = (chosen_sentence.dict['raw'], 'neg')


#print(labels)
print('\n\nThank you!')
print('\nSaving training data (only to a test file)...')
with open('dataset/train_sentiment_test.json', 'w') as outfile:
    json.dump(labels, outfile, indent=2)
with open('dataset/untrainable_sentiment_test.json', 'w') as outfile:
    json.dump(cant_label, outfile, indent=2)
