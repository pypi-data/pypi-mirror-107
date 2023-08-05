import os
import json
from pathlib import Path 


def get_notes_path():
    return relative_to_absolute(load_saves()["location"])

def relative_to_absolute(relative):
    home_dir = Path(os.path.expanduser('~'))
    notes_path = str(Path(f"{str(home_dir)}/{relative}"))
    return notes_path

def load_saves():
    try:
        with open("data.json") as f:
            SAVES = json.load(f)
    except:
        SAVES = dict()
    return SAVES


def get_all_files(path, ignore=[]):
    output = []
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            if not any([i in path for i in ignore]):
                output.append(path)
    return output

def file_to_words(path):
    with open(path) as f:
        content = f.read()
    return content.split()
    



