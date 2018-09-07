import os
import json

prefs_location = home = expanduser("~") + os.sep

def check_prefs_state():
    '''Return if a prefs exists or not'''
    return os.path.exists(prefs_location)

def create_preference_file():
    '''Create a new preference file in the specified prefs_location'''

    data = {"code_directories":["C:\Users\Martin\Github\mayaCore"]}

    file_path = prefs_location _+ "bolt_preferences.json"
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile, indent=3)

def preference_create_dialog():
