# script_parser.py

# {{{ Import Statements
from pathlib import Path
import pprint
import json
import re
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
# }}}

# {{{ Todo & Notes

# TODO
# (*) - Learn about Regular Expressions
#     - find way to find movie scripts with all the common
#       script elements
# (*) - Find Fade in
# (*) - Find Scenes
#       - scene numbers at the end of line
#       - find text on new line a tabbed space away
#         indicating a change in context
# (*) - Count Scenes
# (*) - Find Characters
#       - all caps
#       - capture lists of names
#       - minimal characters in line
# (*) - Annotate dialog
# (*) - Find Behaviours
# ( ) - Find Scene description context (determined un-needed)

# Notes
'''
      - Some text say (cont'd) after character name
      - Try extracting scene numbers from lines in format: (2) INT. (1st AVE.  ST.  BAR) -- Night
      - Script context changes during a space or a change in tab
      - Sometimes desc has multi-paragraphs. But does diag?
      - Sometimes behaviour not always just after name
      - might want to consider removing a name if there was no dialog after
'''

# }}}

# {{{ State Class
# Define state class
'''
used to extract information to be formated in json later
used to figure out state changes in dialog, scene name, and scene description
'''
class State:
    def __init__(self):
        self.in_scene = False
        self.in_dialog = False
        self.char_name_last = False
        self.scene_name = ''
        self.scene_num = ''
        self.char_name = ''
        self.behaviour = ''
        self.desc = False
        self.scn_tab_indices = []
        self.des_tab_indices = []
        self.dia_tab_indices = []
        self.cha_tab_indices = []
        self.last_scn_index = -1
        self.last_dia_index = -1
        self.last_des_index = -1
        self.last_cha_index = -1

    def reset(self):
        self.in_scene = False
        self.in_dialog = False
        self.char_name_last = False
        self.scene_name = ''
        self.scene_num = ''
        self.char_name = ''
        self.behaviour = ''
        self.desc = False
        self.scn_tab_indices = []
        self.des_tab_indices = []
        self.dia_tab_indices = []
        self.cha_tab_indices = []
        self.last_scn_index = -1
        self.last_dia_index = -1
        self.last_des_index = -1
        self.last_cha_index = -1

    # sets line content type, and determines number of tab spaces
    def first_char(self, line, l_type):
        ind = len(line)-len(line.lstrip())
        if l_type == 'scn':
            self.scn_tab_indices.append(ind)
            self.last_scn_index = ind

        elif l_type == 'desc':
            self.des_tab_indices.append(ind)
            self.last_des_index = ind

        elif l_type == 'diag':
            self.dia_tab_indices.append(ind)
            self.last_dia_index = ind

        elif l_type == 'cha':
            self.cha_tab_indices.append(ind)
            self.last_cha_index = ind

        elif l_type == 'na':
            self.last_dia_index = ind

        else: print('typed something in wrong')

        return ind

    #checks if the first character corresponds to a context type
    # used to predict the type of information in a line
    def check_ind(self, line):
        #TODO make sure to do something if last index is -1
        context_list = []
        tab_thresh = 7
        ind = len(line)-len(line.lstrip())
        if ind >= self.last_scn_index - tab_thresh and ind <= self.last_scn_index + tab_thresh:
            context_list.append('scn')

        if ind >= self.last_des_index - tab_thresh and ind <= self.last_des_index + tab_thresh:
            context_list.append('des')

        if ind >= self.last_dia_index - tab_thresh and ind <= self.last_dia_index + tab_thresh:
            context_list.append('dia')

        return context_list

    # determine the average tab for each context type
    def avg_scn_tab(self):
        arr_len = len(self.scn_tab_indices)
        if arr_len > 0:
            tab_sum = 0
            for i in self.scn_tab_indices:
                tab_sum += i
            return round(tab_sum/arr_len)
        else:
            return -1

    def avg_des_tab(self):
        arr_len = len(self.des_tab_indices)
        if arr_len > 0:
            tab_sum = 0
            for i in self.des_tab_indices:
                tab_sum += i
            return round(tab_sum/arr_len)
        else:
            return -1

    def avg_dia_tab(self):
        arr_len = len(self.dia_tab_indices)
        if arr_len > 0:
            tab_sum = 0
            for i in self.dia_tab_indices:
                tab_sum += i
            return round(tab_sum/arr_len)
        else:
            return -1

    def avg_char_name_tab(self):
        arr_len = len(self.cha_tab_indices)
        if arr_len > 0:
            tab_sum = 0
            for i in self.cha_tab_indices:
                tab_sum += i
            return round(tab_sum/arr_len)
        else:
            return -1

