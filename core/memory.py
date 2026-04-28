import json
import os

FILE_MEMORI = os.path.join(os.path.dirname(__file__), 'ingatan.json')

def simpan_catatan(kunci, data):
    memori = buka_memori()
    memori[kunci] = data
    with open(FILE_MEMORI, 'w') as f:
        json.dump(memori, f, indent=4)

def buka_memori():
    if not os.path.exists(FILE_MEMORI):
        return {}
    with open(FILE_MEMORI, 'r') as f:
        return json.load(f)

