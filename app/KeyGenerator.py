import json
from random import randint

from JsonDecorator import save_to_json

with open("Names.txt", "r") as f:
    names = f.read().split(", ")
    KEYS_COUNT = len(names)

KEY_LENGTH = 30

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def generate_key():
    key = ""
    for _ in range(KEY_LENGTH):
        symbol = alphabet[randint(0, len(alphabet) - 1)]
        symbol = symbol.lower() if randint(0, 1) == 1 else symbol.upper()
        key += symbol
    return key

keys_set = set()

while len(keys_set) < KEYS_COUNT:
    keys_set.add(generate_key())

keys = list(keys_set)

keys_dict = {}

for key in keys:
    keys_dict[key] = False

save_to_json(keys_dict, "keys.json")

names_to_keys = {}

for i in range(KEYS_COUNT):
    names_to_keys[names[i]] = keys[i]

save_to_json(names_to_keys, "names_to_keys.json", encoding="utf-32")
