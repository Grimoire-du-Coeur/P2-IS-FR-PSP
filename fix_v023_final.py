import json, glob, re, sys
sys.path.insert(0, 'C:/Users/nolan/Desktop/P2-FR-IS-PSP-main/P2-FR-IS-PSP-main/p2is_tool/server')
from src.core.text import text_to_bytes

trad_dir = 'C:/Users/nolan/Desktop/6666666656/repo/traduction'
files = glob.glob(f'{trad_dir}/**/*.json', recursive=True)

total = 0

for f in files:
    if 'EBOOT_Translation' in f:
        continue
    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except:
        continue

    changed = False
    for entry in data:
        fr = entry.get('texte_fr', '')
        if not fr:
            continue
        original = fr

        # FIX 1: [E1][E2] [E3][E4] space -> newline (84 occurrences)
        fr = fr.replace('[E1][E2] [E3][E4]', '[E1][E2]\n[E3][E4]')
        fr = fr.replace('[E1][E2]  [E3][E4]', '[E1][E2]\n[E3][E4]')

        # FIX 2 & 3: Remove ALL [1205][000A] - the forbidden crash tag
        # Replace with a simple space to avoid words being concatenated
        fr = fr.replace('[1205][000A]', ' ')
        # Clean up double spaces that result
        fr = re.sub(r'  +', ' ', fr)

        if fr != original:
            entry['texte_fr'] = fr
            changed = True
            total += 1

    if changed:
        with open(f, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

print(f'Fixed {total} entries.')

# Now fix the specific overflow entry script_281 id=150
path_281 = 'C:/Users/nolan/Desktop/6666666656/repo/traduction/event_scripts/script_281.json'
with open(path_281, 'r', encoding='utf-8') as f:
    data = json.load(f)

for entry in data:
    if entry['id'] == 150:
        old = entry['texte_fr']
        # Current: "C- Cercle masqué![1205][000F]? Qu-... C'est quoi? J-Je n'ai rien à voir avec tout ça!"
        # Rewrite cleanly, keep [1205][000F] as it's valid (pause without wipe)
        entry['texte_fr'] = "C-Cercle masqué!? Qu-...\nC'est quoi? J-Je n'ai rien à\nvoir avec tout ça!"
        print(f'id=150 rewritten:')
        print(f'  old: {repr(old)}')
        print(f'  new: {repr(entry["texte_fr"])}')
        # Check encoding
        enc = text_to_bytes(entry['texte_fr'])
        slot = entry.get('slot_size', 0)
        print(f'  enc={len(enc)} slot={slot} overflow={len(enc) > slot}')

with open(path_281, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Done.')
