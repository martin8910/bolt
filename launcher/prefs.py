import os
import json
from os.path import expanduser
import qtCore

prefs_location = home = expanduser("~") + os.sep
prefs_file = prefs_location + "bolt_preferences.json"
def check_prefs_state():
    '''Return if a prefs exists or not'''
    return os.path.exists(prefs_file)

def create_preference_file(library_path=None):
    '''Create a new preference file in the specified prefs_location'''

    if library_path:
        data = {"code_directories":[library_path]}

        file_path = prefs_location + "bolt_preferences.json"
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile, indent=3)
    else:
        print "A library path need to be privided"

def get_library_path():
    '''Return the path to the current library'''
    with open(prefs_file) as file:
        data = json.load(file)

    # Check if folder exists
    library_path = data["code_directories"][0]
    if os.path.exists(library_path):
        return library_path
    else:
        print "The path no longer exist:"
        return None
def pick_library_path():
    '''Create a popup to pick a library'''

    path = qtCore.picker_dialog(mode="AnyDirectory", message="Choose a python-library folder")
    return path

def set_library_path(library_path=None):
    '''Create a popup to pick a library'''
    print "Open the library"
    if library_path != None:
        if os.path.exists(library_path):
            if check_prefs_state():
                data = {"code_directories": ["C:\Users\Martin\Github\mayaCore"]}

                file_path = prefs_location + "bolt_preferences.json"
                with open(file_path, 'w') as outfile:
                    json.dump(data, outfile, indent=3)
            else:
                create_preference_file()
        else:
            print "Please provide a proper library path"
    else:
        print "A library-path need to be privided"





