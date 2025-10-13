from json import *

def save_to_json(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        dump(obj, f)

def load_from_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return load(f)
