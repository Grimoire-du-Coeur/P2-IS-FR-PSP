import json
import re
import os

def len_bytes(text):
    t = text
    tags = re.findall(r'\[[^\]]+\]', t)
    for tag in tags:
        t = t.replace(tag, '', 1)
    return (len(t) * 2) + (len(tags) * 2)

replacements = {
    "De quelle rumeur tu veux avoir les \ndétails?": "Laquelle ?",
    "Quoi d'neuf? Je peux t'aider?": "Quoi de neuf ?",
    "Quel type de rumeur t'intéresse?": "Quel type de rumeur ?",
    "Mais de quoi parlerons-nous donc?": "De quoi parlerons-nous ?",
    "Ça marche! T'as quoi en tête?": "Ça marche! Quoi en tête?",
    "Bienvenue? Oh, juste vous\ndeux aujourd'hui? [1205][000F]On dirait que\nquelqu'un fait le premier pas!": "Bienvenue? Juste vous 2?\n[1205][000F]Quelqu'un fait le 1er pas!",
    "Ah, merci d'être venus! Détendez-vous\net restez aussi longtemps que voulu.": "Ah, merci d'être venus! Détendez-vous.",
    "Bienvenue, bienvenue! Ah, vous\nêtes saufs!": "Bienvenue! Ah, vous êtes saufs!",
    "Aujourd'hui je recommande.[1205][000F].. Eh bien,\ntout![1205][000A] C'est tout frais! Que\nvoulez-vous?": "Aujourd'hui je recommande...[1205][000F]\ntout![1205][000A] Que voulez-vous?",
    "Ah, bienvenue, bienvenue! Merci\nd'être venus!": "Ah, bienvenue! Merci d'être venus!",
    "Bienvenue, bien.[1205].[000F].venue... H-Hé,\nqu'y a-t-il? Pourquoi ces têtes?": "Bien.[1205].[000F].venue... Hé,\npourquoi ces têtes?",
    "Très bien. [1205][000F]Le prix sera de 3 000 yens.\nSouhaitez-vous toujours cela?": "Très bien. [1205][000F]Prix: 3 000 yens.\nSouhaitez-vous cela?",
    "Quelle histoire souhaitez-vous?": "Quelle histoire ?",
    "C'est une longue histoire... Ça vous\nconvient?": "Longue histoire... Ça vous va?"
}

files = [
    'script_261.json', 'script_281.json', 'script_285.json', 'script_324.json', 
    'script_325.json', 'script_342.json', 'script_343.json', 'script_373.json', 
    'script_375.json', 'script_376.json', 'script_382.json'
]

trad_dir = r'C:\Users\nolan\Desktop\6666666656\repo\traduction\event_scripts'

for file in files:
    path = os.path.join(trad_dir, file)
    with open(path, 'r', encoding='utf-8') as f:
        d = json.load(f)
    
    changed = False
    for e in d:
        o = e.get('texte_orig', '')
        fr = e.get('texte_fr', '')
        if '[1208]' in o and '[1208]' in fr:
            o_q = o.split('[1208]')[0]
            f_q = fr.split('[1208]')[0]
            
            # Remove trailing \n for dict matching
            f_q_clean = f_q.strip()
            if f_q_clean in replacements:
                new_f_q = replacements[f_q_clean] + '\n'
                e['texte_fr'] = fr.replace(f_q, new_f_q)
                changed = True
                print(f"Fixed question in {file} ID {e['id']}")
            elif len_bytes(f_q) > len_bytes(o_q):
                print(f"STILL OVERFLOW: {f_q_clean}")
                
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)

print("Done fixing question overflows.")
