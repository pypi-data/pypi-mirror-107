import os
from pathlib import Path

from sonic import SearchClient
from sonic import IngestClient
from spekter.utils import file_to_words, get_all_files

def clean_file(file):
    return file.replace(" ", "<space>")

def injest(files):
    with IngestClient("127.0.0.1", 1491, "SecretPassword") as ingestcl:
        ingestcl.flush("files", "spekter")
        for file in files:
            words = file_to_words(file)
            for idx, word in enumerate(words):
                try:
                    ingestcl.push("files", "spekter", f'{clean_file(file)}:{str(idx)}', word)
                except Exception as e:
                    print(f"Failed to push: {file}:{str(idx)} -> {word}")
                    print(e)

def search(query):
    with SearchClient("127.0.0.1", 1491, "SecretPassword") as querycl:
        return querycl.query("files", "spekter", query)

def parse_search(results, before=7, after=7):
    output = []
    for result in results:
        file_path, word_idx = result.split(":")
        file_path = file_path.replace("<space>", " ")
        words = file_to_words(file_path)
        a = max(int(word_idx) - before, 0)
        b = min(int(word_idx) + after, len(words)-1)
        output.append({
            "file_path" : file_path, 
            "word" : words[int(word_idx)], 
            "phrase" : " ".join(words[a:b])
        })
    return output

if __name__=="__main__":
    home_dir = Path(os.path.expanduser('~'))
    files = get_all_files(f"{str(home_dir)}/Documents/Notes", ignore=[".DS_Store", "/data", "/.git", "sonic.cfg"])
    injest(files)
    print(parse_search(search("Template")))
