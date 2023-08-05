import os
from dulwich import porcelain
from dulwich.repo import Repo
from pathlib import Path
from spekter.utils import get_all_files, load_saves, get_notes_path

from dotenv import load_dotenv
load_dotenv()

SAVES = load_saves()

HOST=SAVES.get("host")
REPO=SAVES.get("repo")
USERNAME="spekter"

def create_new_repo(path): 
    repo = porcelain.init(path)
    return repo

def clone_repo(url, path):
    porcelain.clone(url, path)

def get_repo(path):
    repo = Repo(path)
    return repo

def commit(repo, files):
    for file in files:
        porcelain.add(repo, files)
        porcelain.commit(repo, b"Automated commit")

def commit_and_push():
    notes_path = get_notes_path()
    files = get_all_files(notes_path, ignore=[".DS_Store", "/data", "/.git", "sonic.cfg", "\\.git", "\\data"])
    repo = get_repo(notes_path)
    commit(repo, files)
    push(repo)

def push(repo):
    r = porcelain.push(repo.path, f"{USERNAME}@{HOST}:{REPO}", "master")

def pull(repo):
    r = porcelain.pull(repo.path, f"{USERNAME}@{HOST}:{REPO}")

if __name__=="__main__":
    home_dir = Path(os.path.expanduser('~'))
    repo = get_repo(f"{str(home_dir)}/Documents/Notes")
    relative_files = ["." + file.replace(repo.path, "") for file in files]
    commit(repo, files)
    push(repo)

