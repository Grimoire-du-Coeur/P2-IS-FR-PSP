import json
import re

def len_bytes(text):
    t = text
    tags = re.findall(r'\[[^\]]+\]', t)
    for tag in tags:
        t = t.replace(tag, '', 1)
    return (len(t) * 2) + (len(tags) * 2)

files = [
    'script_261.json', 'script_281.json', 'script_285.json', 'script_324.json', 
    'script_325.json', 'script_342.json', 'script_343.json', 'script_373.json', 
    'script_375.json', 'script_376.json', 'script_382.json'
]

trad_dir = r'C:\Users\nolan\Desktop\6666666656\repo\traduction\event_scripts'

for file in files:
    with open(f'{trad_dir}/{file}', 'r', encoding='utf-8') as f:
        d = json.load(f)
    for e in d:
        o = e.get('texte_orig', '')
        if '[1208]' in o:
            o_q = o.split('[1208]')[0]
            f_q = e.get('texte_fr', '').split('[1208]')[0]
            if len_bytes(f_q) > len_bytes(o_q):
                print(f"{file} ID {e.get('id')}: OVERFLOW! Orig={len_bytes(o_q)} FR={len_bytes(f_q)}")
                print(f"  Orig: {repr(o_q)}")
                print(f"  FR:   {repr(f_q)}")