# }}}

# {{{ Initializations for Script Parser
# Init data
data = {}
data['scripts'] = []
state = State()

# Iterate through scripts
print('Iterating through scripts...')
entries = Path('dataset/movie_scripts')
for entry in entries.iterdir():

    # extract name and year data
    info = str(entry).split('/')[-1]
    info = info.split('_')
    name = ' '.join(info[:-1])
    year = info[-1].split('.')[0]

    # Iterate through lines
    state.reset()

    characters = []
    characters_exist = False
    desc_text = []
    dialog_text = []
    context = []
    context_bool = False

    script = open(entry, "r")
    num_of_lines = 0
    fade_in = False

    num_of_lines = 0
    fade_in_count = 0
    scene_count = 0
    fade_in_lines = []
    scenes_exist = False
    scenes = {}
    scene_num = 1
    last_scene_num = -1

# }}}

# {{{ Line Analyzer

    # formates to json
    def create_context(text, name, behaviour):
        dict = {}
        vo_bool = False
        vo_list = ['(vo)', '(os)', '(o.s.)', '(v.o.)']
        name_noc = name.lower().replace('(cont\'d)', '').capitalize()
        r_paran_name = re.search("\(.*\)", name_noc.strip())
        text_string = " ".join(text)
        blob_nb = TextBlob(text_string, analyzer=NaiveBayesAnalyzer())
        sentiment_list = []

        dict['type'] = 'dialog'
        name_novoc = ""
        if r_paran_name:
            for i in vo_list:
                if name_noc.strip().lower().find(i) != -1:
                    name_novoc = name_noc.lower().replace(i, "").capitalize().strip()
                    vo_bool = True
                    break
        if name_novoc == "":
            name_novoc = name_noc.strip()

        behaviour_novo = ""
        for i in vo_list:
            if behaviour.strip().find(i) != -1:
                behavior_novo = behaviour.replace(i, "").strip()
                vo_bool = True
                break
        if behaviour_novo == "":
            behaviour_novo = behaviour.strip()
        behaviour_formated = behaviour_novo.replace('(', '').replace(')', '').strip()

        dict['Name'] = name_novoc #name.lower().replace('(cont\'d)', '').capitalize()
        dict['Off Screen'] = vo_bool
        dict['Behaviour'] = behaviour_formated
        dict['Text'] = text
        context.append(dict)

    for line in script:
        # count number of lines
        num_of_lines += 1

        # check index of first character in line
        f_char = state.first_char(line, 'na')

        # see if script contains:

        # fade in | check if has more than one & if not in first %25 of script
        r_fade_in = re.search("^FADE IN.*:", line.lstrip())
        if r_fade_in:
            state.first_char(line, 'scn')
            fade_in = True
            fade_in_count += 1
            fade_in_lines.append(num_of_lines)

        # Regular expression Definitions
        r_scene = re.search("\WEXT\.*[\s/]|\WINT\.*[\s/]|^INT\.*[\s/]|^EXT\.*[\s/]", line)
        r_char_name = re.search("^[A-Z]+'*[A-Z]*\.*\s*[A-Z]*'*[A-Z]*\s*[A-Z]*'*[A-Z]*(\s#[1-9])*(\s\(.+\))*$", line.strip())
        r_behaviour = re.search("^\(.+|.+\)$|^\(\w+\)$", line.strip())
        r_behaviour_full_orStart = re.search("\(.*\)|\(.*", line.strip())
        r_paran = re.search("\(.*\)", line.strip())

        # Scenes
        if r_scene:
            scenes_exist = True
            state.in_scene = True
            state.first_char(line, 'scn')

            # if new scene found then should append context to previous scene
            if state.in_dialog:
                # TODO add desc data
                create_context(dialog_text, state.char_name, state.behaviour)
                dialog_text = []
                state.behaviour = ''
                state.in_dialog = False
            if context:
                # append context to scene
                scenes[state.scene_num]['Context'] = context
                # empty text and context
                dialog_text = []
                desc_text = []
                context = []

            scene = {}

            # find scene number or create one
            # TODO remove asterisks
            r_scene_num = re.findall("^\w*\d\d*\w*|\w*\d\d*\w*$|^\w+\-\w+|\w+\-\w+$", line.strip())
            if r_scene_num:
                scene['id'] = r_scene_num[0]
                line_no_nl =  re.sub('\n', '', line.strip())
                scene['name'] = re.sub("^\w*\d\d*\w*|\w*\d\d*\w*$|^\w+\-\w+|\w+\-\w+$", '', line_no_nl.strip()).strip()
                state.scene_name = scene['name']
            else:
                scene['id'] = []
                scene['name'] = line.strip()
                state.scene_name = scene['name']


            # create scene
            scene['Context'] = []
            scenes[scene_num] = scene
            scene_count += 1
            state.scene_num = scene_num
            scene_num += 1

        # check for character name
        elif r_char_name and state.in_scene and 'scn' not in state.check_ind(line):
            # if new scene found then should append context to previous scene
            if state.in_dialog:
                # TODO add desc data
                # append current text to context
                #create_context(dialog_text, 'dia')
                create_context(dialog_text, state.char_name, state.behaviour)
                dialog_text = []
                state.behaviour = ''
                state.in_dialog = False

            quit = False
            # filter out THE END
            not_chars = ['THE END', 'MOMENTS LATER', 'CUT TO', 'JUMP CUT TO',
                    'CUT BACK TO', 'LATER', 'END']
            r_not_char_name = re.search("^[A-Z]+\.+$", line.strip())
            if line.strip() in not_chars:
                quit = True
                continue
            elif r_not_char_name:
                quit = True
                continue

            # want to quit this if statement if name is not a character
            if quit:
                continue
            else:
                # setup new state & format
                characters_exist = True
                state.in_dialog = True
                state.char_name_last = True
                state.char_name = line.strip()
                state.first_char(line, 'cha')

                # Add new characters
                if r_paran:
                    n_line = re.sub("\(.*\)", "",  line.strip())
                else:
                    n_line = line.strip()
                if n_line.strip() in characters:
                    continue
                else:
                    characters.append(n_line.strip())

        # if character name found on previous line
        elif state.in_dialog:
            # if space found: countinue
            if line.strip() == '' and state.char_name_last:
                continue
            elif line.strip() == '' and not state.char_name_last:
                create_context(dialog_text, state.char_name, state.behaviour)
                dialog_text = []
                state.behaviour = ''
                state.in_dialog = False

            # if first line after a name found: set tab/look for behaviour

            # if behaviour
            elif r_behaviour and 'scn' not in state.check_ind(line):
                not_b = ['(continuing)', '(more)', '(continuing on)', 'continued', 'then']
                if line.strip().lower() in not_b:
                    continue
                else:
                    if state.behaviour == '':
                        state.behaviour += line.strip()
                    elif r_behaviour_full_orStart:
                        if state.behaviour == line.strip():
                            continue
                        else:
                            state.behaviour += '; ' + line.strip()
                    else:
                        state.behaviour += ' ' + line.strip()

            # if dialog found
            elif 'scn' not in state.check_ind(line):
                not_dialog = ['cut to:']
                if line.strip().lower() in not_dialog:
                    continue
                else:
                    # if first dialog line found
                    if state.char_name_last:
                        # set dialog tab to this location & append dialog
                        state.char_name_last = False
                        state.first_char(line, 'diag')
                        dialog_text.append(line.strip())
                    # otherwise just append dialog
                    elif 'dia' in state.check_ind(line):
                        dialog_text.append(line.strip())
            # otherwise this line is description data
            else:
                #TODO remove name?

                # if dialog_text is not empty
                if dialog_text:
                    #create_context(dialog_text, 'dia')
                    create_context(dialog_text, state.char_name, state.behaviour)
                    state.behaviour = ''
                    dialog_text = []

                # create dialog data, and add to the scene
                # update state
                state.in_dialog = False
                state.char_name_last = False

                #TODO do something with desc

        #else:
            #print('scene, character name, or dialog not found...')

