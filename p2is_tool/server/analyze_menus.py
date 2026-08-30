import sys, json, re
sys.path.append('.')
from src.core.text import text_to_bytes

def get_options(text):
    # Split by [1210] to get options. First element is question.
    parts = text.split('[1210]')
    return parts[1:] if len(parts) > 1 else []

def print_menu_analysis(e):
    o_text = e['texte_orig']
    f_text = e['texte_fr']
    o_opts = get_options(o_text)
    f_opts = get_options(f_text)
    
    print(f"ID {e['id']}:")
    for i, (o, f) in enumerate(zip(o_opts, f_opts)):
        o_len = len(text_to_bytes(o))
        f_len = len(text_to_bytes(f))
        print(f"  Opt {i+1}: {o_len:3d} vs {f_len:3d} | diff={o_len - f_len:3d} | '{f.strip()}' vs '{o.strip()}'")

with open(r'C:\Users\nolan\Desktop\6666666656\repo\traduction\event_scripts\script_382.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for e in data:
    if e['id'] in [32, 33, 34, 35, 36]:
        print_menu_analysis(e)
