import os
from pathlib import Path
import datetime
import json
import time

from spekter.utils import get_all_files, load_saves

def get_last_modified(path):
    ts = os.path.getmtime(path)
    dt = datetime.datetime.fromtimestamp(ts)
    return dt

def get_last_accessed(path):
    ts = os.path.getatime(path)
    dt = datetime.datetime.fromtimestamp(ts)
    return dt

def saved_files(files, SAVES):
    output = []
    for file in files:
        if file not in SAVES["files"]:
            output.append(file)
        else:
            if get_last_modified(file).timestamp() > SAVES["last_checked"]:
                output.append(file)
    return output

def opened_files(files, SAVES):
    output = []
    for file in files:
        if get_last_accessed(file).timestamp() > SAVES["last_checked"]:
            output.append(file)
    return output   

def dump_saves(files):
    SAVES = load_saves()
    SAVES["last_checked"] = datetime.datetime.now().timestamp()
    SAVES["files"] = files
    with open("data.json", "w") as f:
        json.dump(SAVES, f)

class DirLoop:

    def __init__(self, path, wait=5):
        self.path = path
        self.wait = wait

    def set_save_func(self, function, *args, **kwargs):
        self.save_func = function
        self.save_args = args
        self.save_kwargs = kwargs
    
    def set_open_func(self, function, *args, **kwargs):
        self.open_func = function
        self.open_args = args
        self.open_kwargs = kwargs

    def trigger_save(self):
        self.save_func(*self.save_args, **self.save_kwargs)

    def trigger_open(self):
        self.open_func(*self.open_args, **self.open_kwargs)

    def start(self):
        SAVES = load_saves()
        while True: 
            try:
                files = get_all_files(self.path, ignore=[".DS_Store", "/data", "/.git", "sonic.cfg", ".gitignore", "\\data", "\\.git"])
                saved = saved_files(files, SAVES)
                opened = opened_files(files, SAVES)
                opened = [i for i in opened if i not in saved]
                #SAVED
                if len(saved) > 0:
                    if self.save_func:
                        print("Triggering save function.")
                        self.trigger_save()
                #OPENED
                if len(opened) > 0:
                    if self.open_func:
                        print("Triggering open function.")
                        self.trigger_open()
                if len(opened) > 0 or len(saved) > 0:
                    dump_saves(files)
                    SAVES = load_saves()
                    print(SAVES)
                time.sleep(self.wait)
            except KeyboardInterrupt:
                break    

if __name__=="__main__":
    def notify(x):
        print(x)

    home_dir = Path(os.path.expanduser('~'))
    dir_path = f"{str(home_dir)}/Documents/Notes"

    l = DirLoop(path=dir_path, wait=5)
    l.set_save_func(notify, x="SAVED")
    l.set_open_func(notify, x="OPENED")
    l.start()