# }}}

# {{{ JSON Data Format

    # format data
    data['scripts'].append({
        'name':name,
        'year':year,
        'lines': num_of_lines,
        'manually remove': False,
        'fade in': fade_in,
        'fade count': fade_in_count,
        'fade in lines': fade_in_lines,
        'Typical Scene Name Tab Spacing': state.avg_scn_tab(),
        'Typical Description Tab Spacing': state.avg_des_tab(),
        'Typical Character Name Tab Spacing': state.avg_char_name_tab(),
        'Typical Dialog Tab Spacing': state.avg_dia_tab(),
        'scenes exist': scenes_exist,
        'scene count': scene_count,
        'characters exist': characters_exist,
        'character count': len(characters),
        'characters': characters,
        'scenes': scenes
        })

    script.close()

# }}}

# {{{ Movies to Remove Manually
# analytics & manual script removal
print('Complete.\nRunning analytics...')
scripts_to_remove = [
        #'2001 A Space Odyssey',
        '9',
        #'American History X',                  # int/ext at beginning of line (need to re-format)
        'American Outlaws',                     # written on one line
        #'American Psycho'                      # not many scenes
        'Scarface',                             # No EXT or INT
        'Nightbreed',                           # Not formatted; no tabs
        'Lord of the Rings The Two Towers',     # Diff format; desc and behaviour in [ ]
        'Men in Black 3',                       # Weird format, not much EXT/INT; chars not formatted
        'A Prayer Before Dawn',                 # plays around with format
        #'Boondock Saints 2 All Saints Day',     # uses v.o. in name
        'Commando',                             # dialog same tab as desc
        '44 Inch Chest',                        # cut to etc.
        'Coriolanus',                           # following cut due to skewed sentiment values
        'Moneyball',
        'In the Bedroom',
        'Cars 2',
        'Burlesque',
        'Ted',
        'Flight',
        'The Change Up',
        'Erin Brockovich',
        'The Godfather Part III',
        'Indiana Jones and the Last Crusade',
        'Pandorum',
        'The Producer',
        'Deception',
        'Saving Mr. Banks',
        'Margaret',





]
# }}}

# {{{ Analytics & Output
num_of_scripts = len(data['scripts'])
fade_count = 0
empty_count = 0
scene_count = 0
removed_count = 0
char_count = 0
for i in data['scripts']:
    if i['fade in']:
        fade_count += 1
    if i['lines'] < 500:
        empty_count += 1
    if i['scenes']:
        scene_count += 1
    if i['name'] in scripts_to_remove:
        i['manually remove'] = True
        removed_count += 1
    if i['characters exist']:
        char_count += 1


# output
print('Complete.')
#pprint.pprint(data)

print('\nAnalysis:\n')
print('number of scripts:', len(data['scripts']))
print('number of empty scripts:', empty_count)
#print('difference:', len(data['scripts']) - count)
print('number of scripts with \'fade in\':', fade_count)  # 617
print('number of scripts with scenes:', scene_count)  # 617
print('number of scripts with characters:', char_count)  #
print('number of scripts to be manually removed:', removed_count)  # 617

# export
with open('dataset/script_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

# }}}
