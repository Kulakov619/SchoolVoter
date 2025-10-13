import json
from random import randint

KEYS_COUNT = 1000
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

with open("keys.json", "w") as f:
    json.dump(keys_dict, f, indent=2)
