from json import *

def save_to_json(obj, path, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as f:
        dump(obj, f)

def load_from_json(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as f:
        return load(f)
